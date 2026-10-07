const configFields=['projectId','apiKey','authDomain','appId'];
function validConfig(config,expectedProjectId){return config?.enabled===true&&typeof expectedProjectId==='string'&&!!expectedProjectId&&config.projectId===expectedProjectId&&configFields.every(k=>typeof config[k]==='string'&&!!config[k]&&!/\s/.test(config[k]));}
/** Check before importing provider code or enabling controls. Missing setup remains unavailable. */
export function siteRuntimeAllowed(config,expectedProjectId,location){return validConfig(config,expectedProjectId)&&location?.protocol==='https:'&&Array.isArray(config.allowedHosts)&&config.allowedHosts.includes(location.hostname);}
/** Preserve an existing named app/UID; never silently reuse another project's configuration. */
export function selectSiteApp(appSdk,config,appName,expectedProjectId){
 if(!validConfig(config,expectedProjectId)||typeof appName!=='string'||!appName||appName==='[DEFAULT]'||typeof appSdk?.getApps!=='function'||typeof appSdk?.initializeApp!=='function')throw new TypeError('Explicit site Firebase configuration required');
 const existing=appSdk.getApps().find(a=>a.name===appName);
 if(existing){if(configFields.some(k=>existing.options[k]!==config[k]))throw Error('Named Firebase app configuration mismatch');return existing;}
 return appSdk.initializeApp(Object.fromEntries(configFields.map(k=>[k,config[k]])),appName);
}
/** Sign-in is called for an operational reader action, independently of optional Analytics. */
export async function restoreSiteUser(authSdk,instance){
 const auth=authSdk.getAuth(instance);if(auth.app!==instance)throw Error('Site authentication instance mismatch');
 await auth.authStateReady();const user=auth.currentUser??(await authSdk.signInAnonymously(auth)).user;if(!user?.uid)throw Error('Site reader identity unavailable');return user;
}
