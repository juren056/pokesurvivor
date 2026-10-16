"""Generate concise, public machine-readable editions from rendered Wiki pages."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
import html
import json
import re


SITE = 'https://pokemonsurvivorwiki.com'
READING_SLUGS = ('', 'how-to-play', 'mobile', 'move-evolutions', 'starters',
                 'types', 'about', 'builds', 'survivor-vs-burst')
READING_PATHS = {slug: ('/index.md' if not slug else f'/{slug}.md') for slug in READING_SLUGS}


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list[object] = field(default_factory=list)


class TreeParser(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
            'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def find_first(node: Node, tag: str) -> Node | None:
    if node.tag == tag:
        return node
    for child in node.children:
        if isinstance(child, Node):
            result = find_first(child, tag)
            if result:
                return result
    return None


def has_class(node: Node, name: str) -> bool:
    return name in node.attrs.get('class', '').split()


def text_content(node: object) -> str:
    if isinstance(node, str):
        return node
    if not isinstance(node, Node):
        return ''
    if node.tag in {'script', 'style', 'svg', 'button', 'input', 'select', 'option'}:
        return ''
    return ''.join(text_content(child) for child in node.children)


def clean_text(value: str) -> str:
    return re.sub(r'\s+', ' ', value).strip()


def inline(node: object, base_url: str) -> str:
    if isinstance(node, str):
        return re.sub(r'\s+', ' ', node)
    if not isinstance(node, Node):
        return ''
    if node.tag in {'script', 'style', 'svg', 'button', 'input', 'select', 'option',
                    'video', 'source', 'noscript'} or 'hidden' in node.attrs:
        return ''
    body = ''.join(inline(child, base_url) for child in node.children)
    if node.tag in {'strong', 'b'} and clean_text(body):
        return f'**{clean_text(body)}**'
    if node.tag in {'em', 'i'} and clean_text(body):
        return f'*{clean_text(body)}*'
    if node.tag == 'code' and clean_text(body):
        return f'`{clean_text(body)}`'
    if node.tag == 'a':
        label = clean_text(body)
        href = node.attrs.get('href', '')
        if label and href:
            return f'[{label}]({urljoin(base_url, href)})'
    if node.tag == 'span' and has_class(node, 'type') and clean_text(body):
        return clean_text(body) + ' / '
    if node.tag == 'br':
        return ' '
    return body


def table_markdown(node: Node, base_url: str) -> str:
    rows: list[list[str]] = []
    for section in node.children:
        candidates = section.children if isinstance(section, Node) and section.tag in {'thead', 'tbody', 'tfoot'} else [section]
        for row in candidates:
            if not isinstance(row, Node) or row.tag != 'tr':
                continue
            cells = []
            for cell in row.children:
                if isinstance(cell, Node) and cell.tag in {'th', 'td'}:
                    value = clean_text(inline(cell, base_url)).removesuffix(' /').replace('|', '\\|')
                    cells.append(value or '—')
            if cells:
                rows.append(cells)
    if not rows:
        return ''
    width = max(len(row) for row in rows)
    rows = [row + ['—'] * (width - len(row)) for row in rows]
    header = rows[0]
    data = rows[1:]
    lines = ['| ' + ' | '.join(header) + ' |', '| ' + ' | '.join(['---'] * width) + ' |']
    lines.extend('| ' + ' | '.join(row) + ' |' for row in data)
    return '\n'.join(lines)


def blocks(node: Node, base_url: str, depth: int = 0) -> list[str]:
    if node.tag in {'script', 'style', 'svg', 'form', 'input', 'select', 'option',
                    'button', 'fieldset', 'label', 'output', 'video', 'source',
                    'noscript'} or 'hidden' in node.attrs:
        return []
    if has_class(node, 'article-aside') or has_class(node, 'breadcrumbs') or has_class(node, 'mobile-dock'):
        return []
    if node.tag in {'h1', 'h2', 'h3', 'h4'}:
        value = clean_text(inline(node, base_url))
        return [f'{"#" * int(node.tag[1])} {value}'] if value else []
    if node.tag == 'p':
        value = clean_text(inline(node, base_url))
        return [value] if value else []
    if node.tag == 'table':
        value = table_markdown(node, base_url)
        return [value] if value else []
    if node.tag in {'ul', 'ol'}:
        result = []
        index = 0
        for child in node.children:
            if not isinstance(child, Node) or child.tag != 'li':
                continue
            index += 1
            value = clean_text(inline(child, base_url))
            if value:
                marker = f'{index}.' if node.tag == 'ol' else '-'
                result.append(f'{marker} {value}')
        return ['\n'.join(result)] if result else []
    if node.tag == 'dl':
        result = []
        term = ''
        for child in node.children:
            if not isinstance(child, Node):
                continue
            value = clean_text(inline(child, base_url))
            if child.tag == 'dt':
                term = value
            elif child.tag == 'dd' and value:
                result.append(f'- **{term}:** {value}')
        return ['\n'.join(result)] if result else []
    if node.tag == 'img':
        alt = clean_text(node.attrs.get('alt', ''))
        src = node.attrs.get('src', '')
        return [f'![{alt}]({urljoin(base_url, src)})'] if alt and src else []
    if node.tag == 'details':
        title = ''
        result = []
        for child in node.children:
            if isinstance(child, Node) and child.tag == 'summary':
                title = clean_text(inline(child, base_url))
            elif isinstance(child, Node):
                result.extend(blocks(child, base_url, depth + 1))
        return ([f'### {title}'] if title else []) + result
    result: list[str] = []
    for child in node.children:
        if isinstance(child, Node):
            result.extend(blocks(child, base_url, depth + 1))
    return result


def page_to_markdown(html_text: str, canonical: str, reviewed: str, commit: str, home: bool) -> str:
    parser = TreeParser()
    parser.feed(html_text)
    main = find_first(parser.root, 'main')
    if not main:
        raise ValueError(f'Missing <main> in {canonical}')
    target = main if home else find_first(main, 'article')
    if not target:
        raise ValueError(f'Missing article in {canonical}')
    body = blocks(target, canonical)
    if not home:
        heading = find_first(main, 'h1')
        if heading:
            body.insert(0, '# ' + clean_text(inline(heading, canonical)))
    if not body or not any(part.startswith('# ') for part in body):
        raise ValueError(f'Missing readable H1 in {canonical}')
    note = (
        f'> Text edition of [{canonical}]({canonical}). Reviewed {reviewed} against '
        f'game source snapshot `{commit[:7]}`. Interactive search, filters, calculators, '
        'images and videos remain on the HTML page; this edition does not access a game save.'
    )
    return '\n\n'.join([body[0], note, *body[1:]]).strip() + '\n'


def build_llms(page_titles: dict[str, str]) -> str:
    def item(slug: str, note: str) -> str:
        path = READING_PATHS[slug]
        return f'- [{page_titles[slug]}]({SITE}{path}): {note}'
    return '\n'.join([
        '# Pokémon Survivor Wiki',
        '',
        '> Independent English reference for JPTER78’s browser game PokéSurvivor. It is not an official Pokémon website and does not document Pokémon Survivor Burst.',
        '',
        'Mechanics and database facts are derived from the named public game-source snapshot. Editorial recommendations are labeled and are not presented as measured gameplay results. The canonical HTML pages contain interactive tools, images, videos, credits and complete navigation.',
        '',
        '## Start here',
        item('', 'Site scope, primary guides and databases.'),
        item('how-to-play', 'Controls, upgrade choices and first-run sequence.'),
        item('starters', 'All 29 starting partners and their opening moves.'),
        item('move-evolutions', 'Evolution requirements and troubleshooting.'),
        item('types', 'Softened type multipliers and the dual-type cap.'),
        '',
        '## Practical guides',
        item('builds', 'Four source-based starter build routes and tradeoffs.'),
        item('mobile', 'Browser controls, PWA installation and save precautions.'),
        item('survivor-vs-burst', 'Identification guide for two different fan projects.'),
        '',
        '## About the source',
        item('about', 'Editorial method, source scope, media evidence and rights.'),
        f'- [Pokédex]({SITE}/pokedex/): Searchable database of 966 partner records.',
        f'- [Moves]({SITE}/moves/): Searchable database of 64 move definitions.',
        f'- [Updates]({SITE}/updates/): Developer changelog entries from the recorded snapshot.',
        '',
        '## Optional',
        f'- [Robots policy]({SITE}/robots.txt): Crawler policy and sitemap location.',
        f'- [XML sitemap]({SITE}/sitemap.xml): Canonical indexable HTML URLs.',
        '',
    ])


def export(out: Path, pages: dict, reviewed: str, commit: str) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    titles = {slug: page['title'] for slug, page in pages.items()}
    for slug in READING_SLUGS:
        html_path = out / slug / 'index.html'
        canonical = SITE + ('/' if not slug else f'/{slug}/')
        markdown = page_to_markdown(html_path.read_text(encoding='utf-8'), canonical, reviewed, commit, not slug)
        target = out / READING_PATHS[slug].lstrip('/')
        target.write_text(markdown, encoding='utf-8')
        records[READING_PATHS[slug]] = {
            'canonical': canonical,
            'sha256': sha256(target.read_bytes()).hexdigest(),
            'source': canonical,
        }
    llms = build_llms(titles)
    llms_path = out / 'llms.txt'
    llms_path.write_text(llms, encoding='utf-8')
    records['/llms.txt'] = {
        'canonical': SITE + '/llms.txt',
        'sha256': sha256(llms_path.read_bytes()).hexdigest(),
        'source': SITE + '/',
    }
    manifest = {
        'site': SITE,
        'generatedFrom': 'rendered canonical HTML',
        'reviewed': reviewed,
        'sourceCommit': commit,
        'resources': records,
    }
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    (out / 'assets' / 'agent-resources.json').write_text(manifest_text, encoding='utf-8')
    return records


def headers(records: dict[str, dict[str, str]]) -> str:
    lines = [
        '/llms.txt',
        '  Content-Type: text/plain; charset=utf-8',
    ]
    for path, item in records.items():
        if not path.endswith('.md'):
            continue
        canonical_path = item['canonical'].removeprefix(SITE)
        lines += [
            path,
            '  Content-Type: text/markdown; charset=utf-8',
            '  X-Robots-Tag: noindex, follow',
            f'  Link: <{canonical_path}>; rel="canonical", </llms.txt>; rel="describedby"',
        ]
    return '\n'.join(lines) + '\n'
