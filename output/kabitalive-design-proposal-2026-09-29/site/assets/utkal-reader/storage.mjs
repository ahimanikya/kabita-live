/** Inject site storage; never access browser globals or remove legacy keys. */
export function createReaderStore({siteId,storage,onStatus=()=>{}}) {
  if (typeof siteId !== 'string' || !/^[a-z0-9-]+$/.test(siteId)) throw new TypeError('Site namespace required');
  const memory = new Map(), prefix = `utkal-reader:v1:${siteId}:`;
  const key = name => {if(typeof name !== 'string' || !name)throw new TypeError('Storage name required');return prefix+name;};
  return {
    get(name,fallback,validate=()=>true) {
      const k = key(name); let raw;
      try {raw=memory.has(k) ? memory.get(k) : storage?.getItem(k);} catch {raw=memory.get(k);onStatus('session');}
      if(raw===undefined || raw===null)return fallback;
      try {const value=JSON.parse(raw);if(!validate(value)){onStatus('invalid');return fallback;}return value;} catch {onStatus('invalid');return fallback;}
    },
    set(name,value) {
      const k=key(name),raw=JSON.stringify(value);
      if(raw===undefined)throw new TypeError('Serializable value required');
      memory.set(k,raw);
      try {if(!storage)throw new Error('Session only');storage.setItem(k,raw);onStatus('saved');return true;} catch {onStatus('session');return false;}
    }
  };
}
