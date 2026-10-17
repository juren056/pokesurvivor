'use strict';
document.querySelectorAll('.guide-video video').forEach(video=>{
  const showError=()=>{const message=video.closest('.guide-video').querySelector('.video-error');if(message)message.hidden=false;};
  video.addEventListener('error',showError);
  video.querySelector('source')?.addEventListener('error',showError);
});
document.documentElement.classList.add('js');
const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#site-nav');
function closeMenu(){nav?.classList.remove('is-open');menu?.setAttribute('aria-expanded','false');}
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open);});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus();}});
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
    section.querySelector('[data-count]').textContent=`${count} of ${rows.length} entries`;
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
      set('name',partner.name);set('type',partner.types.map(t=>t[0].toUpperCase()+t.slice(1)).join(' / ')+' · Starter partner');
      set('number','#'+String(partner.dex).padStart(3,'0'));set('hp',partner.hp);set('speed',partner.spd);set('attack',partner.atk.toFixed(2)+'×');
      set('move',move.name);set('evolution',move.evolution.name);
      set('requirement',`Level ${move.maxLevel} + ${move.evolution.requirement} in this run, then choose the golden card.`);
      lab.querySelector('[data-lab-link]').href='/move-evolutions/#'+move.id;
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
  result.textContent='Loading move requirements…';
  gameData().then(data=>{
    const move=document.querySelector('#evo-move'),level=document.querySelector('#evo-level'),stat=document.querySelector('#evo-stat');
    function update(){
      const m=data.moves.find(m=>m.id===move.value),n=Number(level.value);
      level.max=String(m.maxLevel);
      if(!m.evolution){result.textContent=`${m.name} has no move evolution in this snapshot.`;return;}
      if(level.value===''||!Number.isInteger(n)||n<1||n>m.maxLevel){result.textContent=`Enter a whole level from 1 to ${m.maxLevel}.`;return;}
      const missing=[];
      if(n<m.maxLevel)missing.push(`reach level ${m.maxLevel}`);
      if(!stat.checked)missing.push(`take ${m.evolution.requirement} in this run`);
      result.textContent=missing.length?`${m.name} → ${m.evolution.name}: ${missing.join(' and ')}.`:`Eligible for ${m.evolution.name}. Choose the golden evolution card when offered; it does not evolve automatically.`;
    }
    move.addEventListener('change',()=>{stat.checked=false;update();});level.addEventListener('input',update);stat.addEventListener('change',update);update();
  }).catch(()=>{result.textContent='The checker could not load. Use the evolution table below or reload to try again.';});
}
const matchup=document.querySelector('[data-matchup]');
if(matchup){
  const out=document.querySelector('#type-result');out.textContent='Loading type rules…';
  gameData().then(data=>{
    const a=document.querySelector('#attack-type'),b=document.querySelector('#defend-type'),c=document.querySelector('#defend-second');
    function update(){
      [...c.options].forEach(o=>o.disabled=o.value===b.value);
      if(c.value===b.value)c.value='';
      const mult=c.value?data.matchups[a.value][b.value][c.value]:data.matrix[a.value][b.value];
      out.textContent=`${a.selectedOptions[0].text} → ${b.selectedOptions[0].text}${c.value?' / '+c.selectedOptions[0].text:''}: ${Number(mult.toFixed(3))}× damage`;
    }
    [a,b,c].forEach(s=>s.addEventListener('change',update));update();
  }).catch(()=>{out.textContent='The calculator could not load. Use the single-type table below or reload to try again.';});
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
      const evolution=m=>m?.evolution?`${m.name} → ${m.evolution.name}: level ${m.maxLevel} + ${m.evolution.requirement}`:`${m?.name||'Move'}: no evolution in this snapshot`;
      result.textContent=`${partner.name} starts with ${evolution(primary)}. Secondary route: ${evolution(extra)}. Compatible pool: ${partner.types.join(' / ')} and Normal moves.`;
      const url=new URL(location.href);url.search='';url.searchParams.set('p',partner.dex);if(extra)url.searchParams.set('m',extra.id);share.dataset.url=url.href;
    }
    refreshMoves(params.get('m'));update();
    starter.addEventListener('change',()=>{refreshMoves();update();});secondary.addEventListener('change',update);
    share.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(share.dataset.url);share.textContent='Link copied';setTimeout(()=>share.textContent='Copy share link',1600);}catch{result.textContent+=' Copying was blocked; use the URL shown in your address bar after changing a selection.';}});
  }).catch(()=>{result.textContent='The planner could not load. Use the routes and evolution table below.';share.disabled=true;});
}
const gacha=document.querySelector('[data-gacha]');
if(gacha){
  const pulls=gacha.querySelector('#gacha-pulls'),pity=gacha.querySelector('#gacha-pity'),out=gacha.querySelector('#gacha-result');
  function updateGacha(){
    const n=Number(pulls.value),p=Number(pity.value);
    if(!Number.isInteger(n)||n<1||n>1000||!Number.isInteger(p)||p<0||p>69){out.textContent='Enter 1–1000 pulls and current pity from 0–69.';return;}
    const five=(1-Math.pow(.985,n))*100,shiny=(1-Math.pow(.99,n))*100,hard=n>=70-p;
    out.textContent=`Base chance of at least one rarity 5: ${five.toFixed(2)}%. Base chance of at least one shiny-eligible roll: ${shiny.toFixed(2)}%. ${hard?`This window reaches the 70-pull hard pity after at most ${70-p} pull${70-p===1?'':'s'}.`:`Hard pity is not guaranteed within this window; ${70-p} pulls remain from the entered state.`}`;
  }
  pulls.addEventListener('input',updateGacha);pity.addEventListener('input',updateGacha);updateGacha();
}
const searchInput=document.querySelector('#search-query');
if(searchInput){
  const form=searchInput.closest('form'),list=document.querySelector('#search-results'),status=document.querySelector('#search-status');
  const initial=new URLSearchParams(location.search).get('q')||'';searchInput.value=initial.slice(0,100);
  let indexPromise;
  function index(){return indexPromise||=fetch('/assets/search.json').then(r=>{if(!r.ok)throw Error('Search unavailable');return r.json();}).catch(err=>{indexPromise=null;throw err;});}
  let version=0;
  async function search(){
    const request=++version,q=searchInput.value.trim().slice(0,100);list.replaceChildren();
    if(!q){status.textContent='Try a Pokémon name, a move or a question such as mobile.';return;}
    status.textContent='Searching…';
    try{
      const entries=await index();if(request!==version)return;
      const words=q.toLocaleLowerCase().split(/\s+/);
      const results=entries.filter(p=>words.every(w=>(p.title+' '+p.text).toLocaleLowerCase().includes(w)));
      status.textContent=results.length?`${results.length} results${results.length>60?' — showing the first 60. Add another word to narrow them down.':'.'}`:'No results. Try a shorter name, a move, or browse the navigation.';
      results.slice(0,60).forEach(p=>{const li=document.createElement('li'),small=document.createElement('small'),a=document.createElement('a'),desc=document.createElement('p');small.textContent=p.kind;a.href=p.url;a.textContent=p.title;desc.textContent=p.text;li.append(small,a,desc);list.append(li);});
    }catch{if(request===version)status.textContent='Search could not load. Submit again to retry, or browse the guides and databases above.';}
  }
  form.addEventListener('submit',e=>{e.preventDefault();const q=searchInput.value.trim().slice(0,100);history.replaceState(null,'',q?'?q='+encodeURIComponent(q):location.pathname);search();});
  window.addEventListener('popstate',()=>{searchInput.value=(new URLSearchParams(location.search).get('q')||'').slice(0,100);search();});search();
}
