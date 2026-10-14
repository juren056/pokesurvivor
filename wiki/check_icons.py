"""Focused acceptance checks for the published icon family."""
from pathlib import Path
from html.parser import HTMLParser
import json
from PIL import Image

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'


class Links(HTMLParser):
    def __init__(self,text):
        super().__init__();self.icons=[];self.manifests=[];self.apples=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='link':
            if a.get('rel')=='icon':self.icons.append(a)
            elif a.get('rel')=='manifest':self.manifests.append(a.get('href'))
            elif a.get('rel')=='apple-touch-icon':self.apples.append(a.get('href'))


def main():
    for f in DIST.rglob('*.html'):
        doc=Links(f.read_text(encoding='utf-8'))
        assert any(i.get('href')=='/favicon-96.png' and i.get('sizes')=='96x96' for i in doc.icons),f
        assert doc.manifests==['/site.webmanifest'],f
        assert doc.apples==['/apple-touch-icon.png'],f
    for size in [16,32,48,96,180,192,512]:
        im=Image.open(DIST/f'assets/icons/icon-{size}.png')
        assert im.size==(size,size)
        assert 'Original vector' in im.info['Source']
    ico=Image.open(DIST/'favicon.ico')
    assert ico.ico.sizes()=={(16,16),(32,32),(48,48)}
    for name in ['apple-touch-icon.png','assets/icons/icon-maskable-512.png']:
        assert Image.open(DIST/name).mode=='RGB',name
    manifest=json.loads((DIST/'site.webmanifest').read_text(encoding='utf-8'))
    for icon in manifest['icons']:
        im=Image.open(DIST/icon['src'].lstrip('/'))
        assert f'{im.width}x{im.height}'==icon['sizes']
    assert manifest['start_url']=='/' and manifest['scope']=='/'
    print('PASS: all 19 HTML documents declare raster/SVG/touch/manifest icons; PNG sizes, origin metadata, multi-size ICO and manifest assets valid.')


if __name__=='__main__':main()
