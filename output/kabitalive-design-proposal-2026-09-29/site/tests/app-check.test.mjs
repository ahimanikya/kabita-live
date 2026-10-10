import {test} from 'node:test';
import assert from 'node:assert/strict';
import {ensureAppCheck} from '../src/app-check.mjs';
const config={appCheck:{enabled:true,provider:'recaptcha-enterprise',siteKey:'6'+'a'.repeat(39)}};
test('disabled protection does not contact the provider',async()=>{await ensureAppCheck({}, {},()=>{throw Error('must not load')});});
test('invalid enabled configuration fails before provider calls',async()=>{await assert.rejects(ensureAppCheck({}, {appCheck:{enabled:true,provider:'other'}}),/Invalid/);});
test('concurrent consumers share attestation and require a token before resolving',async()=>{let init=0,tokens=0;const cache=new WeakMap(),app={};const sdk={ReCaptchaEnterpriseProvider:class{},initializeAppCheck(){init++;return{};},async getToken(){tokens++;return{token:'test'};}};await Promise.all([ensureAppCheck(app,config,async()=>sdk,cache),ensureAppCheck(app,config,async()=>sdk,cache)]);assert.equal(init,1);assert.equal(tokens,1);});
test('failed attestation stays failed and a later explicit call may retry',async()=>{let tries=0;const cache=new WeakMap(),app={};const sdk={ReCaptchaEnterpriseProvider:class{},initializeAppCheck(){return{};},async getToken(){if(++tries===1)throw Error('rejected');return{token:'test'};}};await assert.rejects(ensureAppCheck(app,config,async()=>sdk,cache),/rejected/);await ensureAppCheck(app,config,async()=>sdk,cache);assert.equal(tries,2);});
