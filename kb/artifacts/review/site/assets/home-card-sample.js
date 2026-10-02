(()=>{
 const data=JSON.parse(document.getElementById('home-review-data').textContent),params=new URLSearchParams(location.search),v=Number(params.get('variant'));
 const variant=[0,1,2].includes(v)?v:0;document.body.dataset.cardVariant=variant;
 const cards=[...document.querySelectorAll('.language-card')],section=cards[0].closest('section');section.classList.add('card-study');
 cards.forEach((card,i)=>{
  const h=card.querySelector('h3'),author=card.querySelector('a.byline'),header=document.createElement('div'),copy=document.createElement('div'),portrait=document.createElement('a'),img=document.createElement('img');
  header.className='card-identity';copy.className='card-identity-copy';portrait.className='card-portrait';portrait.href=author.getAttribute('href');portrait.setAttribute('aria-label','Meet '+author.textContent);
  img.src=data.portraits[i];img.alt='';img.width=96;img.height=128;portrait.append(img);h.before(header);copy.append(h,author);header.append(portrait,copy);
  const excerpt=card.querySelector('.excerpt');excerpt.textContent=data.excerpts[[809,810,814][i]].a;
 });
 const duplicate=section.nextElementSibling;if(duplicate?.querySelector('.person'))duplicate.remove();
 const more=document.createElement('a');more.className='text-link';more.href='poets.html';more.textContent='Meet the poets';section.append(more);
 document.querySelectorAll('a[href]').forEach(a=>{if(!a.getAttribute('href').startsWith('#')){a.target='_blank';a.rel='noopener noreferrer';}});
 const focus=()=>section.scrollIntoView({block:'start',behavior:'instant'});let frame;
 addEventListener('load',()=>document.fonts.ready.then(()=>requestAnimationFrame(focus)));
 addEventListener('resize',()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(focus);});
 document.title='Poem cards · '+['A','B','C'][variant]+' · Kabita Live';
})();
