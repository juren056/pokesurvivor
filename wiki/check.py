"""Validate final HTML, index policy, source provenance and internal links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
DIST=HERE/'dist'
SITE='https://pokemonsurvivorwiki.com'


class Document(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.links=[];self.ids=[];self.h1=0;self.canonical=[];self.description=[];self.title=[];self.robots='';self.jsonld=[];self.in_title=False;self.in_ld=False;self.lang=None
        self.feed(text)

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if 'id' in a:self.ids.append(a['id'])
        if tag in ('a','link') and 'href' in a:self.links.append(a['href'])
        if tag in ('script','img','source','track') and 'src' in a:self.links.append(a['src'])
        if tag=='video' and 'poster' in a:self.links.append(a['poster'])
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if tag=='meta' and a.get('name')=='description':self.description.append(a.get('content'))
        if tag=='meta' and a.get('name')=='robots':self.robots=a.get('content','')
        if tag=='title':self.in_title=True
        if tag=='script' and a.get('type')=='application/ld+json':self.in_ld=True

    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag=='script':self.in_ld=False

    def handle_data(self,text):
        if self.in_title:self.title.append(text)
        if self.in_ld:self.jsonld.append(text)


def check():
    failures=[]
    manifest=json.loads((DIST/'build-manifest.json').read_text(encoding='utf-8'))
    docs={}
    for url in manifest:
        path=DIST/url.lstrip('/')/'index.html'
        docs[url]=Document(path.read_text(encoding='utf-8'))
    docs['/404.html']=Document((DIST/'404.html').read_text(encoding='utf-8'))
    titles=[];descriptions=[]
    for url,doc in docs.items():
        if doc.h1!=1:failures.append(f'{url}: {doc.h1} H1 headings')
        if doc.lang!='en':failures.append(f'{url}: wrong HTML language')
        expected=SITE+('/404/' if url=='/404.html' else url)
        if doc.canonical!=[expected]:failures.append(f'{url}: wrong canonical {doc.canonical}')
        if len(doc.ids)!=len(set(doc.ids)):failures.append(f'{url}: duplicate IDs')
        if not doc.title or not doc.description or not doc.description[0]:failures.append(f'{url}: missing metadata')
        titles.append(''.join(doc.title));descriptions.extend(doc.description)
        should_index=manifest.get(url,{}).get('index',False)
        if should_index==('noindex' in doc.robots):failures.append(f'{url}: index policy mismatch')
        try:json.loads(''.join(doc.jsonld))
        except Exception:failures.append(f'{url}: invalid structured data')
        for href in doc.links:
            parts=urlsplit(href)
            if parts.scheme or parts.netloc:continue
            target=unquote(parts.path) or url
            if not target.startswith('/'):failures.append(f'{url}: non-root relative link {href}');continue
            path=DIST/target.lstrip('/')
            if target.endswith('/'):path=path/'index.html'
            if not path.is_file():failures.append(f'{url}: broken link {href}')
            if parts.fragment and target in docs and parts.fragment not in docs[target].ids:failures.append(f'{url}: broken anchor {href}')
    if len(titles)!=len(set(titles)):failures.append('Duplicate titles')
    if len(descriptions)!=len(set(descriptions)):failures.append('Duplicate descriptions')
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sitemap=ET.parse(DIST/'sitemap.xml')
    locations={el.text for el in sitemap.findall('s:url/s:loc',ns)}
    if locations!={SITE+url for url,p in manifest.items() if p['index']}:failures.append('Sitemap/indexable manifest mismatch')
    if len(sitemap.findall('s:url/s:loc',ns))!=len(locations):failures.append('Duplicate sitemap URLs')
    data=json.loads((HERE/'data/game.json').read_text(encoding='utf-8'))
    for file,digest in data['source']['files'].items():
        actual=hashlib.sha256((HERE.parent/file).read_bytes()).hexdigest()
        if digest!=actual:failures.append(f'Snapshot stale: {file}; review and re-export')
    search=json.loads((DIST/'assets/search.json').read_text(encoding='utf-8'))
    for item in search:
        parts=urlsplit(item['url'])
        if parts.path not in docs or (parts.fragment and parts.fragment not in docs[parts.path].ids):failures.append(f'Broken search result {item["url"]}')
    for path in DIST.rglob('*.html'):
        text=path.read_text(encoding='utf-8')
        if any(s in text for s in ('firebaseapp.com','app.min.js','<canvas','serviceWorker.register','pokesurvivor-free','hreflang=')):failures.append(f'Inherited game runtime or locale marker: {path}')
    if failures:
        print('\n'.join(failures));raise SystemExit(1)
    print(f'PASS: {len(docs)} HTML documents; {len(locations)} indexable URLs; {len(search)} search targets; metadata, anchors, links, JSON-LD and source hashes valid.')


if __name__=='__main__':check()
