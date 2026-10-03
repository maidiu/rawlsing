import fs from "node:fs"; import path from "node:path";
const D = "/Users/matthewsmith/Desktop/Rawlsing/review-hq192a2/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/dispatcher.mjs";
const m = await import(D);
const ROOT = "/tmp/hq192a2/lockretest"; fs.rmSync(ROOT, {recursive:true,force:true}); fs.mkdirSync(ROOT,{recursive:true});
const mk = (n) => { const d = path.join(ROOT,n); const st = new m.Store(d); return {d, st, lock: path.join(d,"writer.lock")}; };
const HEX = "abcdef0123456789";

// 1. DEAD owner in the CORRECT lock format -> must be reclaimed fast
{
  const {st, lock} = mk("dead");
  fs.writeFileSync(lock, `pid=999999 token=${HEX}`);
  const t0 = Date.now(); let ok=false, err=null;
  try { st.append({task_id:"D",attempt:1,seq:1,state:"QUEUED"}); ok=true; } catch(e){ err=e.code; }
  console.log(`[${ok?"OK":"FINDING"}] dead-owner reclaim (correct format): reclaimed=${ok} err=${err} in ${Date.now()-t0}ms`);
}
// 2. LIVE owner (our pid) in correct format with OLD mtime -> must NOT reclaim
{
  const {st, lock} = mk("live");
  fs.writeFileSync(lock, `pid=${process.pid} token=${HEX}`);
  const old = Date.now()/1000 - 900; fs.utimesSync(lock, old, old);
  const t0 = Date.now(); let blocked=false, code=null;
  try { st.append({task_id:"L",attempt:1,seq:1,state:"QUEUED"}); } catch(e){ blocked=true; code=e.code; }
  console.log(`[${blocked && code==="WRITER_LOCK_TIMEOUT"?"OK":"FINDING"}] live-owner not reclaimed: blocked=${blocked} code=${code} waited=${Date.now()-t0}ms`);
}
// 3. legacy/token-only lock -> cannot prove dead -> must NOT reclaim
{
  const {st, lock} = mk("legacy");
  fs.writeFileSync(lock, "somelegacytoken");
  const old = Date.now()/1000 - 900; fs.utimesSync(lock, old, old);
  const t0 = Date.now(); let blocked=false, code=null;
  try { st.append({task_id:"G",attempt:1,seq:1,state:"QUEUED"}); } catch(e){ blocked=true; code=e.code; }
  console.log(`[${blocked?"OK":"FINDING"}] legacy token-only lock not reclaimed (owner unknown): blocked=${blocked} code=${code} waited=${Date.now()-t0}ms`);
}
// 4. MR-1 regression under the NEW lock format: concurrent admission still exact
