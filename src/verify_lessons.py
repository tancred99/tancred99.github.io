# Checks lessons.json: explicit forms table vs OpenCorpora (pymorphy3), every exercise answer, every Cyrillic word.
# Run with: /workspace/venv-morph/bin/python src/verify_lessons.py
import json, re, sys
import pymorphy3
M = pymorphy3.MorphAnalyzer()
L = json.load(open("lessons.json"))
# word: (gender, preposition used for location, location form)
T = {
 "магазин": ("m","в","магазине"), "храм": ("m","в","храме"), "паспорт": ("m",None,None), "Минск": ("m","в","Минске"),
 "музей": ("m","в","музее"), "чай": ("m",None,None), "трамвай": ("m",None,None),
 "касса": ("f","на","кассе"), "улица": ("f","на","улице"), "граница": ("f","на","границе"), "работа": ("f","на","работе"),
 "таможня": ("f","на","таможне"), "деревня": ("f","в","деревне"), "Россия": ("f","в","России"),
 "окно": ("n",None,None), "место": ("n","на","месте"), "молоко": ("n",None,None),
 "море": ("n","на","море"), "здание": ("n","в","здании"), "расписание": ("n","в","расписании"),
 "папа": ("m",None,None), "дедушка": ("m",None,None), "батюшка": ("m",None,None), "мужчина": ("m",None,None),
 "ночь": ("f",None,None), "дочь": ("f",None,None), "вещь": ("f",None,None), "новость": ("f",None,None), "радость": ("f",None,None),
 "учитель": ("m",None,None), "водитель": ("m",None,None), "житель": ("m",None,None),
 "рубль": ("m",None,None), "день": ("m",None,None), "Гомель": ("m","в","Гомеле"),
 "церковь": ("f","в","церкви"), "очередь": ("f","в","очереди"), "Беларусь": ("f","в","Беларуси"), "площадь": ("f","на","площади"), "дверь": ("f",None,None),
 "литургия": ("f","на","литургии"), "санаторий": ("m","в","санатории"),
 "Брест": ("m","в","Бресте"), "Витебск": ("m","в","Витебске"), "Могилёв": ("m","в","Могилёве"), "Березино": ("n","в","Березине"),
 "рынок": ("m","на","рынке"), "вокзал": ("m","на","вокзале"), "почта": ("f","на","почте"), "остановка": ("f","на","остановке"),
 "стол": ("m","на","столе"), "служба": ("f","на","службе"), "Франция": ("f","во","Франции"), "Владимир": ("m","во","Владимире"),
 "аэропорт": ("m","в","аэропорту"), "лес": ("m","в","лесу"), "мост": ("m","на","мосту"), "сад": ("m","в","саду"), "пол": ("m","на","полу"), "шкаф": ("m","в","шкафу"),
 "Америка": ("f","в","Америке"),
 "офис": ("m","в","офисе"), "кухня": ("f","на","кухне"), "пастбище": ("n","на","пастбище"),
 "коровник": ("m","в","коровнике"), "концерт": ("m","на","концерте"), "ферма": ("f","на","ферме"),
 "компьютер": ("m",None,None), "письмо": ("n",None,None), "песня": ("f",None,None), "лошадь": ("f",None,None),
 "сервер": ("m","на","сервере"), "гостиница": ("f","в","гостинице"),
}
# forms after о (about) mentioned in the lesson
ABOUT = {"Минск": "Минске", "лес": "лесе", "аэропорт": "аэропорте", "Америка": "Америке"}
GM = {"masc":"m","femn":"f","neut":"n","ms-f":"m"}
errs = []
def parse_noun(w):
    for p in M.parse(w):
        if p.tag.POS == "NOUN" and "nomn" in p.tag and "sing" in p.tag and p.normal_form == w.lower().replace("ё","е") or (p.tag.POS=="NOUN" and p.normal_form==w.lower()):
            return p
    return None
for w,(g,prep,loc) in T.items():
    p = parse_noun(w)
    if not p: errs.append("not in dictionary: "+w); continue
    if GM.get(p.tag.gender) != g: errs.append("gender %s: table %s, dict %s" % (w,g,p.tag.gender))
    if loc:
        forms = set()
        for q in M.parse(w):  # any noun reading (пол = floor vs. sex)
            if q.tag.POS == "NOUN" and q.normal_form == p.normal_form:
                forms |= {x.word for x in [q.inflect({"loct"}), q.inflect({"loc2"})] if x}
        if loc.lower() not in forms: errs.append("location form %s: table %s, dict %s" % (w,loc,forms))
for w,f in ABOUT.items():
    p = parse_noun(w); x = p.inflect({"loct"}).word
    if x != f.lower(): errs.append("о-form %s: %s vs %s" % (w,f,x))
# exercises
GN = {"masculine":"m","feminine":"f","neuter":"n"}
inv = {}
for w,(g,prep,loc) in T.items():
    if loc: inv[loc] = (w,prep)
# Lesson 2: accusative of things. word: (preposition for куда?, accusative form). Checked against the dictionary (inanimate reading).
ACC = {
 "хлеб": (None,"хлеб"), "вода": (None,"воду"), "молоко": (None,"молоко"), "касса": ("на","кассу"), "рыба": (None,"рыбу"),
 "паспорт": (None,"паспорт"), "свеча": (None,"свечу"), "молитва": (None,"молитву"), "церковь": ("в","церковь"), "Беларусь": ("в","Беларусь"),
 "храм": ("в","храм"), "Минск": ("в","Минск"), "граница": ("на","границу"), "работа": ("на","работу"), "магазин": ("в","магазин"),
 "вокзал": ("на","вокзал"), "Березино": ("в","Березино"), "рынок": ("на","рынок"), "аэропорт": ("в","аэропорт"),
 "литургия": ("на","литургию"), "Америка": ("в","Америку"), "Россия": ("в","Россию"), "почта": ("на","почту"), "таможня": ("на","таможню"),
 "музей": ("в","музей"), "Гомель": ("в","Гомель"), "море": ("на","море"), "деревня": ("в","деревню"), "площадь": ("на","площадь"),
 "Франция": ("во","Францию"), "очередь": ("в","очередь"),
 "программа": (None,"программу"), "файл": (None,"файл"), "кухня": ("на","кухню"),
 "Брест": ("в","Брест"), "ферма": ("на","ферму"), "песня": (None,"песню"),
 "коровник": ("в","коровник"), "офис": ("в","офис"), "корм": (None,"корм"),
 "концерт": ("на","концерт"), "письмо": (None,"письмо"), "икона": (None,"икону"),
}
MANUAL = {"Джексон": ("m","в","Джексоне","Джексон")}  # the city; the dictionary only has the surname
for w,(pr,acc) in ACC.items():
    forms = set()
    for q in M.parse(w):
        if q.tag.POS == "NOUN" and q.normal_form == w.lower() and "anim" not in q.tag:
            x = q.inflect({"accs","sing"});
            if x: forms.add(x.word)
    if w == "рыба": forms |= {"рыбу"}  # food reading; the dictionary marks рыба animate, accusative is рыбу either way
    if acc.lower() not in forms: errs.append("accusative %s: table %s, dict %s" % (w,acc,forms))
    if pr and w in T and T[w][1] != pr: errs.append("preposition differs between где/куда for %s" % w)
for w,(g,pr,loc,acc) in MANUAL.items():
    T.setdefault(w,(g,pr,loc)); ACC.setdefault(w,(pr,acc))
# Lesson 3: present tense. Every form shown in the lesson tables, checked against the dictionary.
PERS = ["1s","2s","3s","1p","2p","3p"]
PTAG = {"1s":{"1per","sing"},"2s":{"2per","sing"},"3s":{"3per","sing"},"1p":{"1per","plur"},"2p":{"2per","plur"},"3p":{"3per","plur"}}
def pres(inf, p):
    for q in M.parse(inf):
        if q.tag.POS == "INFN" and q.word == inf:
            x = q.inflect(PTAG[p] | {"pres","indc"})
            if x: return x.word
    return None
TABLE3 = {  # all six forms, or a dict of the persons shown
 "работать": "работаю работаешь работает работаем работаете работают", "читать": "читаю читаешь читает читаем читаете читают",
 "говорить": "говорю говоришь говорит говорим говорите говорят", "звонить": "звоню звонишь звонит звоним звоните звонят",
 "хотеть": "хочу хочешь хочет хотим хотите хотят",
 "учить": {"1s":"учу","2s":"учишь","3p":"учат"}, "слышать": {"1s":"слышу","2s":"слышишь","3p":"слышат"},
 "любить": {"1s":"люблю","2s":"любишь","3p":"любят"}, "готовить": {"1s":"готовлю","2s":"готовишь","3p":"готовят"},
 "ходить": {"1s":"хожу","2s":"ходишь","3p":"ходят"}, "видеть": {"1s":"вижу","2s":"видишь","3p":"видят"},
 "платить": {"1s":"плачу","2s":"платишь","3p":"платят"}, "просить": {"1s":"прошу","2s":"просишь","3p":"просят"},
 "жить": {"1s":"живу","2s":"живёшь","3s":"живёт","3p":"живут"}, "писать": {"1s":"пишу","2s":"пишешь","3p":"пишут"},
 "брать": {"1s":"беру","2s":"берёшь","3p":"берут"}, "пить": {"1s":"пью","2s":"пьёшь","3p":"пьют"},
 "искать": {"1s":"ищу","2s":"ищешь","3p":"ищут"}, "идти": {"1s":"иду","2s":"идёшь","3p":"идут"}, "ехать": {"1s":"еду","2s":"едешь","3p":"едут"},
 "стоять": {"2s":"стоишь"}, "спать": {"2s":"спишь"}, "уметь": {"1s":"умею","2s":"умеешь"},
}
# conjugation group claimed in the lesson (checked via the ты ending)
GROUP3 = {"работать":1,"читать":1,"делать":1,"знать":1,"понимать":1,"думать":1,"слушать":1,"отдыхать":1,"покупать":1,"гулять":1,"завтракать":1,"ужинать":1,
 "говорить":2,"звонить":2,"любить":2,"учить":2,"платить":2,"ходить":2,"смотреть":2,"видеть":2,"сидеть":2,"слышать":2,"стоять":2,"спать":2,"готовить":2,"просить":2,
 "жить":1,"пить":1,"писать":1,"брать":1,"искать":1,"идти":1,"ехать":1,"уметь":1,"хотеть":"mixed"}
for inf,forms in TABLE3.items():
    if isinstance(forms,str): forms = dict(zip(PERS, forms.split()))
    for p,f in forms.items():
        d = pres(inf,p)
        if d != f: errs.append("L3 table %s %s: lesson %s, dict %s" % (inf,p,f,d))
for inf,g in GROUP3.items():
    if g == "mixed":  # хотеть: 1st-conjugation singular, 2nd-conjugation plural
        if not (pres(inf,"2s").endswith("ешь") and pres(inf,"1p").endswith("им")): errs.append("L3 mixed group "+inf)
        continue
    t2 = pres(inf,"2s") or ""
    got = 2 if t2.endswith("ишь") else 1 if (t2.endswith("ешь") or t2.endswith("ёшь")) else None
    if got != g: errs.append("L3 group %s: lesson %s, dict ты-form %s" % (inf,g,t2))
PRON = {"я":"1s","ты":"2s","мы":"1p","вы":"2p","они":"3p","он":"3s","она":"3s"}
def nrm(x): return x.lower().replace("ё","е")
def check_l3(e):
    exp = pres(e["base"], e["p"])
    if exp != e["a"]: errs.append("L3 answer %s %s: %s, dict %s" % (e["s"],e["base"],e["a"],exp))
    toks = [w.strip("?,.!").lower() for w in e["s"].split()]
    ps = {PRON[w] for w in toks if w in PRON}
    if ps and ps != {e["p"]}: errs.append("L3 subject pronoun vs person: %s (%s)" % (e["s"],e["p"]))
    if not ps and e["p"] != "3s":
        plural_noun = False
        if e["p"] == "3p":
            for tok in toks:
                for q in M.parse(tok):
                    if q.tag.POS == "NOUN" and "nomn" in q.tag and "plur" in q.tag:
                        plural_noun = True
                        break
                if plural_noun: break
        if not plural_noun:
            errs.append("L3 noun subject should be 3s: "+e["s"])
    for d in e["d"]:
        if nrm(d) == nrm(e["a"]): errs.append("L3 distractor equals answer (ignoring ё): "+d)
    if e["base"] not in GROUP3: errs.append("L3 verb not covered by the lesson's groups: "+e["base"])

# Lesson 4: genitive. Every genitive form shown in the lesson, checked against the dictionary.
def gen(w):
    out = set()
    for q in M.parse(w):
        if q.tag.POS == "NOUN" and nrm(q.normal_form) == nrm(w) and "plur" not in q.tag and "Fixd" not in q.tag and "Infr" not in q.tag:  # skip indeclinable / informal readings (соль the note, интернет undeclined)
            x = q.inflect({"gent", "sing"})
            if x: out.add(x.word)
    if w == "время": out.add("времени")
    return out
def case_forms(w, case):
    out = set()
    for q in M.parse(w):
        if q.tag.POS == "NOUN" and nrm(q.normal_form) == nrm(w):
            for num in ("sing", "plur"):
                x = q.inflect({case, num})
                if x: out.add(x.word)
    return out
TABLE4 = {"брат":"брата","друг":"друга","сосед":"соседа","фермер":"фермера","Андрей":"Андрея","сарай":"сарая","учитель":"учителя",
 "сено":"сена","молоко":"молока","море":"моря","жена":"жены","сестра":"сестры","мама":"мамы","корова":"коровы","Таня":"Тани",
 "деревня":"деревни","церковь":"церкви","соль":"соли","подруга":"подруги","собака":"собаки","кошка":"кошки","дача":"дачи",
 "батюшка":"батюшки","курица":"курицы","папа":"папы","дедушка":"дедушки","трактор":"трактора","хлеб":"хлеба","служба":"службы",
 "интернет":"интернета","трава":"травы","время":"времени","сдача":"сдачи","виза":"визы","телефон":"телефона","рыба":"рыбы",
 "терминал":"терминала","дом":"дома","билет":"билета","вода":"воды","сосед":"соседа","храм":"храма",
 "компьютер":"компьютера","машина":"машины","индюк":"индюка","песня":"песни","ключ":"ключа",
 "пароль":"пароля","коза":"козы","коллега":"коллеги"}
for w,g in TABLE4.items():
    if g.lower() not in gen(w): errs.append("L4 genitive %s: lesson %s, dict %s" % (w,g,gen(w)))
PRONG = {"я":"меня","ты":"тебя","он":"него","она":"неё","мы":"нас","вы":"вас","они":"них"}
for pr,f in PRONG.items():
    if not any(q.normal_form == pr and "gent" in q.tag for q in M.parse(f)): errs.append("L4 pronoun genitive %s %s" % (pr,f))
def check_l4(e):
    w, a, k = e["w"], e["a"], e["k"]
    if k == "own" and w in PRONG:
        if a != PRONG[w]: errs.append("L4 A pronoun %s: %s" % (w,a))
        if any(nrm(d) == nrm(a) for d in e["d"]): errs.append("L4 distractor = answer "+e["s"])
        return
    G = gen(w)
    if e["part"] in ("A", "B"):
        if a.lower() not in G: errs.append("L4 %s answer %s: %s, dict %s" % (e["part"],w,a,G))
        for d in e["d"]:
            if d.lower() in G: errs.append("L4 distractor is a correct genitive: %s (%s)" % (d,e["s"]))
        if k == "own" and not e["s"].startswith("У ___"): errs.append("L4 A sentence shape "+e["s"])
        if k == "not" and "нет" not in e["s"]: errs.append("L4 B lacks нет "+e["s"])
        return
    g1 = sorted(G)[0]
    right = {"have": "есть " + w, "not": "нет " + g1}
    if a != right[k]: errs.append("L4 C answer %s: %s (expected %s)" % (w,a,right[k]))
    other = right["not" if k == "have" else "have"]
    if other not in e["d"]: errs.append("L4 C missing the opposite as a distractor: "+e["s"])
    ok_forms = {"есть " + w} | {"нет " + x for x in G}
    for d in e["d"]:
        if d != other and d in ok_forms: errs.append("L4 C distractor is grammatical: "+d)
        pre, form = d.split(" ", 1)
        if pre == "нет" and form.lower() in G and d != other: errs.append("L4 C distractor genitive "+d)
        if pre == "есть" and form != w and form.lower() in G and form.lower() in case_forms(w,"nomn"): errs.append("L4 C distractor also a plural nominative (grammatical): "+d)
    if "нет" in e["s"] or "есть" in e["s"]: errs.append("L4 C sentence gives away the answer: "+e["s"])

# Lesson 5: past tense.
PG = {"m": {"past","sing","masc"}, "f": {"past","sing","femn"}, "n": {"past","sing","neut"}, "pl": {"past","plur"}}
def past(inf, g):
    for q in M.parse(inf):
        if q.tag.POS == "INFN" and q.word == inf:
            x = q.inflect(PG[g] | {"indc"})
            if x: return x.word
    return None
TABLE5 = {
 "работать": "работал работала работало работали", "говорить": "говорил говорила говорило говорили", "быть": "был была было были",
 "идти": "шёл шла шло шли", "есть": "ел ела ело ели", "мочь": "мог могла могло могли", "пасти": "пас пасла пасло пасли",
 "учиться": {"m":"учился","f":"училась","pl":"учились"}, "молиться": {"m":"молился","f":"молилась","pl":"молились"},
 "любить": {"m":"любил"}, "писать": {"m":"писал"}, "жить": {"m":"жил"}, "хотеть": {"m":"хотел"}, "ходить": {"m":"ходил"},
}
for inf,forms in TABLE5.items():
    if isinstance(forms,str): forms = dict(zip(["m","f","n","pl"], forms.split()))
    for g,f in forms.items():
        d = past(inf,g)
        if not d or nrm(d) != nrm(f): errs.append("L5 table %s %s: lesson %s, dict %s" % (inf,g,f,d))
SUBJ_G = {"Андрей":"m","Таня":"f","мы":"pl","вы":"pl"}
def subj_g(w):
    if w in SUBJ_G: return SUBJ_G[w]
    for q in M.parse(w):
        if q.tag.POS == "NOUN" and "nomn" in q.tag:
            if "plur" in q.tag: return "pl"
            return {"masc":"m","femn":"f","neut":"n","ms-f":"m"}.get(q.tag.gender)
    return None
MASC_A = {"батюшка"}  # masculine by meaning (Lesson 1)
def check_l5(e):
    exp = past(e["base"], e["g"])
    if not exp or nrm(exp) != nrm(e["a"]): errs.append("L5 answer %s %s %s: %s, dict %s" % (e["s"],e["base"],e["g"],e["a"],exp))
    if e["subj"] is None:
        if e["g"] != "n": errs.append("L5 impersonal not neuter: "+e["s"])
    else:
        sg = "m" if e["subj"] in MASC_A else subj_g(e["subj"])
        if sg != e["g"]: errs.append("L5 subject %s is %s, item says %s: %s" % (e["subj"],sg,e["g"],e["s"]))
        if e["subj"].lower() not in e["s"].lower(): errs.append("L5 subject not in sentence: "+e["s"])
    if e["base"] == "быть" and " не ___" in e["s"] and e["a"] != "было": errs.append("L5 не ___ + genitive must be было: "+e["s"])
    for d in e["d"]:
        if nrm(d) == nrm(e["a"]): errs.append("L5 distractor = answer: "+d)
    if e["part"] in ("A","B"):  # distractors are the other three real forms of the same verb
        others = {nrm(past(e["base"],g) or "") for g in PG if g != e["g"]}
        if {nrm(d) for d in e["d"]} != others: errs.append("L5 distractors not the other three forms: %s %s" % (e["d"],others))


# Review 1: mixed items from lessons 1–4.
GENDER = {"компьютер":"masculine","письмо":"neuter","песня":"feminine","лошадь":"feminine"}
def check_r1(e):
    k, a = e["k"], e["a"]
    if k == "gender":
        w = e["s"].split(" — ")[0]
        if GENDER.get(w) != a: errs.append("R1 gender %s: %s" % (w,a))
        return
    if k == "where":
        w = e["base"]
        if T[w][2] != a: errs.append("R1 where %s: %s vs %s" % (w,a,T[w][2]))
        pre = e["s"].split("___")[0].split()[-1]
        if pre != T[w][1]: errs.append("R1 prep in sentence %s: %s vs %s" % (w,pre,T[w][1]))
        return
    if k == "ven":
        w = e["base"].split(" · ")[0]
        exp = T[w][1]+" "+T[w][2]
        if a != exp: errs.append("R1 ven %s: %s vs %s" % (w,a,exp))
        return
    if k == "acc":
        w = e["base"]
        if ACC[w][1] != a: errs.append("R1 acc %s: %s vs %s" % (w,a,ACC[w][1]))
        return
    if k == "whereto":
        w = e["base"].split(" · ")[0]
        exp = ACC[w][0]+" "+ACC[w][1]
        if a != exp: errs.append("R1 whereto %s: %s vs %s" % (w,a,exp))
        # the где? form should be among the distractors when it differs
        if w in T and T[w][1] and T[w][2]:
            other = T[w][1]+" "+T[w][2]
            if other != exp and other not in e["d"]:
                errs.append("R1 whereto missing где? distractor %s" % e["s"])
        return
    if k == "verb":
        check_l3(e)
        return
    if k in ("own","not","have","notc"):
        e2 = dict(e)
        e2["k"] = "not" if k == "notc" else k
        e2["part"] = {"own":"A","not":"B","have":"C","notc":"C"}[k]
        check_l4(e2)
        return
    errs.append("R1 unknown k %s: %s" % (k,e["s"]))

# Lesson 6: animate accusative.
PRONA = {"я":"меня","ты":"тебя","он":"его","она":"её","оно":"его","мы":"нас","вы":"вас","они":"их"}
def acc_set(w, num, prefer_anim=None):
    out=set()
    for q in M.parse(w):
        if q.tag.POS != "NOUN": continue
        if nrm(q.normal_form) != nrm(w) and not (num=="plur" and nrm(q.normal_form) in {nrm(w)}):
            # allow asking from the lemma only
            if nrm(q.normal_form) != nrm(w): continue
        if prefer_anim is True and "anim" not in q.tag: continue
        if prefer_anim is False and "anim" in q.tag: continue
        if "Geox" in q.tag or "Infr" in q.tag or "Fixd" in q.tag: continue
        x = q.inflect({"accs", num})
        if x: out.add(x.word)
    return out
def check_l6(e):
    w, a, k = e["w"], e["a"], e["k"]
    if k == "pron":
        if nrm(a) != nrm(PRONA[w]): errs.append("L6 pronoun %s: %s vs %s" % (w,a,PRONA[w]))
        for d in e["d"]:
            if nrm(d)==nrm(a): errs.append("L6 distractor = answer "+e["s"])
        return
    num = "plur" if k.endswith("_pl") else "sing"
    prefer = False if k.startswith("inan") else True if k in ("anim_m","anim_pl","fem","masc_a","soft_f") else None
    forms = acc_set(w, num, prefer if k.startswith("inan") or k.startswith("anim") else None)
    # For fem / masc_a / soft_f, take the obvious noun reading (animate if there is one for people/animals).
    if k in ("fem","masc_a","soft_f","inan_m","inan_pl","anim_m","anim_pl"):
        if not forms:
            forms = acc_set(w, num, None)
        if nrm(a) not in {nrm(x) for x in forms}:
            errs.append("L6 answer %s %s: %s, dict %s" % (k,w,a,forms))
    for d in e["d"]:
        if nrm(d)==nrm(a): errs.append("L6 distractor = answer "+e["s"])

# Lesson 7: dative.
PROND = {"я":"мне","ты":"тебе","он":"ему","она":"ей","оно":"ему","мы":"нам","вы":"вам","они":"им"}
PROND_PREP = {"он":"нему","она":"ней","они":"ним"}
def dat_set(w, num):
    out=set()
    lemmas = {nrm(w)}
    # дети / люди are the plural lemmas of ребёнок / человек
    if nrm(w)=="дети": lemmas.add("ребёнок"); lemmas.add("ребенок")
    if nrm(w)=="люди": lemmas.add("человек")
    for q in M.parse(w):
        if q.tag.POS != "NOUN": continue
        x = q.inflect({"datv", num})
        if x: out.add(x.word)
    if not out:
        for lemma in lemmas:
            for q in M.parse(lemma):
                if q.tag.POS != "NOUN": continue
                x = q.inflect({"datv", num})
                if x: out.add(x.word)
    return out
def year_word(n):
    if 11 <= (n % 100) <= 14: return "лет"
    r = n % 10
    if r == 1: return "год"
    if r in (2,3,4): return "года"
    return "лет"
def check_l7(e):
    w, a, k = e["w"], e["a"], e["k"]
    if k in ("pron","age_pron"):
        exp = PROND[w]
        if nrm(a) != nrm(exp): errs.append("L7 pronoun %s: %s vs %s" % (w,a,exp))
        return
    if k == "k_pron":
        exp = PROND_PREP[w]
        if nrm(a) != nrm(exp): errs.append("L7 prep pronoun %s: %s vs %s" % (w,a,exp))
        return
    if k == "nslike":
        g = e.get("g","sg")
        exp = past if False else None
        tag = {"3per","pres","plur" if g=="pl" else "sing","indc"}
        got=None
        for q in M.parse("нравиться"):
            if q.tag.POS=="INFN":
                x=q.inflect(tag)
                if x: got=x.word; break
        if not got or nrm(got)!=nrm(a): errs.append("L7 нравиться %s: %s vs %s" % (e["s"],a,got))
        return
    if k == "age_unit":
        exp = year_word(e["n"])
        if a != exp: errs.append("L7 year word n=%s: %s vs %s" % (e["n"],a,exp))
        return
    num = "plur" if k in ("dat_pl","po") and ("plural" in e.get("base","") or e.get("base") in ("дети","люди") or k=="dat_pl" and e["base"].endswith("plural") or e.get("base") in ("суббота · plural","воскресенье · plural","корова · plural","курица · plural")) else "sing"
    if k == "dat_pl" or (k=="po" and "plural" in e.get("base","")):
        num="plur"
    elif k in ("dat_sg","k") or (k=="po" and "plural" not in e.get("base","")):
        num="sing"
    forms = dat_set(w, num)
    if nrm(a) not in {nrm(x) for x in forms}:
        errs.append("L7 answer %s %s %s: %s, dict %s" % (k,w,num,a,forms))
    for d in e["d"]:
        if nrm(d)==nrm(a): errs.append("L7 distractor = answer "+e["s"])

# Lesson 9: genitive plural (all dictionary readings, so стульев / кур / человек count), genitive / instrumental after a preposition,
# нравится / нравятся agreement, and the кроме / напротив / перед choice checked against the case of the next word.
def l9_forms(w, tags):
    out = set()
    for q in M.parse(w):
        if q.tag.POS != "NOUN": continue
        if nrm(q.normal_form) != nrm(w) and nrm(q.word) != nrm(w): continue
        for f in q.lexeme:
            if tags <= f.tag.grammemes: out.add(nrm(f.word))
    return out
# Trap distractors the dictionary also lists, but that are wrong in these sentences (explained in Step 5):
# годов (decades only, not after a number), стулов (non-standard), человеков (colloquial/jocular), людей vs человек by context.
L9_TRAP = {("год","годов"), ("стул","стулов"), ("человек","человеков"), ("человек","людей"), ("человек","человек")}
L9_GPL_EXTRA = {"куры": {"кур", "куриц"}}  # farm plural of курица (dictionary lemma кура); textbook куриц
def check_l9(e):
    k, a, w = e["k"], e["a"], e["w"]
    if k in ("gpl", "gpl_num"):
        forms = L9_GPL_EXTRA.get(w) or l9_forms(w, {"gent", "plur"})
        if w == "человек" and k == "gpl" and nrm(a) != "людей": errs.append("L9 много + людей expected: "+e["s"])
        if k == "gpl_num" and nrm(a) != nrm(w): errs.append("L9 counting form expected: "+e["s"])
    elif k == "gen":
        num = "plur" if "plural" in e["base"] else "sing"
        forms = l9_forms(w, {"gent", num})
    elif k == "ins":
        forms = l9_forms(w, {"ablt", "sing"})
    elif k == "nslike":
        num = "plur" if e.get("g") == "pl" else "sing"
        forms = {nrm(x.word) for q in M.parse(w) if q.tag.POS == "INFN" for x in [q.inflect({"3per", num, "pres", "indc"})] if x}
    elif k == "prep":
        after = e["s"].split("___")[1].split()[0].strip(".,!?")
        tags = set()
        for q in M.parse(after): tags |= set(q.tag.grammemes)
        exp_ins = "ablt" in tags and "gent" not in tags
        if exp_ins != (nrm(a) == "перед"): errs.append("L9 preposition vs case of %s: %s" % (after, e["s"]))
        if nrm(a) not in ("кроме", "напротив", "перед"): errs.append("L9 prep answer: "+a)
        forms = {nrm(a)}
    else:
        errs.append("L9 unknown k %s: %s" % (k, e["s"])); return
    if nrm(a) not in forms: errs.append("L9 answer %s %s: %s, dict %s" % (k, w, a, sorted(forms)))
    for d in e["d"]:
        if nrm(d) == nrm(a): errs.append("L9 distractor = answer "+e["s"])
        if k != "prep" and nrm(d) in forms and (w, nrm(d)) not in L9_TRAP: errs.append("L9 distractor is also a right form %s: %s" % (d, e["s"]))
    for x in e.get("alt", []):
        if nrm(x) not in forms: errs.append("L9 alt not a real form: "+x)

n = 0
for lid,les in L["lessons"].items():
    for e in les["exercises"]:
        n += 1
        opts = [e["a"]] + e["d"]
        if len(set(opts)) != (3 if (lid == "L1" and e["part"] == "A") else 4): errs.append("options not distinct / wrong count: %s" % opts)
        if not e.get("ex"): errs.append("no explanation: "+e["s"])
        if e["s"].count("___") != 1: errs.append("blank: "+e["s"])
        if not re.search(r"Step", e["ex"]): errs.append("explanation lacks a rule pointer: "+e["s"])
        if lid == "L2":
            w = e["base"].split(" · ")[0]
            if e["part"] == "A":
                if ACC[w][1] != e["a"]: errs.append("L2 A answer %s %s" % (w,e["a"]))
            elif e["part"] == "B":
                if e["a"] != ACC[w][0]+" "+ACC[w][1]: errs.append("L2 B answer %s %s" % (w,e["a"]))
            else:
                k = e.get("k")
                exp = {"where": (T.get(w,("",None,None))[1] or "")+" "+(T.get(w,("",None,None))[2] or ""),
                       "whereto": ACC.get(w,("",""))[0]+" "+ACC.get(w,("",""))[1], "home": "домой"}.get(k)
                if e["a"] != exp: errs.append("L2 C answer %s %s (expected %s)" % (w,e["a"],exp))
                # the other case's form should be among the distractors so the item tests где vs куда
                other = {"where": "whereto", "whereto": "where", "home": None}[k]
                if other:
                    o = {"where": T[w][1]+" "+T[w][2], "whereto": ACC[w][0]+" "+ACC[w][1]}[other]
                    if o not in e["d"]: errs.append("L2 C missing other-case distractor %s" % e["s"])
            for d in e["d"]:
                if d == e["a"]: errs.append("distractor equals answer "+d)
            continue
        if lid == "L3":
            check_l3(e)
            continue
        if lid == "L4":
            check_l4(e)
            continue
        if lid == "L5":
            check_l5(e)
            continue
        if lid == "R1":
            check_r1(e)
            continue
        if lid == "L6":
            check_l6(e)
            continue
        if lid == "L7":
            check_l7(e)
            continue
        if lid == "L9":
            check_l9(e)
            continue
        if e["part"] == "A":
            w = e["s"].split(" — ")[0]
            if GN[e["a"]] != T[w][0]: errs.append("gender answer "+w)
        elif e["part"] == "B":
            w = e["base"]
            if T[w][2] != e["a"]: errs.append("prep answer %s %s" % (w,e["a"]))
            pre = e["s"].split("___")[0].split()[-1]
            if pre != T[w][1]: errs.append("prep in sentence %s: %s vs %s" % (w,pre,T[w][1]))
        else:
            w = e["base"].split(" · ")[0]
            if e["a"] != T[w][1]+" "+T[w][2]: errs.append("C answer %s %s" % (w,e["a"]))
            # every distractor must differ from the answer in preposition or form, and use a wrong form if it uses the real noun form
            for d in e["d"]:
                pr, fo = d.split(" ",1)
                if pr == T[w][1] and fo == T[w][2]: errs.append("distractor equals answer "+d)
# context words in sentences/glosses: check they exist
words = set()
blob = json.dumps(L, ensure_ascii=False)
for m in re.finditer(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)?", blob):
    words.add(m.group(0))
skip_wrong = set()
for les in L["lessons"].values():
    for e in les["exercises"]:
        for d in e["d"]:
            for x in d.split(): skip_wrong.add(x)
unknown = sorted(w for w in words if w not in skip_wrong and not M.word_is_known(w.lower()) and not w.startswith("-") and len(w) > 1)
print("table words:", len(T), " exercises:", n)
print("unknown words (check by hand):", unknown)
# report distractors that are real words (fine, but listed for review)
real = sorted({x for x in skip_wrong if M.word_is_known(x.lower()) and x not in ("в","на","во")})
print("distractor tokens that are real words (wrong here, but real):", real)
print("ERRORS:", len(errs)); [print("  ",x) for x in errs]
sys.exit(1 if errs else 0)
