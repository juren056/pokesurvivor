"""Validate final HTML, index policy, source provenance and internal links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import xml.etree.ElementTree as ET
import localization

HERE=Path(__file__).resolve().parent
DIST=HERE/'dist'
SITE='https://pokemonsurvivorwiki.com'


class Document(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.links=[];self.ids=[];self.h1=0;self.canonical=[];self.alternates={};self.description=[];self.title=[];self.robots='';self.jsonld=[];self.in_title=False;self.in_ld=False;self.lang=None
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
        if tag=='link' and a.get('rel')=='alternate' and a.get('hreflang'):self.alternates[a['hreflang']]=a.get('href')
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
    ledger=json.loads((HERE/'localization-review.json').read_text(encoding='utf-8'))
    for locale in localization.LOCALE_ORDER[1:]:
        actual=sum(1 for item in manifest.values() if item.get('locale')==locale)
        if ledger['locales'][locale]['routes']!=actual:failures.append(f'{locale}: review ledger route count mismatch')
    docs={}
    for url in manifest:
        path=DIST/url.lstrip('/')/'index.html'
        docs[url]=Document(path.read_text(encoding='utf-8'))
    docs['/404.html']=Document((DIST/'404.html').read_text(encoding='utf-8'))
    titles=[];descriptions=[]
    for url,doc in docs.items():
        if doc.h1!=1:failures.append(f'{url}: {doc.h1} H1 headings')
        locale=manifest.get(url,{}).get('locale','en')
        if doc.lang!=localization.LANG.get(locale,'en'):failures.append(f'{url}: wrong HTML language {doc.lang}')
        expected=SITE+('/404/' if url=='/404.html' else url)
        if doc.canonical!=[expected]:failures.append(f'{url}: wrong canonical {doc.canonical}')
        if url!='/404.html':
            slug=url.removeprefix('/'+locale+'/').strip('/') if locale!='en' else url.strip('/')
            expected_alts={localization.LANG[loc]:SITE+localization.url(loc,slug) for loc in localization.LOCALE_ORDER}
            expected_alts['x-default']=SITE+localization.url('en',slug)
            if doc.alternates!=expected_alts:failures.append(f'{url}: wrong hreflang set')
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
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
    sitemap=ET.parse(DIST/'sitemap.xml')
    locations={el.text for el in sitemap.findall('s:url/s:loc',ns)}
    if locations!={SITE+url for url,p in manifest.items() if p['index']}:failures.append('Sitemap/indexable manifest mismatch')
    if len(sitemap.findall('s:url/s:loc',ns))!=len(locations):failures.append('Duplicate sitemap URLs')
    for node in sitemap.findall('s:url',ns):
        loc=node.find('s:loc',ns).text
        path=urlsplit(loc).path
        locale=next((x for x in localization.LOCALE_ORDER[1:] if path.startswith('/'+x+'/') or path=='/'+x+'/'),'en')
        slug=path.removeprefix('/'+locale+'/').strip('/') if locale!='en' else path.strip('/')
        alternates={x.attrib['hreflang']:x.attrib['href'] for x in node.findall('x:link',ns)}
        expected={localization.LANG[x]:SITE+localization.url(x,slug) for x in localization.LOCALE_ORDER}
        expected['x-default']=SITE+localization.url('en',slug)
        if alternates!=expected:failures.append(f'{loc}: sitemap hreflang mismatch')
    data=json.loads((HERE/'data/game.json').read_text(encoding='utf-8'))
    for file,digest in data['source']['files'].items():
        actual=hashlib.sha256((HERE.parent/file).read_bytes()).hexdigest()
        if digest!=actual:failures.append(f'Snapshot stale: {file}; review and re-export')
    search_count=0
    for locale in localization.LOCALE_ORDER:
        name='search.json' if locale=='en' else f'search-{locale}.json'
        search=json.loads((DIST/'assets'/name).read_text(encoding='utf-8'));search_count+=len(search)
        for item in search:
            parts=urlsplit(item['url'])
            if parts.path not in docs or (parts.fragment and parts.fragment not in docs[parts.path].ids):failures.append(f'Broken search result {item["url"]}')
    for path in DIST.rglob('*.html'):
        text=path.read_text(encoding='utf-8')
        if any(s in text for s in ('firebaseapp.com','app.min.js','<canvas','serviceWorker.register','pokesurvivor-free')):failures.append(f'Inherited game runtime: {path}')
        if any(part in path.parts for part in ('es','it','zh-hant')):
            for phrase in ('Find in this table','No matches. Try another name','Keep your run moving','Reference reviewed','On this page','Enable JavaScript for the checker','Loading build data'):
                if phrase in text:failures.append(f'Localized surface contains English UI "{phrase}": {path}')
    if failures:
        print('\n'.join(failures));raise SystemExit(1)
    print(f'PASS: {len(docs)} HTML documents; {len(locations)} indexable URLs; {search_count} localized search targets; metadata, reciprocal hreflang, anchors, links, JSON-LD and source hashes valid.')


if __name__=='__main__':check()
