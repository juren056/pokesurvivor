"""Focused checks for generated machine-readable public resources."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import re

import agent_resources


HERE = Path(__file__).resolve().parent
DIST = HERE / 'dist'
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


manifest_path = DIST / 'assets' / 'agent-resources.json'
require(manifest_path.is_file(), 'Missing public agent resource manifest')
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.is_file() else {'resources': {}}
resources = manifest.get('resources', {})
expected = {'/llms.txt', *agent_resources.READING_PATHS.values()}
require(set(resources) == expected, f'Agent resource inventory differs: {set(resources) ^ expected}')

for path, item in resources.items():
    target = DIST / path.lstrip('/')
    require(target.is_file(), f'Missing resource {path}')
    if not target.is_file():
        continue
    raw = target.read_bytes()
    text = raw.decode('utf-8')
    require(sha256(raw).hexdigest() == item.get('sha256'), f'Hash mismatch for {path}')
    require('<html' not in text.lower(), f'HTML fallback leaked into {path}')
    require(len(text) >= (700 if path.endswith('.md') else 900), f'Resource is unexpectedly short: {path}')
    require(text.startswith('# '), f'Resource lacks a leading H1: {path}')

for slug, md_path in agent_resources.READING_PATHS.items():
    canonical = agent_resources.SITE + ('/' if not slug else f'/{slug}/')
    html_path = DIST / slug / 'index.html'
    html_text = html_path.read_text(encoding='utf-8')
    markdown = (DIST / md_path.lstrip('/')).read_text(encoding='utf-8')
    require(f'<link rel="alternate" href="{md_path}" type="text/markdown">' in html_text,
            f'Missing Markdown alternate on {canonical}')
    require('<link rel="describedby" href="/llms.txt" type="text/plain">' in html_text,
            f'Missing llms discovery link on {canonical}')
    require(f'Text edition of [{canonical}]({canonical})' in markdown,
            f'Missing canonical disclosure in {md_path}')
    require('does not access a game save' in markdown, f'Missing capability limit in {md_path}')
    for match in re.finditer(r'\]\((https://pokemonsurvivorwiki\.com[^)]+)\)', markdown):
        parsed = urlparse(match.group(1))
        target = DIST / parsed.path.lstrip('/')
        if parsed.path.endswith('/'):
            target /= 'index.html'
        require(target.is_file(), f'{md_path} links to missing resource: {parsed.path}')

llms = (DIST / 'llms.txt').read_text(encoding='utf-8')
for match in re.finditer(r'\]\((https://pokemonsurvivorwiki\.com[^)]+)\)', llms):
    parsed = urlparse(match.group(1))
    target = DIST / parsed.path.lstrip('/')
    if parsed.path.endswith('/'):
        target /= 'index.html'
    require(target.is_file(), f'llms.txt links to missing resource: {parsed.path}')

required_phrases = {
    '/how-to-play.md': ('attacks fire automatically', 'golden evolution card', 'Guest progress'),
    '/move-evolutions.md': ('maximum level', 'required stat card', 'golden evolution card'),
    '/types.md': ('1.6×', '0.6×', '2.4×'),
    '/survivor-vs-burst.md': ('different fan projects', 'ClessioTV'),
    '/about.md': ('Source inspection is separate from gameplay testing', 'Credits and rights'),
}
for path, phrases in required_phrases.items():
    text = (DIST / path.lstrip('/')).read_text(encoding='utf-8')
    for phrase in phrases:
        require(phrase.lower() in text.lower(), f'{path} lost key context: {phrase}')

headers = (DIST / '_headers').read_text(encoding='utf-8')
for path in expected:
    require(f'{path}\n' in headers, f'Missing Cloudflare header rule for {path}')
for path in agent_resources.READING_PATHS.values():
    require('X-Robots-Tag: noindex, follow' in headers.split(path + '\n', 1)[1].split('\n/', 1)[0],
            f'Missing noindex header for {path}')

sitemap = (DIST / 'sitemap.xml').read_text(encoding='utf-8')
require('.md</loc>' not in sitemap and 'llms.txt</loc>' not in sitemap,
        'Reading editions must stay out of the HTML XML sitemap')
require((DIST / 'robots.txt').read_text(encoding='utf-8') ==
        'User-agent: *\nAllow: /\n\nSitemap: https://pokemonsurvivorwiki.com/sitemap.xml\n',
        'robots.txt changed unexpectedly')

# Converter regression: pipes must remain a valid Markdown table and interactive controls must vanish.
fixture = '<main><h1>Fixture</h1><article><h2>Data</h2><table><tr><th>A</th><th>B</th></tr><tr><td>x | y</td><td><button>Sort</button>ok</td></tr></table></article></main>'
converted = agent_resources.page_to_markdown(fixture, agent_resources.SITE + '/fixture/', '2026-10-16', 'abcdef0', False)
require('x \\| y' in converted and 'Sort' not in converted and '| A | B |' in converted,
        'Markdown table conversion regression')

if errors:
    raise SystemExit('FAIL:\n- ' + '\n- '.join(errors))
print(f'PASS: {len(resources)} machine-readable resources; canonical, noindex, content, links and sitemap separation valid.')
