// Emits public registration input only; performs no Firebase/admin writes.
import {articleResponseManifest} from '../src/article-responses.mjs';
export function registrationRecords(){return articleResponseManifest().entries.map(({contentKey,contentId,kind,languages,public:isPublic})=>({path:`responseContent/${contentKey}`,data:{contentId,kind,languages,public:isPublic}}));}
if(process.argv[1]&&import.meta.url===new URL(`file://${process.argv[1]}`).href)process.stdout.write(JSON.stringify(registrationRecords(),null,2)+'\n');
