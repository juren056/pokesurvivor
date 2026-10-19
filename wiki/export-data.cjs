/* Read-only snapshot adapter. It does not execute the game, network, or Firebase. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const files = ['js/core/util.js', 'js/core/i18n.js', 'js/data/lang-en.js', 'js/data/pokedex.js', 'js/data/sprites-meta.js', 'js/data/moves.js', 'js/data/starters.js', 'js/data/types.js', 'js/systems/gacha.js', 'js/data/changelog.js'];
const sandbox = {G: {}, console, CanvasRenderingContext2D:function(){}, location:{pathname:'/en/',protocol:'http:'}, navigator: {language:'en',languages:['en']}, localStorage:{getItem:()=> 'en',setItem:()=>{}}, document:{documentElement:{},addEventListener:()=>{}}, window:{}, performance:{now:()=>0}};
sandbox.window = sandbox;
vm.createContext(sandbox);
const english = {};
const hashes = {};
for (const file of files) {
  const raw = fs.readFileSync(path.join(root,file),'utf8');
  hashes[file] = crypto.createHash('sha256').update(raw).digest('hex');
  vm.runInContext(raw,sandbox,{filename:file,timeout:5000});
  if (file==='js/core/i18n.js') {
    const add = sandbox.G.I18n.add;
    sandbox.G.I18n.add = d => {Object.assign(english,d);add(d);};
  }
}
const G = sandbox.G;
const title = id => id.split('-').map(s=>s[0].toUpperCase()+s.slice(1)).join(' ');
const en = text => english[text] || text;
const need = {hp:'Vigor',atk:'Power',spd:'Sprint',cd:'Reflexes',def:'Armor',rgn:'Synthesis',mag:'Magnet',xp:'Learning'};
const moves = Object.values(G.Moves.BY_ID).map(m=>{
  const evo = G.Moves.EVO[m.id];
  return {id:m.id,name:title(m.id),type:m.type,kind:m.kind,category:m.cat ?? null,buffStat:m.stat ?? null,
    description:en(m.desc || ''),maxLevel:m.maxLvl || 5,damage:m.dmg ?? null,cooldown:m.cd ?? null,count:m.count ?? null,
    radius:m.radius ?? null,arc:m.arc ?? null,upgrades:(m.ups || []).map(u=>({text:en(u.t),mods:u.m})),
    evolution:evo?{name:en(evo[0]),stat:evo[1],requirement:en(G.Moves.NEED_NAME[evo[1]]) || need[evo[1]]}:null};
});
const types = Object.keys(G.Types.CHART);
const matrix = Object.fromEntries(types.map(a=>[a,Object.fromEntries(types.map(d=>[d,G.Types.mult(a,[d])]))]));
const matchups = Object.fromEntries(types.map(a=>[a,Object.fromEntries(types.map(b=>[b,Object.fromEntries(types.filter(c=>c!==b).map(c=>[c,G.Types.mult(a,[b,c])]))]))]));
const starters = G.STARTERS.map(s=>({...s,...G.DEX_BY[s.dex]}));
const evidenceFiles = [...new Set([...files,...JSON.parse(fs.readFileSync(path.join(__dirname,'content.json'),'utf8')).pages.flatMap(p=>p.sources), 'js/systems/levelup.js','js/systems/rift.js','js/systems/spawner.js'])];
for(const file of evidenceFiles)hashes[file]=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex');
// A later Wiki-only commit must not change links to the original game source.
const commit=execFileSync('git',['log','-1','--format=%H','--',...evidenceFiles],{cwd:root,encoding:'utf8'}).trim();
execFileSync('git',['diff','--quiet','HEAD','--',...evidenceFiles],{cwd:root});
const dex=G.DEX.map(p=>({...p,gacha:G.Gacha.pool(p.rarity,p.gen).some(entry=>entry.dex===p.dex)}));
const data={source:{repository:'https://github.com/JPTER78/pokesurvivor',commit,verified:'2026-10-19',files:hashes},dex,starters,moves,types,matrix,matchups,
  changelog:G.CHANGELOG.map(c=>({date:c.d,title:c.title[1],new:(c.new||[]).map(x=>x[1]),changed:(c.chg||[]).map(x=>x[1]),fixed:(c.fix||[]).map(x=>x[1])}))};
fs.mkdirSync(path.join(__dirname,'data'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'data','game.json'),JSON.stringify(data,null,2)+'\n');
console.log(`Wiki snapshot: ${data.dex.length} Pokémon, ${starters.length} starters, ${moves.length} moves, ${moves.filter(m=>m.evolution).length} evolutions; ${commit.slice(0,7)}`);
