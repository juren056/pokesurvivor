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
      set('number','#'+String(partner.dex).padStart(3,'0'));set('hp',partner.hp);set('speed',partner.spd);set('attack',partner.pa.toFixed(2)+'× / '+partner.sa.toFixed(2)+'×');
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
    move.addEventListener('change',()=>{stat.checked=false;update();window.wikiTrack?.('evolution_check',{move:move.value});});level.addEventListener('input',update);stat.addEventListener('change',()=>{update();window.wikiTrack?.('evolution_check',{move:move.value,eligible:stat.checked&&Number(level.value)>=Number(level.max)});});update();
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
  const starter=planner.querySelector('#build-starter'),owned=planner.querySelector('#build-start-owned'),starting=planner.querySelector('#build-starting'),repertoire=planner.querySelector('#build-repertoire'),secondOwned=planner.querySelector('#build-second-owned'),secondary=planner.querySelector('#build-secondary'),taught=planner.querySelector('#build-tm'),result=planner.querySelector('#build-result'),share=planner.querySelector('#build-share');
  gameData().then(data=>{
    const params=new URLSearchParams(location.search);
    if(data.starters.some(p=>String(p.dex)===params.get('p')))starter.value=params.get('p');
    const byMove=id=>data.moves.find(move=>move.id===id);
    const tmById=id=>data.tms.find(tm=>tm.id===id);
    function legalIds(partner){
      const ids=new Set(partner.startChoices||[partner.baseStart]);
      const tm=tmById(taught.value);
      if(tm&&tm.compatibleDex.includes(partner.dex)&&!data.naturalMoves[String(partner.dex)].includes(tm.id))ids.add(tm.id);
      return ids;
    }
    function refreshMoves(preferredSecondary,preferredStarting,preferredTm){
      const partner=data.starters.find(p=>p.dex===Number(starter.value));
      const natural=new Set(data.naturalMoves[String(partner.dex)]||[]);
      [...taught.options].forEach(option=>{if(!option.value)return;const tm=tmById(option.value);option.hidden=!tm||!tm.compatibleDex.includes(partner.dex)||natural.has(option.value);option.disabled=option.hidden;});
      const tmChoices=[...taught.options].filter(o=>!o.disabled&&!o.hidden);
      taught.value=tmChoices.some(o=>o.value===preferredTm)?preferredTm:'';
      const legal=legalIds(partner);
      [...starting.options].forEach(option=>{option.hidden=!legal.has(option.value);option.disabled=!legal.has(option.value)||(!owned.checked&&option.value!==partner.baseStart);});
      const legalEnabled=[...starting.options].filter(o=>!o.disabled&&!o.hidden);
      starting.value=legalEnabled.some(o=>o.value===preferredStarting)?preferredStarting:partner.baseStart;
      [...secondary.options].forEach(option=>{const move=byMove(option.value);option.hidden=!legal.has(option.value)||move?.kind==='buff';option.disabled=option.hidden||option.value===starting.value||!repertoire.checked;});
      const candidates=[...secondary.options].filter(o=>!o.hidden&&o.value!==starting.value);
      secondary.value=candidates.some(o=>o.value===preferredSecondary)?preferredSecondary:candidates[0]?.value||'';
      secondOwned.disabled=!repertoire.checked;if(secondOwned.disabled)secondOwned.checked=false;
    }
    function update(){
      const partner=data.starters.find(p=>p.dex===Number(starter.value));
      const base=byMove(partner.baseStart),primary=byMove(starting.value),extra=byMove(secondary.value);
      const evolution=m=>m?.evolution?wikiText('moveEvolution',`${m.name} → ${m.evolution.name}: level ${m.maxLevel} + ${m.evolution.requirement}`,{move:m.name,evolution:m.evolution.name,level:String(m.maxLevel),requirement:m.evolution.requirement}):wikiText('moveNoEvolution',`${m?.name||'Move'}: no evolution in this snapshot`,{move:m?.name||'Move'});
      const fit=m=>{
        if(!m)return '';
        if(!m.category)return `${m.name}: buff ${m.buffStat||''}`.trim();
        const value=m.category==='physical'?partner.pa:partner.sa;
        const other=m.category==='physical'?partner.sa:partner.pa;
        const warning=value<other?'; uses the weaker offensive side':'';
        const mono=partner.types.length===1&&m.type===partner.types[0];
        return `${m.name}: ${m.category}, ${value.toFixed(2)}×${mono?'; matching single-type damage factor 1.20×':''}${warning}`;
      };
      const first=owned.checked?wikiText('startingUnlocked','first selector unlocked'):wikiText('startingLocked','default first move');
      const second=!repertoire.checked?wikiText('repertoireLocked','Repertoire not purchased'):secondOwned.checked?wikiText('secondSelected','second selector unlocked: {move}',{move:extra?.name||''}):wikiText('secondRandom','Repertoire gives a random legal second move; planner preview: {move}',{move:extra?.name||''});
      const secondFit=repertoire.checked&&extra?` [${fit(extra)}]`:'';
      const cost=(owned.checked?400:0)+(repertoire.checked?1500:0)+(secondOwned.checked?400:0);
      result.textContent=`${partner.name}. ${first}: ${evolution(primary)} [${fit(primary)}]. ${second}${secondFit}. Modelled unlock cost: ${cost.toLocaleString()} coins. The 20% factor applies only to damaging moves matching a single-type partner.`;
      const url=new URL(location.href);url.search='';url.searchParams.set('p',partner.dex);if(extra&&repertoire.checked)url.searchParams.set('m',extra.id);if(owned.checked){url.searchParams.set('u','1');url.searchParams.set('s',primary.id);}if(repertoire.checked)url.searchParams.set('r','1');if(secondOwned.checked)url.searchParams.set('u2','1');if(taught.value)url.searchParams.set('tm',taught.value);url.searchParams.set('v','8');share.dataset.url=url.href;
    }
    owned.checked=params.get('u')==='1';repertoire.checked=params.get('r')==='1'||params.has('m');secondOwned.checked=params.get('u2')==='1';refreshMoves(params.get('m'),params.get('s'),params.get('tm'));update();
    starter.addEventListener('change',()=>{refreshMoves();update();});owned.addEventListener('change',()=>{refreshMoves(secondary.value,starting.value,taught.value);update();});repertoire.addEventListener('change',()=>{refreshMoves(secondary.value,starting.value,taught.value);update();});secondOwned.addEventListener('change',()=>{refreshMoves(secondary.value,starting.value,taught.value);update();});taught.addEventListener('change',()=>{refreshMoves(secondary.value,starting.value,taught.value);update();});starting.addEventListener('change',()=>{refreshMoves(secondary.value,starting.value,taught.value);update();window.wikiTrack?.('starting_move_select',{partner:String(starter.value),move:starting.value});});secondary.addEventListener('change',update);
    share.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(share.dataset.url);window.wikiTrack?.('build_share',{locale:wikiLocale});share.textContent=wikiText('linkCopied','Link copied');setTimeout(()=>share.textContent=wikiText('copyLink','Copy share link'),1600);}catch{result.textContent+=' '+wikiText('copyFail','Copying was blocked; use the URL shown in your address bar.');}});
  }).catch(()=>{result.textContent=wikiText('plannerFail','The planner could not load. Use the routes and evolution table below.');share.disabled=true;});
}

const shopPreview=document.querySelector('[data-shop-preview]');
if(shopPreview){
  const partner=shopPreview.querySelector('#shop-partner'),out=shopPreview.querySelector('#shop-result'),list=shopPreview.querySelector('#shop-tms');
  const seedText=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Madrid',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  const hash=text=>{let h=2166136261;for(const c of text){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;};
  const shuffle=(items,seed)=>{let x=hash(seed);const a=[...items];for(let i=a.length-1;i>0;i--){x=(Math.imul(x,1664525)+1013904223)>>>0;const j=x%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;};
  gameData().then(data=>{
    function update(){const dex=Number(partner.value),date=seedText(),natural=new Set(data.naturalMoves[String(dex)]||[]),base=shuffle(data.tms,`kecleon:${date}`).slice(0,data.shop.dailyTmCount),learnable=data.tms.filter(t=>t.compatibleDex.includes(dex)&&!natural.has(t.id));let offers=[...base];if(!offers.some(t=>learnable.some(x=>x.id===t.id))&&learnable.length)offers[offers.length-1]=shuffle(learnable,`kecleon:${date}:${dex}`)[0];const name=data.dex.find(p=>p.dex===dex)?.name||'';out.textContent=`${date} · Europe/Madrid · ${name}: ${offers.length} rule-based TM offers. Empty taught-TM assumption.`;list.replaceChildren(...offers.map(t=>{const li=document.createElement('li');li.textContent=`${t.name} — ${t.price.toLocaleString()} coins${t.compatibleDex.includes(dex)&&!natural.has(t.id)?' · compatible':''}`;return li;}));}
    partner.addEventListener('change',update);update();
  }).catch(()=>out.textContent='The source-backed preview could not load. Use the rules below.');
}

const tmChecker=document.querySelector('[data-tm-checker]');
if(tmChecker){
  const partner=tmChecker.querySelector('#tm-partner'),move=tmChecker.querySelector('#tm-move'),taught=tmChecker.querySelector('#tm-taught'),out=tmChecker.querySelector('#tm-result'),share=tmChecker.querySelector('#tm-share');
  gameData().then(data=>{const params=new URLSearchParams(location.search);if(data.dex.some(p=>String(p.dex)===params.get('p')))partner.value=params.get('p');if(data.tms.some(t=>t.id===params.get('tm')))move.value=params.get('tm');taught.checked=params.get('taught')==='1';function update(){const dex=Number(partner.value),p=data.dex.find(x=>x.dex===dex),tm=data.tms.find(x=>x.id===move.value),natural=(data.naturalMoves[String(dex)]||[]).includes(tm.id);let state=natural?'natural move — no TM needed':tm.compatibleDex.includes(dex)?taught.checked?'compatible and modelled as already taught':'compatible, not taught; obtain and use the TM':'incompatible in this source snapshot';out.textContent=`${p.name} → ${tm.name}: ${state}. Shop price: ${tm.price.toLocaleString()} coins.`;const url=new URL(location.href);url.search='';url.searchParams.set('p',dex);url.searchParams.set('tm',tm.id);if(taught.checked)url.searchParams.set('taught','1');share.dataset.url=url.href;}[partner,move,taught].forEach(x=>x.addEventListener('change',update));share.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(share.dataset.url);share.textContent=wikiText('linkCopied','Link copied');setTimeout(()=>share.textContent=wikiText('copyLink','Copy share link'),1600);}catch{out.textContent+=' Copying was blocked; use the address bar.';}});update();}).catch(()=>{out.textContent='Compatibility data could not load.';share.disabled=true;});
}

const natureCalculator=document.querySelector('[data-nature-calculator]');
if(natureCalculator){
  const partner=natureCalculator.querySelector('#nature-partner'),choice=natureCalculator.querySelector('#nature-choice'),out=natureCalculator.querySelector('#nature-result');
  gameData().then(data=>{function update(){const p=data.dex.find(x=>x.dex===Number(partner.value)),n=data.natures.find(x=>x.id===choice.value),labels={pa:'Attack',sa:'Special Attack',df:'Defense',sd:'Special Defense',spd:'Speed'},stats=['pa','sa','df','sd','spd'].map(k=>`${labels[k]} ${(p[k]*(n.up===k?1.1:n.down===k?.9:1)).toFixed(2)}`);out.textContent=`${p.name} · ${n.names[wikiLocale]||n.names.en}: HP ${p.hp} (unchanged); ${stats.join(' · ')}.`;}partner.addEventListener('change',update);choice.addEventListener('change',update);update();}).catch(()=>out.textContent='Nature data could not load.');
}

const abilityChecker=document.querySelector('[data-ability-checker]');
if(abilityChecker){
  const partner=abilityChecker.querySelector('#ability-partner'),out=abilityChecker.querySelector('#ability-result');
  gameData().then(data=>{function update(){const dex=Number(partner.value),p=data.dex.find(x=>x.dex===dex),slots=data.abilitySlots[String(dex)]||[],name=id=>data.abilities.find(a=>a.id===id),describe=(id,label)=>{const a=name(id);return a?`${label}: ${a.names[wikiLocale]||a.names.en} — ${(a.effects&&a.effects[wikiLocale])||a.effect}`:`${label}: ${wikiText('abilityNone','none')}`;};out.textContent=`${p.name}. ${describe(slots[0],wikiText('abilityRegular1','Regular 1'))} ${describe(slots[1],wikiText('abilityRegular2','Regular 2'))} ${describe(slots[2],wikiText('abilityHidden','Hidden'))}`;}partner.addEventListener('change',update);update();}).catch(()=>out.textContent=wikiText('abilityLoadFail','Ability data could not load.'));
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
  const game=saveDiagnostic.querySelector('#save-game'),login=saveDiagnostic.querySelector('#save-login'),copy=saveDiagnostic.querySelector('#save-copy'),state=saveDiagnostic.querySelector('#save-state'),second=saveDiagnostic.querySelector('#save-second'),timing=saveDiagnostic.querySelector('#save-timing');
  const result=saveDiagnostic.querySelector('#save-result'),report=saveDiagnostic.querySelector('#save-report'),run=saveDiagnostic.querySelector('[data-diagnostic-run]'),copyButton=saveDiagnostic.querySelector('[data-report-copy]');
  const labels=select=>select.selectedOptions[0].textContent.trim();
  function diagnose(){
    let next;
    if(copy.value==='yes'&&(second.value==='no'||state.value!=='success'))next=wikiText('savePreserveMismatch','Preserve the original device and its browser profile. Saved locally, pending, syncing, cloud success and loaded on the second device are different states. Do not clear site data or upload an older copy while investigating.');
    else if(copy.value==='yes')next=wikiText('savePreserve','Preserve that browser and profile. Do not clear site data or uninstall the PWA. Link the account only through the official game if it is safe to do so.');
    else if(login.value==='linked')next=wikiText('saveLinked','On the official domain, use Sign in with Google with the same linked Gmail. If progress stays missing, contact the developer with this non-sensitive report.');
    else if(login.value==='guest')next=wikiText('saveGuest','Recovery is uncertain for an unlinked guest. Keep the original browser and profile unchanged and contact the developer; do not trust a site asking for credentials or a save upload.');
    else next=wikiText('saveUnknown','Recovery is uncertain. Preserve any remaining browser data and contact the developer with non-sensitive facts before trying destructive changes.');
    result.textContent=next;
    report.value=[
      'PokéSurvivor recovery report (no credentials or save data)',
      `Device handoff: ${labels(game)}`,
      `Account state: ${labels(login)}`,
      `Original device complete: ${labels(copy)}`,
      `Original save state: ${labels(state)}`,
      `Second device same collection: ${labels(second)}`,
      `Difference appeared: ${labels(timing)}`,
      `Safe next step: ${next}`
    ].join('\n');
    copyButton.disabled=false;
  }
  run.addEventListener('click',diagnose);
  copyButton.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(report.value);copyButton.textContent=wikiText('reportCopied','Report copied');setTimeout(()=>copyButton.textContent=wikiText('copyReport','Copy report'),1600);}catch{result.textContent+=' '+wikiText('reportCopyFail','Copying was blocked. Select the report text and copy it manually.');}});
}
const coopDiagnostic=document.querySelector('[data-coop-diagnostic]');
if(coopDiagnostic){
  const site=coopDiagnostic.querySelector('#coop-site'),stage=coopDiagnostic.querySelector('#coop-stage'),network=coopDiagnostic.querySelector('#coop-network');
  const result=coopDiagnostic.querySelector('#coop-result'),report=coopDiagnostic.querySelector('#coop-report'),run=coopDiagnostic.querySelector('[data-coop-run]'),copyButton=coopDiagnostic.querySelector('[data-coop-copy]');
  function coopCheck(){
    const steps=[];
    if(site.value==='embedded')steps.push(wikiText('coopOfficial','Open pokesurvivor.com directly. The current game blocks third-party iframe play; this Wiki cannot provide a proxy or restore an account.'));
    if(stage.value==='friend')steps.push(wikiText('coopInvite','Confirm the intended accounts, accepted friendship and one fresh invitation to the current room.'));
    if(stage.value==='connecting'){
      steps.push(wikiText('coopConnecting','Appearing in a room does not prove the peer connection is ready. Check the current version and keep the host active.'));
      if(network.value==='different')steps.push(wikiText('coopDifferent','The current client prefers a direct connection and can use the TURN pilot for authorized accounts. Without credentials it continues with STUN only; this does not prove universal service availability.'));
      if(network.value==='same')steps.push(wikiText('coopSame','The same network does not rule out another cause. Record the result without resetting accounts or deleting data.'));
    }
    if(stage.value==='boss')steps.push(wikiText('coopBoss','This is a running-game issue. The October 19 changelog describes a far-away boss spawning fix; check the visible version and whether it still repeats.'));
    if(stage.value==='move')steps.push(wikiText('coopMove','Record the move, level, evolution state, partner, mode and game version. Issue #232 is a player report, not proof that every move is broken.'));
    steps.push(wikiText('coopReport','Record the exact message, host or join role, browser/device category and approximate time. Remove nicknames, IP addresses and private details.'));
    result.textContent=steps.join(' ');
    report.value=[wikiText('coopReportTitle','PokéSurvivor co-op checklist (no credentials, saves or raw WebRTC data)'),`Site: ${site.selectedOptions[0].textContent.trim()}`,`Stage: ${stage.selectedOptions[0].textContent.trim()}`,`Network comparison: ${network.selectedOptions[0].textContent.trim()}`,...steps.map((x,i)=>`${i+1}. ${x}`)].join('\n');
    copyButton.disabled=false;
    window.wikiTrack?.('diagnosis_complete',{tool:'coop',stage:stage.value,network:network.value});
  }
  run.addEventListener('click',coopCheck);
  copyButton.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(report.value);copyButton.textContent=wikiText('checklistCopied','Checklist copied');setTimeout(()=>copyButton.textContent=wikiText('copyChecklist','Copy checklist'),1600);}catch{result.textContent+=' '+wikiText('checklistCopyFail','Copying was blocked. Select the checklist and copy it manually.');}});
}
const moveMaster=document.querySelector('[data-move-master]');
if(moveMaster){
  const KEY='pokesurvivor.wiki.moveMaster.v1',SCHEMA=1,MAX_FILE=200000;
  const list=moveMaster.querySelector('#master-list'),count=moveMaster.querySelector('#master-count'),status=moveMaster.querySelector('#master-status');
  const search=moveMaster.querySelector('#master-search'),filter=moveMaster.querySelector('#master-filter'),importer=moveMaster.querySelector('[data-master-import]');
  let memoryOnly=false,known=[],completed=new Set(),unknown=[];
  const store=()=>{const value={schemaVersion:SCHEMA,datasetVersion:'2026-10-21',completedMoveIds:[...completed],unknownMoveIds:unknown,updatedAt:new Date().toISOString()};try{localStorage.setItem(KEY,JSON.stringify(value));}catch{memoryOnly=true;status.textContent=wikiText('masterMemory','Storage is unavailable. Changes remain only until this page closes.');}return value;};
  const load=()=>{try{const raw=localStorage.getItem(KEY);if(!raw)return;if(raw.length>MAX_FILE)throw Error();const value=JSON.parse(raw);if(value.schemaVersion!==SCHEMA||!Array.isArray(value.completedMoveIds))throw Error();completed=new Set(value.completedMoveIds.filter(x=>typeof x==='string'));unknown=Array.isArray(value.unknownMoveIds)?value.unknownMoveIds.filter(x=>typeof x==='string'):[];}catch{memoryOnly=true;status.textContent=wikiText('masterInvalidStored','The saved checklist was invalid. A temporary empty checklist is open.');}};
  function renderMaster(){
    const q=search.value.trim().toLocaleLowerCase(),mode=filter.value;
    list.replaceChildren();let shown=0;
    known.filter(m=>{const done=completed.has(m.id);return(!q||(m.name+' '+m.evolution.name).toLocaleLowerCase().includes(q))&&(mode==='all'||(mode==='done'&&done)||(mode==='open'&&!done));}).forEach(m=>{
      shown++;const label=document.createElement('label'),box=document.createElement('input'),span=document.createElement('span');box.type='checkbox';box.checked=completed.has(m.id);box.setAttribute('aria-label',`${m.name} → ${m.evolution.name}`);span.textContent=`${m.name} → ${m.evolution.name}`;box.addEventListener('change',()=>{box.checked?completed.add(m.id):completed.delete(m.id);store();renderMaster();window.wikiTrack?.('move_master_toggle',{state:box.checked?'done':'open'});});label.append(box,span);list.append(label);
    });
    const valid=[...completed].filter(id=>known.some(m=>m.id===id)).length;
    count.textContent=wikiText('masterCount',`${valid} of ${known.length} completed · ${shown} shown`,{done:String(valid),total:String(known.length),shown:String(shown)})+(memoryOnly?' · '+wikiText('masterMemoryShort','temporary memory only'):'');
  }
  load();
  gameData().then(data=>{known=data.moves.filter(m=>m.evolution);const ids=new Set(known.map(m=>m.id));unknown=[...new Set([...unknown,...completed].filter(id=>!ids.has(id)))];completed=new Set([...completed].filter(id=>ids.has(id)));store();renderMaster();}).catch(()=>{status.textContent=wikiText('masterLoadFail','The checklist could not load. Use the static table below.');});
  search.addEventListener('input',renderMaster);filter.addEventListener('change',renderMaster);
  moveMaster.querySelector('[data-master-export]').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(store(),null,2)+'\n'],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='pokesurvivor-move-master.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),0);window.wikiTrack?.('move_master_export',{count:String(completed.size)});});
  importer.addEventListener('change',async()=>{const file=importer.files[0];importer.value='';if(!file)return;if(file.size>MAX_FILE){status.textContent=wikiText('masterTooLarge','Import rejected: the file is too large.');return;}try{const value=JSON.parse(await file.text());if(value.schemaVersion!==SCHEMA||!Array.isArray(value.completedMoveIds))throw Error();const ids=new Set(known.map(m=>m.id)),incoming=[...new Set(value.completedMoveIds.filter(x=>typeof x==='string'))],bad=incoming.filter(id=>!ids.has(id));completed=new Set(incoming.filter(id=>ids.has(id)));unknown=[...new Set([...(Array.isArray(value.unknownMoveIds)?value.unknownMoveIds:[]),...bad].filter(x=>typeof x==='string'))];store();renderMaster();status.textContent=bad.length?wikiText('masterUnknown',`Imported with ${bad.length} unknown ID(s) retained for review.`,{count:String(bad.length)}):wikiText('masterImported','Checklist imported.');window.wikiTrack?.('move_master_import',{unknown:String(bad.length)});}catch{status.textContent=wikiText('masterInvalid','Import rejected: choose a valid Move Master JSON file.');}});
  moveMaster.querySelector('[data-master-reset]').addEventListener('click',()=>{if(!confirm(wikiText('masterResetConfirm','Reset every completed move in this browser checklist?')))return;completed.clear();unknown=[];store();renderMaster();status.textContent=wikiText('masterReset','Checklist reset.');window.wikiTrack?.('move_master_reset',{});});
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
