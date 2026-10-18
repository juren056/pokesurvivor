'use strict';
const wikiLocale=window.WIKI_LOCALE||'en';
const wikiI18n=window.WIKI_I18N||{};
function wikiText(key,fallback,vars={}){let value=wikiI18n[key]||fallback;for(const [name,replacement] of Object.entries(vars))value=value.replaceAll(`{${name}}`,replacement);return value;}
document.querySelectorAll('.guide-video video').forEach(video=>{
  const showError=()=>{const message=video.closest('.guide-video').querySelector('.video-error');if(message)message.hidden=false;};
  video.addEventListener('error',showError);
  video.querySelector('source')?.addEventListener('error',showError);
});
document.documentElement.classList.add('js');
const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#site-nav');
const languageMenu=document.querySelector('.language-menu');
function closeMenu(){nav?.classList.remove('is-open');menu?.setAttribute('aria-expanded','false');}
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open);});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(menu?.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus();}if(languageMenu?.open){languageMenu.open=false;languageMenu.querySelector('summary').focus();}}});
document.addEventListener('click',e=>{if(languageMenu?.open&&!languageMenu.contains(e.target))languageMenu.open=false;});
nav?.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});

document.querySelectorAll('[data-table]').forEach(section=>{
  const form=section.querySelector('[data-filter-form]');
  if(!form)return;
  const input=form.querySelector('[data-filter]'),type=form.querySelector('[data-type]');
  const rows=[...section.querySelectorAll('tbody tr')];
  const initialType=new URLSearchParams(location.search).get('type');
  if(initialType&&[...type.options].some(option=>option.value===initialType))type.value=initialType;
  const filter=()=>{
    const q=input.value.trim().toLocaleLowerCase();
    let count=0;
    rows.forEach(row=>{const match=row.textContent.toLocaleLowerCase().includes(q)&&(!type.value||row.dataset.types.split(' ').includes(type.value));row.hidden=!match;if(match)count++;});
    section.querySelector('[data-count]').textContent=wikiText('entries',`${count} of ${rows.length} entries`,{count:String(count),total:String(rows.length)});
    section.querySelector('[data-empty]').hidden=count!==0;
  };
  form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('input',filter);form.addEventListener('change',filter);form.addEventListener('reset',()=>setTimeout(filter,0));filter();
  section.querySelectorAll('[data-sort]').forEach(button=>button.addEventListener('click',()=>{
    const heading=button.closest('th'),column=Number(button.dataset.sort),ascending=heading.getAttribute('aria-sort')!=='ascending';
    section.querySelectorAll('th').forEach(h=>h.setAttribute('aria-sort','none'));
    heading.setAttribute('aria-sort',ascending?'ascending':'descending');
    const direction=ascending?1:-1;
    rows.sort((a,b)=>{
      const av=a.cells[column].textContent.trim(),bv=b.cells[column].textContent.trim();
      if(av==='—'||bv==='—')return av===bv?0:av==='—'?1:-1;
      const an=Number.parseFloat(av),bn=Number.parseFloat(bv);
      return direction*(Number.isNaN(an)||Number.isNaN(bn)?av.localeCompare(bv):an-bn);
    });
    section.querySelector('tbody').append(...rows);
    filter();
  }));
});

let dataPromise;
function gameData(){return dataPromise||=fetch('/assets/game.json').then(r=>{if(!r.ok)throw Error('Reference data unavailable');return r.json();});}
const lab=document.querySelector('[data-starter-lab]');
if(lab){
  gameData().then(data=>{
    const set=(name,text)=>{lab.querySelector(`[data-lab-${name}]`).textContent=text;};
    function update(){
      const selected=lab.querySelector('input[name="opening-partner"]:checked');
      const partner=data.starters.find(p=>p.dex===Number(selected.value));
      const move=data.moves.find(m=>m.id===partner.start);
      lab.dataset.element=partner.types[0];
      const typeNames=wikiI18n.typeNames||{};
      set('name',partner.name);set('type',partner.types.map(t=>typeNames[t]||t[0].toUpperCase()+t.slice(1)).join(' / ')+' · '+wikiText('starterPartner','Starter partner'));
      set('number','#'+String(partner.dex).padStart(3,'0'));set('hp',partner.hp);set('speed',partner.spd);set('attack',partner.atk.toFixed(2)+'×');
      set('move',move.name);set('evolution',move.evolution.name);
      set('requirement',wikiText('levelRequirement',`Level ${move.maxLevel} + ${move.evolution.requirement} in this run, then choose the golden card.`,{level:String(move.maxLevel),requirement:move.evolution.requirement}));
      lab.querySelector('[data-lab-link]').href=(wikiLocale==='en'?'/':'/'+wikiLocale+'/')+'move-evolutions/#'+move.id;
      const glyph=selected.closest('label').querySelector('svg').cloneNode(true);
      glyph.setAttribute('width','37');glyph.setAttribute('height','37');
      lab.querySelector('[data-lab-emblem]').replaceChildren(glyph);
    }
    lab.querySelectorAll('input[name="opening-partner"]').forEach(input=>input.addEventListener('change',update));update();
  }).catch(()=>{
    lab.querySelector('.starter-choices').hidden=true;
    const notice=document.createElement('p');notice.className='lab-requirement';notice.setAttribute('role','status');
    notice.textContent='Interactive preview could not load. The Charmander example is shown; use the starter guide to compare every option.';
    lab.append(notice);
  });
}
const evo=document.querySelector('[data-evolution]');
if(evo){
  const result=document.querySelector('#evo-result');
  result.textContent=wikiText('loadingEvolution','Loading move requirements…');
  gameData().then(data=>{
    const move=document.querySelector('#evo-move'),level=document.querySelector('#evo-level'),stat=document.querySelector('#evo-stat');
    function update(){
      const m=data.moves.find(m=>m.id===move.value),n=Number(level.value);
      level.max=String(m.maxLevel);
      if(!m.evolution){result.textContent=wikiText('noEvolution',`${m.name} has no move evolution in this snapshot.`,{move:m.name});return;}
      if(level.value===''||!Number.isInteger(n)||n<1||n>m.maxLevel){result.textContent=wikiText('invalidLevel',`Enter a whole level from 1 to ${m.maxLevel}.`,{max:String(m.maxLevel)});return;}
      const missing=[];
      if(n<m.maxLevel)missing.push(wikiText('reachLevel',`reach level ${m.maxLevel}`,{level:String(m.maxLevel)}));
      if(!stat.checked)missing.push(wikiText('takeStat',`take ${m.evolution.requirement} in this run`,{stat:m.evolution.requirement}));
      result.textContent=missing.length?`${m.name} → ${m.evolution.name}: ${missing.join(wikiLocale==='zh-hant'?'、':' + ')}.`:wikiText('eligible',`Eligible for ${m.evolution.name}. Choose the golden evolution card when offered; it does not evolve automatically.`,{evolution:m.evolution.name});
    }
    move.addEventListener('change',()=>{stat.checked=false;update();});level.addEventListener('input',update);stat.addEventListener('change',update);update();
  }).catch(()=>{result.textContent=wikiText('loadFail','The checker could not load. Use the evolution table below or reload to try again.');});
}
const matchup=document.querySelector('[data-matchup]');
if(matchup){
  const out=document.querySelector('#type-result');out.textContent=wikiText('loadingTypes','Loading type rules…');
  gameData().then(data=>{
    const a=document.querySelector('#attack-type'),b=document.querySelector('#defend-type'),c=document.querySelector('#defend-second');
    function update(){
      [...c.options].forEach(o=>o.disabled=o.value===b.value);
      if(c.value===b.value)c.value='';
      const mult=c.value?data.matchups[a.value][b.value][c.value]:data.matrix[a.value][b.value];
      out.textContent=wikiText('damage',`${a.selectedOptions[0].text} → ${b.selectedOptions[0].text}${c.value?' / '+c.selectedOptions[0].text:''}: ${Number(mult.toFixed(3))}× damage`,{attack:a.selectedOptions[0].text,defense:b.selectedOptions[0].text+(c.value?' / '+c.selectedOptions[0].text:''),mult:String(Number(mult.toFixed(3)))});
    }
    [a,b,c].forEach(s=>s.addEventListener('change',update));update();
  }).catch(()=>{out.textContent=wikiText('typeFail','The calculator could not load. Use the single-type table below or reload to try again.');});
}
const planner=document.querySelector('[data-build-planner]');
if(planner){
  const starter=planner.querySelector('#build-starter'),secondary=planner.querySelector('#build-secondary'),result=planner.querySelector('#build-result'),share=planner.querySelector('#build-share');
  gameData().then(data=>{
    const params=new URLSearchParams(location.search);
    if(data.starters.some(p=>String(p.dex)===params.get('p')))starter.value=params.get('p');
    function allowed(partner,move){return move.type==='normal'||partner.types.includes(move.type);}
    function refreshMoves(preferred){
      const partner=data.starters.find(p=>p.dex===Number(starter.value));
      [...secondary.options].forEach(option=>{const move=data.moves.find(m=>m.id===option.value);option.hidden=!allowed(partner,move);option.disabled=!allowed(partner,move)||move.id===partner.start;});
      const candidates=[...secondary.options].filter(o=>!o.disabled&&!o.hidden);
      secondary.value=candidates.some(o=>o.value===preferred)?preferred:candidates[0]?.value||'';
    }
    function update(){
      const partner=data.starters.find(p=>p.dex===Number(starter.value));
      const primary=data.moves.find(m=>m.id===partner.start),extra=data.moves.find(m=>m.id===secondary.value);
      const evolution=m=>m?.evolution?wikiText('moveEvolution',`${m.name} → ${m.evolution.name}: level ${m.maxLevel} + ${m.evolution.requirement}`,{move:m.name,evolution:m.evolution.name,level:String(m.maxLevel),requirement:m.evolution.requirement}):wikiText('moveNoEvolution',`${m?.name||'Move'}: no evolution in this snapshot`,{move:m?.name||'Move'});
      result.textContent=wikiText('buildSummary',`${partner.name} starts with ${evolution(primary)}. Secondary route: ${evolution(extra)}. Compatible pool: ${partner.types.join(' / ')} and Normal moves.`,{partner:partner.name,primary:evolution(primary),secondary:evolution(extra),types:partner.types.join(' / ')});
      const url=new URL(location.href);url.search='';url.searchParams.set('p',partner.dex);if(extra)url.searchParams.set('m',extra.id);share.dataset.url=url.href;
    }
    refreshMoves(params.get('m'));update();
    starter.addEventListener('change',()=>{refreshMoves();update();});secondary.addEventListener('change',update);
    share.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(share.dataset.url);share.textContent=wikiText('linkCopied','Link copied');setTimeout(()=>share.textContent=wikiText('copyLink','Copy share link'),1600);}catch{result.textContent+=' '+wikiText('copyFail','Copying was blocked; use the URL shown in your address bar.');}});
  }).catch(()=>{result.textContent=wikiText('plannerFail','The planner could not load. Use the routes and evolution table below.');share.disabled=true;});
}
const gacha=document.querySelector('[data-gacha]');
if(gacha){
  const pulls=gacha.querySelector('#gacha-pulls'),pity=gacha.querySelector('#gacha-pity'),out=gacha.querySelector('#gacha-result');
  function updateGacha(){
    const n=Number(pulls.value),p=Number(pity.value);
    if(!Number.isInteger(n)||n<1||n>1000||!Number.isInteger(p)||p<0||p>69){out.textContent=wikiText('gachaInvalid','Enter 1–1000 pulls and current pity from 0–69.');return;}
    const five=(1-Math.pow(.985,n))*100,shiny=(1-Math.pow(.99,n))*100,hard=n>=70-p;
    const base=wikiText('gachaSummary',`Base chance of at least one rarity 5: ${five.toFixed(2)}%. Base chance of at least one shiny-eligible roll: ${shiny.toFixed(2)}%.`,{five:five.toFixed(2),shiny:shiny.toFixed(2)});
    const pityText=hard?wikiText('pityReach',`This window reaches the 70-pull hard pity after at most ${70-p} pulls.`,{pulls:String(70-p)}):wikiText('pityRemain',`Hard pity is not guaranteed within this window; ${70-p} pulls remain from the entered state.`,{pulls:String(70-p)});
    out.textContent=base+' '+pityText;
  }
  pulls.addEventListener('input',updateGacha);pity.addEventListener('input',updateGacha);updateGacha();
}
const saveDiagnostic=document.querySelector('[data-save-diagnostic]');
if(saveDiagnostic){
  const game=saveDiagnostic.querySelector('#save-game'),login=saveDiagnostic.querySelector('#save-login'),copy=saveDiagnostic.querySelector('#save-copy'),symptom=saveDiagnostic.querySelector('#save-symptom');
  const result=saveDiagnostic.querySelector('#save-result'),report=saveDiagnostic.querySelector('#save-report'),run=saveDiagnostic.querySelector('[data-diagnostic-run]'),copyButton=saveDiagnostic.querySelector('[data-report-copy]');
  const labels=select=>select.selectedOptions[0].textContent.trim();
  function diagnose(){
    let next;
    if(copy.value==='yes')next=wikiText('savePreserve','Preserve that browser and profile. Do not clear site data or uninstall the PWA. Link the account only through the official game if it is safe to do so.');
    else if(login.value==='linked')next=wikiText('saveLinked','On the official domain, use Sign in with Google with the same linked Gmail. If progress stays missing, contact the developer with this non-sensitive report.');
    else if(login.value==='guest')next=wikiText('saveGuest','Recovery is uncertain for an unlinked guest. Keep the original browser and profile unchanged and contact the developer; do not trust a site asking for credentials or a save upload.');
    else next=wikiText('saveUnknown','Recovery is uncertain. Preserve any remaining browser data and contact the developer with non-sensitive facts before trying destructive changes.');
    result.textContent=next;
    report.value=[
      'PokéSurvivor recovery report (no credentials or save data)',
      `Location: ${labels(game)}`,
      `Account state: ${labels(login)}`,
      `Surviving copy: ${labels(copy)}`,
      `Visible symptom: ${labels(symptom)}`,
      `Safe next step: ${next}`
    ].join('\n');
    copyButton.disabled=false;
  }
  run.addEventListener('click',diagnose);
  copyButton.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(report.value);copyButton.textContent=wikiText('reportCopied','Report copied');setTimeout(()=>copyButton.textContent=wikiText('copyReport','Copy report'),1600);}catch{result.textContent+=' '+wikiText('reportCopyFail','Copying was blocked. Select the report text and copy it manually.');}});
}
const searchInput=document.querySelector('#search-query');
if(searchInput){
  const form=searchInput.closest('form'),list=document.querySelector('#search-results'),status=document.querySelector('#search-status');
  const initial=new URLSearchParams(location.search).get('q')||'';searchInput.value=initial.slice(0,100);
  let indexPromise;
  function index(){const file=wikiLocale==='en'?'/assets/search.json':`/assets/search-${wikiLocale}.json`;return indexPromise||=fetch(file).then(r=>{if(!r.ok)throw Error('Search unavailable');return r.json();}).catch(err=>{indexPromise=null;throw err;});}
  let version=0;
  async function search(){
    const request=++version,q=searchInput.value.trim().slice(0,100);list.replaceChildren();
    if(!q){status.textContent=wikiText('searchHint','Try a Pokémon name, a move or a question such as mobile.');return;}
    status.textContent=wikiText('searching','Searching…');
    try{
      const entries=await index();if(request!==version)return;
      const words=q.toLocaleLowerCase().split(/\s+/);
      const results=entries.filter(p=>words.every(w=>(p.title+' '+p.text).toLocaleLowerCase().includes(w)));
      status.textContent=results.length?wikiText('results',`${results.length} results.`,{count:String(results.length)}):wikiText('noResults','No results. Try a shorter name, a move, or browse the navigation.');
      results.slice(0,60).forEach(p=>{const li=document.createElement('li'),small=document.createElement('small'),a=document.createElement('a'),desc=document.createElement('p');small.textContent=p.kind;a.href=p.url;a.textContent=p.title;desc.textContent=p.text;li.append(small,a,desc);list.append(li);});
    }catch{if(request===version)status.textContent=wikiText('searchFail','Search could not load. Submit again to retry, or browse the guides and databases above.');}
  }
  form.addEventListener('submit',e=>{e.preventDefault();const q=searchInput.value.trim().slice(0,100);history.replaceState(null,'',q?'?q='+encodeURIComponent(q):location.pathname);search();});
  window.addEventListener('popstate',()=>{searchInput.value=(new URLSearchParams(location.search).get('q')||'').slice(0,100);search();});search();
}
