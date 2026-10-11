import {analyticsEvent,ANALYTICS_CONTRACT_VERSION} from './vendor/utkal-analytics/contract.mjs';
export {ANALYTICS_CONTRACT_VERSION};
// The catalogue is supplied by the public exporter, never by a form or browser title.
export function createKabitaEventValidator(catalogue){
 return (name,input)=>analyticsEvent(name,input,catalogue);
}
