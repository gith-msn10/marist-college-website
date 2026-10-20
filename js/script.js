(()=>{"use strict";
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const y=$("#yr");if(y)y.textContent=new Date().getFullYear();
// Mobile menu
const b=$(".burger"),n=$("#nav");
if(b&&n){const set=o=>{n.classList.toggle("open",o);b.setAttribute("aria-expanded",o);b.setAttribute("aria-label",o?"Close menu":"Open menu")};
b.addEventListener("click",()=>set(!n.classList.contains("open")));
$$("a",n).forEach(a=>a.addEventListener("click",()=>set(false)));
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&n.classList.contains("open")){set(false);b.focus()}})}
// Back to top
const t=$("#top");if(t){addEventListener("scroll",()=>{t.hidden=scrollY<500},{passive:true});t.addEventListener("click",()=>scrollTo({top:0}))}
// Gallery filter + lightbox
const items=$$(".gal li");let cur=0,vis=[];
$$(".chip").forEach(c=>c.addEventListener("click",()=>{$$(".chip").forEach(x=>x.classList.toggle("on",x===c));items.forEach(li=>li.hidden=c.dataset.f!=="all"&&li.dataset.cat!==c.dataset.f)}));
const lb=$("#lb");
if(lb){const img=$("#lbi"),cap=$("#lbc");
const show=i=>{vis=items.filter(l=>!l.hidden);cur=(i+vis.length)%vis.length;const g=$(".gi",vis[cur]);img.src=g.dataset.full;img.alt=$("img",g).alt;cap.textContent=g.dataset.cap};
items.forEach(li=>$(".gi",li).addEventListener("click",()=>{vis=items.filter(l=>!l.hidden);show(vis.indexOf(li));lb.showModal()}));
lb.addEventListener("click",e=>{const a=e.target.dataset&&e.target.dataset.a;if(a==="close"||e.target===lb)lb.close();if(a==="prev")show(cur-1);if(a==="next")show(cur+1)});
lb.addEventListener("keydown",e=>{if(e.key==="ArrowLeft")show(cur-1);if(e.key==="ArrowRight")show(cur+1)})}
// News search
const ns=$("#ns");if(ns)ns.addEventListener("input",()=>{const q=ns.value.toLowerCase();let c=0;$$("#nl .card").forEach(a=>{const h=!a.textContent.toLowerCase().includes(q);a.hidden=h;if(!h)c++});$("#nn").hidden=c>0});
// Enquiry form: validates, then opens email or WhatsApp. Never claims it was sent.
const f=$("#enq");
if(f){let via="mail";$$("button[type=submit]",f).forEach(x=>x.addEventListener("click",()=>via=x.dataset.via));
const msgs={pn:"Enter your name.",ph:"Enter a valid phone number.",em:"Enter a valid email address.",cl:"Choose a class.",ms:"Write your enquiry.",cn:"Tick this box to continue."};
const chk=el=>{const e=el.parentElement.querySelector(".err");if(!e)return true;const ok=el.checkValidity();el.setAttribute("aria-invalid",!ok);e.textContent=ok?"":msgs[el.name];return ok};
$$("input,select,textarea",f).forEach(el=>el.addEventListener("blur",()=>chk(el)));
f.addEventListener("submit",e=>{e.preventDefault();const s=$("#fs");const bad=$$("input,select,textarea",f).filter(el=>!chk(el));
if(bad.length){bad[0].focus();s.textContent="Please correct the highlighted fields.";return}
const v=k=>f.elements[k].value.trim();
const body=`Parent/guardian: ${v("pn")}\nPhone: ${v("ph")}\nEmail: ${v("em")}\nStudent: ${v("sn")}\nClass: ${v("cl")}\n\n${v("ms")}`;
const u=via==="wa"?`https://wa.me/${f.dataset.wa}?text=${encodeURIComponent(body)}`:`mailto:${f.dataset.mail}?subject=${encodeURIComponent("Admission enquiry")}&body=${encodeURIComponent(body)}`;
s.textContent=via==="wa"?"Opening WhatsApp. Press send there to deliver your message.":"Opening your email app. Press send there to deliver your message.";location.href=u})}
})();