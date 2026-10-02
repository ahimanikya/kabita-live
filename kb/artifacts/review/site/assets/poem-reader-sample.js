(()=>{
 const raw=Number(new URLSearchParams(location.search).get('variant')),variant=[0,1,2].includes(raw)?raw:1;
 document.body.dataset.readerVariant=variant;
 if(variant){
  const opening=document.querySelector('.poem-opening'),heading=opening.querySelector('.poem-heading'),reader=document.querySelector('.reader'),layout=document.querySelector('.reading-layout'),art=opening.querySelector('.poem-art');
  const issue=document.querySelector('.breadcrumb a:last-child').cloneNode(true),language=heading.querySelector('.eyebrow').textContent.split(' · ')[0];
  const meta=document.createElement('p');meta.className='reader-meta';meta.append(issue,document.createTextNode(' · '+language));
  heading.querySelector('.eyebrow').replaceWith(meta);document.querySelector('.breadcrumb').remove();
  document.querySelector('.reading-aside')?.remove();
  const summary=reader.querySelector('.author-summary'),poet=summary?.querySelector('a')?.cloneNode(true),next=reader.querySelector('.next-prev a:last-child')?.cloneNode(true);
  const correction=document.createElement('a');correction.className='reader-correction';correction.href='contact.html?reason=correction&poem='+JSON.parse(document.querySelector('#poem-data').textContent)[0].id;correction.textContent='Suggest a correction';
  reader.querySelectorAll('.author-summary,.next-prev').forEach(e=>e.remove());
  reader.querySelectorAll(':scope>p').forEach(e=>{if(e.querySelector('a[href="contact.html"]'))e.remove();});
  const after=document.createElement('nav');after.className='poem-after';after.setAttribute('aria-label','Continue reading');
  if(poet){poet.textContent='More by this poet';after.append(poet);}
  if(next){const label=next.querySelector('small');if(label)label.textContent='Next poem';after.append(next);}
  reader.append(after,correction);
  if(variant===2){
   const flow=document.createElement('div');flow.className='poem-first-layout';opening.before(flow);flow.append(opening,layout,art);
  }
 }
 document.querySelectorAll('a[href]').forEach(a=>{if(!a.getAttribute('href').startsWith('#')){a.target='_blank';a.rel='noopener noreferrer';}});
 document.title=['Current reader','A · Quiet illustrated opening','B · The poem first'][variant]+' · Kabita Live mockup';
})();
