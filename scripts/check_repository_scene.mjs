/* Focused scene/control/failure checks using a DOM/canvas/deck test double.
 * Camera parameters and loader behavior are checked; browser/GPU drawing is not.
 */
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import path from "node:path";
import {fileURLToPath} from "node:url";
import vm from "node:vm";
import {webcrypto} from "node:crypto";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const directory=path.join(root,"static/repository-examples");
const bytes=await readFile(path.join(directory,"scene-data.json"));
const provenance=JSON.parse(await readFile(path.join(directory,"provenance.json"),"utf8"));
const program=await readFile(path.join(directory,"story.js"),"utf8");
const source=JSON.parse(bytes.toString("utf8")).events;
const staticHtml=await readFile(path.join(directory,"index.html"),"utf8");
for(const event of source){
  assert(staticHtml.includes(`<a href="${event.source_url}" aria-label="Open USGS event ${event.id} source">${event.id}</a>`),`Static source anchor missing: ${event.id}`);
}
const delay=()=>new Promise(resolve=>setTimeout(resolve,5));
async function until(condition){for(let i=0;i<100&&!condition();i++)await delay();assert(condition(),"Asynchronous scene operation did not settle");}

function environment({badHash=false,failedFetch=false,stalledFetch=false,stalledBody=false,noCanvas=false,deckOutcomes=["error"]}={}){
  const elements=new Map(), drawings=[], downloads=[], blobs=new Map(), scripts=[], deckInstances=[], windowEvents=new Map();
  let context, requestSignal;
  class Element{
    constructor(tag="div"){this.tag=tag;this.children=[];this.value="";this.textContent="";this.handlers={};this.dataset={};this.clientWidth=1000;this.clientHeight=620;}
    set textContent(value){this._textContent=String(value);this.children=[];}
    get textContent(){return this._textContent+this.children.map(child=>child.textContent).join("");}
    addEventListener(name,fn){this.handlers[name]=fn;}
    appendChild(child){this.children.push(child);return child;}
    replaceChildren(...children){this._textContent="";this.children=children.flatMap(child=>child.tag==="fragment"?child.children:[child]);}
    setAttribute(name,value){this[name]=value;}
    getBoundingClientRect(){return {left:0,top:0};}
    remove(){this.removed=true;}
    click(){if(this.tag==="a")downloads.push({name:this.download,href:this.href,blob:blobs.get(this.href)});else this.handlers.click?.({});}
    getContext(){return noCanvas?null:{setTransform(){},clearRect(){drawings.length=0;},beginPath(){},moveTo(){},lineTo(){},stroke(){},fill(){},fillText(){},arc(x,y,r){drawings.push({x,y,r});}};}
  }
  const mockDeck={
    DeckGL:class{constructor(props){this.props=props;deckInstances.push(this);}setProps(props){Object.assign(this.props,props);}},
    OrbitView:class{constructor(props){this.props=props;}},
    PointCloudLayer:class{constructor(props){this.props=props;}},
    COORDINATE_SYSTEM:{CARTESIAN:0}
  };
  const get=id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id);};
  for(const [id,value] of Object.entries({view:"2d",magnitude:"4.5",day:"31",exaggeration:"1",azimuth:"25",tilt:"45"}))get(id).value=value;
  get("scene-checksum").textContent=JSON.stringify(badHash?"invalid":provenance.scene_sha256);
  get("event-rows").children=source.map(()=>new Element("tr"));
  const chapters=["overview","sequence","depth"].map(name=>{const button=new Element("button");button.dataset.chapter=name;return button;});
  const document={getElementById:get,querySelectorAll:()=>chapters,createElement:tag=>new Element(tag),createDocumentFragment:()=>new Element("fragment"),
    head:{appendChild:script=>{
      scripts.push(script);
      const outcome=deckOutcomes[scripts.length-1] || "error";
      setTimeout(()=>{if(outcome==="success"){context.deck=mockDeck;script.onload();}else if(outcome==="error")script.onerror();},0);
    }}};
  context=vm.createContext({document,window:{devicePixelRatio:1,addEventListener(name,fn){windowEvents.set(name,fn);}},crypto:webcrypto,
    fetch:async(url,options)=>{
      requestSignal=options.signal;
      if(stalledFetch)return new Promise(()=>{});
      return {ok:!failedFetch,status:503,arrayBuffer:async()=>stalledBody?new Promise(()=>{}):bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)};
    },
    TextDecoder,Blob,AbortController,
    URL:{createObjectURL(blob){const url=`blob:test-${blobs.size}`;blobs.set(url,blob);return url;},revokeObjectURL(){}},
    setTimeout:(fn,ms)=>setTimeout(fn,ms===15000?30:ms),clearTimeout,console});
  vm.runInContext(program,context);
  return {get,drawings,downloads,chapters,scripts,deckInstances,windowEvents,signal:()=>requestSignal,run:code=>vm.runInContext(code,context)};
}

function parseCsv(text){
  const rows=[];let row=[],field="",quoted=false;
  for(let i=0;i<text.length;i++){
    const char=text[i];
    if(quoted){if(char==='"'){if(text[i+1]==='"'){field+='"';i++;}else quoted=false;}else field+=char;}
    else if(char==='"'){assert.equal(field,"");quoted=true;}
    else if(char===','){row.push(field);field="";}
    else if(char==='\r'||char==='\n'){if(char==='\r'&&text[i+1]==='\n')i++;row.push(field);rows.push(row);row=[];field="";}
    else field+=char;
  }
  assert(!quoted,"Unterminated CSV quote");
  if(field||row.length){row.push(field);rows.push(row);}
  return rows;
}
async function checkDownload(app,expected){
  app.get("filtered-download").click();
  const download=app.downloads.at(-1);
  assert.match(download.name,/usgs-filtered/);
  assert(download.blob instanceof Blob);
  const csv=parseCsv(await download.blob.text());
  const keys=["id","time_utc","longitude","latitude","depth_km","magnitude","magnitude_type","place","source_url"];
  assert.deepEqual(csv[0],keys);
  assert.equal(csv.length-1,expected.length);
  assert.deepEqual(csv.slice(1),expected.map(event=>keys.map(key=>String(event[key]))));
}

const app=environment();
await until(()=>app.run("source.length")===78);
assert.equal(app.run("selected.length"),78);
assert.equal(app.get("event-rows").children.length,78);
assert.equal(app.drawings.length,78);
for(const [i,row] of app.get("event-rows").children.entries()){
  const link=row.children[0].children[0];
  assert.equal(link.href,source[i].source_url);
  assert.equal(link.textContent,source[i].id);
  assert.equal(link["aria-label"],`Open USGS event ${source[i].id} source`);
}
app.run("showEvent(source.find(event=>Number(event.time_utc.slice(8,10))>3))");
assert(app.run("inspectedId"));
app.chapters[1].click();
const early=source.filter(event=>event.magnitude>=5&&Number(event.time_utc.slice(8,10))<=3);
assert.equal(app.run("selected.length"),early.length);
assert.equal(app.get("event-rows").children.length,early.length);
assert.equal(app.run("inspectedId"),null);
assert.match(app.get("inspect").textContent,/Select a point/);
assert.equal(app.get("inspect").children.length,0);
await checkDownload(app,early);
app.chapters[2].click();
assert.equal(app.get("view").value,"3d");
assert.equal(app.get("exaggeration").value,"2");
assert.equal(app.run("local({longitude:138,latitude:38,depth_km:100})[2]"),-100);
for(const exag of [1,6])for(const azimuth of [0,90,180,270])for(const tilt of [5,85]){
  app.get("exaggeration").value=String(exag);app.get("azimuth").value=String(azimuth);app.get("tilt").value=String(tilt);app.run("update()");
  assert(app.drawings.every(p=>p.x>=30&&p.x<=970&&p.y>=30&&p.y<=590),"Canvas controls clipped an event");
}
const oldBounds=app.run("JSON.stringify(bounds)");
app.get("magnitude").value="7.5";app.run("update()");
assert.equal(app.run("JSON.stringify(bounds)"),oldBounds,"Filtering changed canvas extent");
app.get("reset").click();
assert.equal(app.run("selected.length"),78);
assert.equal(app.get("chapter-title").textContent,"Locate the selection");
assert.equal(app.chapters[0]["aria-pressed"],"true");
assert(app.chapters.slice(1).every(button=>button["aria-pressed"]==="false"));
assert.equal(app.get("exaggeration").value,"1");
assert.equal(app.run("inspectedId"),null);
// Change only an isolated test fixture to exercise commas, quotes and embedded CRLF.
const quotedPlace='Fixture "quoted", first line\r\nsecond line';
app.run(`source[0].place=${JSON.stringify(quotedPlace)};update()`);
await checkDownload(app,source.map((event,index)=>({...event,place:index===0?quotedPlace:event.place})));
assert.equal(parseCsv(await app.downloads.at(-1).blob.text())[1][7],quotedPlace);

for(const firstOutcome of ["error","stall"]){
  const retry=environment({deckOutcomes:[firstOutcome,"success"]});
  await until(()=>retry.run("source.length")===78);
  retry.get("view").value="deck";retry.run("update()");
  await until(()=>retry.get("view").value==="3d");
  assert.match(retry.get("status").textContent,/Optional deck.gl unavailable/);
  assert.equal(retry.run("deckLoad"),null);
  assert(retry.scripts[0].removed);
  retry.get("view").value="deck";
  await retry.run("enableDeck()");
  assert.equal(retry.scripts.length,2);
  assert.equal(retry.deckInstances.length,1);
  assert.equal(retry.get("event-rows").children.length,78);
}
const successful=environment({deckOutcomes:["success"]});
await until(()=>successful.run("source.length")===78);
successful.get("view").value="deck";
await successful.run("enableDeck()");
const deck=successful.deckInstances[0];
assert.equal(deck.props.views.props.orthographic,true);
assert.equal(successful.scripts.length,1);
assert.equal(successful.scripts[0].src,"https://cdn.jsdelivr.net/npm/deck.gl@9.1.0/dist.min.js");
for(const width of [1000,320])for(const exag of [1,6])for(const azimuth of [0,90,180,270])for(const tilt of [5,85]){
  successful.get("deck-scene").clientWidth=width;
  successful.get("exaggeration").value=String(exag);successful.get("azimuth").value=String(azimuth);successful.get("tilt").value=String(tilt);
  await successful.run("enableDeck()");
  const camera=deck.props.viewState,layer=deck.props.layers[0].props;
  assert(Number.isFinite(camera.zoom)&&camera.target.every(Number.isFinite));
  assert.equal(camera.rotationX,tilt);assert.equal(camera.rotationOrbit,azimuth);
  for(const event of source){
    const p=layer.getPosition(event);
    assert.equal(p[2],-event.depth_km*exag);
    const radius=Math.hypot(...p.map((value,axis)=>value-camera.target[axis]));
    assert(radius*2**camera.zoom <= (Math.min(width,620)-60)/2+1e-6,"Orthographic camera clips the transformed full-source extent");
  }
}
const fullCamera=JSON.stringify(deck.props.viewState);
successful.get("magnitude").value="7.5";successful.run("update()");await successful.run("enableDeck()");
assert.equal(JSON.stringify(deck.props.viewState),fullCamera,"Filtering changed deck camera");
successful.get("deck-scene").clientWidth=280;successful.windowEvents.get("resize")();await delay();
assert(deck.props.viewState.zoom<JSON.parse(fullCamera).zoom,"Mobile resize did not refit camera");
for(const options of [{badHash:true},{failedFetch:true},{stalledFetch:true},{stalledBody:true}]){
  const failed=environment(options);
  await until(()=>failed.get("status").textContent.includes("Scene loading failed"));
  assert.equal(failed.run("source.length"),0);
  failed.run("update()");
  assert.equal(failed.get("event-rows").children.length,78,"A failed load/control cleared the static fallback table");
  if(options.stalledFetch||options.stalledBody){assert.match(failed.get("status").textContent,/timed out/);assert(failed.signal().aborted);}
}
const withoutCanvas=environment({noCanvas:true});
await until(()=>withoutCanvas.run("source.length")===78);
assert.equal(withoutCanvas.get("event-rows").children.length,78);
assert.match(withoutCanvas.get("status").textContent,/Canvas is unavailable/);
console.log("Scene regressions passed: reset/inspection state; static and filtered source anchors; decoded CSV values/quoting; loader success/error/timeout/retry; desktop/mobile orthographic camera fit; fetch/body deadlines; checksum/HTTP/canvas fallbacks. Browser/GPU drawing remains untested.");
