(function(){
"use strict";
var E=window.RuEngine;
var SP=window.RuSpeech||{accent:function(s){return s},setEnabled:function(){}};
var CYR=/[А-Яа-яЁё]/;
var CATS=[["all","All"],["basics","Basics"],["cases","Cases"],["conjugation","Verbs"],["aspect","Aspect"],["motion","Motion"],["home","At home"],["kakoy","какой / какая / какое / какие"],["frequency","никогда / иногда / всегда / часто / редко"]];
var LEVELS=[["A1-A2","A1–A2"],["B1-C1","B1–C1"]];
var MODES=[["choice","Choice"],["type","Type"]];
var NR=window.RuNumbers||null,NDRILLS=NR?NR.DRILLS:[],NRANGES=NR?NR.RANGES.concat([["all","Any"]]):[];
var VDRILLS=[["mixed","Mixed"],["cases","Cases"],["plurals","Plurals"],["numbers","Numbers"],["conj","Verbs"],["cards","Flashcards"]];
var KIND_LABEL={thing:"thing",food:"food/drink",place:"place",person:"person",event:"service/event",transport:"transport",money:"money",unit:"measure",home:"furniture/spot in a room",abstract:"abstract (feeling, sound, idea)",body:"body part",animal:"farm animal",wild:"wild animal",farm:"fence, gate, equipment",feed:"feed, hay, grass"};
var POS_LABEL={adj:"adjective",verb:"verb",phrase:"phrase",adv:"adverb/particle"};
var G_LABEL={m:"masc.",f:"fem.",n:"neut.",pl:"plural only"};
var FORM_LABEL={gen:"Genitive (нет …)",dat:"Dative (к …)",acc:"Accusative (вижу …)",ins:"Instrumental (с …)",prep:"Prepositional (о …)",npl:"Nominative plural",gpl:"Genitive plural (много …)"};
var LS="ruDrills.v1",LSW="ruDrills.words.v1",LSL="ruDrills.lessons.v1",LSC="ruDrills.sets.v1";
var SIZES=[[10,"10"],[15,"15"],[20,"20"],[0,"All"]];
var DATA=[],STARTER=[],WORDS=[],COURSE={course:[],lessons:{}};
var lprog=load(LSL);if(!lprog||typeof lprog.lessons!=="object"||!lprog.lessons)lprog={version:1,lessons:{}};
var store=load(LS)||{};
var cyc=load(LSC);if(!cyc||typeof cyc!=="object")cyc={};
var st={tab:store.tab||"lessons",lview:"map",lid:null,first:0,lsaved:false,level:store.level||"A1-A2",showTr:false,cat:store.cat||"all",sub:"all",mode:store.mode||"choice",
  vtheme:store.vtheme||"all",size:sizeOf(store.setSize),tts:store.tts!==false,nview:store.nview==="practice"?"practice":"learn",ndrill:store.ndrill||"mixed",nrange:store.nrange||"r0",ntheme:store.ntheme||"",setN:0,setDone:0,pk:null,pending:null,setInfo:null,setClosed:false,vdrill:store.vdrill||"mixed",wtheme:"all",queue:[],cur:null,answered:false,right:0,total:0,streak:0,picked:null,editing:null,importing:null};

function load(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}}
function sizeOf(n){return (n===0||n===10||n===15||n===20)?n:10}
function saveCyc(){try{localStorage.setItem(LSC,JSON.stringify(cyc))}catch(e){}}
var listeners=[],started=false;
function changed(kind){listeners.forEach(function(f){try{f(kind)}catch(e){}})}
function saveLocal(){try{store.cat=st.cat;store.mode=st.mode;store.level=st.level;store.tab=st.tab;store.vtheme=st.vtheme;store.vdrill=st.vdrill;store.nview=st.nview;store.ndrill=st.ndrill;store.nrange=st.nrange;store.ntheme=st.ntheme;store.setSize=st.size;store.tts=st.tts;localStorage.setItem(LS,JSON.stringify(store))}catch(e){}}
function save(){saveLocal();changed("drills")}
function saveLessons(){try{localStorage.setItem(LSL,JSON.stringify(lprog))}catch(e){}changed("lessons")}
function saveWords(){try{localStorage.setItem(LSW,JSON.stringify({version:1,words:WORDS}))}catch(e){alert("Couldn't save words in this browser (storage full or blocked).")}changed("words")}
function $(id){return document.getElementById(id)}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function norm(s){return String(s).replace(/\u0301/g,"").toLowerCase().replace(/ё/g,"е").replace(/[.,!?;:«»"]/g,"").replace(/\s+/g," ").trim()}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function clone(o){return JSON.parse(JSON.stringify(o))}
var CAT_LABEL={basics:"Basics",cases:"Cases",conjugation:"Verbs",aspect:"Aspect",motion:"Motion",home:"At home",kakoy:"какой / какая / какое / какие",frequency:"никогда / иногда / всегда / часто / редко",vocab:"Vocabulary",lesson:"Lesson"};
function lvl(){return DATA.filter(function(e){return e.level===st.level})}
function themes(){var t=[];WORDS.forEach(function(w){if(t.indexOf(w.theme)<0)t.push(w.theme)});return t}
function themeWords(th){return WORDS.filter(function(w){return th==="all"||w.theme===th})}

// ---------- Numbers ----------
function numTheme(){var t=st.ntheme||(themes().indexOf("Around the farm")>=0?"Around the farm":"all");return (t==="all"||themes().indexOf(t)>=0)?t:"all"}
// nouns the number drills may count: countable, with certain genitive singular and plural
function numNouns(){
  var out=[];
  themeWords(numTheme()).forEach(function(w){
    if(w.pos!=="noun"||w.indecl||w.mass||w.g==="pl"||!w.g||w.kind==="event"||w.nonum||/\s/.test(w.ru))return;
    var F=E.usable(w);if(!F.gen||!F.gpl)return;
    out.push({ru:w.ru,forms:[w.ru,F.gen,F.gpl],g:w.g,en:E.en1(w),enPl:E.enPl(w),npl:F.npl,dat:F.dat,money:w.kind==="money"});
  });
  return out;
}
function numSize(){return st.size||20}
function newNumbersSession(){
  var set=NR?NR.makeSet({drill:st.ndrill,range:st.nrange,nouns:numNouns(),size:numSize()}):[];
  st.pending=null;st.setInfo={random:true,total:set.length};st.setDone=0;st.setClosed=false;st.pk=null;st.setN=set.length;
  st.queue=set.map(function(e){return {e:e,again:false}});
  st.right=0;st.total=0;st.streak=0;st.first=0;st.lsaved=false;
  next();
}
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
    if(!st.size){
      var ex=E.buildSession(themeWords(st.vtheme),st.vdrill,0);
      if(st.sub!=="all")ex=ex.filter(function(e){return e.sub===st.sub});
      return ex.slice(0,25);
    }
    // sized sets draw from every item the drill can make (deduped), so "next set" can avoid repeats
    var tw=themeWords(st.vtheme),types=st.vdrill==="mixed"?{cases:1,plurals:1,numbers:1,cards:1,conj:1}:{},all=[],seenK={};types[st.vdrill]=1;
    tw.forEach(function(w){E.wordExercises(w,types,tw).forEach(function(e){if(st.sub!=="all"&&e.sub!==st.sub)return;var k=exKey(e);if(seenK[k])return;seenK[k]=1;all.push(e)})});
    return all;
  }
  return lvl().filter(function(e){return (st.cat==="all"||e.cat===st.cat)&&(st.sub==="all"||e.sub===st.sub)});
}
// stable id for "have I seen this question in this round": grammar ids, word+drill for generated vocab items
function exKey(e){if(e.id!=null)return String(e.id);return "v:"+e.word+"|"+e.sub+"|"+(e.sub==="numbers"?e.a:e.s)}
function poolKey(){return st.tab==="grammar"?["g",st.level,st.cat,st.sub,st.mode].join("|"):["v",st.vtheme,st.vdrill,st.sub,st.mode].join("|")}
function cycOf(pk){var c=cyc[pk];if(!c||typeof c!=="object")c={};if(!c.seen||typeof c.seen!=="object")c.seen={};if(!c.wrong||typeof c.wrong!=="object")c.wrong={};if(!Array.isArray(c.prev))c.prev=[];return c}
// take n, preferring items for words not already in the set (variety in vocab drills)
function varied(arr,n){var out=[],used={},rest=[];arr.forEach(function(e){if(out.length<n&&(e.word==null||!used[e.word])){out.push(e);if(e.word!=null)used[e.word]=1}else rest.push(e)});return out.concat(rest.slice(0,n-out.length))}
function pickSet(items,N,pk){
  var c=cycOf(pk),total=items.length;
  if(!N||total<=N)return {set:shuffle(items),commit:null,info:{total:total,whole:true}};
  var prev={};c.prev.forEach(function(k){prev[k]=1});
  var seen=c.seen,round=c.round||1,newRound=false;
  var unseen=items.filter(function(e){return !seen[exKey(e)]});
  if(!unseen.length){seen={};round++;unseen=items.slice()}
  function byPrev(a){a=shuffle(a);return a.filter(function(e){return !prev[exKey(e)]}).concat(a.filter(function(e){return prev[exKey(e)]}))}
  var pick,fill=[];
  if(unseen.length>=N)pick=varied(byPrev(unseen),N);
  else{
    // last few new ones of this round, topped up with earlier questions (missed ones first), then a new round starts
    var inU={};unseen.forEach(function(e){inU[exKey(e)]=1});
    var old=byPrev(items.filter(function(e){return !inU[exKey(e)]}));
    old=old.filter(function(e){return c.wrong[exKey(e)]}).concat(old.filter(function(e){return !c.wrong[exKey(e)]}));
    fill=varied(old,N-unseen.length);pick=unseen.concat(fill);newRound=true;
  }
  var ns={};
  if(newRound){fill.forEach(function(e){ns[exKey(e)]=1});round++}
  else{Object.keys(seen).forEach(function(k){ns[k]=1});pick.forEach(function(e){ns[exKey(e)]=1})}
  var commit={seen:ns,wrong:c.wrong,prev:pick.map(exKey),round:round};
  var keys={};items.forEach(function(e){keys[exKey(e)]=1});
  var seenAfter=newRound?total:Object.keys(ns).filter(function(k){return keys[k]}).length;
  return {set:shuffle(pick),commit:commit,info:{total:total,seenAfter:seenAfter,fresh:pick.length-fill.length,refill:fill.length,newRound:newRound}};
}
function lessonKey(){return "L|"+st.lid}
function subsFor(){
  if(st.tab==="vocab"){var s=[];E.buildSession(themeWords(st.vtheme),st.vdrill,0).forEach(function(e){if(s.indexOf(e.sub)<0)s.push(e.sub)});return s.sort()}
  var subs=[];lvl().forEach(function(e){if((st.cat==="all"||e.cat===st.cat)&&subs.indexOf(e.sub)<0)subs.push(e.sub)});return subs;
}

function renderControls(){
  Array.prototype.forEach.call(document.querySelectorAll(".tab"),function(b){b.setAttribute("aria-selected",String(b.dataset.tab===st.tab))});
  var lex=st.tab==="lessons"&&st.lview==="ex";
  var isNum=st.tab==="numbers",nPrac=isNum&&st.nview==="practice";
  $("drillArea").classList.toggle("hidden",st.tab==="words"||(st.tab==="lessons"&&!lex)||(isNum&&!nPrac));
  $("numbersArea").classList.toggle("hidden",!isNum||nPrac);
  $("numNav").classList.toggle("hidden",!isNum);
  $("sizeRow").classList.toggle("hidden",isNum);$("numMore").classList.toggle("hidden",!nPrac);
  $("numCtl").classList.toggle("hidden",!nPrac);
  $("wordsArea").classList.toggle("hidden",st.tab!=="words");
  $("lessonsArea").classList.toggle("hidden",st.tab!=="lessons"||lex);
  $("lessCtl").classList.toggle("hidden",!lex);
  $("gramCtl").classList.toggle("hidden",st.tab!=="grammar");
  $("vocCtl").classList.toggle("hidden",st.tab!=="vocab");
  $("sub").classList.toggle("hidden",st.tab==="lessons"||isNum);
  if(st.tab==="words"){renderWords();return}
  $("sizes").innerHTML=SIZES.map(function(z){return '<button class="chip" data-size="'+z[0]+'" aria-pressed="'+(st.size===z[0])+'">'+z[1]+'</button>'}).join("");
  if(st.tab==="lessons"){$("modes").innerHTML=MODES.map(function(m){return '<button class="chip" data-mode="'+m[0]+'" aria-pressed="'+(st.mode===m[0])+'">'+m[1]+'</button>'}).join("");if(!lex)renderLessons();return}
  if(isNum){renderNumbers();return}
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
  var subN={};
  if(st.tab==="grammar")lvl().forEach(function(e){if(st.cat==="all"||e.cat===st.cat)subN[e.sub]=(subN[e.sub]||0)+1});
  var allLabel=st.tab==="vocab"?"All drill types":"All subtopics";
  var allCount=st.tab==="grammar"?(st.cat==="all"?lvl().length:lvl().filter(function(e){return e.cat===st.cat}).length):0;
  $("sub").innerHTML='<option value="all">'+allLabel+(allCount?" · "+allCount:"")+'</option>'+subs.map(function(s){return '<option value="'+esc(s)+'"'+(st.sub===s?" selected":"")+'>'+esc(s)+(subN[s]!=null?" · "+subN[s]:"")+'</option>'}).join("");
  $("modes").innerHTML=MODES.map(function(m){return '<button class="chip" data-mode="'+m[0]+'" aria-pressed="'+(st.mode===m[0])+'">'+m[1]+'</button>'}).join("");
}

function newSession(){
  if(st.tab==="words")return;
  if(st.tab==="lessons"&&st.lview!=="ex"){st.queue=[];st.cur=null;st.answered=false;return}
  if(st.tab==="numbers"){if(st.nview!=="practice"){st.queue=[];st.cur=null;st.answered=false;return}newNumbersSession();return}
  var items=pool(),set;
  st.pending=null;st.setInfo=null;st.setDone=0;st.setClosed=false;st.setN=0;st.pk=null;
  if(st.tab==="lessons"){
    var L=COURSE.lessons[st.lid],lk=lessonKey(),run=cyc[lk],ids=items.map(function(e){return e.id});
    if(!run||!Array.isArray(run.order)||run.order.length!==ids.length||run.order.some(function(id){return ids.indexOf(id)<0})||!(run.pos<ids.length)){
      run={order:ids,pos:0,first:0};
    }
    cyc[lk]=run;saveCyc();
    var byId={};items.forEach(function(e){byId[e.id]=e});
    var part=run.order.slice(run.pos,st.size?run.pos+st.size:run.order.length);
    set=part.map(function(id){return byId[id]});
    if(set.length<ids.length)st.setN=set.length;
    st.setInfo={total:ids.length,from:run.pos+1,to:run.pos+set.length};
  }else{
    st.pk=poolKey();
    var r=pickSet(items,st.size,st.pk);set=r.set;st.pending=r.commit;st.setInfo=r.info;
    if(st.size&&items.length)st.setN=set.length;
  }
  st.queue=set.map(function(e){return {e:e,again:false}});
  st.right=0;st.total=0;st.streak=0;st.first=0;st.lsaved=false;
  next();
}
// a set just ended: lessons advance their run; finishing the last part completes the lesson
function closeSet(){
  st.setClosed=true;
  if(st.tab==="lessons"){
    var lk=lessonKey(),run=cyc[lk];if(!run)return;
    run.first=(run.first||0)+st.first;run.pos+=st.setInfo?(st.setInfo.to-st.setInfo.from+1):0;
    if(run.pos>=run.order.length){st.first=run.first;st.setN=0;delete cyc[lk]}
    saveCyc();
  }
}
function useChoice(e){return st.mode==="choice"||e.choiceOnly}
function next(){
  st.cur=st.queue.shift()||null;st.answered=false;st.picked=null;st.showTr=false;
  if(!st.cur&&st.total&&!st.setClosed)closeSet();
  if(st.cur)st.cur.opts=shuffle([st.cur.e.a].concat(st.cur.e.d));
  render();
}
function itemKey(e){if(e.numkey)return "n:"+e.numkey;return e.id!=null?String(e.id):("v:"+e.word+"|"+e.sub+"|"+e.s)}
function check(val){
  if(st.answered||!st.cur)return;
  var e=st.cur.e,ok;
  if(e.digits){var dv=String(val).replace(/\D/g,"");ok=dv.length>0&&dv===String(e.a).replace(/\D/g,"")}
  else ok=[e.a].concat(e.alt||[]).some(function(a){return norm(a)===norm(val)});
  st.answered=true;st.picked=val;st.ok=ok;st.total++;
  var rec=store.items=store.items||{};var k=itemKey(e);var r=rec[k]=rec[k]||{seen:0,right:0};r.seen++;
  if(st.pk){
    if(st.pending){cyc[st.pk]=st.pending;st.pending=null}
    if(!st.cur.again){var c=cyc[st.pk]=cycOf(st.pk),xk=exKey(e);if(ok)delete c.wrong[xk];else c.wrong[xk]=1}
    saveCyc();
  }
  if(!st.cur.again)st.setDone++;
  if(ok&&!st.cur.again)st.first++;
  if(ok){st.right++;st.streak++;r.right++;if(st.streak>(store.best||0))store.best=st.streak}
  else{st.streak=0;var pos=Math.min(st.queue.length,3+Math.floor(Math.random()*4));st.queue.splice(pos,0,{e:e,again:true})}
  save();render();
}

function disp(e,s){return (e.accMap&&e.accMap[s])||SP.accent(s)}
function sentenceHTML(e,fill,cls,acc){
  var parts=e.s.split("___"),f=acc?function(x){return SP.accent(x)}:function(x){return x};
  return esc(f(parts[0]))+'<span class="blank '+(cls||"")+'">'+(fill?esc(disp(e,fill)):"&nbsp;")+'</span>'+esc(f(parts[1]));
}
// what 🔊 reads after an answer: the completed sentence (flashcards: just the Russian word)
function sayText(e){
  var t;
  if(e.say)return CYR.test(e.say)?e.say:"";
  if(/^flashcard/.test(e.sub||"")&&e.word)t=e.word;
  else{var rest=e.s.replace("___","");t=CYR.test(e.a)?(CYR.test(rest)?e.s.replace("___",e.a):e.a):rest}
  t=String(t).replace(/^[\s—–-]+|[\s—–-]+$/g,"");
  return CYR.test(t)?t:"";
}
function syncTts(){SP.setEnabled(st.tts);["ttsT","ttsT2"].forEach(function(id){var el=$(id);if(el)el.checked=st.tts})}
function render(){
  $("sScore").textContent=st.right+"/"+st.total;
  $("sStreak").textContent=st.streak;
  $("sBest").textContent=store.best||0;
  $("sLeft").textContent=st.queue.length+(st.cur?1:0);
  var items=store.items||{},seen=0,right=0;Object.keys(items).forEach(function(k){seen+=items[k].seen;right+=items[k].right});
  $("lifetime").textContent=seen?("All-time: "+right+" correct out of "+seen+" answers."):"";
  var c=$("card");
  if(st.tab==="lessons")renderLessonHead();
  if(!st.cur&&st.tab==="lessons"&&st.total){if(st.setN){lessonSetDone(c);return}lessonComplete(c);return}
  if(!st.cur){
    if(!st.total){c.innerHTML='<div class="done"><h2>Nothing to drill here yet</h2><p class="muted">'+(st.tab==="vocab"?"This theme has no words that fit this drill. Nouns need a gender and forms the app is sure about, and Flashcards work with any word. Add words in My words.":"No exercises match these settings.")+'</p></div>';return}
    if(st.setN){setDone(c);return}
    var pct=Math.round(100*st.right/st.total);
    c.innerHTML='<div class="done"><h2>Отлично, сессия окончена!</h2><p class="muted">'+st.right+' correct out of '+st.total+' answers ('+pct+'%). Every missed item came back until you got it right.</p><button class="btn" id="again">Start a new session</button></div>';
    $("again").onclick=newSession;return;
  }
  var e=st.cur.e,h="",choice=useChoice(e);
  h+='<div class="meta"><span class="tag">'+esc(e.catLabel||CAT_LABEL[e.cat])+'</span><span class="tag">'+esc(e.sub)+'</span>'+(st.cur.again?'<span class="tag again">again</span>':'')+(st.setN?'<span class="tag pos" id="setPos">'+Math.min(st.setN,st.setDone+(st.cur.again||st.answered?0:1))+'/'+st.setN+'</span>':'')+'</div>';
  var fill=st.answered?e.a:"",cls=st.answered?(st.ok?"ok":"bad"):"";
  var say=st.answered?sayText(e):"";
  h+='<div class="sentence" lang="ru">'+sentenceHTML(e,fill,cls,st.answered&&/^flashcard/.test(e.sub||""))+(say?'<button class="say" id="sayBtn" data-say="'+esc(say)+'" aria-label="Hear the sentence" title="Hear it (Shift-click or right-click: slowly)">🔊</button>':'')+'</div>';
  if(e.listen&&!st.answered)h+='<div class="lis"><button class="btn" id="numPlay" type="button">🔊 Play</button><button class="btn quiet" id="numSlow" type="button">🐢 Slower</button></div>';
  if(e.base)h+='<div class="base">(<b lang="ru">'+esc(e.base)+'</b>)</div>';
  if(e.glosses&&e.glosses.length)h+='<div class="gl">'+esc(e.glosses.join(" · "))+'</div>';
  if(!st.answered&&e.translation)h+=st.showTr?'<div class="tr">'+esc(e.translation)+'</div>':'<button class="trbtn" id="trBtn">'+esc(e.trLabel||"Show translation")+'</button>';
  if(choice){
    h+='<div class="opts" lang="ru">'+st.cur.opts.map(function(o,i){
      var k="";if(st.answered){if(o===e.a)k="ok";else if(o===st.picked)k="bad"}
      return '<button class="opt '+k+'" data-i="'+i+'"'+(st.answered?" disabled":"")+'>'+esc(st.answered&&o===e.a?disp(e,o):o)+'</button>'}).join("")+'</div>';
  }else{
    h+='<input type="text" id="typed" lang="ru" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" enterkeyhint="done" placeholder="'+esc(e.ph||"Type the missing form")+'"'+(e.digits?' inputmode="numeric"':"")+' '+(st.answered?'disabled value="'+esc(st.picked)+'"':'')+'>';
    if(!st.answered)h+='<button class="btn" id="checkBtn">Check</button>';
  }
  if(st.answered){
    h+='<div class="fb '+(st.ok?"ok":"bad")+'"><strong>'+(st.ok?"Верно!":"Not quite. It will come back later.")+'</strong>'+
      (st.ok?"":'<div>Answer: <span class="ans" lang="ru">'+esc(disp(e,e.a))+'</span>'+((e.alt&&e.alt.length)?' (also accepted: '+esc(e.alt.join(", "))+')':'')+'</div>')+
      ((e.translation&&!e.listen)?'<div class="tr">'+esc(e.translation)+'</div>':'')+'<div>'+esc(e.ex)+'</div></div>';
    h+='<button class="btn" id="nextBtn">Next →</button>';
  }
  c.innerHTML=h;
  if(e.listen&&!st.answered){
    var pb=$("numPlay"),sb=$("numSlow");
    if(pb)pb.onclick=function(){if(SP.speak)SP.speak(e.say,false)};
    if(sb)sb.onclick=function(){if(SP.speak)SP.speak(e.say,true)};
    if(!st.cur.played){st.cur.played=true;if(SP.speak)setTimeout(function(){SP.speak(e.say,false)},120)}
  }
  if(choice&&!st.answered){Array.prototype.forEach.call(c.querySelectorAll(".opt"),function(b){b.onclick=function(){check(st.cur.opts[+b.dataset.i])}})}
  if(!choice&&!st.answered){var inp=$("typed");$("checkBtn").onclick=function(){if(inp.value.trim())check(inp.value)};
    inp.onkeydown=function(ev){if(ev.key==="Enter"&&!ev.isComposing&&inp.value.trim()){ev.preventDefault();ev.stopPropagation();check(inp.value)}};setTimeout(function(){inp.focus()},30)}
  var tb=$("trBtn");if(tb)tb.onclick=function(){st.showTr=true;var v=$("typed")?$("typed").value:"";render();if(v&&$("typed"))$("typed").value=v};
  if(st.answered){var nb=$("nextBtn");nb.onclick=next;if(!choice)nb.focus()}
}

function setDone(c){
  var n=st.setN,f=st.first,i=st.setInfo||{},sz=st.size||(st.tab==="numbers"?20:0);
  var h='<div class="done"><h2>Отлично, set done!</h2><p><b style="font-size:28px">'+f+'/'+n+'</b><br><span class="muted">right on the first try</span></p>';
  h+='<p class="muted">Every missed item came back until you got it right.';
  if(i.random)h+=' The numbers are random, so the next set is all new.';
  else if(i.whole)h+=' This topic only has '+i.total+' question'+(i.total===1?'':'s')+', so each set uses all of them.';
  else if(i.newRound)h+=' That finished all '+i.total+' questions here'+(i.refill?' (the last '+i.refill+' were repeats to fill the set, missed ones first)':'')+'. The next set starts a fresh round.';
  else h+=' You’ve now seen '+i.seenAfter+' of '+i.total+' questions here; the next set has none from this round.';
  h+='</p><button class="btn" id="nextSet">'+(i.whole?'Practice these again':'Next '+sz+' →')+'</button><button class="btn quiet" id="toTop">Choose another topic</button></div>';
  c.innerHTML=h;$("nextSet").onclick=newSession;$("toTop").onclick=function(){window.scrollTo({top:0,behavior:"smooth"})};
}
function lessonSetDone(c){
  var L=COURSE.lessons[st.lid],i=st.setInfo,run=cyc[lessonKey()]||{pos:i.to};
  var left=L.exercises.length-run.pos,nn=st.size?Math.min(st.size,left):left;
  var h='<div class="done"><h2>Set done: '+i.from+'–'+i.to+' of '+i.total+'</h2><p><b style="font-size:28px">'+st.first+'/'+(i.to-i.from+1)+'</b><br><span class="muted">right on the first try</span></p>';
  h+='<p class="muted">'+left+' exercise'+(left===1?'':'s')+' left in this lesson. Your place is saved, so you can come back later.</p>';
  h+='<button class="btn" id="nextSet">Next '+nn+' →</button><button class="btn quiet" data-lread="1">Re-read the lesson</button><button class="btn quiet" data-lmap="1">Back to all lessons</button></div>';
  c.innerHTML=h;$("nextSet").onclick=newSession;
}
function renderNumbers(){
  $("numNav").innerHTML=[["learn","Learn"],["practice","Practice"]].map(function(v){return '<button class="chip" data-nview="'+v[0]+'" aria-pressed="'+(st.nview===v[0])+'">'+v[1]+'</button>'}).join("");
  if(st.nview!=="practice"){renderNumbersLearn($("numbersArea"));return}
  $("ndrill").innerHTML=NDRILLS.map(function(d){return '<option value="'+d[0]+'"'+(st.ndrill===d[0]?" selected":"")+'>'+esc(d[1])+'</option>'}).join("");
  var useRange=["phone","ord"].indexOf(st.ndrill)<0;
  $("nrange").classList.toggle("hidden",!useRange);
  $("nrange").innerHTML=NRANGES.map(function(r){return '<option value="'+r[0]+'"'+(st.nrange===r[0]?" selected":"")+'>Range: '+esc(r[1])+'</option>'}).join("");
  var th=themes(),cur=numTheme(),nn=["noun","mixed"].indexOf(st.ndrill)>=0;
  $("nthemeRow").classList.toggle("hidden",!nn);
  $("ntheme").innerHTML='<option value="all"'+(cur==="all"?" selected":"")+'>Nouns from all my words</option>'+th.map(function(x){return '<option value="'+esc(x)+'"'+(cur===x?" selected":"")+'>Nouns from: '+esc(x)+'</option>'}).join("");
  $("nsizes").innerHTML=SIZES.filter(function(z){return z[0]!==0}).map(function(z){return '<button class="chip" data-size="'+z[0]+'" aria-pressed="'+(numSize()===z[0])+'">'+z[1]+'</button>'}).join("");
  $("numMoreSum").textContent="⚙ More settings · "+numSize()+" questions per set"+(nn?" · "+(cur==="all"?"all my nouns":cur):"");
  $("modes").innerHTML=MODES.map(function(m){return '<button class="chip" data-mode="'+m[0]+'" aria-pressed="'+(st.mode===m[0])+'">'+m[1]+'</button>'}).join("");
}
function renderNumbersLearn(a){
  var N=COURSE.numbers;
  if(!N){a.innerHTML='<div class="lesson"><h2>Numbers</h2><p class="goal">The numbers lesson is not available in this copy of the course.</p><button class="btn" data-nview="practice">Go to practice</button></div>';return}
  var h='<div class="lesson"><h2>'+esc(N.title)+'</h2><p class="goal">'+esc(N.goal)+'<br>'+esc(N.minutes)+'</p>';
  h+='<div style="display:flex;gap:8px"><button class="sbtn" data-nexpand="1" style="flex:1">Open all steps</button><button class="sbtn" data-nexpand="0" style="flex:1">Close all</button></div>';
  N.sections.forEach(function(s){h+='<details class="ls"'+(s.open?" open":"")+'><summary>'+esc(s.h)+'</summary><div>'+s.html+'</div></details>'});
  var pr=N.practice;
  if(pr)h+='<div class="practice"><b>'+esc(pr.title)+'</b><div>'+esc(pr.text)+'</div><div class="muted" style="margin-top:6px">For example:</div><ul lang="ru">'+pr.examples.map(function(x){return '<li>'+esc(x)+'</li>'}).join("")+'</ul></div>';
  h+='<button class="btn" data-nview="practice">Start practicing →</button><p class="muted">Practice has random numbers that never run out: digits to words, words to digits, listening, numbers with nouns, prices and ages, phone numbers and ordinals.</p></div>';
  a.innerHTML=h;
}
// ---------- Lessons ----------
function lp(id){return lprog.lessons[id]||null}
function lessonName(L){return L.review?L.title:("Lesson "+L.n)}
function renderLessons(){
  var a=$("lessonsArea");
  if(st.lview==="read"&&COURSE.lessons[st.lid]){renderLesson(a,COURSE.lessons[st.lid]);return}
  var h='<div class="lesson"><h2>Course roadmap · A1–A2</h2><p class="goal">The classroom way: read a short lesson, practice that one rule, then review. Lessons unlock as they’re written.</p>';
  if(COURSE.numbers)h+='<div class="numcard"><div class="lt1"><b>Numbers: 0 to a million</b><span>Say, read and hear numbers, and use the right noun after them (две коровы, пять коров). Own tab, with endless random practice.</span></div><button class="go" data-gonum="1">Open</button></div>';
  h+='<ol class="course">';
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
  var h='<div class="lesson"><div class="lhead"><button class="back" data-lmap="1">← All lessons</button><div class="lt2">'+esc(lessonName(L))+(p&&p.completed?' · ✓ best '+p.best+'/'+p.of:'')+'</div></div>';
  h+='<h2>'+esc(L.title)+'</h2><p class="goal">'+esc(L.goal)+'<br>'+esc(L.minutes)+'</p>';
  h+='<div style="display:flex;gap:8px"><button class="sbtn" data-lexpand="1" style="flex:1">Open all steps</button><button class="sbtn" data-lexpand="0" style="flex:1">Close all</button></div>';
  L.sections.forEach(function(s){h+='<details class="ls"'+(s.open?" open":"")+'><summary>'+esc(s.h)+'</summary><div>'+s.html+'</div></details>'});
  var run=cyc["L|"+L.id];
  if(run&&run.pos>0&&run.pos<L.exercises.length)h+='<button class="btn" data-lstart="'+L.id+'">Continue the exercises ('+(run.order.length-run.pos)+' of '+L.exercises.length+' left)</button><button class="btn quiet" data-lrestart="'+L.id+'">Start over</button>';
  else h+='<button class="btn" data-lstart="'+L.id+'">Start the exercises ('+L.exercises.length+')</button>';
  h+='<p class="muted">'+Object.keys(L.parts).map(function(k){return esc(L.parts[k])}).join(", ")+'. Every answer comes with the rule behind it.</p></div>';
  a.innerHTML=h;
}
function renderLessonHead(){
  var L=COURSE.lessons[st.lid];if(!L)return;
  var part=st.cur&&st.cur.e.part?L.parts[st.cur.e.part]:"Results";
  $("lessCtl").innerHTML='<button class="back" data-lread="1">← '+esc(lessonName(L))+'</button><div class="lt2"><b>'+esc(part||"")+'</b>'+esc(L.title)+'</div>';
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
  var h='<div class="done"><h2>'+esc(lessonName(L))+' complete!</h2>';
  h+='<p><b style="font-size:28px">'+first+'/'+n+'</b><br><span class="muted">right on the first try ('+pct+'%) · best '+best+'/'+n+'</span></p>';
  h+='<p class="muted">'+(pct>=90?"Excellent. You’ve got this rule.":pct>=70?"Good work. Re-read the steps you missed, then try again.":"This one takes practice. Re-read the lesson, then redo the exercises.")+' Every missed item came back until you got it right.</p>';
  if(pr)h+='<div class="practice"><b>'+esc(pr.title)+'</b><div>'+esc(pr.text)+'</div><div class="muted" style="margin-top:6px">For example:</div><ul lang="ru">'+pr.examples.map(function(x){return '<li>'+esc(x)+'</li>'}).join("")+'</ul></div>';
  h+='<button class="btn" id="lAgain">Redo the exercises</button><button class="btn quiet" data-lread="1">Re-read the lesson</button><button class="btn quiet" data-lmap="1">Back to all lessons</button></div>';
  c.innerHTML=h;$("lAgain").onclick=function(){delete cyc[lessonKey()];saveCyc();newSession()};
}
$("lessonsArea").addEventListener("click",function(ev){
  var b=ev.target.closest("button");if(!b)return;
  if(b.dataset.lexpand!=null){Array.prototype.forEach.call($("lessonsArea").querySelectorAll("details.ls"),function(d){d.open=b.dataset.lexpand==="1"})}
});
document.addEventListener("click",function(ev){
  var b=ev.target.closest&&ev.target.closest("[data-lopen],[data-lstart],[data-lmap],[data-lread],[data-lrestart]");if(!b)return;
  if(b.dataset.lrestart){st.lid=b.dataset.lrestart;delete cyc["L|"+st.lid];saveCyc();st.lview="ex"}
  else if(b.dataset.lopen){st.lid=b.dataset.lopen;st.lview="read"}
  else if(b.dataset.lstart){st.lid=b.dataset.lstart;st.lview="ex"}
  else if(b.dataset.lmap){st.lview="map"}
  else if(b.dataset.lread){st.lview="read"}
  renderControls();
  if(st.lview==="ex")newSession();else{st.queue=[];st.cur=null;st.answered=false}
  window.scrollTo(0,0);
});

// ---------- My words ----------
function wordStatus(w){
  if(w.pos!=="noun")return {txt:w.pos==="verb"&&w.conj?"conjugation + flashcards":"flashcards",fo:false};
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
      var meta=w.pos==="noun"?[G_LABEL[w.g]||"gender?",w.anim?"animate":"",KIND_LABEL[w.kind]||"",(w.kind==="place"||w.kind==="home")?(w.pp||"в")+" + place":""].filter(Boolean).join(" · "):(POS_LABEL[w.pos]||w.pos)+(w.asp?" · "+w.asp+".":"");
      h+='<div class="witem"><div class="wt"><div class="wr" lang="ru">'+esc(SP.accent(w.ru))+'</div><div class="we">'+esc(w.en)+'</div>'+(w.note?'<div class="wm">'+esc(w.note)+'</div>':'')+'<div class="wm">'+esc(meta)+' · <span class="'+(s.fo?"fo":"")+'">'+esc(s.txt)+'</span></div></div>'+
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
  h+='<label class="f" for="fPos">Type</label><select id="fPos">'+[["noun","Noun"],["adj","Adjective"],["verb","Verb"],["adv","Adverb/particle"],["phrase","Phrase"]].map(function(o){return '<option value="'+o[0]+'"'+(w.pos===o[0]?" selected":"")+'>'+o[1]+'</option>'}).join("")+'</select>';
  h+='<div id="nounBox"'+(w.pos==="noun"?"":' class="hidden"')+'>';
  h+='<div class="fgrid"><div><label class="f" for="fG">Gender</label><select id="fG"><option value="">choose…</option>'+["m","f","n","pl"].map(function(g){return '<option value="'+g+'"'+(w.g===g?" selected":"")+'>'+{m:"masculine",f:"feminine",n:"neuter",pl:"plural only"}[g]+'</option>'}).join("")+'</select></div>';
  h+='<div><label class="f" for="fKind">Used like a…</label><select id="fKind">'+Object.keys(KIND_LABEL).map(function(k){return '<option value="'+k+'"'+(w.kind===k?" selected":"")+'>'+KIND_LABEL[k]+'</option>'}).join("")+'</select></div></div>';
  h+='<div id="ppBox"'+(w.kind==="place"||w.kind==="home"?"":' class="hidden"')+'><label class="f" for="fPp">Place takes</label><select id="fPp"><option value="в"'+(w.pp!=="на"?" selected":"")+'>в (в магазине)</option><option value="на"'+(w.pp==="на"?" selected":"")+'>на (на вокзале)</option></select></div>';
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
      nw.g=$("fG").value;nw.kind=$("fKind").value;if(nw.kind==="place"||nw.kind==="home")nw.pp=$("fPp").value;
      ["anim","indecl","mass","fleet","es"].forEach(function(c){if($("c_"+c).checked)nw[c]=true});
      var f={};E.KEYS.forEach(function(k){var v=$("fm_"+k).value.trim();if(v)f[k]=v});nw.forms=f;
      ["skip","loc","enp","enprep","enSg","noArt","approach","gplAlt","noFleet","put","lie","nonum"].forEach(function(k){if(w[k]!=null&&nw.ru===w.ru)nw[k]=w[k]});
      if(w.forms&&w.forms.loc&&nw.ru===w.ru)nw.forms.loc=w.forms.loc;
    }
    if(nw.ru===w.ru){["note"].concat(nw.pos==="verb"&&w.pos==="verb"?["asp","conj","frames"]:[]).forEach(function(k){if(w[k]!=null)nw[k]=w[k]})}
    return nw;
  }
  function preview(){
    var nw=readForm();$("nounBox").classList.toggle("hidden",nw.pos!=="noun");
    if(nw.pos!=="noun"){$("fNote").innerHTML='<div class="note">Adjectives, verbs, adverbs and phrases are drilled as flashcards in both directions.'+(nw.conj?' Its saved conjugation forms are drilled under Verbs too.':'')+'</div>';return}
    $("ppBox").classList.toggle("hidden",nw.kind!=="place"&&nw.kind!=="home");
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
["ttsT","ttsT2"].forEach(function(id){var el=$(id);if(el)el.onchange=function(){st.tts=this.checked;syncTts();save()}});

// ---------- events ----------
document.addEventListener("click",function(ev){
  var t=ev.target.closest&&ev.target.closest("[data-cat],[data-mode],[data-level],[data-tab],[data-vdrill],[data-size]");if(!t)return;
  if(t.dataset.size!=null){st.size=sizeOf(+t.dataset.size);save();renderControls();newSession();return}
  if(t.dataset.tab){if(t.dataset.tab==="lessons"&&st.tab==="lessons")st.lview="map";st.tab=t.dataset.tab;st.sub="all";save();renderControls();newSession();return}
  if(t.dataset.level){st.level=t.dataset.level;st.cat="all";st.sub="all";renderControls();save();newSession();return}
  if(t.dataset.vdrill){st.vdrill=t.dataset.vdrill;st.sub="all";renderControls();save();newSession();return}
  if(t.dataset.cat){st.cat=t.dataset.cat;st.sub="all";renderControls();save();newSession()}
  if(t.dataset.mode){st.mode=t.dataset.mode;renderControls();save();if(st.cur&&!st.answered)render()}
});
$("numbersArea").addEventListener("click",function(ev){
  var b=ev.target.closest("button");if(!b)return;
  if(b.dataset.nexpand!=null){Array.prototype.forEach.call($("numbersArea").querySelectorAll("details.ls"),function(d){d.open=b.dataset.nexpand==="1"})}
});
document.addEventListener("click",function(ev){
  var b=ev.target.closest&&ev.target.closest("[data-nview],[data-rv],[data-gonum]");if(!b)return;
  if(b.dataset.rv){var box=b.closest(".rv");if(!box)return;var on=box.classList.toggle("nostress");b.textContent=on?"Show stress ´":"Hide stress ´";b.setAttribute("aria-pressed",String(!on));return}
  if(b.dataset.gonum){st.tab="numbers";st.sub="all";save();renderControls();newSession();window.scrollTo(0,0);return}
  if(b.dataset.nview){st.nview=b.dataset.nview;save();renderControls();newSession();window.scrollTo(0,0);return}
});
$("ndrill").onchange=function(){st.ndrill=this.value;save();renderControls();newSession()};
$("nrange").onchange=function(){st.nrange=this.value;save();newSession()};
$("ntheme").onchange=function(){st.ntheme=this.value;save();newSession()};
document.addEventListener("keydown",function(ev){if(!$("drillArea").classList.contains("hidden")&&st.cur&&ev.key==="Enter"&&st.answered&&document.activeElement.id!=="nextBtn"){ev.preventDefault();next()}});
$("sub").onchange=function(){st.sub=this.value;newSession()};
$("vtheme").onchange=function(){st.vtheme=this.value;st.sub="all";save();renderControls();newSession()};
$("reset").onclick=function(){if(confirm("Reset drill scores on this device? Your words and lesson progress are kept.")){var keepTab=st.tab;store={tab:keepTab};try{localStorage.removeItem(LS)}catch(e){};changed("drills");newSession()}};

function start(d,v,les){
  if(les&&Array.isArray(les.course))COURSE=les;
  DATA=d.map(function(e){if(!e.level)e.level="B1-C1";return e});
  STARTER=v||[];
  var saved=load(LSW);WORDS=(saved&&Array.isArray(saved.words))?saved.words:clone(STARTER);
  addNewStarterThemes();
  if(!lvl().length)st.level="A1-A2";if(!lvl().some(function(e){return st.cat==="all"||e.cat===st.cat}))st.cat="all";
  started=true;syncTts();renderControls();newSession();
}
// New built-in themes reach people who already have a saved word list (once per theme, so deleting one sticks).
var OLD_THEMES=["At the grocery store","At the checkout","At church","At the restaurant","At the border","Travel"];
function addNewStarterThemes(){
  var all=[];STARTER.forEach(function(w){if(all.indexOf(w.theme)<0)all.push(w.theme)});
  var seen=Array.isArray(store.seenThemes)?store.seenThemes:OLD_THEMES,saved=load(LSW),n=0;
  var fresh=all.filter(function(t){return seen.indexOf(t)<0});
  if(saved&&Array.isArray(saved.words)&&fresh.length){
    STARTER.forEach(function(s){if(fresh.indexOf(s.theme)>=0&&!WORDS.some(function(w){return w.ru===s.ru&&w.theme===s.theme})){WORDS.push(clone(s));n++}});
  }
  if(String(seen)!==String(all)||!Array.isArray(store.seenThemes)){store.seenThemes=all;save()}
  if(n){saveWords();if(st.tab==="words")renderWords();else if(st.tab==="vocab")renderControls()}
}
// ---------- bridge for cloud sync (cloud.js) ----------
function applyPrefs(){st.tab=store.tab||st.tab;st.level=store.level||st.level;st.cat=store.cat||"all";st.mode=store.mode||st.mode;st.vtheme=store.vtheme||"all";st.vdrill=store.vdrill||"mixed";st.nview=store.nview==="practice"?"practice":"learn";st.ndrill=store.ndrill||"mixed";st.nrange=store.nrange||"r0";st.ntheme=store.ntheme||"";st.size=sizeOf(store.setSize);st.tts=store.tts!==false;st.sub="all";syncTts();
  if(started){if(!lvl().length)st.level="A1-A2";if(!lvl().some(function(e){return st.cat==="all"||e.cat===st.cat}))st.cat="all"}}
window.RuApp={
  keys:{drills:LS,lessons:LSL,words:LSW},
  snapshot:function(){if(started)saveLocal();return {drills:load(LS)||{},lessons:load(LSL)||{version:1,lessons:{}},words:load(LSW)}},
  hasLocalProgress:function(){var d=load(LS)||{},l=load(LSL);return !!((d.items&&Object.keys(d.items).length)||d.best||(l&&l.lessons&&Object.keys(l.lessons).length)||load(LSW))},
  apply:function(snap){
    store=(snap.drills&&typeof snap.drills==="object")?snap.drills:{};
    lprog=(snap.lessons&&typeof snap.lessons.lessons==="object"&&snap.lessons.lessons)?snap.lessons:{version:1,lessons:{}};
    try{localStorage.setItem(LS,JSON.stringify(store));localStorage.setItem(LSL,JSON.stringify(lprog));
      if(snap.words&&Array.isArray(snap.words.words))localStorage.setItem(LSW,JSON.stringify(snap.words));else localStorage.removeItem(LSW)}catch(e){}
    if(started){WORDS=(snap.words&&Array.isArray(snap.words.words))?snap.words.words:clone(STARTER);setTimeout(addNewStarterThemes,0)}
    cyc=load(LSC);if(!cyc||typeof cyc!=="object")cyc={};
    applyPrefs();st.editing=null;st.importing=null;
    if(started){if(st.tab==="lessons"&&st.lview==="ex"&&st.cur)render();else{renderControls();newSession()}}
  },
  clearLocal:function(){cyc={};[LS,LSL,LSW,LSC].forEach(function(k){try{localStorage.removeItem(k)}catch(e){}})},
  onChange:function(f){listeners.push(f)}
};
var emb={exercises:[],vocab:[],lessons:null};try{emb=JSON.parse($("embedded").textContent)}catch(e){}
function getJSON(u,fb){return fetch(u,{cache:"no-cache"}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(x){return Array.isArray(x)&&x.length?x:fb}).catch(function(){return fb})}
if(location.protocol.indexOf("http")===0&&window.fetch&&window.Promise){
  var getLessons=fetch("lessons.json",{cache:"no-cache"}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(x){return x&&Array.isArray(x.course)?x:emb.lessons}).catch(function(){return emb.lessons});
  Promise.all([getJSON("exercises.json",emb.exercises),getJSON("vocab.json",emb.vocab),getLessons]).then(function(r){start(r[0],r[1],r[2])});
}else start(emb.exercises,emb.vocab,emb.lessons);
})();
