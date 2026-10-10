// App Check protects Firebase calls; static poetry stays readable without scripts.
const registryKey=Symbol.for('kabita.appCheck.instances');
const instances=globalThis[registryKey]??=new WeakMap();
export async function ensureAppCheck(app,config,load=()=>import('firebase/app-check'),cache=instances){
 const settings=config?.appCheck;
 if(!settings?.enabled)return;
 if(settings.provider!=='recaptcha-enterprise'||!/^6[\w-]{20,}$/.test(settings.siteKey??''))throw Error('Invalid App Check configuration');
 let pending=cache.get(app);
 if(!pending){
  pending=(async()=>{const sdk=await load();const check=sdk.initializeAppCheck(app,{provider:new sdk.ReCaptchaEnterpriseProvider(settings.siteKey),isTokenAutoRefreshEnabled:true});await sdk.getToken(check,false);return check;})();
  cache.set(app,pending);
 }
 try{await pending;}catch(error){if(cache.get(app)===pending)cache.delete(app);throw error;}
}
