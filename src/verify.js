const E=require('./engine.js');const words=require('../vocab.json');const table=require('./forms_table.json');
let bad=0,checked=0,unc=[];
for(const w of words){ if(w.pos!=='noun')continue; const t=table[w.ru]; const d=E.decline(w);
  for(const k of E.KEYS){ const exp=t[k]; if(exp==='-')continue; if((w.mass)&&(k==='npl'||k==='gpl')&&!(w.forms&&w.forms[k]))continue;
    checked++; if(d.unc[k]){unc.push(w.ru+'.'+k);continue;} if(d.f[k]!==exp){bad++;console.log('MISMATCH',w.ru,k,'engine=',d.f[k],'table=',exp);} } }
console.log('checked',checked,'mismatches',bad,'uncertain(no override)',unc);
// engine-only (no overrides) to show what the irregular overrides cover
let irr=[];for(const w of words){if(w.pos!=='noun'||!w.forms)continue;const d=E.decline(Object.assign({},w,{forms:{}}));const t=table[w.ru];
 for(const k of Object.keys(w.forms)){ if(d.unc[k]) irr.push(w.ru+'.'+k+'(engine unsure)'); else if(d.f[k]!==t[k]) irr.push(w.ru+'.'+k+': engine '+d.f[k]+' → stored '+t[k]); else irr.push(w.ru+'.'+k+' (override redundant)'); }}
console.log('overrides:',irr.join('; '));
// generate everything and sanity-check exercises
let ex=[];for(const w of words) ex=ex.concat(E.wordExercises(w,{cases:1,plurals:1,numbers:1,cards:1,conj:1},words));
let probs=ex.filter(e=>!e.a||e.d.length<2||e.d.some(x=>!x||x.toLowerCase()===e.a.toLowerCase())||new Set(e.d).size!==e.d.length||e.s.split('___').length!==2);
console.log('exercises',ex.length,'problems',probs.length,probs.slice(0,5));
const by={};ex.forEach(e=>by[e.sub]=(by[e.sub]||0)+1);console.log(by);
require('fs').writeFileSync('/tmp/gen_sentences.txt',ex.filter(e=>!e.sub.startsWith('flash')).map(e=>e.s.replace('___',e.a.toUpperCase())+'   | '+e.translation).join('\n'));
// every option shown for a starter noun must be a real form from the hand table
let invented=[];
for(const e of ex){ if(e.sub.startsWith('flashcard'))continue; const w=words.find(x=>x.ru===e.word&&(e.sub==='conjugation'?x.conj:x.pos==='noun'));
  if(e.sub==='conjugation'){ const ok=new Set([w.ru,...Object.values(w.conj)]); for(const o of [e.a,...e.d]) if(!ok.has(o)) invented.push(w.ru+':'+o); continue; }
  const t=table[w.ru];
  const ok=new Set([w.ru,...Object.values(t).filter(x=>x!=='-'),w.loc,(w.forms||{}).loc,w.gplAlt].filter(Boolean));
  for(const o of [e.a,...e.d]) if(!ok.has(o)) invented.push(w.ru+':'+o); }
console.log('options not in hand table:',invented.length,[...new Set(invented)].slice(0,20));
