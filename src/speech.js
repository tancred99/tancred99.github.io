// Tap-to-hear for Russian words + stress marks. Exposes window.RuSpeech.
(function(){
"use strict";
var STRESS={};try{STRESS=JSON.parse(document.getElementById("stressData").textContent)||{}}catch(e){}
var ACUTE="\u0301",VOW="аеёиоуыэюяАЕЁИОУЫЭЮЯ";
var WORD_RE=/[А-Яа-яЁё\u0301]+(?:-[А-Яа-яЁё\u0301]+)*/g,CYR=/[А-Яа-яЁё]/;
var SKIP="button,input,textarea,select,option,script,style,summary,a,label,code,.opt,.chip,.ru-w,[data-notts],#authOv";
var HELP_KEY="ruDrills.ttsHelp.v1";
var R={enabled:true};

// ---------- stress ----------
function strip(s){return String(s==null?"":s).replace(/\u0301/g,"")}
function accentWord(w){
  if(w.indexOf(ACUTE)>=0||/[ёЁ]/.test(w))return w;
  var k=STRESS[w.toLowerCase()];
  return (typeof k==="number"&&k<w.length&&VOW.indexOf(w[k])>=0)?w.slice(0,k+1)+ACUTE+w.slice(k+1):w;
}
// Adds a stress mark to every word the dictionary knows for sure; leaves the rest untouched.
function accent(s){return String(s==null?"":s).replace(/[А-Яа-яЁё]+/g,accentWord)}

// ---------- voices ----------
var synth=window.speechSynthesis||null,voice=null,voicesTried=false;
function isRu(v){return /^ru([-_]|$)/i.test(v.lang||"")}
function score(v){var n=v.name||"",s=0;
  if(/natural/i.test(n))s+=10;if(/online/i.test(n))s+=4;if(/google/i.test(n))s+=5;
  if(/svetlana|dmitry|dariya/i.test(n))s+=3;if(/^ru[-_]ru$/i.test(v.lang||""))s+=1;return s}
function pickVoice(){
  if(!synth||!synth.getVoices)return null;
  var vs=[];try{vs=synth.getVoices()||[]}catch(e){}
  if(vs.length)voicesTried=true;
  var ru=vs.filter(isRu).sort(function(a,b){return score(b)-score(a)});
  voice=ru[0]||null;return voice;
}
if(synth){pickVoice();try{synth.addEventListener?synth.addEventListener("voiceschanged",pickVoice):(synth.onvoiceschanged=pickVoice)}catch(e){}}

// ---------- help toast (once per device) ----------
function toast(msg){
  var t=document.createElement("div");t.className="sptoast";t.setAttribute("role","status");t.setAttribute("data-notts","1");
  t.innerHTML='<div>'+msg+'</div><button class="tx" aria-label="Close">✕</button>';
  document.body.appendChild(t);
  var close=function(){t.remove()};t.querySelector(".tx").onclick=close;setTimeout(close,15000);
}
function helpOnce(noSynth){
  try{if(localStorage.getItem(HELP_KEY))return;localStorage.setItem(HELP_KEY,"1")}catch(e){}
  toast(noSynth?"<b>This browser can’t speak text.</b> Try Chrome or Edge to hear Russian words.":
    "<b>No Russian voice found on this device.</b> If you don’t hear anything, add one:<br>"+
    "• Android: Settings → Speech / Text-to-speech → Speech Services by Google → Install voice data → Russian.<br>"+
    "• Windows: Settings → Time &amp; language → Speech → Add voices → Russian.<br>"+
    "• iPhone/Mac: Settings → Accessibility → Spoken Content → Voices → Russian.");
}
function checkVoice(){
  if(voice)return;
  if(voicesTried){helpOnce(false);return}
  setTimeout(function(){pickVoice();if(!voice)helpOnce(false)},1500); // voices can load late
}

// ---------- speaking ----------
function speak(text,slow){
  text=strip(text).replace(/\s+/g," ").trim();if(!text)return false;
  if(!synth||typeof window.SpeechSynthesisUtterance!=="function"){helpOnce(true);return false}
  if(!voice)pickVoice();
  var u=new SpeechSynthesisUtterance(text);u.lang="ru-RU";if(voice)u.voice=voice;u.rate=slow?0.7:1;u.pitch=1;
  try{if(synth.speaking||synth.pending){synth.cancel();setTimeout(function(){synth.speak(u)},60)}else synth.speak(u)}catch(e){}
  checkVoice();return true;
}

// ---------- wrap Cyrillic words in tappable spans ----------
function wrapText(node){
  var txt=node.nodeValue;if(!txt||!CYR.test(txt))return;
  var p=node.parentNode;if(!p||p.nodeType!==1||(p.closest&&p.closest(SKIP)))return;
  WORD_RE.lastIndex=0;var m,last=0,frag=document.createDocumentFragment(),any=false;
  while((m=WORD_RE.exec(txt))){
    if(!CYR.test(m[0]))continue;any=true;
    if(m.index>last)frag.appendChild(document.createTextNode(txt.slice(last,m.index)));
    var s=document.createElement("span");s.className="ru-w";s.textContent=m[0];frag.appendChild(s);last=m.index+m[0].length;
  }
  if(!any)return;
  if(last<txt.length)frag.appendChild(document.createTextNode(txt.slice(last)));
  p.replaceChild(frag,node);
}
function wrap(root){
  if(!root)return;
  if(root.nodeType===3){wrapText(root);return}
  if(root.nodeType!==1||(root.closest&&root.closest(SKIP)))return;
  var w=document.createTreeWalker(root,4,null,false),list=[],n;
  while((n=w.nextNode()))if(CYR.test(n.nodeValue))list.push(n);
  list.forEach(wrapText);
}
function observe(){
  wrap(document.body);
  if(!window.MutationObserver)return;
  new MutationObserver(function(muts){muts.forEach(function(m){
    if(m.type==="characterData"){wrapText(m.target);return}
    for(var i=0;i<m.addedNodes.length;i++)wrap(m.addedNodes[i]);
  })}).observe(document.body,{childList:true,subtree:true,characterData:true});
}

// ---------- events: tap = normal, long-press / Shift-click / right-click = slow ----------
function target(el){
  var t=el&&el.closest?el.closest(".ru-w,[data-say]"):null;if(!t)return null;
  if(t.classList.contains("ru-w")&&!R.enabled)return null;
  return t;
}
function textOf(t){return t.hasAttribute("data-say")?t.getAttribute("data-say"):t.textContent}
function flash(t){if(!t.classList.contains("ru-w"))return;t.classList.add("ru-say");setTimeout(function(){t.classList.remove("ru-say")},700)}
var lp=null,lastSlow={el:null,at:0},suppressClick=0;
function say(t,slow){
  if(slow){var now=Date.now();if(lastSlow.el===t&&now-lastSlow.at<1200)return;lastSlow={el:t,at:now}}
  flash(t);speak(textOf(t),slow);
}
document.addEventListener("click",function(ev){
  var t=target(ev.target);if(!t)return;
  if(Date.now()<suppressClick){ev.preventDefault();return}
  say(t,!!ev.shiftKey);
});
document.addEventListener("mousedown",function(ev){if(ev.shiftKey&&target(ev.target))ev.preventDefault()});
document.addEventListener("contextmenu",function(ev){
  var t=target(ev.target);if(!t)return;
  ev.preventDefault();say(t,true);
});
document.addEventListener("touchstart",function(ev){
  if(lp){clearTimeout(lp.timer);lp=null}
  var t=target(ev.target);if(!t||ev.touches.length!==1)return;
  var p=ev.touches[0];
  lp={t:t,x:p.clientX,y:p.clientY,fired:false};
  lp.timer=setTimeout(function(){if(!lp)return;lp.fired=true;say(t,true)},500);
},{passive:true});
document.addEventListener("touchmove",function(ev){
  if(!lp)return;var p=ev.touches[0];
  if(Math.abs(p.clientX-lp.x)>10||Math.abs(p.clientY-lp.y)>10){clearTimeout(lp.timer);lp=null}
},{passive:true});
function endTouch(ev){
  if(!lp)return;clearTimeout(lp.timer);
  if(lp.fired){suppressClick=Date.now()+700;if(ev.cancelable)ev.preventDefault()}
  lp=null;
}
document.addEventListener("touchend",endTouch,{passive:false});
document.addEventListener("touchcancel",endTouch,{passive:true});

R.accent=accent;R.strip=strip;R.speak=speak;R.wrap=wrap;R.voice=function(){return voice};
R.setEnabled=function(on){R.enabled=!!on;document.body.classList.toggle("tts-off",!R.enabled)};
window.RuSpeech=R;
if(document.body)observe();else document.addEventListener("DOMContentLoaded",observe);
})();
