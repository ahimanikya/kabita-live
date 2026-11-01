// Owner-operated activation tooling. Never print credentials or participant data.
const {createRequire} = require('node:module');
const path = require('node:path');
const fs = require('node:fs');
const site = path.resolve(__dirname, '../../../projects/site');
const dep = createRequire(path.join(site, 'package.json'));
const project = 'kabita-live';
const projectNumber = '461114477576';
const appId = '1:461114477576:web:6fb2d3b62585037e9b55bd';
const bucket = 'kabita-live.firebasestorage.app';
const db = `projects/${project}/databases/(default)/documents`;
const evidence = path.resolve(__dirname, '../../research/toshali-anthology-2026-10-21/activation');
async function ownerToken() {
  const auth = dep('firebase-tools/lib/auth');
  const options = {project, ...auth.getGlobalDefaultAccount()};
  await dep('firebase-tools/lib/requireAuth').requireAuth(options);
  return (await auth.getAccessToken(options.tokens.refresh_token, options.authScopes)).access_token;
}
async function request(url, {token, method='GET', body, headers={}, allowed=[]}={}) {
  const res = await fetch(url, {method, headers:{...(token?{Authorization:`Bearer ${token}`} : {}), ...(body?{'Content-Type':'application/json'}:{}), ...headers}, body:body?JSON.stringify(body):undefined});
  const text = await res.text();
  let data; try {data=JSON.parse(text);} catch {data={};}
  if (!res.ok && !allowed.includes(res.status)) {
    let detail=String(data.error?.message || '');
    for(const value of [token, body?.token, body?.debugToken].filter(Boolean)) detail=detail.split(value).join('[redacted]');
    detail=detail.replace(/AIza[\w-]+/g,'[redacted]').slice(0,600);
    throw new Error(`${method} ${new URL(url).origin}${new URL(url).pathname}: HTTP ${res.status} (${data.error?.status || 'request rejected'}): ${detail}`);
  }
  return {status:res.status, data};
}
function fields(data) {
  return Object.fromEntries(Object.entries(data).map(([k,v])=>[k,typeof v==='boolean'?{booleanValue:v}:typeof v==='number'?{integerValue:String(v)}:{stringValue:v}]));
}
function save(name, value) {
  fs.writeFileSync(path.join(evidence,name), JSON.stringify(value,null,2)+'\n', {flag:'wx'});
}
module.exports={fs,path,site,dep,project,projectNumber,appId,bucket,db,evidence,ownerToken,request,fields,save};
