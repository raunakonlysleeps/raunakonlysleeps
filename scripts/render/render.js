const {chromium}=require('playwright');const fs=require('fs');
const [,,only,N0]=process.argv;const N=+N0||1;
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
for(const s of only.split(',')){const V={hero:[1280,560],mods:[640,440],roblox:[640,440],city:[1280,380]}[s];const p=await b.newPage({viewport:{width:V[0],height:V[1]}});p.on('pageerror',e=>console.log(s,e.message));
await p.goto('http://localhost:8765/scene.html?s='+s);await p.waitForFunction('window.ready');await p.evaluate(()=>document.fonts.ready);
const d=`frames/${s}`;fs.mkdirSync(d,{recursive:true});
for(let i=0;i<N;i++){await p.evaluate(t=>frame(t),N==1?.3:i/N);await p.screenshot({path:`${d}/${String(i).padStart(3,'0')}.png`})}
await p.close();console.log(s,'done')}await b.close()})();
