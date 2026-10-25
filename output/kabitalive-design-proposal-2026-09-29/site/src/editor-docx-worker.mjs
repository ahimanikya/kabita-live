import {Unzip,UnzipInflate} from 'fflate';
export function documentXML(bytes){
 if(bytes.byteLength>5_000_000)throw Error('Choose a Word file smaller than 5 MB.');
 let chunks=[],size=0,found=false,finished=false,count=0;
 const zip=new Unzip(file=>{if(++count>2000)throw Error('This Word file has too many embedded parts.');if(file.name!=='word/document.xml')return;if(found)throw Error('Duplicate document content.');found=true;if(file.originalSize>2_000_000)throw Error('This Word document is too large.');file.ondata=(err,data,final)=>{if(err)throw err;size+=data.length;if(size>2_000_000){file.terminate();throw Error('This Word document is too large.');}chunks.push(data);finished=final;};file.start();});
 zip.register(UnzipInflate);for(let i=0;i<bytes.length;i+=4096)zip.push(bytes.subarray(i,i+4096),i+4096>=bytes.length);
 if(!found||!finished)throw Error('This is not a complete DOCX document.');const out=new Uint8Array(size);let offset=0;for(const chunk of chunks){out.set(chunk,offset);offset+=chunk.length;}return new TextDecoder('utf-8',{fatal:true}).decode(out);
}
if(typeof self!=='undefined')self.onmessage=e=>{try{self.postMessage({xml:documentXML(new Uint8Array(e.data))});}catch(err){self.postMessage({error:err.message||'Unable to read this Word file.'});}};
