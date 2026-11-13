import json
words=[];table={};theme=None
PERS=('1s','2s','3s','1p','2p','3p')
for line in open('vocab_source.txt'):
    line=line.rstrip('\n')
    if not line or line.startswith('#'): continue
    if line.startswith('@'): theme=line[1:]; continue
    p=line.split('|')
    ru,en,pg=p[0],p[1],p[2]
    if pg in('adj','verb','phrase','adv'):
        w=dict(ru=ru,en=en,theme=theme,pos=pg)
        # optional 4th field (Молчат Дома words): aspect, conjugation forms 1s..3p, sentence frames f1s..f3p, note
        if len(p)>3 and p[3]:
            conj={};frames={}
            for f in p[3].split():
                if f in('impf','pf'): w['asp']=f; continue
                k,v=f.split('=',1); v=v.replace('_',' ')
                if k=='note': w['note']=v
                elif k in PERS: conj[k]=v
                elif k[:1]=='f' and k[1:] in PERS: frames[k[1:]]=v
                else: raise SystemExit('unknown flag '+f+' in '+ru)
            if conj: w['conj']=conj
            if frames: w['frames']=frames
        words.append(w); continue
    kind,flags=p[3],p[4]
    w=dict(ru=ru,en=en,theme=theme,pos='noun',g=pg,kind=kind)
    forms={}
    for f in flags.split():
        if '=' in f:
            k,v=f.split('=',1)
            v=v.replace('_',' ')
            if k=='pp': w['pp']=v
            elif k in('put','lie'): w[k]=v
            elif k=='skip': w['skip']=v.split(',')
            elif k=='enp': w['enp']=v
            elif k=='gpl_alt': w['gplAlt']=v
            elif k=='enprep': w['enprep']=v
            elif k=='note': w['note']=v
            else: forms[k]=v
        else: w[f]=True
    if forms: w['forms']=forms
    words.append(w)
    table[ru]=dict(zip(['gen','dat','acc','ins','prep','npl','gpl'],p[5:12]))
json.dump(words,open('../vocab.json','w'),ensure_ascii=False,indent=1)
json.dump(table,open('forms_table.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(words),Counter(w['theme'] for w in words),Counter(w['pos'] for w in words))
