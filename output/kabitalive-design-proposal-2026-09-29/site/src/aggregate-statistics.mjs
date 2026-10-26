import {observeReading} from './analytics-reading.mjs';
export const OPT_OUT='kabita-audience-opt-out-v1';
export function referralCategory(referrer,origin){
 if(!referrer)return 'direct_or_unknown';
 try{const u=new URL(referrer);if(u.origin===origin)return 'internal';const h=u.hostname.toLowerCase();
 if(/(^|\.)(google\.[a-z.]+|bing\.com|duckduckgo\.com)$/.test(h))return 'search';
 if(/(^|\.)(facebook\.com|instagram\.com|t\.co|twitter\.com|x\.com|linkedin\.com)$/.test(h))return 'social';
 return 'other';}catch{return 'direct_or_unknown';}
}
export function foregroundTime(perf,fallback,start=0){
 const entries=perf.getEntriesByType('visibility-state');
 if(!entries.length)return fallback;
 return entries.reduce((total,e,i)=>total+(e.name==='visible'?Math.max(0,(entries[i+1]?.startTime??perf.now())-Math.max(start,e.startTime)):0),0);
}
export function startAggregate(runtime,{win=window,doc=document,send=fetch}={}){
 const c=runtime.audience,publicPages=c?.publicPages||{};
 const path=win.location.pathname;
 if(c?.enabled!==true||c.policyReviewed!==true||win.location.protocol!=='https:'||!c.allowedHosts?.includes(win.location.hostname)||!Object.hasOwn(publicPages,path)||!/^https:\/\/asia-south1-kabita-live\.cloudfunctions\.net\/audienceCount$/.test(c.endpoint||''))return null;
 let optedOut=false;try{optedOut=win.localStorage.getItem(OPT_OUT)==='yes';}catch{}
 const blocked=()=>optedOut||win.navigator.globalPrivacyControl===true||win.navigator.doNotTrack==='1'||win.doNotTrack==='1';
 const seen=new Set(),screen=win.innerWidth<768?'small':win.innerWidth<1200?'medium':'large';let sent=0;
 const publish=(metric,route=path)=>{
  if(blocked()||doc.visibilityState!=='visible'||sent>=40||!Object.hasOwn(publicPages,route)||seen.has(route+':'+metric))return false;
  seen.add(route+':'+metric);sent++;
  // Fixed public path and enum only. No cookies, referrer header, IDs, query strings or timestamps.
  Promise.resolve(send(c.endpoint,{method:'POST',credentials:'omit',referrerPolicy:'no-referrer',headers:{'Content-Type':'application/json'},body:JSON.stringify({path:route,metric}),keepalive:true})).catch(()=>{});
  return true;
 };
 const view=()=>{publish('view');publish('screen_'+screen);publish('referral_'+referralCategory(doc.referrer,win.location.origin));};
 const state=doc.createElement('span'),button=doc.createElement('button');button.type='button';button.className='btn';
 const update=()=>{button.textContent=optedOut?'Allow aggregate statistics':'Turn off aggregate statistics';state.textContent=blocked()?' Aggregate statistics are off.':' Aggregate statistics are on; Google Analytics remains a separate choice.';};
 button.addEventListener('click',()=>{optedOut=!optedOut;try{if(optedOut)win.localStorage.setItem(OPT_OUT,'yes');else win.localStorage.removeItem(OPT_OUT);}catch{}update();if(!blocked())view();});
 const privacy=doc.getElementById('aggregate-statistics-choice');if(privacy){privacy.hidden=false;privacy.append(button,state);update();}
 win.addEventListener('storage',e=>{if(e.key===OPT_OUT||e.key===null){optedOut=e.newValue==='yes';update();}});
 const routeFor=input=>{const content=runtime.analytics?.catalogue?.content?.[input?.contentId];if(!content?.languages?.includes(input.language))return null;
 if(/^kbl:\d+$/.test(input.contentId)){const p=c.contentRoutes?.[input.contentId];return Object.hasOwn(publicPages,p)?p:null;}return path;};
 const track=(name,input)=>{const route=routeFor(input);if(!route)return false;
 if(name==='content_view'||name==='language_change')return publish('language_'+input.language,route);
 if(name==='share_complete'||name==='copy_link_complete')return publish(name==='share_complete'?'share':'copy',route);
 if(name==='listen_start')return publish('audio_start',route);
 return false;};
 const reading=observeReading(doc,track,win.MutationObserver);
 let foreground=0,last=win.performance.now(),measurementStart=last,visible=doc.visibilityState==='visible';
 const tick=()=>{const now=win.performance.now();if(visible)foreground+=now-last;last=now;visible=doc.visibilityState==='visible';if(blocked()){foreground=0;measurementStart=now;return;}if(!visible)return;
 view();reading.refresh();const seconds=foregroundTime(win.performance,foreground,measurementStart)/1000;
 for(const n of [30,60,120])if(seconds>=n)publish('foreground_'+n);
 // Milestones refer to the displayed poem, not the footer or an inferred completed read.
 const verse=doc.getElementById('experience-verse');if(verse&&seconds>=10){const rect=verse.getBoundingClientRect();if(rect.height>0&&rect.bottom>0){const reached=(win.innerHeight-rect.top)/rect.height;for(const n of [50,90])if(reached>=n/100)publish('reading_'+n);}}
 };
 const timer=win.setInterval(tick,5000);doc.addEventListener('visibilitychange',tick);win.addEventListener('pagehide',event=>{if(!event.persisted){win.clearInterval(timer);reading.stop();}});
 view();reading.refresh();return {track};
}
