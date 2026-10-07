/** Recompute a stale concurrent count in a fresh transaction; permanent errors still reject. */
export async function retryLikeTransaction(operation,{attempts=3,wait=ms=>new Promise(resolve=>setTimeout(resolve,ms))}={}){
 if(typeof operation!=='function'||!Number.isInteger(attempts)||attempts<1||attempts>3||typeof wait!=='function')throw new TypeError('Bounded like transaction required');
 for(let attempt=0;attempt<attempts;attempt++){
  try{return await operation();}catch(error){if(attempt===attempts-1||!['permission-denied','aborted'].includes(error?.code))throw error;await wait(40*(attempt+1));}
 }
}
