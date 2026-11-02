import json
words=[];table={};theme=None
for line in open('vocab_source.txt'):
    line=line.rstrip('\n')
    if not line or line.startswith('#'): continue
    if line.startswith('@'): theme=line[1:]; continue
    p=line.split('|')
    ru,en,pg=p[0],p[1],p[2]
    if pg in('adj','verb','phrase'):
        words.append(dict(ru=ru,en=en,theme=theme,pos=pg)); continue
    kind,flags=p[3],p[4]
    w=dict(ru=ru,en=en,theme=theme,pos='noun',g=pg,kind=kind)
    forms={}
    for f in flags.split():
        if '=' in f:
            k,v=f.split('=',1)
            if k=='pp': w['pp']=v
            elif k=='skip': w['skip']=v.split(',')
            elif k=='enp': w['enp']=v
            elif k=='gpl_alt': w['gplAlt']=v
            elif k=='enprep': w['enprep']=v
            else: forms[k]=v
        else: w[f]=True
    if forms: w['forms']=forms
    words.append(w)
    table[ru]=dict(zip(['gen','dat','acc','ins','prep','npl','gpl'],p[5:12]))
json.dump(words,open('../vocab.json','w'),ensure_ascii=False,indent=1)
json.dump(table,open('forms_table.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(words),Counter(w['theme'] for w in words),Counter(w['pos'] for w in words))
