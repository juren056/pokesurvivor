/* Read-only snapshot adapter. It does not execute the game, network, or Firebase. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const SOURCE_COMMIT = 'd567c6da88e4ef66634ab54a01b5a3607501e03a';
const files = ['js/core/util.js', 'js/core/locales.js', 'js/core/i18n.js', 'js/data/lang-en.js', 'js/data/lang-updates.js', 'js/data/pokedex.js', 'js/data/sprites-meta.js', 'js/data/moves.js', 'js/data/starters.js', 'js/data/types.js', 'js/data/upgrades.js', 'js/data/abilities.js', 'js/data/natures.js', 'js/data/tms.js', 'js/data/ability-fx.js', 'js/data/shop.js', 'js/systems/gacha.js', 'js/systems/orbs.js', 'js/data/changelog.js'];
const sandbox = {G: {}, console, CanvasRenderingContext2D:function(){}, location:{pathname:'/en/',protocol:'http:'}, navigator: {language:'en',languages:['en']}, localStorage:{getItem:()=> 'en',setItem:()=>{}}, document:{documentElement:{},currentScript:null,write:()=>{},addEventListener:()=>{}}, window:{}, performance:{now:()=>0}};
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
    sandbox.G.I18n.add = (d, language='en', context='') => {
      if (language === 'en' && !context) Object.assign(english,d);
      add(d,language,context);
    };
  }
}
const G = sandbox.G;
const sourceAt = file => execFileSync('git',['show',`${SOURCE_COMMIT}:${file}`],{cwd:root,encoding:'utf8'});
const makeTranslator = (locale, pathname, languageFile=null) => {
  const s = {G:{},console,CanvasRenderingContext2D:function(){},location:{pathname,protocol:'http:'},navigator:{language:locale,languages:[locale]},localStorage:{getItem:()=>locale,setItem:()=>{}},document:{documentElement:{},currentScript:null,write:()=>{},addEventListener:()=>{}},window:{},performance:{now:()=>0}};
  s.window=s; s.PS_LANG_Q=[]; vm.createContext(s);
  for (const file of ['js/core/locales.js', ...(languageFile?[languageFile]:[]), 'js/core/i18n.js', 'js/data/lang-en.js', 'js/data/lang-updates.js']) {
    const raw=sourceAt(file);
    if (languageFile===file) hashes[file]=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex');
    vm.runInContext(raw,s,{filename:file,timeout:5000});
  }
  return text=>s.G.I18n.t(text);
};
const abilityTranslators = {
  en: makeTranslator('en','/en/'),
  it: makeTranslator('it','/it/','js/lang/it.js'),
  'zh-hant': makeTranslator('zh-Hant','/zh-hant/','js/lang/zh-Hant.js')
};
const legacySnapshot = JSON.parse(execFileSync('git',['show','8b306c24:wiki/data/game.json'],{cwd:root,encoding:'utf8',maxBuffer:16*1024*1024}));
const legacyEvolutionNames = Object.fromEntries(legacySnapshot.moves.filter(m=>m.evolution).map(m=>[m.id,m.evolution.name]));
const title = id => id.split('-').map(s=>s[0].toUpperCase()+s.slice(1)).join(' ');
const en = text => english[text] || text;
const need = {hp:'Vigor',atk:'Power',spd:'Sprint',cd:'Reflexes',def:'Armor',rgn:'Synthesis',mag:'Magnet',xp:'Learning'};
const moves = Object.values(G.Moves.BY_ID).map(m=>{
  const evo = G.Moves.EVO[m.id];
  return {id:m.id,name:title(m.id),type:m.type,kind:m.kind,category:m.cat ?? null,buffStat:m.stat ?? null,
    description:en(m.desc || ''),maxLevel:m.maxLvl || 5,damage:m.dmg ?? null,cooldown:m.cd ?? null,count:m.count ?? null,
    radius:m.radius ?? null,arc:m.arc ?? null,upgrades:(m.ups || []).map(u=>({text:en(u.t),mods:u.m})),
    evolution:evo?{name:`${title(m.id)} +`,stat:evo,requirement:en(G.Moves.NEED_NAME[evo]) || need[evo],historicalName:legacyEvolutionNames[m.id]||null}:null};
});
const types = Object.keys(G.Types.CHART);
const matrix = Object.fromEntries(types.map(a=>[a,Object.fromEntries(types.map(d=>[d,G.Types.mult(a,[d])]))]));
const matchups = Object.fromEntries(types.map(a=>[a,Object.fromEntries(types.map(b=>[b,Object.fromEntries(types.filter(c=>c!==b).map(c=>[c,G.Types.mult(a,[b,c])]))]))]));
const starters = G.STARTERS.map(s=>({...s,...G.DEX_BY[s.dex],baseStart:G.baseStartOf(s.dex),startChoices:G.startChoices(s.dex)}));
const evidenceFiles = [...new Set([...files,...JSON.parse(fs.readFileSync(path.join(__dirname,'content.json'),'utf8')).pages.flatMap(p=>p.sources), 'js/core/db.js','js/entities/player.js','js/systems/combat.js','js/systems/levelup.js','js/systems/mons.js','js/systems/rift.js','js/systems/spawner.js','js/net/coop.js'])];
for(const file of evidenceFiles)hashes[file]=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex');
// Refuse a mixed-version export: all factual game files must match the locked source commit.
const lockedFiles = ['js/data/moves.js','js/data/starters.js','js/data/upgrades.js','js/data/changelog.js','js/data/abilities.js','js/data/natures.js','js/data/tms.js','js/data/ability-fx.js','js/data/shop.js','js/systems/gacha.js','js/systems/orbs.js','js/systems/judgment.js','js/core/db.js','js/entities/player.js','js/systems/combat.js','js/systems/levelup.js','js/systems/mons.js','js/net/coop.js'];
execFileSync('git',['diff','--quiet',SOURCE_COMMIT,'--',...lockedFiles],{cwd:root});
const commit=SOURCE_COMMIT;
// Wiki copy and diagrams may be edited in the same release. Only the locked
// game-source files must remain byte-identical to the reviewed source commit.
const dex=G.DEX.map(p=>({...p,gacha:G.Gacha.pool(p.rarity,p.gen).some(entry=>entry.dex===p.dex)}));
const playableDex = new Set(dex.map(p=>p.dex));
const natureNames = n => ({es:n.n[0],en:n.n[1],it:n.n[3],'zh-hant':n.n[5]});
const natures = G.NATURES.map(n=>({id:n.id,names:natureNames(n),up:n.up||null,down:n.down||null,neutral:!n.up&&!n.down}));
const usedAbilityIds = new Set();
const abilitySlots = {};
for (const p of dex) {
  const slots = (G.DEX_ABIL[p.dex] || [0,0,0]).map(x=>x||null);
  abilitySlots[p.dex] = slots;
  slots.filter(Boolean).forEach(id=>usedAbilityIds.add(id));
}
const abilityNames = n => ({es:n[0],en:n[1],it:n[3],'zh-hant':n[5]});
const fallbackEffects = {
  es:'Efecto base: +8 % de daño con movimientos del tipo principal del compañero.',
  en:'Fallback: +8% damage with moves matching the partner’s primary type.',
  it:'Effetto base: +8% di danno con mosse del tipo principale del compagno.',
  'zh-hant':'後備效果：與夥伴主要屬性相同的招式傷害增加 8%。'
};
const localizedAbilityEffects = description => ({
  es: description,
  en: abilityTranslators.en(description),
  it: abilityTranslators.it(description),
  'zh-hant': abilityTranslators['zh-hant'](description)
});
const abilities = [...usedAbilityIds].sort().map(id=>{
  const fx=G.AbilityFX.FX[id];
  const effects=fx?localizedAbilityEffects(fx.d):fallbackEffects;
  return {id,names:abilityNames(G.ABIL[id]),effects,effect:effects.en,effectType:fx?'specialized':'fallback'};
});
const tms = Object.keys(G.TM_MOVES).filter(id=>G.Moves.BY_ID[id]).sort().map(id=>({id,name:title(id),price:G.TM_PRICE[id]||400,compatibleDex:G.TM_MOVES[id].filter(d=>playableDex.has(d))}));
const naturalMoves = Object.fromEntries(dex.map(p=>[p.dex,G.Moves.poolFor(p,true)]));
const data={source:{repository:'https://github.com/JPTER78/pokesurvivor',commit,verified:'2026-10-24',files:hashes},dex,starters,moves,types,matrix,matchups,natures,abilities,abilitySlots,tms,naturalMoves,
  orbs:{slots:G.Orbs.SLOTS,stack:G.Orbs.STACK,cooldownSeconds:1,nearbyRadius:384,items:G.Orbs.LIST.map(x=>({id:x.id,name:x.name,duration:x.dur||null,description:x.desc}))},
  shop:{items:Object.fromEntries(Object.entries(G.Shop.ITEMS).map(([id,x])=>[id,{name:en(x.name),price:x.price,hidden:!!x.hidden}])),dailyTmCount:8,timeZone:'Europe/Madrid',defaultTmPrice:400},
  upgrades:G.Upgrades.LIST.map(u=>({id:u.id,name:en(u.name),unit:en(u.unit),max:u.max,base:u.base,grow:u.grow,needs:u.needs||null})),
  rules:{startingMove:{upgradeId:'start',cost:400,max:1,excludesKind:'buff',defaultAlwaysAllowed:true},secondStartingMove:{upgradeId:'start2',cost:400,max:1,requires:'moves',cannotDuplicateFirst:true,usesStartChoices:true},repertoire:{upgradeId:'moves',cost:1500,startMoves:2},singleTypeDamage:{multiplier:1.2,requiresSingleType:true,requiresMatchingMoveType:true,damagingOnly:true},cloudSave:{automaticUploads:false,manualButton:true,beforeUpdate:true,beforeLogout:true,minUploadGapMs:25000,hiddenScheduledRuleGapMs:21000,revisionConflictProtection:true,conflictAction:'read-merge-retry',sourceCommit:'d667c216ddc99ee7bbb16a0ca0528f25461f037e'}},
  changelog:G.CHANGELOG.map(c=>({date:c.d,title:c.title[1],new:(c.new||[]).map(x=>x[1]),changed:(c.chg||[]).map(x=>x[1]),fixed:(c.fix||[]).map(x=>x[1])}))};
fs.mkdirSync(path.join(__dirname,'data'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'data','game.json'),JSON.stringify(data,null,2)+'\n');
console.log(`Wiki snapshot: ${data.dex.length} Pokémon, ${starters.length} starters, ${moves.length} moves, ${moves.filter(m=>m.evolution).length} evolutions; ${commit.slice(0,7)}`);
