// Aggregate-only storage: a server day plus fixed public page and metric counters.
import {readFileSync} from 'node:fs';
const titles=JSON.parse(readFileSync(new URL('./audience-pages.json',import.meta.url)));
const pages=new Set(Object.keys(titles));
export const METRICS=Object.freeze(['view','screen_small','screen_medium','screen_large','referral_direct_or_unknown','referral_internal','referral_search','referral_social','referral_other','language_or','language_hi','language_en','share','copy','audio_start','foreground_30','foreground_60','foreground_120','reading_50','reading_90']);
export function validateCount(input){if(!input||Array.isArray(input)||Object.keys(input).sort().join()!=='metric,path'||!pages.has(input.path)||!METRICS.includes(input.metric))throw Error('Invalid count');return {path:input.path,metric:input.metric};}
export const dayOf=date=>new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Kolkata',year:'numeric',month:'2-digit',day:'2-digit'}).format(date);
export async function recordCount(db,input,now=new Date()){
 const {path,metric}=validateCount(input),day=dayOf(now),ref=db.doc('audienceDays/'+day),settings=db.doc('audienceSettings/current');
 return db.runTransaction(async tx=>{const [config,snap]=await tx.getAll(settings,ref);if(config.data()?.enabled!==true||config.data()?.policyReviewed!==true)throw Error('Unavailable');
 const data=snap.data()||{day,total:0,pages:{}};if(data.total>=50000)throw Error('Daily capacity reached');
 const counts=data.pages[path]||{};counts[metric]=(counts[metric]||0)+1;data.pages[path]=counts;data.total++;
 tx.set(ref,data);return true;});
}
export function combineDays(days){const totals=new Map();for(const day of days)for(const [path,counts]of Object.entries(day.pages||{})){
 if(!pages.has(path))continue;const row=totals.get(path)||{label:path.slice(1)||'index.html',title:titles[path],visits:0,shares:0,metrics:{}};
 for(const metric of METRICS){const n=counts[metric]||0;if(!Number.isSafeInteger(n)||n<0)throw Error('Invalid statistics');row.metrics[metric]=(row.metrics[metric]||0)+n;}
 row.visits=row.metrics.view;row.shares=row.metrics.share+row.metrics.copy;totals.set(path,row);
 }return [...totals.values()].sort((a,b)=>b.visits-a.visits);}
export async function audienceReport(db,{range='28',now=new Date()}={}){
 if(!['7','28','all'].includes(range))throw Error('Unknown report period');const config=(await db.doc('audienceSettings/current').get()).data();
 if(!config?.enabled)return null;
 const end=dayOf(now),start=range==='all'?config.startedOn:new Date(Date.parse(end+'T00:00:00Z')-(Number(range)-1)*86400000).toISOString().slice(0,10);
 if(!/^\d{4}-\d{2}-\d{2}$/.test(start||''))throw Error('Collection start not configured');
 const cache=db.doc('audienceReports/'+range),old=(await cache.get()).data();if(old&&Date.parse(old.updatedAt)>now.getTime()-900000)return old;
 const docs=await db.collection('audienceDays').where('day','>=',start).where('day','<=',end).orderBy('day').limit(4001).get();if(docs.size>4000)throw Error('Report needs archival aggregation');
 const report={available:true,source:'Kabita aggregate statistics',period:start+' to '+end,updatedAt:now.toISOString(),startedOn:config.startedOn,rows:combineDays(docs.docs.map(x=>x.data())),capacityLimited:docs.docs.some(x=>x.data().total>=50000),consentLimited:false,sharesAreActions:true};await cache.set(report);return report;
}
