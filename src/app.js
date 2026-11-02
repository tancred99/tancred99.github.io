(function(){
"use strict";
var E=window.RuEngine;
var CATS=[["all","All"],["basics","Basics"],["cases","Cases"],["conjugation","Verbs"],["aspect","Aspect"],["motion","Motion"]];
var LEVELS=[["A1-A2","A1–A2"],["B1-C1","B1–C1"]];
var MODES=[["choice","Choice"],["type","Type"]];
var VDRILLS=[["mixed","Mixed"],["cases","Cases"],["plurals","Plurals"],["numbers","Numbers"],["cards","Flashcards"]];
var KIND_LABEL={thing:"thing",food:"food/drink",place:"place",person:"person",event:"service/event",transport:"transport",money:"money",unit:"measure"};
var G_LABEL={m:"masc.",f:"fem.",n:"neut.",pl:"plural only"};
var FORM_LABEL={gen:"Genitive (нет …)",dat:"Dative (к …)",acc:"Accusative (вижу …)",ins:"Instrumental (с …)",prep:"Prepositional (о …)",npl:"Nominative plural",gpl:"Genitive plural (много …)"};
var LS="ruDrills.v1",LSW="ruDrills.words.v1",LSL="ruDrills.lessons.v1";
var DATA=[],STARTER=[],WORDS=[],COURSE={course:[],lessons:{}};
var lprog=load(LSL);if(!lprog||typeof lprog.lessons!=="object"||!lprog.lessons)lprog={version:1,lessons:{}};
var store=load(LS)||{};
var st={tab:store.tab||"lessons",lview:"map",lid:null,first:0,lsaved:false,level:store.level||"A1-A2",showTr:false,cat:store.cat||"all",sub:"all",mode:store.mode||"choice",
  vtheme:store.vtheme||"all",vdrill:store.vdrill||"mixed",wtheme:"all",queue:[],cur:null,answered:false,right:0,total:0,streak:0,picked:null,editing:null,importing:null};

function load(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}}
function save(){try{store.cat=st.cat;store.mode=st.mode;store.level=st.level;store.tab=st.tab;store.vtheme=st.vtheme;store.vdrill=st.vdrill;localStorage.setItem(LS,JSON.stringify(store))}catch(e){}}
function saveLessons(){try{localStorage.setItem(LSL,JSON.stringify(lprog))}catch(e){}}
function saveWords(){try{localStorage.setItem(LSW,JSON.stringify({version:1,words:WORDS}))}catch(e){alert("Couldn't save words in this browser (storage full or blocked).")}}
function $(id){return document.getElementById(id)}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function norm(s){return String(s).toLowerCase().replace(/ё/g,"е").replace(/[.,!?;:«»"]/g,"").replace(/\s+/g," ").trim()}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function clone(o){return JSON.parse(JSON.stringify(o))}
var CAT_LABEL={basics:"Basics",cases:"Cases",conjugation:"Verbs",aspect:"Aspect",motion:"Motion",vocab:"Vocabulary",lesson:"Lesson"};
function lvl(){return DATA.filter(function(e){return e.level===st.level})}
function themes(){var t=[];WORDS.forEach(function(w){if(t.indexOf(w.theme)<0)t.push(w.theme)});return t}
function themeWords(th){return WORDS.filter(function(w){return th==="all"||w.theme===th})}

// ---------- drill pool ----------
function lessonItems(L){
  var parts=[];L.exercises.forEach(function(e){if(parts.indexOf(e.part)<0)parts.push(e.part)});
  var out=[];parts.forEach(function(p){
    out=out.concat(shuffle(L.exercises.map(function(e,i){var x=clone(e);x.id=L.id+":"+i;x.cat="lesson";x.catLabel="Lesson "+L.n;return x}).filter(function(e){return e.part===p})))});
  return out;
}
function pool(){
  if(st.tab==="lessons"){var L=COURSE.lessons[st.lid];return L?lessonItems(L):[]}
  if(st.tab==="vocab"){
    var ex=E.buildSession(themeWords(st.vtheme),st.vdrill,0);
    if(st.sub!=="all")ex=ex.filter(function(e){return e.sub===st.sub});
    return ex.slice(0,25);
  }
  return lvl().filter(function(e){return (st.cat==="all"||e.cat===st.cat)&&(st.sub==="all"||e.sub===st.sub)});
}
function subsFor(){
  if(st.tab==="vocab"){var s=[];E.buildSession(themeWords(st.vtheme),st.vdrill,0).forEach(function(e){if(s.indexOf(e.sub)<0)s.push(e.sub)});return s.sort()}
  var subs=[];lvl().forEach(function(e){if((st.cat==="all"||e.cat===st.cat)&&subs.indexOf(e.sub)<0)subs.push(e.sub)});return subs;
}

function renderControls(){
  Array.prototype.forEach.call(document.querySelectorAll(".tab"),function(b){b.setAttribute("aria-selected",String(b.dataset.tab===st.tab))});
  var lex=st.tab==="lessons"&&st.lview==="ex";
  $("drillArea").classList.toggle("hidden",st.tab==="words"||(st.tab==="lessons"&&!lex));
  $("wordsArea").classList.toggle("hidden",st.tab!=="words");
  $("lessonsArea").classList.toggle("hidden",st.tab!=="lessons"||lex);
  $("lessCtl").classList.toggle("hidden",!lex);
  $("gramCtl").classList.toggle("hidden",st.tab!=="grammar");
  $("vocCtl").classList.toggle("hidden",st.tab!=="vocab");
  $("sub").classList.toggle("hidden",st.tab==="lessons");
  if(st.tab==="words"){renderWords();return}
  if(st.tab==="lessons"){$("modes").innerHTML=MODES.map(function(m){return '<button class="chip" data-mode="'+m[0]+'" aria-pressed="'+(st.mode===m[0])+'">'+m[1]+'</button>'}).join("");if(!lex)renderLessons();return}
  if(st.tab==="grammar"){
    var L=lvl();
    $("levels").innerHTML=LEVELS.map(function(l){return '<button class="chip" data-level="'+l[0]+'" aria-pressed="'+(st.level===l[0])+'">'+l[1]+'</button>'}).join("");
    $("cats").innerHTML=CATS.map(function(c){var n=c[0]==="all"?L.length:L.filter(function(e){return e.cat===c[0]}).length;if(!n)return "";
      return '<button class="chip" data-cat="'+c[0]+'" aria-pressed="'+(st.cat===c[0])+'">'+c[1]+' · '+n+'</button>'}).join("");
  }else{
    var th=themes();if(st.vtheme!=="all"&&th.indexOf(st.vtheme)<0)st.vtheme="all";
    $("vtheme").innerHTML='<option value="all">All my words · '+WORDS.length+'</option>'+th.map(function(x){return '<option value="'+esc(x)+'"'+(st.vtheme===x?" selected":"")+'>'+esc(x)+' · '+themeWords(x).length+'</option>'}).join("");
    $("vdrills").innerHTML=VDRILLS.map(function(d){return '<button class="chip" data-vdrill="'+d[0]+'" aria-pressed="'+(st.vdrill===d[0])+'">'+d[1]+'</button>'}).join("");
  }
  var subs=subsFor();if(subs.indexOf(st.sub)<0)st.sub="all";
  $("sub").innerHTML='<option value="all">'+(st.tab==="vocab"?"All drill types":"All subtopics")+'</option>'+subs.map(function(s){return '<option value="'+esc(s)+'"'+(st.sub===s?" selected":"")+'>'+esc(s)+'</option>'}).join("");
  $("modes").innerHTML=MODES.map(function(m){return '<button class="chip" data-mode="'+m[0]+'" aria-pressed="'+(st.mode===m[0])+'">'+m[1]+'</button>'}).join("");
}

function newSession(){
  if(st.tab==="words")return;
  if(st.tab==="lessons"&&st.lview!=="ex"){st.queue=[];st.cur=null;st.answered=false;return}
  var items=pool();
  st.queue=(st.tab==="lessons"?items:shuffle(items)).map(function(e){return {e:e,again:false}});
  st.right=0;st.total=0;st.streak=0;st.first=0;st.lsaved=false;
  next();
}
function useChoice(e){return st.mode==="choice"||e.choiceOnly}
function next(){
  st.cur=st.queue.shift()||null;st.answered=false;st.picked=null;st.showTr=false;
  if(st.cur)st.cur.opts=shuffle([st.cur.e.a].concat(st.cur.e.d));
  render();
}
function itemKey(e){return e.id!=null?String(e.id):("v:"+e.word+"|"+e.sub+"|"+e.s)}
function check(val){
  if(st.answered||!st.cur)return;
  var e=st.cur.e,ok=[e.a].concat(e.alt||[]).some(function(a){return norm(a)===norm(val)});
  st.answered=true;st.picked=val;st.ok=ok;st.total++;
  var rec=store.items=store.items||{};var k=itemKey(e);var r=rec[k]=rec[k]||{seen:0,right:0};r.seen++;
  if(ok&&!st.cur.again)st.first++;
  if(ok){st.right++;st.streak++;r.right++;if(st.streak>(store.best||0))store.best=st.streak}
  else{st.streak=0;var pos=Math.min(st.queue.length,3+Math.floor(Math.random()*4));st.queue.splice(pos,0,{e:e,again:true})}
  save();render();
}

function sentenceHTML(e,fill,cls){
  var parts=e.s.split("___");
  return esc(parts[0])+'<span class="blank '+(cls||"")+'">'+(fill?esc(fill):"&nbsp;")+'</span>'+esc(parts[1]);
}
function render(){
  $("sScore").textContent=st.right+"/"+st.total;
  $("sStreak").textContent=st.streak;
  $("sBest").textContent=store.best||0;
  $("sLeft").textContent=st.queue.length+(st.cur?1:0);
  var items=store.items||{},seen=0,right=0;Object.keys(items).forEach(function(k){seen+=items[k].seen;right+=items[k].right});
  $("lifetime").textContent=seen?("All-time on this device: "+right+" correct out of "+seen+" answers."):"";
  var c=$("card");
  if(st.tab==="lessons")renderLessonHead();
  if(!st.cur&&st.tab==="lessons"&&st.total){lessonComplete(c);return}
  if(!st.cur){
    if(!st.total){c.innerHTML='<div class="done"><h2>Nothing to drill here yet</h2><p class="muted">'+(st.tab==="vocab"?"This theme has no words that fit this drill. Nouns need a gender and forms the app is sure about, and Flashcards work with any word. Add words in My words.":"No exercises match these settings.")+'</p></div>';return}
    var pct=Math.round(100*st.right/st.total);
    c.innerHTML='<div class="done"><h2>Отлично, сессия окончена!</h2><p class="muted">'+st.right+' correct out of '+st.total+' answers ('+pct+'%). Every missed item came back until you got it right.</p><button class="btn" id="again">Start a new session</button></div>';
    $("again").onclick=newSession;return;
  }
  var e=st.cur.e,h="",choice=useChoice(e);
  h+='<div class="meta"><span class="tag">'+esc(e.catLabel||CAT_LABEL[e.cat])+'</span><span class="tag">'+esc(e.sub)+'</span>'+(st.cur.again?'<span class="tag again">again</span>':'')+'</div>';
  var fill=st.answered?e.a:"",cls=st.answered?(st.ok?"ok":"bad"):"";
  h+='<div class="sentence" lang="ru">'+sentenceHTML(e,fill,cls)+'</div>';
  if(e.base)h+='<div class="base">(<b lang="ru">'+esc(e.base)+'</b>)</div>';
  if(e.glosses&&e.glosses.length)h+='<div class="gl">'+esc(e.glosses.join(" · "))+'</div>';
  if(!st.answered&&e.translation)h+=st.showTr?'<div class="tr">'+esc(e.translation)+'</div>':'<button class="trbtn" id="trBtn">Show translation</button>';
  if(choice){
    h+='<div class="opts" lang="ru">'+st.cur.opts.map(function(o,i){
      var k="";if(st.answered){if(o===e.a)k="ok";else if(o===st.picked)k="bad"}
      return '<button class="opt '+k+'" data-i="'+i+'"'+(st.answered?" disabled":"")+'>'+esc(o)+'</button>'}).join("")+'</div>';
  }else{
    h+='<input type="text" id="typed" lang="ru" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" enterkeyhint="done" placeholder="Type the missing form" '+(st.answered?'disabled value="'+esc(st.picked)+'"':'')+'>';
    if(!st.answered)h+='<button class="btn" id="checkBtn">Check</button>';
  }
  if(st.answered){
    h+='<div class="fb '+(st.ok?"ok":"bad")+'"><strong>'+(st.ok?"Верно!":"Not quite. It will come back later.")+'</strong>'+
      (st.ok?"":'<div>Answer: <span class="ans" lang="ru">'+esc(e.a)+'</span>'+((e.alt&&e.alt.length)?' (also accepted: '+esc(e.alt.join(", "))+')':'')+'</div>')+
      (e.translation?'<div class="tr">'+esc(e.translation)+'</div>':'')+'<div>'+esc(e.ex)+'</div></div>';
    h+='<button class="btn" id="nextBtn">Next →</button>';
  }
  c.innerHTML=h;
  if(choice&&!st.answered){Array.prototype.forEach.call(c.querySelectorAll(".opt"),function(b){b.onclick=function(){check(st.cur.opts[+b.dataset.i])}})}
  if(!choice&&!st.answered){var inp=$("typed");$("checkBtn").onclick=function(){if(inp.value.trim())check(inp.value)};
    inp.onkeydown=function(ev){if(ev.key==="Enter"&&!ev.isComposing&&inp.value.trim()){ev.preventDefault();ev.stopPropagation();check(inp.value)}};setTimeout(function(){inp.focus()},30)}
  var tb=$("trBtn");if(tb)tb.onclick=function(){st.showTr=true;var v=$("typed")?$("typed").value:"";render();if(v&&$("typed"))$("typed").value=v};
  if(st.answered){var nb=$("nextBtn");nb.onclick=next;if(!choice)nb.focus()}
}

// ---------- Lessons ----------
function lp(id){return lprog.lessons[id]||null}
function renderLessons(){
  var a=$("lessonsArea");
  if(st.lview==="read"&&COURSE.lessons[st.lid]){renderLesson(a,COURSE.lessons[st.lid]);return}
  var h='<div class="lesson"><h2>Course roadmap · A1–A2</h2><p class="goal">The classroom way: read a short lesson, practice that one rule, then review. Lessons unlock as they’re written.</p><ol class="course">';
  COURSE.course.forEach(function(c){
    var L=COURSE.lessons[c.id],p=lp(c.id),ready=!!L,done=p&&p.completed;
    var cls=(c.review?"review ":"")+(ready?"":"soon ")+(done?"fin":"");
    var stx=ready?(done?'<div class="st ok">✓ Completed<br>best '+p.best+'/'+p.of+'</div>':''):'<div class="st">Coming soon</div>';
    h+='<li class="'+cls+'"><div class="num">'+(c.review?"★":c.n)+'</div><div class="lt1"><b>'+(c.review?"":"Lesson "+c.n+": ")+esc(c.title)+'</b><span>'+esc(c.topic)+'</span></div>'+stx+
      (ready?'<button class="go" data-lopen="'+c.id+'">'+(done?"Review":"Start")+'</button>':'')+'</li>';
  });
  a.innerHTML=h+'</ol></div>';
}
function renderLesson(a,L){
  var p=lp(L.id);
  var h='<div class="lesson"><div class="lhead"><button class="back" data-lmap="1">← All lessons</button><div class="lt2">Lesson '+L.n+(p&&p.completed?' · ✓ best '+p.best+'/'+p.of:'')+'</div></div>';
  h+='<h2>'+esc(L.title)+'</h2><p class="goal">'+esc(L.goal)+'<br>'+esc(L.minutes)+'</p>';
  h+='<div style="display:flex;gap:8px"><button class="sbtn" data-lexpand="1" style="flex:1">Open all steps</button><button class="sbtn" data-lexpand="0" style="flex:1">Close all</button></div>';
  L.sections.forEach(function(s){h+='<details class="ls"'+(s.open?" open":"")+'><summary>'+esc(s.h)+'</summary><div>'+s.html+'</div></details>'});
  h+='<button class="btn" data-lstart="'+L.id+'">Start the exercises ('+L.exercises.length+')</button>';
  h+='<p class="muted">Three parts: '+Object.keys(L.parts).map(function(k){return esc(L.parts[k])}).join(", ")+'. Every answer comes with the rule behind it.</p></div>';
  a.innerHTML=h;
}
function renderLessonHead(){
  var L=COURSE.lessons[st.lid];if(!L)return;
  var part=st.cur&&st.cur.e.part?L.parts[st.cur.e.part]:"Results";
  $("lessCtl").innerHTML='<button class="back" data-lread="1">← Lesson '+L.n+'</button><div class="lt2"><b>'+esc(part||"")+'</b>'+esc(L.title)+'</div>';
}
function lessonComplete(c){
  var L=COURSE.lessons[st.lid],n=L.exercises.length,first=st.first,pct=Math.round(100*first/n);
  if(!st.lsaved){
    var p=lprog.lessons[L.id]||{attempts:0,best:0};
    p.completed=true;p.attempts=(p.attempts||0)+1;p.of=n;p.last=first;p.lastDate=new Date().toISOString();
    if(first>=(p.best||0))p.best=first;
    lprog.lessons[L.id]=p;saveLessons();st.lsaved=true;
  }
  var pr=L.practice,best=lprog.lessons[L.id].best;
  var h='<div class="done"><h2>Lesson '+L.n+' complete!</h2>';
  h+='<p><b style="font-size:28px">'+first+'/'+n+'</b><br><span class="muted">right on the first try ('+pct+'%) · best '+best+'/'+n+'</span></p>';
  h+='<p class="muted">'+(pct>=90?"Excellent. You’ve got this rule.":pct>=70?"Good work. Re-read the steps you missed, then try again.":"This one takes practice. Re-read the lesson, then redo the exercises.")+' Every missed item came back until you got it right.</p>';
  if(pr)h+='<div class="practice"><b>'+esc(pr.title)+'</b><div>'+esc(pr.text)+'</div><div class="muted" style="margin-top:6px">For example:</div><ul lang="ru">'+pr.examples.map(function(x){return '<li>'+esc(x)+'</li>'}).join("")+'</ul></div>';
  h+='<button class="btn" id="lAgain">Redo the exercises</button><button class="btn quiet" data-lread="1">Re-read the lesson</button><button class="btn quiet" data-lmap="1">Back to all lessons</button></div>';
  c.innerHTML=h;$("lAgain").onclick=newSession;
}
$("lessonsArea").addEventListener("click",function(ev){
  var b=ev.target.closest("button");if(!b)return;
  if(b.dataset.lexpand!=null){Array.prototype.forEach.call($("lessonsArea").querySelectorAll("details.ls"),function(d){d.open=b.dataset.lexpand==="1"})}
});
document.addEventListener("click",function(ev){
  var b=ev.target.closest&&ev.target.closest("[data-lopen],[data-lstart],[data-lmap],[data-lread]");if(!b)return;
  if(b.dataset.lopen){st.lid=b.dataset.lopen;st.lview="read"}
  else if(b.dataset.lstart){st.lid=b.dataset.lstart;st.lview="ex"}
  else if(b.dataset.lmap){st.lview="map"}
  else if(b.dataset.lread){st.lview="read"}
  renderControls();
  if(st.lview==="ex")newSession();else{st.queue=[];st.cur=null;st.answered=false}
  window.scrollTo(0,0);
});

// ---------- My words ----------
function wordStatus(w){
  if(w.pos!=="noun")return {txt:"flashcards",fo:false};
  if(w.indecl)return {txt:"indeclinable · flashcards only",fo:true};
  var ex=E.wordExercises(w,{cases:1,plurals:1,numbers:1},null);
  if(!ex.length)return {txt:"flashcards only until you add its forms",fo:true};
  var kinds=[];ex.forEach(function(x){var k=x.sub.indexOf("plural")>=0?"plurals":(x.sub==="numbers"?"numbers":"cases");if(kinds.indexOf(k)<0)kinds.push(k)});
  return {txt:kinds.join(", ")+" + flashcards",fo:false};
}
function renderWords(){
  var th=themes();if(st.wtheme!=="all"&&th.indexOf(st.wtheme)<0)st.wtheme="all";
  $("wtheme").innerHTML='<option value="all">All themes · '+WORDS.length+' words</option>'+th.map(function(x){return '<option value="'+esc(x)+'"'+(st.wtheme===x?" selected":"")+'>'+esc(x)+' · '+themeWords(x).length+'</option>'}).join("");
  renderPanel();
  var h="";
  (st.wtheme==="all"?th:[st.wtheme]).forEach(function(t){
    h+='<div class="wtheme">'+esc(t)+'</div>';
    WORDS.forEach(function(w,i){if(w.theme!==t)return;var s=wordStatus(w);
      var meta=w.pos==="noun"?[G_LABEL[w.g]||"gender?",w.anim?"animate":"",KIND_LABEL[w.kind]||"",w.kind==="place"?(w.pp||"в")+" + place":""].filter(Boolean).join(" · "):w.pos;
      h+='<div class="witem"><div class="wt"><div class="wr" lang="ru">'+esc(w.ru)+'</div><div class="we">'+esc(w.en)+'</div><div class="wm">'+esc(meta)+' · <span class="'+(s.fo?"fo":"")+'">'+esc(s.txt)+'</span></div></div>'+
        '<button class="sbtn" data-edit="'+i+'" aria-label="Edit '+esc(w.ru)+'">Edit</button><button class="sbtn del" data-del="'+i+'" aria-label="Delete '+esc(w.ru)+'">✕</button></div>';
    });
  });
  $("wlist").innerHTML=h||'<p class="muted">No words yet. Tap “+ Add word”.</p>';
}
function blankWord(){return {ru:"",en:"",theme:st.wtheme!=="all"?st.wtheme:(themes()[0]||"My words"),pos:"noun",g:"",kind:"thing",pp:"в",forms:{}}}
function renderPanel(){
  var p=$("wpanel");
  if(st.importing){
    var n=st.importing.length;
    p.innerHTML='<div class="card"><b>Import '+n+' word'+(n===1?"":"s")+'</b><p class="muted">Merge adds new words and updates words with the same Russian and theme. Replace swaps your whole list for the imported one.</p>'+
      '<button class="btn" id="impMerge">Merge into my list</button><button class="btn quiet" id="impReplace">Replace my list</button><button class="btn quiet" id="impCancel">Cancel</button></div>';
    $("impMerge").onclick=function(){var add=0,upd=0;st.importing.forEach(function(w){var j=WORDS.findIndex(function(x){return x.ru===w.ru&&x.theme===w.theme});if(j>=0){WORDS[j]=w;upd++}else{WORDS.push(w);add++}});st.importing=null;saveWords();renderWords();alert("Imported: "+add+" new, "+upd+" updated.")};
    $("impReplace").onclick=function(){if(!confirm("Replace all "+WORDS.length+" words with the "+n+" imported words?"))return;WORDS=st.importing;st.importing=null;saveWords();renderWords()};
    $("impCancel").onclick=function(){st.importing=null;renderWords()};
    return;
  }
  if(!st.editing){p.innerHTML="";return}
  var w=st.editing.w,th=themes();if(th.indexOf(w.theme)<0&&w.theme)th.push(w.theme);
  var h='<div class="card" id="editor"><b>'+(st.editing.i<0?"Add a word":"Edit word")+'</b>';
  h+='<label class="f" for="fRu">Russian</label><input class="fin" id="fRu" lang="ru" autocomplete="off" autocapitalize="none" value="'+esc(w.ru)+'">';
  h+='<label class="f" for="fEn">English</label><input class="fin" id="fEn" autocomplete="off" value="'+esc(w.en)+'">';
  h+='<label class="f" for="fTheme">Theme</label><select id="fTheme">'+th.map(function(x){return '<option'+(x===w.theme?" selected":"")+'>'+esc(x)+'</option>'}).join("")+'<option value="__new">New theme…</option></select>';
  h+='<input class="fin hidden" id="fThemeNew" placeholder="Theme name, e.g. At the pharmacy" style="margin-top:6px">';
  h+='<label class="f" for="fPos">Type</label><select id="fPos">'+[["noun","Noun"],["adj","Adjective"],["verb","Verb"],["phrase","Phrase"]].map(function(o){return '<option value="'+o[0]+'"'+(w.pos===o[0]?" selected":"")+'>'+o[1]+'</option>'}).join("")+'</select>';
  h+='<div id="nounBox"'+(w.pos==="noun"?"":' class="hidden"')+'>';
  h+='<div class="fgrid"><div><label class="f" for="fG">Gender</label><select id="fG"><option value="">choose…</option>'+["m","f","n","pl"].map(function(g){return '<option value="'+g+'"'+(w.g===g?" selected":"")+'>'+{m:"masculine",f:"feminine",n:"neuter",pl:"plural only"}[g]+'</option>'}).join("")+'</select></div>';
  h+='<div><label class="f" for="fKind">Used like a…</label><select id="fKind">'+Object.keys(KIND_LABEL).map(function(k){return '<option value="'+k+'"'+(w.kind===k?" selected":"")+'>'+KIND_LABEL[k]+'</option>'}).join("")+'</select></div></div>';
  h+='<div id="ppBox"'+(w.kind==="place"?"":' class="hidden"')+'><label class="f" for="fPp">Place takes</label><select id="fPp"><option value="в"'+(w.pp!=="на"?" selected":"")+'>в (в магазине)</option><option value="на"'+(w.pp==="на"?" selected":"")+'>на (на вокзале)</option></select></div>';
  h+='<div class="checks">'+[["anim","animate (a person or animal)"],["indecl","indeclinable (кофе, меню)"],["mass","no plural (молоко)"],["fleet","fleeting vowel (платок → платка)"],["es","stressed ending (ножом, рублём)"]].map(function(c){return '<label><input type="checkbox" id="c_'+c[0]+'"'+(w[c[0]]?" checked":"")+'> '+c[1]+'</label>'}).join("")+'</div>';
  h+='<div class="muted">Forms: grey text is generated automatically. Type in a box to override it. Red dashed boxes are forms the app isn’t sure about, and they’re skipped in drills until you fill them in.</div>';
  h+='<div class="fgrid" id="formsGrid" style="margin-top:8px">'+E.KEYS.map(function(k){return '<div><label for="fm_'+k+'">'+FORM_LABEL[k]+'</label><input id="fm_'+k+'" lang="ru" autocomplete="off" autocapitalize="none" value="'+esc((w.forms||{})[k]||"")+'"></div>'}).join("")+'</div>';
  h+='<button class="sbtn" id="fillSug" style="margin-top:8px;width:100%">Use the suggested forms for unsure boxes</button>';
  h+='</div><div id="fNote"></div>';
  h+='<button class="btn" id="fSave">Save word</button><button class="btn quiet" id="fCancel">Cancel</button></div>';
  p.innerHTML=h;
  function readForm(){
    var nw={ru:$("fRu").value.trim(),en:$("fEn").value.trim(),pos:$("fPos").value};
    nw.theme=$("fTheme").value==="__new"?($("fThemeNew").value.trim()||"My words"):$("fTheme").value;
    if(nw.pos==="noun"){
      nw.g=$("fG").value;nw.kind=$("fKind").value;if(nw.kind==="place")nw.pp=$("fPp").value;
      ["anim","indecl","mass","fleet","es"].forEach(function(c){if($("c_"+c).checked)nw[c]=true});
      var f={};E.KEYS.forEach(function(k){var v=$("fm_"+k).value.trim();if(v)f[k]=v});nw.forms=f;
      ["skip","loc","enp","enprep","noArt","approach","gplAlt","noFleet"].forEach(function(k){if(w[k]!=null&&nw.ru===w.ru)nw[k]=w[k]});
      if(w.forms&&w.forms.loc&&nw.ru===w.ru)nw.forms.loc=w.forms.loc;
    }
    return nw;
  }
  function preview(){
    var nw=readForm();$("nounBox").classList.toggle("hidden",nw.pos!=="noun");
    if(nw.pos!=="noun"){$("fNote").innerHTML='<div class="note">Adjectives, verbs and phrases are drilled as flashcards in both directions.</div>';return}
    $("ppBox").classList.toggle("hidden",nw.kind!=="place");
    var auto=E.decline(Object.assign({},nw,{forms:{}}));
    E.KEYS.forEach(function(k){var el=$("fm_"+k);el.placeholder=auto.f[k]?(auto.unc[k]?"? "+auto.f[k]:auto.f[k]):"?";el.classList.toggle("unc",!!auto.unc[k]&&!el.value.trim())});
    var notes=[];if(auto.note)notes.push(auto.note);
    if(!nw.g&&!nw.indecl)notes.push("Pick a gender. Case drills need it.");
    if(nw.indecl)notes.push("Indeclinable nouns never change form, so they're drilled only as flashcards.");
    var s=wordStatus(nw);notes.push("This word will appear in: "+s.txt+".");
    $("fNote").innerHTML='<div class="note'+(s.fo?" warn":"")+'">'+notes.map(esc).join("<br>")+'</div>';
  }
  Array.prototype.forEach.call(p.querySelectorAll("input,select"),function(el){el.addEventListener("input",preview);el.addEventListener("change",preview)});
  $("fTheme").addEventListener("change",function(){$("fThemeNew").classList.toggle("hidden",this.value!=="__new");if(this.value==="__new")$("fThemeNew").focus()});
  $("fillSug").onclick=function(){var nw=readForm();var auto=E.decline(Object.assign({},nw,{forms:{}}));E.KEYS.forEach(function(k){var el=$("fm_"+k);if(auto.unc[k]&&!el.value.trim()&&auto.f[k])el.value=auto.f[k]});preview()};
  $("fCancel").onclick=function(){st.editing=null;renderWords()};
  $("fSave").onclick=function(){
    var nw=readForm();if(!nw.ru||!nw.en){alert("Please fill in both the Russian and the English.");return}
    if(st.editing.i>=0){if(nw.ru!==w.ru&&w.forms&&Object.keys(w.forms).length&&!confirm("You changed the Russian word, so its saved forms were regenerated. Check them before saving. Save now?"))return;WORDS[st.editing.i]=nw}
    else WORDS.push(nw);
    st.editing=null;st.wtheme=nw.theme;saveWords();renderWords();
  };
  if(st.editing.i>=0&&st.editing.w.ru!==w.ru){} 
  preview();
  $("fRu").addEventListener("input",function(){if(st.editing.i>=0&&$("fRu").value.trim()!==w.ru){E.KEYS.forEach(function(k){$("fm_"+k).value=""});preview()}});
  setTimeout(function(){p.scrollIntoView({behavior:"smooth",block:"start"})},30);
}
$("wlist").addEventListener("click",function(ev){
  var b=ev.target.closest("button");if(!b)return;
  if(b.dataset.edit!=null){var i=+b.dataset.edit;st.importing=null;st.editing={i:i,w:clone(WORDS[i])};renderPanel()}
  if(b.dataset.del!=null){var j=+b.dataset.del;if(confirm("Delete “"+WORDS[j].ru+"”?")){WORDS.splice(j,1);saveWords();st.editing=null;renderWords()}}
});
$("addW").onclick=function(){st.importing=null;st.editing={i:-1,w:blankWord()};renderPanel();setTimeout(function(){$("fRu").focus()},60)};
$("expW").onclick=function(){
  var data=JSON.stringify({app:"ruDrills",version:1,exported:new Date().toISOString(),words:WORDS},null,1);
  var dt=new Date(),name="russian-words-"+dt.getFullYear()+"-"+("0"+(dt.getMonth()+1)).slice(-2)+"-"+("0"+dt.getDate()).slice(-2)+".json";
  try{var blob=new Blob([data],{type:"application/json"});var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500)}
  catch(e){prompt("Copy this text and save it as "+name,data)}
};
$("impW").onclick=function(){$("impFile").value="";$("impFile").click()};
$("impFile").onchange=function(){
  var f=this.files&&this.files[0];if(!f)return;var r=new FileReader();
  r.onload=function(){try{var d=JSON.parse(r.result);var arr=Array.isArray(d)?d:d.words;if(!Array.isArray(arr))throw 0;
      arr=arr.filter(function(w){return w&&typeof w.ru==="string"&&typeof w.en==="string"&&w.ru.trim()}).map(function(w){if(!w.theme)w.theme="My words";if(!w.pos)w.pos="noun";return w});
      if(!arr.length)throw 0;st.editing=null;st.importing=arr;renderPanel();$("wpanel").scrollIntoView({behavior:"smooth"})}
    catch(e){alert("That file doesn't look like an exported word list.")}};
  r.readAsText(f);
};
$("restoreW").onclick=function(){var n=0;STARTER.forEach(function(s){if(!WORDS.some(function(w){return w.ru===s.ru&&w.theme===s.theme})){WORDS.push(clone(s));n++}});saveWords();renderWords();alert(n?("Restored "+n+" starter word"+(n===1?"":"s")+"."):"All starter words are already in your list.")};
$("wtheme").onchange=function(){st.wtheme=this.value;renderWords()};

// ---------- events ----------
document.addEventListener("click",function(ev){
  var t=ev.target.closest&&ev.target.closest("[data-cat],[data-mode],[data-level],[data-tab],[data-vdrill]");if(!t)return;
  if(t.dataset.tab){if(t.dataset.tab==="lessons"&&st.tab==="lessons")st.lview="map";st.tab=t.dataset.tab;st.sub="all";save();renderControls();newSession();return}
  if(t.dataset.level){st.level=t.dataset.level;st.cat="all";st.sub="all";renderControls();save();newSession();return}
  if(t.dataset.vdrill){st.vdrill=t.dataset.vdrill;st.sub="all";renderControls();save();newSession();return}
  if(t.dataset.cat){st.cat=t.dataset.cat;st.sub="all";renderControls();save();newSession()}
  if(t.dataset.mode){st.mode=t.dataset.mode;renderControls();save();if(st.cur&&!st.answered)render()}
});
document.addEventListener("keydown",function(ev){if(!$("drillArea").classList.contains("hidden")&&st.cur&&ev.key==="Enter"&&st.answered&&document.activeElement.id!=="nextBtn"){ev.preventDefault();next()}});
$("sub").onchange=function(){st.sub=this.value;newSession()};
$("vtheme").onchange=function(){st.vtheme=this.value;st.sub="all";save();renderControls();newSession()};
$("reset").onclick=function(){if(confirm("Reset drill scores on this device? Your words and lesson progress are kept.")){var keepTab=st.tab;store={tab:keepTab};try{localStorage.removeItem(LS)}catch(e){};newSession()}};

function start(d,v,les){
  if(les&&Array.isArray(les.course))COURSE=les;
  DATA=d.map(function(e){if(!e.level)e.level="B1-C1";return e});
  STARTER=v||[];
  var saved=load(LSW);WORDS=(saved&&Array.isArray(saved.words))?saved.words:clone(STARTER);
  if(!lvl().length)st.level="A1-A2";if(!lvl().some(function(e){return st.cat==="all"||e.cat===st.cat}))st.cat="all";
  renderControls();newSession();
}
var emb={exercises:[],vocab:[],lessons:null};try{emb=JSON.parse($("embedded").textContent)}catch(e){}
function getJSON(u,fb){return fetch(u,{cache:"no-cache"}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(x){return Array.isArray(x)&&x.length?x:fb}).catch(function(){return fb})}
if(location.protocol.indexOf("http")===0&&window.fetch&&window.Promise){
  var getLessons=fetch("lessons.json",{cache:"no-cache"}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(x){return x&&Array.isArray(x.course)?x:emb.lessons}).catch(function(){return emb.lessons});
  Promise.all([getJSON("exercises.json",emb.exercises),getJSON("vocab.json",emb.vocab),getLessons]).then(function(r){start(r[0],r[1],r[2])});
}else start(emb.exercises,emb.vocab,emb.lessons);
})();
