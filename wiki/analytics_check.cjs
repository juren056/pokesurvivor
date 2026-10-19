const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(__dirname + '/public/analytics.js', 'utf8');
for (const name of ['official_game_click','build_share','diagnosis_complete','video_start']) assert.ok(source.includes(`'${name}'`), name);
for (const obsolete of ['outbound_game_click','diagnostic_complete']) assert.ok(!source.includes(`'${obsolete}'`), obsolete);
function fixture(host = 'pokemonsurvivorwiki.com', saved = null, gpc = false) {
  const scripts = [], events = {}, settings = {};
  const panel = {hidden:false, setAttribute(){}, querySelector(){return {focus(){}};}, addEventListener(k,v){events[k]=v;}};
  const context = {location:{hostname:host, origin:'https://' + host, pathname:'/search/', search:'?q=private'}, navigator:{globalPrivacyControl:gpc}, localStorage:{getItem(){return saved;},setItem(k,v){saved=v;}}, document:{referrer:'https://example.com/path?q=secret', cookie:'_ga=sample', createElement(tag){return tag==='script'?{}:panel;}, head:{append(s){scripts.push(s);}},body:{append(){}}, querySelector(){return {setAttribute(){},addEventListener(k,v){settings[k]=v;}};}}, URL, Date};
  context.window = context; vm.createContext(context); vm.runInContext(source, context);
  const choose = value => events.click({target:{closest(){return {dataset:{analytics:value}};}}});
  return {context, scripts, panel, choose, settings};
}
let f=fixture(); assert.equal(f.scripts.length,0); assert.equal(f.panel.hidden,false);
f.choose('denied'); assert.equal(f.scripts.length,0);
f.choose('granted'); assert.equal(f.scripts.length,1);
const config=f.context.dataLayer.find(x=>x[0]==='config')[2];
assert.equal(config.page_location,'https://pokemonsurvivorwiki.com/search/');
assert.equal(config.page_referrer,'https://example.com/path');
f.choose('denied'); assert.equal(f.context['ga-disable-G-GEQDCG9L1K'],true);
f.choose('granted'); assert.equal(f.scripts.length,1); assert.equal(f.context['ga-disable-G-GEQDCG9L1K'],false);
assert.equal(fixture('pokemonsurvivorwiki.com','granted').scripts.length,1);
assert.equal(fixture('pokemonsurvivorwiki.com','granted',true).scripts.length,0);
assert.equal(fixture('pokemonsurvivorwiki.pages.dev','granted').scripts.length,0);
console.log('PASS: opt-in, refusal, withdrawal/re-enable, query removal, saved choice, GPC and preview isolation.');
