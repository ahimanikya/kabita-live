// Review-only enhancement; live page behaviour remains untouched.
(()=>{
 const toc=document.querySelector('.edition-glance'),mobile=matchMedia('(max-width:760px)');
 function placeContents(){
  const parent=mobile.matches?document.querySelector('#page-bookmarks'):document.querySelector('.poem-art');
  if(!parent||!toc)return;
  const related=document.querySelector('#poem-secondary-links'),focused=document.activeElement;
  parent.append(toc);
  if(related)toc.append(related);
  if(toc.contains(focused))focused.focus({preventScroll:true});
 }
 placeContents();requestAnimationFrame(placeContents);
 mobile.addEventListener('change',()=>requestAnimationFrame(placeContents));
 const dialog=document.querySelector('#focus-reader'),pages=document.querySelector('#focus-pages');
 // A trackpad burst, including momentum, produces at most one turn.
 let last=0,total=0,turned=false;
 pages.addEventListener('wheel',event=>{
  if(!dialog.open||!document.querySelector('#focus-settings').hidden||event.ctrlKey||event.metaKey||!getSelection().isCollapsed)return;
  const now=performance.now();if(now-last>220){total=0;turned=false}last=now;
  if(Math.abs(event.deltaX)<Math.abs(event.deltaY)*1.35||Math.abs(event.deltaX)<1)return;
  event.preventDefault();if(turned)return;
  const delta=event.deltaX*(event.deltaMode===1?16:event.deltaMode===2?pages.clientWidth:1);
  if(total&&Math.sign(total)!==Math.sign(delta))total=0;
  total+=delta;if(Math.abs(total)<65)return;
  turned=true;document.querySelector(total>0?'#focus-next':'#focus-prev').click();
 },{passive:false});
 dialog.addEventListener('close',()=>{last=0;total=0;turned=false});
})();
