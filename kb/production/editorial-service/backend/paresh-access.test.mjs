import {test} from 'node:test';
import assert from 'node:assert/strict';
import {authorize} from './core.mjs';
const correct='pareshkpatnaik@gmail.com', legacy='areshkpatnaik@gmail.com';
const identity=email=>({email,email_verified:true,firebase:{sign_in_provider:'google.com'}});
test('Paresh corrected identity needs active per-desk access; typo stays denied even with a grant',async()=>{
 let active=true; const db={doc:path=>path,getAll:async(...paths)=>paths.map(path=>({data:()=>({enabled:path==='editorWorkspace/config'||active})}))};
 for(const stream of ['monthly','anthology']){
  assert.equal(await authorize(db,identity(correct),stream),correct);
  await assert.rejects(authorize(db,identity(legacy),stream),/Editor access required/);
  active=false;await assert.rejects(authorize(db,identity(correct),stream),/disabled/);active=true;
 }
 await assert.rejects(authorize(db,{...identity(correct),email_verified:false},'monthly'),/Google sign-in/);
});
