// Mechanical responsive encoding only: creative imagery is produced by imagegen.
const fs=require('fs'),path=require('path');
const sharp=require(require.resolve('sharp',{paths:[process.env.CODEX_MEDIA_NODE_MODULES||'C:/Users/lenovo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules']}));
const root=__dirname, out=path.join(root,'public/media');fs.mkdirSync(out,{recursive:true});
async function encode(source,id){
 const meta=await sharp(source).metadata();
 const variants=[...new Set([480,960,1440].filter(w=>w<=meta.width).concat(Math.min(1440,meta.width)))].sort((a,b)=>a-b);
 for(const width of variants){
  await sharp(source).resize({width}).webp({quality:83,effort:5}).toFile(path.join(out,`${id}-${width}.webp`));
 }
 const width=Math.min(1440,meta.width);const height=Math.round(meta.height*width/meta.width);
 return {width,height,variants};
}
(async()=>{
 const specs=JSON.parse(fs.readFileSync(path.join(root,'media-art.json'),'utf8'));
 const shots=JSON.parse(fs.readFileSync(path.join(root,'artifacts/media-raw/shots.json'),'utf8'));
 const assets=[];
 for(const art of specs){
  const meta=await encode(path.isAbsolute(art.source)?art.source:path.join(root,art.source),art.id);
  assets.push({...art,...meta,kind:'concept',source:undefined,rights:'Original AI-assisted concept art commissioned for this independent Wiki; no claim of official game artwork.',created:'2026-10-15'});
 }
 for(const shot of shots){
  const meta=await encode(path.join(root,'artifacts/media-raw',shot.id+'.png'),shot.id);
  assets.push({...shot,...meta,kind:'capture',controlledFixture:shot.id.startsWith('controlled-'),alt:shot.caption,created:'2026-10-15',
   source:'Local untouched JPTER78 game source, fresh disposable guest session; automatic keyboard/touch inputs. Gameplay clips use the unbundled dev.html build.',
   build:'b29708900da26b34e70d2dc07ad1659a719f4a78',scope:shot.id.startsWith('controlled-')?'Preconfigured Ember level five and Power; exposed developer level-up trigger. Visible controlled-demo label. Not an unassisted run.':'Normal game UI and keyboard/touch inputs; no stat, card or save-state edits.',platform:shot.id.startsWith('mobile-')?'Chromium touch emulation; not physical-device certification':'Windows Chromium, desktop keyboard',
   rights:'Game capture for the noncommercial fan guide. Game code MIT; embedded SpriteCollab artwork CC BY-NC 4.0. Attribution and individual artist credits linked beside media. Pokémon belongs to its owners.',
   attribution:'JPTER78 / PokéSurvivor; SpriteCollab artists (see linked CREDITS.md); Nintendo / Creatures / GAME FREAK'});
 }
 fs.writeFileSync(path.join(root,'media-images.json'),JSON.stringify(assets,null,2)+'\n');
 console.log(`Encoded ${assets.length} image masters into responsive WebP variants`);
})().catch(e=>{console.error(e);process.exitCode=1});
