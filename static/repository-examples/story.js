/* Original local evidence scene. No live-data calls; deck.gl is an optional view. */
"use strict";
const $ = id => document.getElementById(id);
const controls = ["view", "magnitude", "day", "exaggeration", "azimuth", "tilt"];
const canvas = $("scene"), ctx = canvas.getContext("2d");
let source = [], selected = [], plotted = [], deckView = null, deckLoad = null;
let inspectedId = null;
const INSPECT_PROMPT = "Select a point to inspect its ID, time, magnitude type, depth and source. The table contains the same records.";
const LOAD_TIMEOUT_MS = 15000;
let bounds = {minX:-1000,maxX:1000,minY:-1000,maxY:1000};
const rad = value => value * Math.PI / 180;
function local(event) {
  return [rad(event.longitude - 138) * 6371 * Math.cos(rad(38)), rad(event.latitude - 38) * 6371, -event.depth_km];
}
function color(depth) {
  const t = Math.max(0, Math.min(1, depth / 600));
  return [Math.round(225 - 187*t), Math.round(165 - 49*t), Math.round(62 + 73*t)];
}
function transform(position, mode) {
  let [x, y, z] = position;
  if (mode !== "2d") {
    z *= Number($("exaggeration").value);
    const angle = rad(Number($("azimuth").value)), tilt = rad(Number($("tilt").value));
    const rotatedX = x*Math.cos(angle) - y*Math.sin(angle);
    y = (x*Math.sin(angle) + y*Math.cos(angle))*Math.cos(tilt) + z*Math.sin(tilt);
    x = rotatedX;
  }
  return [x,y];
}
function project(position, mode, width, height) {
  const [x,y]=transform(position,mode);
  // Fit the complete source, never the filtered subset. Exaggeration/rotation
  // can change extent, but a filter alone never silently zooms the display.
  const scale=Math.min((width-90)/(bounds.maxX-bounds.minX),(height-90)/(bounds.maxY-bounds.minY));
  return [width/2+(x-(bounds.maxX+bounds.minX)/2)*scale,
          height/2-(y-(bounds.maxY+bounds.minY)/2)*scale];
}
function draw() {
  if (!ctx) { $("status").textContent = "Canvas is unavailable. Use the event table and downloads below."; return; }
  const dpr = window.devicePixelRatio || 1;
  const width = canvas.clientWidth || 900, height = canvas.clientHeight || 470;
  canvas.width = width*dpr; canvas.height = height*dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, width, height);
  const mode = $("view").value;
  const full=source.map(event=>transform(local(event),mode));
  full.push(...[[0,0,0],[500,0,0],[0,500,0],[0,0,-500]].map(p=>transform(p,mode)));
  bounds={minX:Math.min(...full.map(p=>p[0])),maxX:Math.max(...full.map(p=>p[0])),
          minY:Math.min(...full.map(p=>p[1])),maxY:Math.max(...full.map(p=>p[1]))};
  ctx.strokeStyle = "#d4dfe3"; ctx.lineWidth = 1; ctx.font = "12px system-ui";
  for (let offset=-1000; offset<=1000; offset+=500) {
    for (const pair of [[[offset,-1000,0],[offset,1000,0]],[[-1000,offset,0],[1000,offset,0]]]) {
      const a=project(pair[0],mode,width,height), b=project(pair[1],mode,width,height);
      ctx.beginPath(); ctx.moveTo(...a); ctx.lineTo(...b); ctx.stroke();
    }
  }
  const origin=project([0,0,0],mode,width,height);
  for (const [end,label] of [[[500,0,0],"E +500 km"],[[0,500,0],"N +500 km"],[[0,0,-500],"depth +500 km"]]) {
    if (mode === "2d" && end[2]) continue;
    const target=project(end,mode,width,height);
    ctx.strokeStyle="#768f9c"; ctx.fillStyle="#3d5e6f";
    ctx.beginPath(); ctx.moveTo(...origin); ctx.lineTo(...target); ctx.stroke();
    ctx.fillText(label,target[0]+4,target[1]-4);
  }
  plotted = selected.map(event => ({event, point: project(local(event),mode,width,height)}));
  for (const {event,point} of plotted) {
    const radius=Math.sqrt(12+18*(event.magnitude-4.5+1)**2)/2;
    ctx.beginPath(); ctx.arc(point[0],point[1],radius,0,Math.PI*2);
    ctx.fillStyle=`rgba(${color(event.depth_km).join(",")},0.8)`; ctx.fill();
    ctx.strokeStyle="white"; ctx.stroke();
  }
  ctx.fillStyle="#385868";
  ctx.fillText(mode === "2d" ? "2D · approximate local km · depth is color only" : `Canvas 3D · z = −depth × ${$("exaggeration").value} · display rotation`, 12, 20);
}
function showEvent(event) {
  if (!selected.some(row=>row.id === event.id)) return clearInspection();
  inspectedId = event.id;
  $("inspect").textContent = `${event.id} · ${event.time_utc} · magnitude ${event.magnitude} ${event.magnitude_type} · depth ${event.depth_km} km positive down · ${event.place}. `;
  const link=document.createElement("a"); link.href=event.source_url; link.textContent="USGS event source";
  $("inspect").appendChild(link);
}
function clearInspection() {
  inspectedId = null;
  $("inspect").textContent = INSPECT_PROMPT;
}
function renderTable() {
  const fragment=document.createDocumentFragment();
  for (const event of selected) {
    const tr=document.createElement("tr");
    for (const key of ["id","time_utc","longitude","latitude","depth_km","magnitude","magnitude_type","place"]) {
      const td=document.createElement("td");
      if (key === "id") {
        const link=document.createElement("a"); link.href=event.source_url; link.textContent=event.id;
        link.setAttribute("aria-label",`Open USGS event ${event.id} source`); td.appendChild(link);
      } else td.textContent=String(event[key]);
      tr.appendChild(td);
    }
    fragment.appendChild(tr);
  }
  $("event-rows").replaceChildren(fragment);
  $("table-title").textContent=`Filtered event table · ${selected.length} of ${source.length} records`;
}
function loadDeck() {
  if (globalThis.deck?.DeckGL) return Promise.resolve();
  if (deckLoad) return deckLoad;
  const script=document.createElement("script");
  script.src="https://cdn.jsdelivr.net/npm/deck.gl@9.1.0/dist.min.js";
  deckLoad = new Promise((resolve,reject) => {
    const fail=message=>{clearTimeout(timer);reject(new Error(message));};
    const timer=setTimeout(()=>fail("Pinned deck.gl resource timed out"),LOAD_TIMEOUT_MS);
    script.onload=()=>{clearTimeout(timer);resolve();};
    script.onerror=()=>fail("Pinned deck.gl resource could not be loaded");
    document.head.appendChild(script);
  }).catch(error=>{deckLoad=null;script.remove();throw error;});
  return deckLoad;
}
function deckCamera() {
  const exaggeration=Number($("exaggeration").value);
  const positions=source.map(event=>{const p=local(event);p[2]*=exaggeration;return p;});
  const target=[0,1,2].map(axis=>(Math.min(...positions.map(p=>p[axis]))+Math.max(...positions.map(p=>p[axis])))/2);
  // The full-source bounding sphere fits every rotation in an orthographic view.
  // OrbitView zoom 0 means one world unit per pixel; units here are local km.
  const diameter=2*Math.max(...positions.map(p=>Math.hypot(...p.map((value,axis)=>value-target[axis])))) || 1;
  const width=$("deck-scene").clientWidth || canvas.clientWidth || 900;
  const height=$("deck-scene").clientHeight || canvas.clientHeight || 470;
  const usable=Math.max(1,Math.min(width,height)-60);
  return {target,rotationX:Number($("tilt").value),rotationOrbit:Number($("azimuth").value),zoom:Math.log2(usable/diameter)};
}
async function enableDeck() {
  if (!source.length) return;
  try {
    await loadDeck();
    if ($("view").value !== "deck") return;
    const camera=deckCamera();
    if (!deckView) {
      deckView=new deck.DeckGL({container:$("deck-scene"), views:new deck.OrbitView({id:"orbit",orthographic:true}),
        initialViewState:camera, controller:false,
        getTooltip:({object})=>object ? `${object.id}\nM ${object.magnitude} ${object.magnitude_type}\ndepth ${object.depth_km} km` : null,
        onClick:info=>{if(info.object)showEvent(info.object);},
        onError:error=>{$("status").textContent=`deck.gl resource/GPU error: ${error.message}. Select the canvas view or use the table/downloads.`;}});
    }
    deckView.setProps({viewState:camera,
      layers:[new deck.PointCloudLayer({id:"catalog-events",data:selected,coordinateSystem:deck.COORDINATE_SYSTEM.CARTESIAN,
        getPosition:event=>{const p=local(event);p[2]*=Number($("exaggeration").value);return p;},
        getColor:event=>[...color(event.depth_km),220],pointSize:5,pickable:true,
        updateTriggers:{getPosition:[$("exaggeration").value]}})]});
  } catch(error) {
    if ($("view").value !== "deck") return;
    $("status").textContent=`Optional deck.gl unavailable: ${error.message}. Canvas/table fallback is active.`;
    $("view").value="3d"; $("deck-scene").hidden=true; canvas.hidden=false; draw();
  }
}
function update() {
  // Keep the server-rendered evidence table intact during loading or a failure.
  if (!source.length) return;
  selected=source.filter(event=>event.magnitude >= Number($("magnitude").value) && Number(event.time_utc.slice(8,10)) <= Number($("day").value));
  if (inspectedId && !selected.some(event=>event.id === inspectedId)) clearInspection();
  for (const id of controls.slice(1)) $(id+"-value").textContent=$(id).value + (id === "exaggeration" ? "×" : ["azimuth","tilt"].includes(id) ? "°" : "");
  $("status").textContent=`${selected.length} of ${source.length} checksum-validated catalog events · magnitude ≥${$("magnitude").value} · through January ${$("day").value} UTC · ${$("view").value === "2d" ? "depth color only" : "vertical exaggeration "+$("exaggeration").value+"×"}`;
  const optional=$("view").value === "deck";
  $("deck-scene").hidden=!optional; canvas.hidden=optional;
  renderTable();
  if (optional) enableDeck(); else draw();
}
function reset() {
  for (const [id,value] of Object.entries({view:"2d",magnitude:"4.5",day:"31",exaggeration:"1",azimuth:"25",tilt:"45"})) $(id).value=value;
  clearInspection();
  selectChapter("overview");
}
canvas.addEventListener("click",event=>{
  const box=canvas.getBoundingClientRect(), x=event.clientX-box.left,y=event.clientY-box.top;
  const nearest=plotted.map(point=>({...point,distance:Math.hypot(point.point[0]-x,point.point[1]-y)})).sort((a,b)=>a.distance-b.distance)[0];
  if(nearest && nearest.distance < 15)showEvent(nearest.event);
});
for (const id of controls) $(id).addEventListener("input",update);
$("reset").addEventListener("click",reset);
const chapters={overview:["Locate the selection","The query selected magnitude ≥4.5 events between 30–46° N and 128–148° E, January 1 inclusive to February 1 exclusive UTC. These 78 epicenters are a bounded catalog selection; map overlap does not predict another event.","2d","4.5","31","1"],
  sequence:["Focus on the first days","This view emphasizes reported magnitude ≥5 through January 3 UTC. A temporal/spatial cluster describes this filtered catalog, not a proven causal sequence or an aftershock classification. Compare the visible count with the full 78-record selection.","2d","5","3","1"],
  depth:["Look below the surface","Return to all selected events and rotate the canvas scene. Catalog depth is positive down, so scene z is negative. The initial 2× exaggeration makes separation easier to see but changes perspective; try 1× and compare the numeric depths.","3d","4.5","31","2"]};
function selectChapter(name) {
  const [title,text,view,mag,day,exag]=chapters[name];
  $("chapter-title").textContent=title;$("chapter-text").textContent=text;
  for(const other of document.querySelectorAll("[data-chapter]"))other.setAttribute("aria-pressed",String(other.dataset.chapter===name));
  $("view").value=view;$("magnitude").value=mag;$("day").value=day;$("exaggeration").value=exag;update();
}
for (const button of document.querySelectorAll("[data-chapter]"))button.addEventListener("click",()=>selectChapter(button.dataset.chapter));
$("filtered-download").addEventListener("click",()=>{
  const keys=["id","time_utc","longitude","latitude","depth_km","magnitude","magnitude_type","place","source_url"];
  const quote=value=>'"'+String(value).replaceAll('"','""')+'"';
  const csv=[keys.join(","),...selected.map(event=>keys.map(key=>quote(event[key])).join(","))].join("\r\n");
  const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));
  const link=document.createElement("a");link.href=url;link.download=`usgs-filtered-m${$("magnitude").value}-day${$("day").value}.csv`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
window.addEventListener("resize",()=>{$("view").value === "deck" ? enableDeck() : draw();});
async function sceneBytes() {
  const controller=new AbortController();
  let timer;
  try {
    return await Promise.race([
      (async()=>{
        const response=await fetch("scene-data.json",{signal:controller.signal});
        if(!response.ok)throw new Error(`Local data HTTP ${response.status}`);
        return response.arrayBuffer();
      })(),
      new Promise((resolve,reject)=>{timer=setTimeout(()=>{controller.abort();reject(new Error("Local scene fetch/body timed out after 15 seconds"));},LOAD_TIMEOUT_MS);})
    ]);
  } finally { clearTimeout(timer); }
}
(async()=>{
  try {
    const bytes=await sceneBytes();
    if(!globalThis.crypto?.subtle)throw new Error("Checksum verification requires HTTPS or localhost");
    const digest=await crypto.subtle.digest("SHA-256",bytes);
    const actual=Array.from(new Uint8Array(digest),byte=>byte.toString(16).padStart(2,"0")).join("");
    if(actual !== JSON.parse($("scene-checksum").textContent))throw new Error("Scene checksum mismatch; no substitute events will be generated");
    const payload=JSON.parse(new TextDecoder().decode(bytes));
    if(payload.events.length !== 78 || payload.events.some(event=>![event.longitude,event.latitude,event.depth_km,event.magnitude].every(Number.isFinite)))throw new Error("Scene schema/count mismatch");
    source=payload.events;$("filtered-download").disabled=false;update();
  }catch(error){$("status").textContent=`Scene loading failed: ${error.message}. The static table and packaged downloads remain available.`;}
})();
