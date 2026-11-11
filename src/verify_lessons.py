# Checks lessons.json: explicit forms table vs OpenCorpora (pymorphy3), every exercise answer, every Cyrillic word.
# Run with: /tmp/morph/bin/python src/verify_lessons.py
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
    if not ps and e["p"] != "3s": errs.append("L3 noun subject should be 3s: "+e["s"])
    for d in e["d"]:
        if nrm(d) == nrm(e["a"]): errs.append("L3 distractor equals answer (ignoring ё): "+d)
    if e["base"] not in GROUP3: errs.append("L3 verb not covered by the lesson's groups: "+e["base"])

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
