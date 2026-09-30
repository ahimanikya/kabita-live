(()=>{
const params=new URLSearchParams(location.search),id=params.get('element')||'spacing',variant=params.get('variant')==='1'?1:0;
const allowed=['identity','colour','type','paper','spacing','openings','navigation','reader','actions','cards','forms','feedback','search','sharing','imagery','ornament','motion','credits'];
if(!allowed.includes(id)){document.querySelector('main').textContent='This design sample is unavailable.';return;}
const sample=window.KabitaSamples.render(id,variant);document.title='Kabita Live · '+id+' · direction '+(variant+1);document.body.className='group-'+id+' variant-'+variant;
const style=document.createElement('style');style.textContent=sample.css;document.head.append(style);document.querySelector('main').innerHTML=sample.html;
const script=document.createElement('script');script.textContent=sample.script;document.body.append(script);
})();
