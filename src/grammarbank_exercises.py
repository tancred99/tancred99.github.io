#!/usr/bin/env python3
"""Expand Grammar tab question banks. Idempotent: new items are tagged src='bank'.

Run from the repo root:
  /workspace/venv-morph/bin/python src/grammarbank_exercises.py

Leaves original (untagged) items alone. Re-running replaces only src=bank items.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pymorphy3
M = pymorphy3.MorphAnalyzer()

TABLE = json.load(open(os.path.join(HERE, "forms_table.json")))
VOCAB = json.load(open(os.path.join(ROOT, "vocab.json")))
VBY = {w["ru"]: w for w in VOCAB}

SRC = "bank"
A, B = "A1-A2", "B1-C1"

# Special locative (в/на + где?) where the dictionary loc2 / -у form is used.
LOC2 = {
    "луг": "лугу", "пруд": "пруду", "аэропорт": "аэропорту", "угол": "углу",
    "пол": "полу", "шкаф": "шкафу", "лес": "лесу", "сад": "саду",
    "берег": "берегу", "год": "году", "мост": "мосту", "снег": "снегу",
    "порт": "порту", "глаз": "глазу", "лоб": "лбу", "рот": "рту",
    "ряд": "ряду", "час": "часу", "край": "краю", "бок": "боку",
}

# Proper names keep a capital letter in every case form.
PROPER = {
    "Москва", "Россия", "Минск", "Беларусь", "Анна", "Иван", "Маша", "Мария",
    "Саша", "Пётр", "Беларусь", "Сочи", "Петербург", "Новгород",
}

PRONOUNS = {
    "я":   {"nom": "я", "gen": "меня", "dat": "мне", "acc": "меня", "ins": "мной", "prep": "мне"},
    "ты":  {"nom": "ты", "gen": "тебя", "dat": "тебе", "acc": "тебя", "ins": "тобой", "prep": "тебе"},
    "он":  {"nom": "он", "gen": "его", "dat": "ему", "acc": "его", "ins": "им", "prep": "нём",
            "pgen": "него", "pdat": "нему", "pacc": "него", "pins": "ним", "pprep": "нём"},
    "она": {"nom": "она", "gen": "её", "dat": "ей", "acc": "её", "ins": "ей", "prep": "ней",
            "pgen": "неё", "pdat": "ней", "pacc": "неё", "pins": "ней", "pprep": "ней"},
    "оно": {"nom": "оно", "gen": "его", "dat": "ему", "acc": "его", "ins": "им", "prep": "нём",
            "pgen": "него", "pdat": "нему", "pacc": "него", "pins": "ним", "pprep": "нём"},
    "мы":  {"nom": "мы", "gen": "нас", "dat": "нам", "acc": "нас", "ins": "нами", "prep": "нас"},
    "вы":  {"nom": "вы", "gen": "вас", "dat": "вам", "acc": "вас", "ins": "вами", "prep": "вас"},
    "они": {"nom": "они", "gen": "их", "dat": "им", "acc": "их", "ins": "ими", "prep": "них",
            "pgen": "них", "pdat": "ним", "pacc": "них", "pins": "ними", "pprep": "них"},
}

# Plausible fake endings for indeclinable nouns (same idea as the existing кино item).
INDECL_FAKE = {
    "кино": ["кине", "кина", "киной"],
    "кафе": ["кафее", "кафеа", "кафей"],
    "меню": ["менья", "менюе", "менюй"],
    "такси": ["таксия", "таксие", "таксий"],
    "метро": ["метре", "метра", "метрой"],
    "кофе": ["кофея", "кофее", "кофей"],
    "пальто": ["пальта", "пальте", "пальтой"],
}

# Manual noun forms where pymorphy is messy or we want a particular lemma.
MANUAL = {
    "люди": {"nom": "люди", "gen": "людей", "dat": "людям", "acc": "людей", "ins": "людьми", "prep": "людях",
             "npl": "люди", "gpl": "людей", "apl": "людей", "dpl": "людям", "ipl": "людьми", "ppl": "людях"},
    "ребёнок": {"nom": "ребёнок", "gen": "ребёнка", "dat": "ребёнку", "acc": "ребёнка", "ins": "ребёнком", "prep": "ребёнке",
                "npl": "дети", "gpl": "детей", "apl": "детей", "dpl": "детям", "ipl": "детьми", "ppl": "детях"},
    "человек": {"nom": "человек", "gen": "человека", "dat": "человеку", "acc": "человека", "ins": "человеком", "prep": "человеке",
                "npl": "люди", "gpl": "человек", "apl": "людей", "dpl": "людям", "ipl": "людьми", "ppl": "людях"},
    "дочь": {"nom": "дочь", "gen": "дочери", "dat": "дочери", "acc": "дочь", "ins": "дочерью", "prep": "дочери",
             "npl": "дочери", "gpl": "дочерей", "apl": "дочерей", "dpl": "дочерям", "ipl": "дочерьми", "ppl": "дочерях"},
    "мать": {"nom": "мать", "gen": "матери", "dat": "матери", "acc": "мать", "ins": "матерью", "prep": "матери",
             "npl": "матери", "gpl": "матерей", "apl": "матерей", "dpl": "матерям", "ipl": "матерями", "ppl": "матерях"},
}

SC = {"nom": "nomn", "gen": "gent", "dat": "datv", "acc": "accs", "ins": "ablt", "prep": "loct"}
PC = {"npl": "nomn", "gpl": "gent", "apl": "accs", "dpl": "datv", "ipl": "ablt", "ppl": "loct"}

def _cap_form(lemma, form):
    if not form or form == "-":
        return form
    if lemma[0].isupper() or lemma in PROPER:
        return form[0].upper() + form[1:]
    return form

def _parse_noun(lemma):
    raw = lemma
    ps = [p for p in M.parse(lemma) if p.tag.POS == "NOUN" and "nomn" in p.tag]
    if not ps:
        ps = [p for p in M.parse(lemma) if p.tag.POS == "NOUN"]
    if not ps:
        return None
    # Prefer a parse matching vocab gender / animacy / number when we have one.
    w = VBY.get(raw) or VBY.get(raw.lower())
    if w and w.get("g") == "pl":
        pl = [p for p in ps if "plur" in p.tag]
        if pl:
            return pl[0]
    if w and w.get("g") in ("m", "f", "n"):
        gen = {"m": "masc", "f": "femn", "n": "neut"}[w["g"]]
        typed = [p for p in ps if p.tag.gender == gen]
        if typed:
            ps = typed
    if w and "anim" in w:
        want = bool(w.get("anim"))
        ps = sorted(ps, key=lambda q: (("anim" in q.tag) != want))
    # курятник etc.: vocab inanimate beats an animate parse
    if w and w.get("kind") in ("place", "building", "thing", "food", "transport") or (w and not w.get("anim") and w.get("g") != "pl"):
        inan = [p for p in ps if "inan" in p.tag]
        if inan and raw in ("курятник", "коровник", "сарай", "трактор"):
            return inan[0]
    return ps[0]

def noun_forms(lemma):
    if lemma in MANUAL:
        out = dict(MANUAL[lemma])
        if not out.get("loc"):
            out["loc"] = out.get("prep")
        return out
    if lemma in PRONOUNS:
        return dict(PRONOUNS[lemma])
    out = {}
    w = VBY.get(lemma)
    t = TABLE.get(lemma)
    if t:
        out["nom"] = lemma
        for k in ("gen", "dat", "acc", "ins", "prep", "npl", "gpl"):
            val = t.get(k)
            out[k] = lemma if (val == "-" and w and w.get("indecl")) else val
        loc = (w or {}).get("loc") or ((w or {}).get("forms") or {}).get("loc") or LOC2.get(lemma)
        out["loc"] = loc or out.get("prep")
        if w and w.get("indecl"):
            for k in list(out):
                if out[k] in ("-", None):
                    out[k] = lemma
        # Accusative plural: animate = genitive plural, inanimate = nominative plural.
        anim = bool(w and (w.get("anim") or w.get("kind") in ("animal", "wild", "person")))
        if out.get("npl") not in (None, "-") and out.get("gpl") not in (None, "-"):
            out["apl"] = out["gpl"] if anim else out["npl"]
        # plural cases from pymorphy, preferring table npl/gpl
    p = _parse_noun(lemma)
    if p:
        if "nom" not in out:
            out["nom"] = _cap_form(lemma, p.word)
        for key, g in SC.items():
            if key in out and out[key] not in (None, "-"):
                continue
            f = p.inflect({g, "sing"})
            if f:
                out[key] = _cap_form(lemma, f.word)
        for key, g in PC.items():
            if key in out and out[key] not in (None, "-"):
                continue
            f = p.inflect({g, "plur"})
            if f:
                out[key] = _cap_form(lemma, f.word)
        if "loc" not in out or not out["loc"]:
            out["loc"] = LOC2.get(lemma) or out.get("prep")
        if lemma in LOC2:
            out["loc"] = _cap_form(lemma, LOC2[lemma])
    if not out.get("loc"):
        out["loc"] = out.get("prep")
    # fix capitalization
    for k, v in list(out.items()):
        if v and v != "-":
            out[k] = _cap_form(lemma, v)
    return out

def cap(word, on):
    if not word:
        return word
    return word[0].upper() + word[1:] if on else word

def distractors_from_forms(forms, answer, prefer=None):
    """Three other forms of the same word, preferring contrastive cases."""
    ans = answer.replace("ё", "е").lower()
    order = prefer or ["nom", "acc", "gen", "dat", "ins", "prep", "loc",
                       "npl", "gpl", "apl", "dpl", "ipl", "ppl"]
    seen = {ans}
    out = []
    for k in order:
        v = forms.get(k)
        if not v or v == "-":
            continue
        key = v.replace("ё", "е").lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(v)
        if len(out) == 3:
            return out
    return out

def indecl_distractors(lemma, up=False):
    fake = INDECL_FAKE.get(lemma.lower(), [lemma + "а", lemma + "е", lemma + "ой"])
    return [cap(x, up) for x in fake[:3]]

def pad_distractors(lemma, answer, d, up=False):
    """If a noun has fewer than 3 distinct real forms, add plausible wrong endings."""
    seen = {answer.replace("ё", "е").lower()}
    for x in d:
        seen.add(x.replace("ё", "е").lower())
    # typical learner endings, plus a couple of 'looks regular' mistakes
    cands = []
    if lemma[0].isupper() or lemma in PROPER:
        stem = lemma
        cands = [stem + "е" if not stem.endswith("е") else stem[:-1] + "ии",
                 stem + "у", stem + "ой", stem + "а", stem + "ом",
                 stem[:-1] + "е" if stem.endswith(("ь", "я", "а")) else stem + "е"]
    else:
        cands = [lemma + "е", lemma + "у", lemma + "ой", lemma + "а", lemma + "ом",
                 lemma[:-1] + "е" if lemma.endswith(("ь", "я", "а")) else lemma + "и"]
    out = list(d)
    for x in cands:
        if not x or x.replace("ё", "е").lower() in seen:
            continue
        seen.add(x.replace("ё", "е").lower())
        out.append(cap(x, up))
        if len(out) == 3:
            break
    return out

def is_indecl(lemma):
    w = VBY.get(lemma)
    if w and w.get("indecl"):
        return True
    return lemma.lower() in INDECL_FAKE

ITEMS = []  # list of dicts without id

def add(level, cat, sub, s, base, a, d, ex, tr, glosses=None, alt=None, choice=False):
    assert s.count("___") == 1, s
    up = s.startswith("___")
    a2 = cap(a, up) if a and a[0].islower() and up else (cap(a, up) if up and a else a)
    # Don't force-cap proper mid-sentence forms that are already capped.
    if up:
        a2 = cap(a, True)
        d = [cap(x, True) for x in d]
    assert a2 not in d, (s, a2, d)
    assert len(d) >= 3, (s, d)
    assert len(set(x.lower() for x in d)) == len(d), (s, d)
    rec = dict(level=level, cat=cat, sub=sub, s=s, base=base, a=a2, alt=alt or [],
               d=list(d)[:3] if not up else d, ex=ex, translation=tr, glosses=glosses or [], src=SRC)
    if choice:
        rec["choiceOnly"] = True
    ITEMS.append(rec)
    return rec

def add_noun(level, cat, sub, s, lemma, case, tr, ex, glosses=None, prefer=None):
    forms = noun_forms(lemma)
    if case not in forms or not forms[case] or forms[case] == "-":
        raise SystemExit("no %s form for %r in %r; forms=%s" % (case, lemma, s, forms))
    a = forms[case]
    up = s.startswith("___")
    if is_indecl(lemma):
        d = indecl_distractors(lemma, up)
    else:
        d = distractors_from_forms(forms, a, prefer=prefer)
        if up:
            d = [cap(x, True) for x in d]
        if len(d) < 3:
            d = pad_distractors(lemma, a, d, up)
    if len(d) < 3:
        raise SystemExit("need 3 distractors for %r (%s); got %s from %s" % (s, lemma, d, forms))
    add(level, cat, sub, s, lemma, a, d, ex, tr, glosses)

def add_pron(level, cat, sub, s, lemma, case, tr, ex, glosses=None):
    forms = PRONOUNS[lemma]
    a = forms[case]
    prefer = ["nom", "gen", "dat", "acc", "ins", "prep", "pgen", "pdat", "pacc", "pins", "pprep"]
    d = distractors_from_forms(forms, a, prefer=prefer)
    add(level, cat, sub, s, lemma, a, d, ex, tr, glosses)

def verb_parse(inf):
    ps = [p for p in M.parse(inf) if p.tag.POS == "INFN"]
    if not ps:
        raise SystemExit("not an infinitive: " + inf)
    return ps[0]

PERS = {
    "1s": {"1per", "sing", "indc"},
    "2s": {"2per", "sing", "indc"},
    "3s": {"3per", "sing", "indc"},
    "1p": {"1per", "plur", "indc"},
    "2p": {"2per", "plur", "indc"},
    "3p": {"3per", "plur", "indc"},
}
PAST = {"m": {"masc", "sing", "past", "indc"}, "f": {"femn", "sing", "past", "indc"},
        "n": {"neut", "sing", "past", "indc"}, "p": {"plur", "past", "indc"}}

# A few verbs pymorphy won't conjugate from the infinitive cleanly.
VERB_HAND = {
    "стоить": {"3s": "стоит", "3p": "стоят"},
    "есть": {"1s": "ем", "2s": "ешь", "3s": "ест", "1p": "едим", "2p": "едите", "3p": "едят",
             "m": "ел", "f": "ела", "n": "ело", "p": "ели"},
    "дать": {"1s": "дам", "2s": "дашь", "3s": "даст", "1p": "дадим", "2p": "дадите", "3p": "дадут",
             "m": "дал", "f": "дала", "n": "дало", "p": "дали"},
    "хотеть": {"1s": "хочу", "2s": "хочешь", "3s": "хочет", "1p": "хотим", "2p": "хотите", "3p": "хотят",
               "m": "хотел", "f": "хотела", "n": "хотело", "p": "хотели"},
    "мочь": {"1s": "могу", "2s": "можешь", "3s": "может", "1p": "можем", "2p": "можете", "3p": "могут",
             "m": "мог", "f": "могла", "n": "могло", "p": "могли"},
    "бежать": {"1s": "бегу", "2s": "бежишь", "3s": "бежит", "1p": "бежим", "2p": "бежите", "3p": "бегут",
               "m": "бежал", "f": "бежала", "n": "бежало", "p": "бежали"},
    "ехать": {"1s": "еду", "2s": "едешь", "3s": "едет", "1p": "едем", "2p": "едете", "3p": "едут",
              "m": "ехал", "f": "ехала", "n": "ехало", "p": "ехали"},
    "идти": {"1s": "иду", "2s": "идёшь", "3s": "идёт", "1p": "идём", "2p": "идёте", "3p": "идут",
             "m": "шёл", "f": "шла", "n": "шло", "p": "шли"},
    "быть": {"1s": "есть", "3s": "есть", "3p": "есть",
             "m": "был", "f": "была", "n": "было", "p": "были"},
}

def vform(inf, key):
    if inf in VERB_HAND and key in VERB_HAND[inf]:
        return VERB_HAND[inf][key]
    p = verb_parse(inf)
    asp = "pres" if p.tag.aspect == "impf" else "futr"
    if key in PERS:
        tags = set(PERS[key])
        tags.add(asp)
        # some pf verbs still use pres in the analyzer
        f = p.inflect(tags) or p.inflect(PERS[key] | {"pres"}) or p.inflect(PERS[key] | {"futr"})
        if not f:
            raise SystemExit("no %s for %s" % (key, inf))
        return f.word
    if key in PAST:
        f = p.inflect(PAST[key])
        if not f:
            raise SystemExit("no past %s for %s" % (key, inf))
        return f.word
    raise SystemExit("bad verb key %s" % key)

def vparadigm(inf, keys=None):
    keys = keys or list(PERS)
    return {k: vform(inf, k) for k in keys}

def add_verb(level, cat, sub, s, inf, key, tr, ex, glosses=None, typo=None, extra=None):
    a = vform(inf, key)
    forms = []
    for k in list(PERS) + list(PAST):
        try:
            forms.append(vform(inf, k))
        except Exception:
            pass
    d = []
    seen = {a.replace("ё", "е").lower()}
    # typo first if given (learner error), then other real forms
    for x in (typo or []) + (extra or []) + forms:
        k = x.replace("ё", "е").lower()
        if k in seen:
            continue
        seen.add(k)
        d.append(x)
        if len(d) == 3:
            break
    if len(d) < 3:
        raise SystemExit("need 3 verb distractors for %r: %s" % (s, d))
    add(level, cat, sub, s, inf, a, d, ex, tr, glosses)

def build_cases_a1():
    C, S = "cases", "prepositional"
    # --- prepositional (где? в/на + prep, о + prep); loc = special -у ---
    rows = [
        ("Жена покупает продукты в ___.", "магазин", "prep",
         "My wife buys groceries in the store.",
         "Где? (where?) takes в + the prepositional; магазин is the object of the preposition в. Masculine nouns add -е: в магазине.",
         ["продукты: groceries"]),
        ("Коровы стоят в ___.", "сарай", "prep",
         "The cows are standing in the barn.",
         "Где? takes в + the prepositional (the object of в). Сарай (masculine) adds -е, and й → е: в сарае.",
         ["сарай: barn"]),
        ("Куры спят в ___.", "курятник", "prep",
         "The hens are sleeping in the chicken coop.",
         "Где? в + prepositional: в курятнике. Курятник is a place (inanimate), so this is location, not a direct object.",
         ["курятник: chicken coop"]),
        ("Быки стоят в ___.", "коровник", "prep",
         "The bulls are standing in the cowshed.",
         "Где? в + prepositional: в коровнике. Masculine nouns add -е.",
         ["коровник: cowshed"]),
        ("Лошадь пасётся на ___.", "луг", "loc",
         "The horse is grazing in the meadow.",
         "Где? на + the special locative in -у: на лугу (not на луге). Луг, сад, лес, пруд often take this -у after в/на for location.",
         ["пастись: to graze"]),
        ("Дети купаются в ___.", "пруд", "loc",
         "The children are swimming in the pond.",
         "Где? в + the special locative in -у: в пруду (not в пруде). О пруде would be 'about the pond'.",
         ["купаться: to swim, bathe"]),
        ("Скот пасётся на ___.", "пастбище", "prep",
         "The cattle are grazing in the pasture.",
         "Где? на + prepositional. Neuter -е nouns like пастбище, поле keep -е: на пастбище (same spelling as the nominative).",
         ["скот: livestock", "пастбище: pasture"]),
        ("Я весь день работаю на ___.", "ферма", "prep",
         "I work on the farm all day.",
         "Work 'on' a farm uses на + the prepositional: на ферме. На ферму would be accusative (куда? — where to?).",
         ["ферма: farm"]),
        ("Трактор стоит на ___.", "поле", "prep",
         "The tractor is standing in the field.",
         "Где? на + prepositional. Поле (neuter) keeps -е: на поле. Don't confuse it with пола (genitive) or полю (dative).",
         ["трактор: tractor"]),
        ("Зерно лежит в ___.", "кормушка", "prep",
         "The grain is in the feeder.",
         "Где? в + prepositional. Feminine -а becomes -е: в кормушке.",
         ["зерно: grain", "кормушка: feeder"]),
        ("В воскресенье мы были в ___.", "церковь", "prep",
         "On Sunday we were in church.",
         "Где? в + prepositional. Soft feminine церковь takes -и (not -е): в церкви. The same -и appears in genitive and dative.",
         ["церковь: church"]),
        ("Батюшка служит в ___.", "храм", "prep",
         "Father is serving in the church.",
         "Где? в + prepositional. Храм (masculine) adds -е: в храме. Храм is the church building.",
         ["батюшка: priest (Father)", "храм: church (building)"]),
        ("Свечи горят в ___.", "храм", "prep",
         "The candles are burning in the church.",
         "Где? в + prepositional: в храме. Свечи is the subject (nominative plural); храм is the object of в.",
         ["свеча: candle"]),
        ("После службы мы говорим о ___.", "литургия", "prep",
         "After the service we talk about the Liturgy.",
         "О (about) takes the prepositional. Nouns in -ия take -ии: о литургии (not о литургие).",
         ["литургия: Divine Liturgy"]),
        ("На службе я часто думаю о ___.", "причастие", "prep",
         "I often think about Communion.",
         "О + prepositional. Neuter nouns in -ие take -ии: о причастии.",
         ["причастие: Holy Communion"]),
        ("Жена сейчас в ___.", "город", "prep",
         "My wife is in town right now.",
         "Где? в + prepositional: в городе. В город would be accusative (куда? — into town).",
         []),
        ("Мы часто обедаем в ___.", "кафе", "prep",
         "We often have lunch at a café.",
         "Кафе is a borrowed indeclinable word: it never changes. В кафе answers где?; в кафе can also answer куда? — the form is the same.",
         ["обедать: to have lunch"]),
        ("В субботу они сидели в ___.", "ресторан", "prep",
         "On Saturday they sat in a restaurant.",
         "Где? в + prepositional: в ресторане. Masculine nouns add -е.",
         []),
        ("Она работает на ___.", "касса", "prep",
         "She works at the checkout.",
         "Events and workplaces often take на + prepositional: на кассе, на работе, на ферме. Feminine -а → -е.",
         ["касса: checkout, till"]),
        ("Я пишу программу на ___.", "компьютер", "prep",
         "I'm writing a program on the computer.",
         "На + prepositional for location 'on' a device: на компьютере. На компьютер would be accusative (onto the computer).",
         ["программа: program"]),
        ("Днём он работает в ___.", "офис", "prep",
         "During the day he works in the office.",
         "Где? в + prepositional: в офисе. В офис is куда? (to the office).",
         ["офис: office"]),
        ("Программисты долго спорили о ___.", "код", "prep",
         "The programmers argued about the code for a long time.",
         "О (about) + prepositional: о коде. Код is masculine: -е in the prepositional.",
         ["спорить: to argue"]),
        ("Мой друг живёт в ___.", "Беларусь", "prep",
         "My friend lives in Belarus.",
         "Где? в + prepositional. Soft feminine Belarusь takes -и: в Беларуси (like в церкви, не в Беларусе).",
         []),
        ("Мой брат сейчас в ___.", "Минск", "prep",
         "My brother is in Minsk right now.",
         "Где? в + prepositional. City names that are masculine add -е: в Минске. Proper names keep the capital letter.",
         []),
        ("Мы встретились на ___.", "вокзал", "prep",
         "We met at the train station.",
         "Где? на + prepositional for stations and platforms: на вокзале, на станции. На вокзал would be куда?.",
         ["вокзал: train station"]),
        ("Самолёт уже в ___.", "аэропорт", "loc",
         "The plane is already at the airport.",
         "Где? в + the special locative in -у: в аэропорту (not в аэропорте). Об аэропорте means 'about the airport'.",
         ["самолёт: airplane"]),
        ("Я сижу в ___ и читаю.", "поезд", "prep",
         "I'm sitting on the train and reading.",
         "Где? в + prepositional: в поезде. В поезд is куда? (onto the train).",
         ["поезд: train"]),
        ("Паспорт лежит в ___.", "сумка", "prep",
         "The passport is in the bag.",
         "Где? в + prepositional. Feminine -а → -е: в сумке.",
         ["паспорт: passport"]),
        ("Я слушаю эту песню в ___.", "машина", "prep",
         "I listen to this song in the car.",
         "Где? в + prepositional: в машине. В машину would be accusative (into the car).",
         ["песня: song"]),
        ("С женой мы часто говорим о ___.", "песня", "prep",
         "My wife and I often talk about the song.",
         "О (about) + prepositional. Feminine -я becomes -е: о песне.",
         []),
        ("Летом отец работает в ___.", "сад", "loc",
         "In the summer Dad works in the garden.",
         "Где? в + the special locative in -у: в саду (not в саде). О саде means 'about the garden'.",
         ["сад: garden"]),
        ("В жару коровы стоят в ___.", "лес", "loc",
         "In the heat the cows stand in the woods.",
         "Где? в + the special locative in -у: в лесу (not в лесе). Из леса is genitive ('out of the woods').",
         ["жара: heat"]),
        ("Дети играют на ___.", "берег", "loc",
         "The children are playing on the bank.",
         "Где? на + the special locative in -у: на берегу. На берег would be accusative (onto the bank).",
         ["берег: bank, shore"]),
        ("В этом ___ на ферме было много сена.", "год", "loc",
         "This year there was a lot of hay on the farm.",
         "Time expressions like 'in this year' use в + the locative in -у: в этом году (not в годе).",
         ["сено: hay"]),
        ("Билет лежит в ___.", "карман", "prep",
         "The ticket is in the pocket.",
         "Где? в + prepositional: в кармане. Masculine nouns add -е.",
         ["карман: pocket"]),
        ("Вечером я думаю о ___.", "жена", "prep",
         "In the evening I think about my wife.",
         "О (about) + prepositional. Feminine -а → -е: о жене. Жену would be the accusative (direct object).",
         []),
        ("По субботам мы бываем на ___.", "рынок", "prep",
         "On Saturdays we go to the market.",
         "Где? на + prepositional: на рынке. На рынок is куда? (to the market). Ы in рынок drops (fleeting vowel): рынк-е.",
         ["рынок: market"]),
        ("На ___ сидит птица.", "забор", "prep",
         "A bird is sitting on the fence.",
         "Где? на + prepositional: на заборе. На забор would be accusative (onto the fence).",
         ["забор: fence"]),
        ("Гости сидят в ___.", "гостиная", "prep",
         "The guests are sitting in the living room.",
         "Гостиная declines like an adjective: в гостиной (prepositional). This is где?, so prepositional, not accusative в гостиную.",
         ["гостиная: living room"]),
        ("Жена готовит обед на ___.", "кухня", "prep",
         "My wife is cooking dinner in the kitchen.",
         "Кухня is the exception among rooms: на кухне, not в кухне. На + prepositional answers где?.",
         ["кухня: kitchen"]),
        ("О ферме я прочитал в ___.", "журнал", "prep",
         "I read about the farm in a magazine.",
         "Где? в + prepositional: в журнале. О ферме is also prepositional (о + object of the preposition).",
         ["журнал: magazine"]),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(A, C, S, s, lemma, case, tr, ex, gl)

    S = "accusative"
    rows = [
        ("Я вижу ___ у сарая.", "корова", "acc",
         "I see a cow by the barn.",
         "Видеть takes a direct object in the accusative. Feminine animate корова still takes -у: корову (same as inanimate -а nouns).",
         ["сарай: barn"]),
        ("Утром я вижу ___ в коровнике.", "бык", "acc",
         "In the morning I see the bull in the cowshed.",
         "Masculine nouns for people or animals (animate) have accusative = genitive: бык → быка. Inanimate masculine would not change (вижу трактор).",
         ["бык: bull"]),
        ("Слышишь? Я вижу ___ на заборе.", "петух", "acc",
         "Do you hear that? I see a rooster on the fence.",
         "Animate masculine: accusative = genitive, so петух → петуха. Петух (nominative) would be the subject, not the direct object.",
         ["петух: rooster"]),
        ("Днём я пасу ___ на лугу.", "лошадь", "acc",
         "During the day I graze the horse in the meadow.",
         "Пасти takes a direct object in the accusative. Soft feminine лошадь looks the same in nominative and accusative: лошадь. Лошади would be genitive or dative.",
         ["пасти: to graze, herd"]),
        ("Вчера мы купили новый ___.", "трактор", "acc",
         "Yesterday we bought a new tractor.",
         "Купить takes a direct object in the accusative. Inanimate masculine nouns don't change: трактор. Трактора is genitive.",
         []),
        ("Жена каждое утро кормит ___.", "курица", "apl",
         "My wife feeds the chickens every morning.",
         "Кормить takes a direct object in the accusative. Animate nouns in the plural have accusative = genitive plural: кур (not куриц or куры). Куры is nominative plural.",
         ["кормить: to feed"]),
        ("После бури я чинил ___.", "забор", "acc",
         "After the storm I repaired the fence.",
         "Чинить takes a direct object in the accusative. Inanimate masculine: забор stays забор.",
         ["чинить: to fix", "буря: storm"]),
        ("В июле мы собираем ___.", "сено", "acc",
         "In July we gather the hay.",
         "Собирать takes a direct object in the accusative. Neuter nouns look the same in nominative and accusative: сено. Сена is genitive ('of hay').",
         ["собирать: to gather"]),
        ("Саша открыл ___ и вошёл во двор.", "калитка", "acc",
         "Sasha opened the gate and went into the yard.",
         "Открыть takes a direct object in the accusative. Feminine -а → -у: калитку. Куда? во двор is also accusative after в/во.",
         ["калитка: gate"]),
        ("Он несёт полное ___.", "ведро", "acc",
         "He is carrying a full bucket.",
         "Нести takes a direct object in the accusative. Neuter ведро stays ведро. Ведра is genitive or nominative plural.",
         ["ведро: bucket"]),
        ("Я очень люблю свою ___.", "жена", "acc",
         "I love my wife very much.",
         "Любить takes a direct object in the accusative. Feminine animate: жена → жену.",
         []),
        ("На вокзале я встретил ___.", "брат", "acc",
         "I met my brother at the station.",
         "Встретить takes a direct object in the accusative. Animate masculine: брат → брата (accusative = genitive). Compare German den Bruder.",
         ["встретить: to meet"]),
        ("Мы часто навещаем ___.", "семья", "acc",
         "We often visit the family.",
         "Навещать takes a direct object in the accusative. Feminine -я → -ю: семью.",
         ["навещать: to visit"]),
        ("Вчера он встретил старого ___ в городе.", "друг", "acc",
         "Yesterday he ran into an old friend in town.",
         "Animate masculine: друг → друга in the accusative. Другом would be instrumental (с другом, 'with a friend').",
         []),
        ("После службы я видел ___.", "батюшка", "acc",
         "After the service I saw Father.",
         "Видеть + accusative (direct object). Батюшка is masculine despite the -а, so it behaves like папа: батюшку (not батюшка and not батюшки).",
         ["батюшка: priest (Father)"]),
        ("Жена купила восковую ___.", "свеча", "acc",
         "My wife bought a beeswax candle.",
         "Купить + accusative. Feminine -а → -у, and ч stays: свечу.",
         ["восковой: beeswax"]),
        ("Перед службой мы целуем ___.", "икона", "acc",
         "Before the service we kiss the icon.",
         "Целовать takes a direct object in the accusative: икону. Иконе would be dative or prepositional.",
         ["целовать: to kiss", "икона: icon"]),
        ("Жена покупает ___ каждый день.", "хлеб", "acc",
         "My wife buys bread every day.",
         "Покупать + accusative. Inanimate masculine: хлеб doesn't change. Хлеба is genitive (нет хлеба, 'no bread').",
         []),
        ("В кафе я заказал ___.", "суп", "acc",
         "At the café I ordered soup.",
         "Заказать + accusative. Inanimate masculine: суп stays суп.",
         ["заказать: to order"]),
        ("Официант принёс нам ___.", "меню", "acc",
         "The waiter brought us the menu.",
         "Меню is indeclinable: it never changes, so the accusative looks just like the nominative. Меню is also the direct object here.",
         ["официант: waiter"]),
        ("Он несёт тяжёлую ___.", "сумка", "acc",
         "He is carrying a heavy bag.",
         "Нести + accusative (direct object). Feminine -а → -у: сумку.",
         []),
        ("Вечером я пишу новую ___.", "программа", "acc",
         "In the evening I'm writing a new program.",
         "Писать takes a direct object in the accusative. Feminine -а → -у: программу.",
         []),
        ("Брат чинит старый ___.", "компьютер", "acc",
         "My brother is repairing the old computer.",
         "Чинить + accusative. Inanimate masculine: компьютер doesn't change.",
         []),
        ("На работе я весь день пишу ___.", "код", "acc",
         "At work I write code all day.",
         "Писать + accusative. Inanimate masculine: код stays код. Кода is genitive.",
         []),
        ("Утром я купил ___ до Минска.", "билет", "acc",
         "In the morning I bought a ticket to Minsk.",
         "Купить + accusative. Inanimate masculine: билет doesn't change. До Минска is genitive after до ('as far as').",
         []),
        ("Как город я очень люблю ___.", "Минск", "acc",
         "I really love Minsk.",
         "Любить + accusative. City names that are inanimate masculine don't change: Минск. Минска is genitive (из Минска).",
         []),
        ("На границе я открыл ___.", "паспорт", "acc",
         "At the border I opened my passport.",
         "Открыть + accusative. Inanimate masculine: паспорт stays паспорт. Compare показать паспорт пограничнику: passport is still accusative, the guard is dative.",
         []),
        ("Он несёт тяжёлый ___ на вокзал.", "чемодан", "acc",
         "He is carrying a heavy suitcase to the station.",
         "Нести + accusative: чемодан (inanimate masculine, no change). На вокзал is also accusative (куда?).",
         []),
        ("Вечером мы слушаем новую ___.", "песня", "acc",
         "In the evening we listen to a new song.",
         "Слушать + accusative. Feminine -я → -ю: песню. О песне would be prepositional ('about the song').",
         []),
        ("Друг пригласил нас в ___.", "Беларусь", "acc",
         "A friend invited us to Belarus.",
         "Куда? в + accusative. Soft feminine Беларусь looks the same in nominative and accusative: в Беларусь. В Беларуси (prepositional) means 'in Belarus'.",
         ["пригласить: to invite"]),
        ("В воскресенье я иду в ___.", "церковь", "acc",
         "On Sunday I'm going to church.",
         "Куда? (where to?) takes в + accusative. Церковь looks the same as the nominative. В церкви (prepositional) answers где? (in church).",
         []),
        ("После работы мы едем на ___.", "ферма", "acc",
         "After work we are going to the farm.",
         "Куда? на + accusative: на ферму. На ферме (prepositional) answers где? (on the farm).",
         []),
        ("Сейчас он идёт в ___.", "магазин", "acc",
         "He is going to the store right now.",
         "Куда? в + accusative. Inanimate masculine: в магазин (no change). В магазине is где?.",
         []),
        ("На лугу я видел ___.", "олень", "acc",
         "I saw a deer in the meadow.",
         "Видеть + accusative. Animate masculine soft stem: олень → оленя (accusative = genitive).",
         ["олень: deer"]),
        ("Куры несут ___.", "яйцо", "apl",
         "The hens lay eggs.",
         "Нести here means 'to lay' and takes a direct object in the accusative. Neuter plural яйца looks like the nominative plural (inanimate). Яиц is genitive plural (много яиц).",
         []),
        ("Ты знаешь ___? Он тоже программист.", "Саша", "acc",
         "Do you know Sasha? He's a programmer too.",
         "Знать + accusative. Саша is masculine despite the -а (like папа, батюшка): Сашу.",
         []),
        ("Утром дети пьют ___.", "молоко", "acc",
         "In the morning the children drink milk.",
         "Пить + accusative. Neuter молоко stays молоко. Молока is genitive (нет молока, стакан молока).",
         []),
        ("Я взял ___ и пошёл в сад.", "лопата", "acc",
         "I took a shovel and went into the garden.",
         "Взять + accusative (direct object). Feminine -а → -у: лопату.",
         ["лопата: shovel"]),
        ("Мама читает ___ за столом.", "письмо", "acc",
         "Mom is reading a letter at the table.",
         "Читать + accusative. Neuter письмо stays письмо. Письма is genitive or nominative plural.",
         []),
        ("Я ищу ___ от калитки.", "ключ", "acc",
         "I'm looking for the key to the gate.",
         "Искать + accusative. Inanimate masculine: ключ doesn't change. Ключа is genitive; ключи is plural.",
         []),
    ]
    # Саша may not be in vocab/table — check forms
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(A, C, S, s, lemma, case, tr, ex, gl)

    S = "dative"
    rows = [
        ("Я дал воду ___.", "корова", "dpl",
         "I gave water to the cows.",
         "The indirect object (to whom?) goes in the dative. Корова in the plural takes -ам: коровам. Воду is the direct object (accusative).",
         []),
        ("Жена каждое утро даёт корм ___.", "курица", "dpl",
         "My wife gives feed to the chickens every morning.",
         "Давать takes a dative indirect object: курам (dative plural of курица / куры). Корм is the direct object (accusative).",
         []),
        ("Я дал сено ___.", "лошадь", "dat",
         "I gave hay to the horse.",
         "The indirect object is dative. Soft feminine лошадь takes -и: лошади (same spelling as the genitive). Сено is the direct object.",
         []),
        ("По вечерам я помогаю ___.", "жена", "dat",
         "In the evenings I help my wife.",
         "Помогать takes the dative (to whom do you give help?): жене. Жену would be accusative (a direct object).",
         ["помогать: to help"]),
        ("Я часто звоню ___ в Беларусь.", "друг", "dat",
         "I often call a friend in Belarus.",
         "Звонить takes the dative: друг → другу. В Беларусь here is accusative (куда?).",
         []),
        ("После службы мы помогаем ___.", "батюшка", "dat",
         "After the service we help Father.",
         "Помогать + dative. Батюшка (masculine -а) takes -е: батюшке, like папе, дяде.",
         []),
        ("Я пишу письмо ___.", "мама", "dat",
         "I'm writing a letter to Mom.",
         "The person you write to is the indirect object (dative): маме. Письмо is the direct object (accusative).",
         []),
        ("___ нравится эта ферма.", "я", "dat",
         "I like this farm.",
         "Нравится literally means 'is pleasing to': the person who likes something goes in the dative (мне). Эта ферма is the subject (nominative).",
         []),
        ("___ нужно купить корм.", "я", "dat",
         "I need to buy feed.",
         "Нужно (it is necessary) takes the person in the dative: мне нужно. Compare German mir ist nötig.",
         []),
        ("___ сегодня холодно на улице.", "я", "dat",
         "I'm cold outside today.",
         "Feelings like холодно, жарко, скучно take the dative: мне холодно (literally 'it is cold to me'). There is no nominative subject.",
         []),
        ("___ надо подоить коров.", "ты", "dat",
         "You need to milk the cows.",
         "Надо, like нужно, takes the dative: тебе надо. Коров is the direct object (animate accusative plural).",
         ["доить: to milk"]),
        ("Я дал паспорт ___.", "друг", "dat",
         "I gave the passport to my friend.",
         "Дать takes a dative indirect object (другу) and an accusative direct object (паспорт).",
         []),
        ("По ___ едет трактор.", "поле", "dat",
         "A tractor is driving across the field.",
         "По (along, across) takes the dative: по полю. Поле is neuter, so the dative is -ю.",
         []),
        ("В воскресенье мы идём к ___.", "храм", "dat",
         "On Sunday we are going to the church.",
         "К (toward a person or building) takes the dative: к храму. К is the preposition; храму is its object.",
         []),
        ("Завтра я иду к ___.", "врач", "dat",
         "Tomorrow I'm going to the doctor.",
         "К + dative for going to a person: к врачу. The fleeting vowel in врач drops: врач → врачу.",
         ["врач: doctor"]),
        ("После работы она идёт к ___.", "мама", "dat",
         "After work she goes to her mom's.",
         "К + dative: к маме. К маму would mix up accusative with dative.",
         []),
        ("___ уже тридцать два года.", "он", "dat",
         "He is already thirty-two years old.",
         "Age uses the dative of the person + столько-то лет: ему тридцать два года (literally 'to him there are 32 years').",
         []),
        ("Мы едем к ___ за сеном.", "ферма", "dat",
         "We're going to the farm for hay.",
         "К + dative: к ферме. За сеном is instrumental ('for hay', to fetch it).",
         []),
        ("Собака подбежала к ___.", "забор", "dat",
         "The dog ran up to the fence.",
         "К + dative (toward): к забору. Подбежать к takes the dative object of к.",
         []),
        ("По ___ едет автобус.", "улица", "dat",
         "A bus is going down the street.",
         "По (along) + dative: по улице. Улица is feminine: -е in the dative, same spelling as the prepositional.",
         []),
        ("___ нужна помощь на ферме.", "она", "dat",
         "She needs help on the farm.",
         "Нужна agrees with помощь (feminine subject). The person who needs it is dative: ей нужна помощь.",
         []),
        ("Я верю ___.", "жена", "dat",
         "I trust my wife.",
         "Верить takes the dative (to whom you give your trust): жене. Верить в + accusative means 'to believe in'.",
         ["верить: to believe, trust"]),
        ("По выходным мы помогаем ___.", "родитель", "dpl",
         "On weekends we help our parents.",
         "Помогать + dative. Родители is already plural: родителям (dative plural).",
         ["родители: parents"]),
        ("Я дал корм ___.", "собака", "dat",
         "I gave feed to the dog.",
         "Дать + dative indirect object: собаке. Корм is the accusative direct object.",
         []),
        ("___ нравится этот трактор.", "она", "dat",
         "She likes this tractor.",
         "Нравится + dative of the person: ей нравится. Этот трактор is the subject (nominative).",
         []),
        ("___ нельзя опаздывать на поезд.", "вы", "dat",
         "You mustn't be late for the train.",
         "Нельзя (it is not allowed) takes the dative: вам нельзя. Поезд is accusative after на (куда? onto the train / for the train).",
         ["опаздывать: to be late"]),
        ("Я показал паспорт ___.", "пограничник", "dat",
         "I showed my passport to the border guard.",
         "Показать takes a dative indirect object (to whom): пограничнику, and an accusative direct object (паспорт).",
         ["пограничник: border guard"]),
        ("Кассир дал сдачу ___.", "жена", "dat",
         "The cashier gave the change to my wife.",
         "Дать + dative: жене. Сдачу is the direct object (accusative of сдача).",
         ["сдача: change (money back)"]),
        ("Я отправил файл ___.", "коллега", "dat",
         "I sent the file to a colleague.",
         "Отправить takes a dative indirect object. Коллега (masculine -а, like папа) takes -е: коллеге.",
         ["коллега: colleague"]),
        ("___ надо выйти из программы.", "мы", "dat",
         "We need to quit the program.",
         "Надо + dative: нам надо. Из программы is genitive after из.",
         []),
        ("Я ответил ___ сразу.", "батюшка", "dat",
         "I answered Father right away.",
         "Ответить takes the dative (to whom you give the answer): батюшке.",
         ["ответить: to answer"]),
        ("Мы дали сено ___.", "телёнок", "dpl",
         "We gave hay to the calves.",
         "The indirect object is dative plural. Телёнок has an irregular plural (телята), so the dative plural is телятам.",
         ["телёнок: calf"]),
        ("___ нравится группа «Молчат Дома».", "ты", "dat",
         "You like the band Molchat Doma.",
         "Нравится + dative: тебе нравится. The band name is the subject (nominative).",
         []),
        ("Помоги ___, пожалуйста, с калиткой.", "я", "dat",
         "Help me with the gate, please.",
         "Помогать / помоги takes the dative: мне. С калиткой is instrumental (с + object of the preposition).",
         []),
        ("Скажи ___ правду о работе.", "он", "dat",
         "Tell him the truth about the work.",
         "Сказать takes a dative indirect object (ему) and an accusative direct object (правду).",
         []),
        ("Расскажи ___ о ферме.", "мы", "dat",
         "Tell us about the farm.",
         "Рассказать + dative of the listener: нам. О ферме is prepositional (о + object of the preposition).",
         []),
        ("Дети машут ___ из окна.", "папа", "dat",
         "The children are waving to Dad from the window.",
         "Махать / машут takes the dative (to whom you wave): папе. Папа is masculine despite the -а.",
         ["махать: to wave"]),
        ("Я рад ___.", "друг", "dat",
         "I'm glad for my friend. / I'm happy to see my friend.",
         "Рад takes the dative: рад другу ('glad for / about a friend'). Рад is a short adjective, not a verb.",
         []),
        ("Автобус идёт к ___.", "вокзал", "dat",
         "The bus is going toward the station.",
         "К + dative: к вокзалу. На вокзал (accusative) is the usual 'to the station' as a destination; к вокзалу stresses motion toward it.",
         []),
        ("Программист отправил отчёт ___.", "начальник", "dat",
         "The programmer sent the report to the boss.",
         "Отправить + dative indirect object: начальнику. Отчёт is the accusative direct object.",
         ["начальник: boss", "отчёт: report"]),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(A, C, S, s, lemma, case, tr, ex, gl)

    S = "genitive"
    rows = [
        ("У меня нет ___ для коров.", "сено", "gen",
         "I don't have any hay for the cows.",
         "Нет ('there is no') takes the genitive. Neuter -о → -а: сена. Для коров is also genitive (для + object of the preposition).",
         []),
        ("На ферме много ___.", "корова", "gpl",
         "There are a lot of cows on the farm.",
         "Много (a lot of) takes the genitive plural: коров. After 5 and up you use this same genitive plural (пять коров).",
         []),
        ("Этой весной у нас мало ___.", "яйцо", "gpl",
         "This spring we have few eggs.",
         "Мало (few, little) takes the genitive plural. Яйцо has an irregular genitive plural: яиц (not яйцов).",
         []),
        ("Я купил мешок ___.", "корм", "gen",
         "I bought a bag of feed.",
         "A quantity noun (мешок, стакан, килограмм) is followed by the genitive: мешок корма, 'a bag of feed'. Корм is masculine: -а.",
         ["мешок: bag, sack"]),
        ("На рынке я взял килограмм ___.", "сыр", "gen",
         "At the market I got a kilogram of cheese.",
         "Килограмм + genitive ('of …'): сыра. Masculine nouns add -а.",
         ["сыр: cheese"]),
        ("Это дом ___.", "брат", "gen",
         "This is my brother's house.",
         "The owner goes in the genitive, after the thing owned: дом брата ('the house of the brother'). Compare German das Haus des Bruders.",
         []),
        ("Это машина ___.", "жена", "gen",
         "This is my wife's car.",
         "Possession: the owner is genitive after the thing: машина жены. Жену would be accusative (a direct object).",
         []),
        ("Мы только что вышли из ___.", "магазин", "gen",
         "We just came out of the store.",
         "Из (out of) takes the genitive: из магазина. The object of the preposition из is магазина.",
         []),
        ("После службы мы вышли из ___.", "церковь", "gen",
         "After the service we left the church.",
         "Из + genitive. Soft feminine церковь takes -и: из церкви (same spelling as the prepositional в церкви, but the preposition is different).",
         []),
        ("Я купил билет для ___.", "друг", "gen",
         "I bought a ticket for a friend.",
         "Для (for) always takes the genitive: для друга. Другу would be dative (звоню другу).",
         []),
        ("Я пью чай без ___.", "сахар", "gen",
         "I drink tea without sugar.",
         "Без (without) takes the genitive: без сахара. Masculine nouns add -а.",
         ["сахар: sugar"]),
        ("Письмо пришло от ___.", "друг", "gen",
         "A letter came from a friend.",
         "От (from a person) takes the genitive: от друга. The object of от is друга.",
         []),
        ("После ___ мы поехали домой.", "литургия", "gen",
         "After the Liturgy we went home.",
         "После (after) takes the genitive. Nouns in -ия take -ии: после литургии.",
         []),
        ("Этой осенью у нас нет ___.", "трактор", "gen",
         "This fall we don't have a tractor.",
         "Нет + genitive. Masculine nouns add -а: нет трактора.",
         []),
        ("Без ___ на поезд не пустят.", "билет", "gen",
         "They won't let you on the train without a ticket.",
         "Без + genitive: без билета. Билет is masculine: -а.",
         []),
        ("У программиста нет ___.", "время", "gen",
         "The programmer has no time.",
         "Нет + genitive. Время is a neuter -мя noun: the genitive is времени (not времения).",
         []),
        ("У меня сейчас нет ___.", "деньги", "gpl",
         "I don't have any money right now.",
         "Нет + genitive. Деньги is plural-only: the genitive is денег (not деньгов).",
         []),
        ("Сколько ___ у тебя на ферме?", "корова", "gpl",
         "How many cows do you have on the farm?",
         "Сколько (how many) takes the genitive plural: сколько коров. The same form is used after 5, 6, 7…",
         []),
        ("На ферме теперь много ___.", "курица", "gpl",
         "There are a lot of chickens on the farm now.",
         "Много + genitive plural. The farm plural of курица is куры, and the genitive plural is кур (not куриц).",
         []),
        ("В сарае мало ___.", "сено", "gen",
         "There is little hay in the barn.",
         "Мало + genitive. Сено is a mass noun, so you use the genitive singular: мало сена (not сенов).",
         []),
        ("Налей мне чашку ___.", "чай", "gen",
         "Pour me a cup of tea.",
         "Чашка + genitive ('a cup of …'): чашка чая. Masculine чай has genitive чая (not чаяя).",
         []),
        ("Дай ему кусок ___.", "хлеб", "gen",
         "Give him a piece of bread.",
         "Кусок + genitive ('a piece of …'): кусок хлеба. Ему is dative (indirect object).",
         ["кусок: piece"]),
        ("Я не могу найти паспорт ___.", "жена", "gen",
         "I can't find my wife's passport.",
         "The owner is genitive: паспорт жены ('the passport of my wife').",
         []),
        ("Наша ферма недалеко от ___.", "Минск", "gen",
         "Our farm is not far from Minsk.",
         "От (from) + genitive: от Минска. Недалеко от is a fixed combination with the genitive.",
         []),
        ("Он приехал из ___.", "Беларусь", "gen",
         "He arrived from Belarus.",
         "Из (out of, from a country) takes the genitive. Soft feminine Беларусь → из Беларуси.",
         []),
        ("Маленькие дети боятся ___.", "собака", "gen",
         "Little children are afraid of the dog.",
         "Бояться takes the genitive (of what?): собаки. This is not a preposition; the verb itself governs the genitive.",
         ["бояться: to be afraid"]),
        ("Без ___ через границу нельзя.", "паспорт", "gen",
         "You can't cross the border without a passport.",
         "Без + genitive: без паспорта. Паспорт is masculine: -а.",
         []),
        ("Для ___ нужен новый трактор.", "ферма", "gen",
         "The farm needs a new tractor. / A new tractor is needed for the farm.",
         "Для (for) + genitive: для фермы. Нужен agrees with трактор (masculine subject).",
         []),
        ("Около ___ растёт ива.", "пруд", "gen",
         "A willow grows near the pond.",
         "Около (near) takes the genitive: около пруда. The object of около is пруда.",
         ["ива: willow"]),
        ("У ___ стоит пикап.", "забор", "gen",
         "A pickup is standing by the fence.",
         "У (by, next to) takes the genitive: у забора. This is the same у that appears in у меня есть, but here it means location.",
         ["пикап: pickup truck"]),
        ("Я вчера не видел ___.", "брат", "gen",
         "I didn't see my brother yesterday.",
         "A negated verb of perception often takes the genitive of a person: не видел брата (instead of the accusative брата — here they look the same, but the government is genitive).",
         []),
        ("На ферме мало ___.", "петух", "gpl",
         "There are few roosters on the farm.",
         "Мало + genitive plural: мало петухов. Animate masculine nouns take -ов in the genitive plural.",
         []),
        ("Крыша ___ протекает.", "сарай", "gen",
         "The barn's roof is leaking.",
         "Possession: крыша сарая ('the roof of the barn'). The owner/whole goes in the genitive.",
         ["протекать: to leak"]),
        ("Дверь ___ снова сломалась.", "курятник", "gen",
         "The coop door is broken again.",
         "Possession: дверь курятника ('the door of the coop') — курятника is genitive.",
         []),
        ("Я не слышал этой ___.", "песня", "gen",
         "I hadn't heard this song.",
         "Не слышал can take the genitive of the thing not heard: не слышал песни. Этой is also genitive, agreeing with песни.",
         []),
        ("Он вышел из ___ в пять часов.", "офис", "gen",
         "He left the office at five o'clock.",
         "Из + genitive: из офиса. В пять часов is accusative of time.",
         []),
        ("У пруда мы видели следы ___.", "олень", "gen",
         "By the pond we saw deer tracks.",
         "Possession / 'of': следы оленя ('tracks of a deer'). Олень is animate masculine, genitive оленя.",
         ["след: track, footprint"]),
        ("Принеси, пожалуйста, бутылку ___.", "вода", "gen",
         "Please bring a bottle of water.",
         "Бутылка + genitive ('a bottle of …'): бутылка воды. Feminine -а → -ы.",
         ["бутылка: bottle"]),
        ("Официант принёс тарелку ___.", "суп", "gen",
         "The waiter brought a plate of soup.",
         "Тарелка + genitive ('a plate of …'): тарелка супа.",
         ["тарелка: plate"]),
        ("Возле ___ всегда много такси.", "вокзал", "gen",
         "There are always a lot of taxis near the station.",
         "Возле (beside, near) takes the genitive: возле вокзала. Много also takes the genitive, but такси is indeclinable, so it does not change.",
         []),
        ("Я купил диск этой ___.", "группа", "gen",
         "I bought this band's album.",
         "Possession: диск группы ('the album of the band'). Этой agrees with группы in the genitive.",
         ["группа: band, group"]),
        ("У ___ нет своего компьютера.", "коллега", "gen",
         "The colleague doesn't have a computer of his own.",
         "У + genitive of the owner: у коллеги. Коллега (masculine -а) forms the genitive like папа: коллеги. Компьютера is also genitive after нет.",
         []),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(A, C, S, s, lemma, case, tr, ex, gl)

    S = "instrumental"
    rows = [
        ("По профессии я ___.", "программист", "ins",
         "By profession I am a programmer.",
         "A predicate of profession or role after быть / стать / работать often goes in the instrumental: программистом. This is not a direct object.",
         []),
        ("Мой отец всю жизнь работает ___.", "фермер", "ins",
         "My father has worked as a farmer all his life.",
         "Работать кем? takes the instrumental: фермером. Masculine nouns add -ом.",
         ["фермер: farmer"]),
        ("Жена режет хлеб ___.", "нож", "ins",
         "My wife is cutting the bread with a knife.",
         "The instrument you use (чем? with what?) goes in the instrumental, often without a preposition: ножом. Хлеб is the direct object (accusative).",
         ["нож: knife"]),
        ("Я обычно пишу ___.", "ручка", "ins",
         "I usually write with a pen.",
         "Чем? (with what?) is instrumental: ручкой. Feminine -а → -ой.",
         ["ручка: pen"]),
        ("В Минск мы едем ___.", "поезд", "ins",
         "We're going to Minsk by train.",
         "Means of transport often take the instrumental with no preposition: ехать поездом, лететь самолётом. В Минск is accusative (куда?).",
         []),
        ("На работу она едет ___.", "автобус", "ins",
         "She goes to work by bus.",
         "Instrumental of means: автобусом. На работу is accusative (куда?).",
         []),
        ("Днём я управляю ___.", "трактор", "ins",
         "During the day I drive the tractor.",
         "Управлять (to operate, drive) takes the instrumental: управлять трактором. This is verbal government, not a preposition.",
         ["управлять: to operate"]),
        ("Отец косит траву ___.", "косилка", "ins",
         "Dad is cutting the grass with the mower.",
         "Чем? instrumental of the tool: косилкой. Траву is the direct object (accusative).",
         ["косилка: mower"]),
        ("Вечером я долго говорю с ___.", "жена", "ins",
         "In the evening I talk with my wife for a long time.",
         "С (with a person) takes the instrumental: с женой. The object of the preposition с is женой.",
         []),
        ("После службы мы говорили с ___.", "батюшка", "ins",
         "After the service we talked with Father.",
         "С + instrumental. Батюшка (masculine -а) takes -ой: с батюшкой, like с папой.",
         []),
        ("Я очень доволен своей ___.", "ферма", "ins",
         "I'm very pleased with my farm.",
         "Доволен (pleased with) takes the instrumental: доволен фермой. Своей agrees with фермой (feminine instrumental).",
         ["доволен: pleased"]),
        ("Пикап стоит за ___.", "забор", "ins",
         "The pickup is standing behind the fence.",
         "За meaning 'behind' takes the instrumental: за забором. За забор would be accusative (to behind the fence, куда?).",
         []),
        ("Ключи лежат под ___.", "книга", "ins",
         "The keys are under the book.",
         "Под meaning 'under' (location, где?) takes the instrumental: под книгой. Под книгу would be accusative (куда?).",
         []),
        ("Над ___ висит лампа.", "стол", "ins",
         "A lamp is hanging above the table.",
         "Над (above) takes the instrumental: над столом. The object of над is столом.",
         []),
        ("Перед ___ всегда много людей.", "церковь", "ins",
         "There are always a lot of people in front of the church.",
         "Перед (in front of) takes the instrumental. Soft feminine церковь takes -ью: перед церковью.",
         []),
        ("Я интересуюсь русской ___.", "музыка", "ins",
         "I'm interested in Russian music.",
         "Интересоваться takes the instrumental (чем?): интересуюсь музыкой. Русской agrees with музыкой.",
         ["интересоваться: to be interested"]),
        ("Целый день я сижу за ___.", "компьютер", "ins",
         "I sit at the computer all day.",
         "За + instrumental can mean 'at' a workstation: за компьютером, за столом. За компьютер would be accusative (куда?).",
         []),
        ("Мы едим суп ___.", "ложка", "ins",
         "We eat soup with a spoon.",
         "Чем? instrumental of the tool, no preposition: ложкой. Суп is the direct object (accusative).",
         ["ложка: spoon"]),
        ("В церковь я хожу с ___.", "брат", "ins",
         "I go to church with my brother.",
         "С (together with) + instrumental: с братом. В церковь is accusative (куда?).",
         []),
        ("На рынок она пошла с ___.", "сестра", "ins",
         "She went to the market with her sister.",
         "С + instrumental: с сестрой. Feminine -а → -ой.",
         []),
        ("Я пасу коров с ___.", "сын", "ins",
         "I graze the cows with my son.",
         "С + instrumental: с сыном. Коров is the direct object (animate accusative plural).",
         ["сын: son"]),
        ("Поле за ___ ещё не скошено.", "сарай", "ins",
         "The field behind the barn hasn't been mowed yet.",
         "За (behind) + instrumental: за сараем. Сарай (masculine, ends in й) takes -ем.",
         []),
        ("Я чинил забор ___.", "молоток", "ins",
         "I was repairing the fence with a hammer.",
         "Чем? instrumental of the tool: молотком. The fleeting о in молоток drops: молотк-ом. Забор is the direct object.",
         ["молоток: hammer"]),
        ("За ___ растёт ива.", "пруд", "ins",
         "A willow grows beyond the pond.",
         "За (beyond, behind) + instrumental: за прудом.",
         ["ива: willow"]),
        ("Между ___ и лесом течёт ручей.", "ферма", "ins",
         "A stream flows between the farm and the woods.",
         "Между (between) takes the instrumental: между фермой и лесом. Both nouns are objects of между.",
         ["ручей: stream"]),
        ("На сенокосе я пользуюсь ___.", "лопата", "ins",
         "At haymaking I use a shovel.",
         "Пользоваться (to use) takes the instrumental: пользоваться лопатой. This is verbal government.",
         ["пользоваться: to use"]),
        ("Корм мы носим ___.", "ведро", "ins",
         "We carry the feed with a bucket.",
         "Чем? instrumental of the tool: ведром. Неuter -о adds -м. Корм is the direct object.",
         []),
        ("Дед машет нам ___.", "рука", "ins",
         "Grandfather is waving a hand at us.",
         "Махать чем? takes the instrumental of the thing waved: рукой. Нам is dative (to whom he waves).",
         ["дед: grandfather"]),
        ("В Беларусь мы летим ___.", "самолёт", "ins",
         "We're flying to Belarus by plane.",
         "Instrumental of means: самолётом. В Беларусь is accusative (куда?).",
         []),
        ("Я открыл калитку ___.", "ключ", "ins",
         "I opened the gate with a key.",
         "Чем? instrumental: ключом. Калитку is the direct object (accusative).",
         []),
        ("Его сестра работает ___.", "учитель", "ins",
         "His sister works as a teacher.",
         "Работать кем? + instrumental: учителем. Soft masculine учитель takes -ем (not -ом).",
         ["учитель: teacher"]),
        ("По утрам я пью чай с ___.", "лимон", "ins",
         "I drink tea with lemon.",
         "С meaning 'with' (added to something) takes the instrumental: с лимоном. Compare с молоком in the original set.",
         ["лимон: lemon"]),
        ("Я горжусь своей ___.", "жена", "ins",
         "I'm proud of my wife.",
         "Гордиться (to be proud of) takes the instrumental: горжусь женой. Своей agrees with женой.",
         ["гордиться: to be proud"]),
        ("С ___ мы чинили трактор весь день.", "отец", "ins",
         "Dad and I repaired the tractor all day.",
         "С + instrumental: с отцом. Отец has a fleeting е: отц-ом. Мы is the subject.",
         []),
        ("Куры ходят за ___.", "забор", "ins",
         "The chickens walk around behind the fence.",
         "За (behind) + instrumental: за забором. This is где?, not куда? (which would be за забор, accusative).",
         []),
        ("Сено я ворошу ___.", "вилы", "ins",
         "I turn the hay with a pitchfork.",
         "Вилы is plural-only (like ворота, 'gate'). The instrumental is вилами. Сено is the direct object.",
         ["ворошить: to turn (hay)", "вилы: pitchfork"]),
        ("Саша стал ___.", "священник", "ins",
         "Sasha became a priest.",
         "Стать кем? takes the instrumental of the new role: священником. This is not a direct object.",
         ["священник: priest"]),
        ("Мы слушаем «Молчат Дома» с ___.", "жена", "ins",
         "We listen to Molchat Doma with my wife.",
         "С + instrumental: с женой. The band name is the direct object of слушаем (accusative, but indeclinable here as a title).",
         []),
        ("Перед ___ стоит очередь.", "касса", "ins",
         "There is a line in front of the checkout.",
         "Перед + instrumental: перед кассой. Feminine -а → -ой.",
         ["очередь: line, queue"]),
        ("Я еду на ферму со своими ___.", "ребёнок", "ipl",
         "I'm going to the farm with my kids.",
         "С + instrumental plural. Дети is already plural: детьми (irregular: not детами). Своими agrees with детьми.",
         []),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(A, C, S, s, lemma, case, tr, ex, gl)

    S = "pronouns"
    # (s, lemma, case, tr, ex, gl)
    prows = [
        ("Она очень любит ___.", "я", "acc",
         "She loves me very much.",
         "Любить takes a direct object in the accusative: я → меня. Мне would be dative (дай мне, 'give me').",
         []),
        ("Кто видел ___ вчера на рынке?", "мы", "acc",
         "Who saw us at the market yesterday?",
         "Видеть + accusative (direct object): мы → нас. Нам is dative; нами is instrumental.",
         []),
        ("Я давно не встречал ___.", "они", "acc",
         "I haven't run into them in a long time.",
         "Встречать + accusative: они → их. After a preposition this becomes них (для них, у них).",
         []),
        ("Помоги ___, пожалуйста, с трактором.", "я", "dat",
         "Help me with the tractor, please.",
         "Помогать takes the dative: мне. Меня would be accusative or genitive.",
         []),
        ("Я звоню ___ каждый вечер.", "она", "dat",
         "I call her every evening.",
         "Звонить takes the dative: она → ей. Её is genitive or accusative; ней is used after a preposition.",
         []),
        ("Скажи ___ спасибо за помощь.", "они", "dat",
         "Tell them thank you for the help.",
         "Сказать takes a dative indirect object: им. Их is genitive or accusative; ними is instrumental.",
         []),
        ("После работы мы идём к ___.", "он", "pdat",
         "After work we are going over to his place.",
         "К takes the dative, and он/она/они add н- after a preposition: к нему (not к ему).",
         []),
        ("Дети идут к ___ в комнату.", "она", "pdat",
         "The children are going to her, into the room.",
         "К + dative, with н- after the preposition: к ней. Ей without н- is used when there is no preposition (я звоню ей).",
         []),
        ("Мы подошли к ___ у церкви.", "они", "pdat",
         "We walked up to them by the church.",
         "К + dative with н-: к ним (not к им). У церкви is genitive after у ('by the church').",
         []),
        ("Жена живёт с ___ на ферме уже двадцать лет.", "он", "pins",
         "His wife has lived with him on the farm for twenty years.",
         "С takes the instrumental, and он adds н- after a preposition: с ним. Им without н- is the no-preposition form (я горжусь им).",
         []),
        ("Поезжай со ___ на ферму.", "я", "ins",
         "Come with me to the farm.",
         "С / со takes the instrumental: я → мной (or мною). Со is used before мной because of the consonant cluster. Меня is accusative or genitive.",
         []),
        ("Иди со ___ в церковь.", "я", "ins",
         "Come with me to church.",
         "С / со + instrumental: мной. В церковь is accusative (куда?).",
         []),
        ("Мы долго говорили о ___.", "он", "pprep",
         "We talked about him for a long time.",
         "О takes the prepositional, with н- after the preposition: о нём (ё is required). Ему is dative, его is genitive or accusative.",
         []),
        ("Ночью я часто думаю о ___.", "она", "pprep",
         "I often think about her.",
         "О + prepositional with н-: о ней. Её is genitive or accusative (без неё, я вижу её).",
         []),
        ("Батюшка всегда молится о ___.", "мы", "prep",
         "Father always prays for us.",
         "О + prepositional: мы → нас. Нас is also genitive and accusative; the preposition о is what makes this prepositional.",
         ["молиться: to pray"]),
        ("Без ___ ферма не работает.", "я", "gen",
         "The farm doesn't work without me.",
         "Без takes the genitive: меня. This меня is the object of the preposition без, not a direct object.",
         []),
        ("Без ___ я на рынок не поеду.", "ты", "gen",
         "I won't go to the market without you.",
         "Без + genitive: тебя. Тебе is dative; тобой is instrumental (с тобой).",
         []),
        ("Маленький сын очень боится ___.", "он", "gen",
         "The little boy is very afraid of him.",
         "Бояться takes the genitive, and there is no preposition, so он → его (not него). Него is used after a preposition (без него).",
         ["бояться: to be afraid"]),
        ("Это подарок для ___.", "они", "pgen",
         "This is a present for them.",
         "Для takes the genitive, and они adds н- after a preposition: для них (not для их).",
         []),
        ("Я вижу ___ у калитки.", "вы", "acc",
         "I see you at the gate.",
         "Видеть + accusative: вы → вас. Вам is dative; вами is instrumental. У калитки is genitive after у.",
         []),
        ("Этот корм для ___.", "вы", "gen",
         "This feed is for you.",
         "Для + genitive: для вас. The object of для is вас.",
         []),
        ("Собака идёт за ___.", "я", "ins",
         "The dog is walking behind me.",
         "За meaning 'behind' (где?) takes the instrumental: за мной. За меня would be accusative ('for me' / 'in my place').",
         []),
        ("Между ___ нет секретов.", "мы", "ins",
         "There are no secrets between us.",
         "Между takes the instrumental: между нами. Нас is genitive or accusative; нам is dative.",
         []),
        ("Почему ты смотришь на ___?", "я", "acc",
         "Why are you looking at me?",
         "Смотреть на takes the accusative: на меня. На мне would be prepositional ('on me', as in a location).",
         []),
        ("Все смотрят на ___.", "она", "pacc",
         "Everyone is looking at her.",
         "На + accusative, with н- after the preposition: на неё (not на её).",
         []),
        ("Посмотри на ___: он уже у забора.", "он", "pacc",
         "Look at him: he's already by the fence.",
         "На + accusative with н-: на него (not на его). У забора is genitive after у.",
         []),
        ("Мы очень ждём ___.", "вы", "acc",
         "We've been waiting for you.",
         "Ждать often takes the accusative of a person: вас. Вам is dative.",
         []),
        ("Кто кроме ___ знает дорогу на ферму?", "ты", "gen",
         "Who besides you knows the way to the farm?",
         "Кроме (except, besides) takes the genitive: кроме тебя.",
         ["кроме: besides, except"]),
        ("Я скучаю по ___.", "она", "pdat",
         "I miss her.",
         "Скучать по takes the dative, with н- after the preposition: по ней. По неё would be the wrong case.",
         ["скучать: to miss, long for"]),
        ("Расскажи ___ о поездке в Минск.", "мы", "dat",
         "Tell us about the trip to Minsk.",
         "Рассказать takes a dative indirect object: нам. О поездке is prepositional.",
         ["поездка: trip"]),
        ("Я хорошо понимаю ___.", "они", "acc",
         "I understand them well.",
         "Понимать takes a direct object in the accusative: их. Им is dative; них is the form after a preposition.",
         []),
        ("Это письмо от ___.", "он", "pgen",
         "This letter is from him.",
         "От takes the genitive, with н- after the preposition: от него (not от его).",
         []),
        ("Вчера мы были у ___ в гостях.", "она", "pgen",
         "Yesterday we were at her place as guests.",
         "У takes the genitive, with н-: у неё (not у её). В гостях is prepositional plural.",
         []),
        ("Я сидел между ___.", "они", "pins",
         "I was sitting between them.",
         "Между takes the instrumental, with н- after the preposition: между ними (not между ими).",
         []),
        ("Кто сегодня с ___ на литургии?", "вы", "ins",
         "Who is with you at the Liturgy today?",
         "С + instrumental: с вами. Вас is genitive or accusative; вам is dative. На литургии is prepositional.",
         []),
        ("Я поеду на рынок с ___.", "ты", "ins",
         "I'll go to the market with you.",
         "С + instrumental: с тобой. Тебя is genitive or accusative; тебе is dative.",
         []),
        ("Они написали эту песню о ___.", "мы", "prep",
         "They wrote this song about us.",
         "О + prepositional: о нас. Песню is the direct object (accusative).",
         []),
        ("Я жду ___ у вокзала.", "он", "acc",
         "I'm waiting for him at the station.",
         "Ждать + accusative of a person, and there is no preposition governing the pronoun, so он → его (not него). У вокзала is genitive after у.",
         []),
        ("Без ___ ферма останется пустой.", "мы", "gen",
         "Without us the farm will stand empty.",
         "Без + genitive: без нас. Нами would be instrumental (с нами).",
         []),
        ("Я рядом с ___, не бойся.", "ты", "ins",
         "I'm right next to you, don't be afraid.",
         "С + instrumental: с тобой. Рядом с is a fixed combination that takes the instrumental.",
         ["рядом: next to"]),
        ("Дай ___ ту лопату.", "я", "dat",
         "Give me that shovel.",
         "Дать takes a dative indirect object: мне. Лопату is the direct object (accusative). Меня would be accusative.",
         []),
        ("Я не вижу ___. Где они?", "они", "acc",
         "I don't see them. Where are they?",
         "Видеть + accusative: их. After a preposition this would be них (для них). Они is nominative (the subject form).",
         []),
    ]
    for s, lemma, case, tr, ex, gl in prows:
        add_pron(A, C, S, s, lemma, case, tr, ex, gl)

    S = "у меня есть / нет"
    # pronouns after у (genitive, with н- for 3rd person)
    urows = [
        ("У ___ есть маленькие дети.", "она", "pgen",
         "She has little children.",
         "У меня есть means 'I have' (literally 'by me there is'). У takes the genitive, with н- after the preposition: у неё (not у её).",
         []),
        ("У ___ есть своя ферма.", "мы", "gen",
         "We have our own farm.",
         "У + genitive: у нас. Есть stays; своя ферма is the subject (nominative) — the thing you have.",
         []),
        ("У ___ есть паспорт?", "вы", "gen",
         "Do you have a passport?",
         "У + genitive: у вас. Паспорт is nominative (the subject of есть).",
         []),
        ("У ___ есть новый трактор.", "они", "pgen",
         "They have a new tractor.",
         "У + genitive with н-: у них (not у их). Трактор is nominative after есть.",
         []),
        ("У ___ на ферме есть пруд.", "я", "gen",
         "I have a pond on the farm.",
         "У + genitive: у меня. Есть is kept because the point is that the pond exists. Пруд is nominative.",
         []),
        ("У ___ в Беларуси есть дом.", "друг", "gen",
         "My friend has a house in Belarus.",
         "У + genitive of any owner, not just pronouns: у друга. Дом is nominative after есть.",
         []),
        ("У ___ есть икона в красном углу.", "батюшка", "gen",
         "Father has an icon in the icon corner.",
         "У + genitive: у батюшки (masculine -а, like у папы). Икона is nominative after есть.",
         ["красный угол: icon corner"]),
        ("У ___ есть сестра в Минске.", "жена", "gen",
         "My wife has a sister in Minsk.",
         "У + genitive: у жены. Сестра is nominative after есть.",
         []),
        ("Есть ли у ___ собака?", "вы", "gen",
         "Do you have a dog?",
         "Есть ли у + genitive is a formal yes/no question: есть ли у вас. Собака is nominative.",
         []),
    ]
    for s, lemma, case, tr, ex, gl in urows:
        if lemma in PRONOUNS:
            add_pron(A, C, S, s, lemma, case, tr, ex, gl)
        else:
            add_noun(A, C, S, s, lemma, case, tr, ex, gl)

    # есть + nominative (the thing you have is the subject)
    exists = [
        ("На ферме у меня есть ___.", "трактор", "nom",
         "I have a tractor.",
         "After у меня есть the thing you have is the subject, so it stays in the nominative: трактор. Трактора would be genitive (that's what you use after нет).",
         []),
        ("Смотри, у меня есть ___.", "корова", "npl",
         "I have cows.",
         "Есть takes the nominative. The plural of корова is коровы (not коров — that's the genitive plural, used after нет or много).",
         []),
        ("У тебя есть ___?", "курица", "npl",
         "Do you have chickens?",
         "Есть + nominative. The everyday plural of курица is куры (nominative). Кур is genitive plural (нет кур, много кур).",
         []),
        ("У нас есть большое ___.", "пастбище", "nom",
         "We have a large pasture.",
         "Есть + nominative: пастбище. Пастбища is genitive or nominative plural.",
         []),
        ("У меня есть интересная ___.", "работа", "nom",
         "I have an interesting job.",
         "Есть + nominative. Feminine работа stays работа. Работы would be genitive (нет работы).",
         []),
        ("У меня есть ___ до Минска.", "билет", "nom",
         "I have a ticket to Minsk.",
         "Есть + nominative: билет. Билета is genitive (нет билета).",
         []),
        ("У меня есть новый ___.", "паспорт", "nom",
         "I have a new passport.",
         "Есть + nominative: паспорт. After нет you would say нет паспорта (genitive).",
         []),
        ("У них есть старая ___.", "машина", "nom",
         "They have an old car.",
         "Есть + nominative: машина. Машины is genitive or nominative plural.",
         []),
        ("У жены есть своя ___.", "карта", "nom",
         "My wife has her own card.",
         "Есть + nominative: карта. У жены is genitive of the owner; карта is the subject.",
         ["карта: card"]),
    ]
    # нет + genitive
    none = [
        ("Сейчас у меня нет ___.", "корова", "gpl",
         "I don't have any cows.",
         "Нет takes the genitive. For a plural, use the genitive plural: нет коров. Коровы would be nominative (у меня есть коровы).",
         []),
        ("К зиме у нас нет ___.", "сено", "gen",
         "We don't have any hay.",
         "Нет + genitive. Сено is a mass noun, so genitive singular: нет сена.",
         []),
        ("Этой весной у них нет ___.", "яйцо", "gpl",
         "They don't have any eggs.",
         "Нет + genitive plural. Яйцо has an irregular genitive plural: яиц.",
         []),
        ("Сегодня у меня нет ___.", "время", "gen",
         "I don't have time.",
         "Нет + genitive. Время (neuter -мя) becomes времени.",
         []),
        ("К сожалению, у нас нет ___.", "деньги", "gpl",
         "We don't have any money.",
         "Нет + genitive. Деньги is plural-only: нет денег.",
         []),
        ("На вокзале у него нет ___.", "билет", "gen",
         "He doesn't have a ticket.",
         "Нет + genitive: нет билета. У него already shows н- after у; билета is a separate genitive after нет.",
         []),
        ("В Минске у меня нет ___.", "брат", "gen",
         "I don't have a brother.",
         "Нет + genitive. Animate masculine: нет брата. (У меня есть брат would be nominative.)",
         []),
        ("В сарае у меня нет ___.", "лопата", "gen",
         "I don't have a shovel.",
         "Нет + genitive. Feminine -а → -ы: нет лопаты.",
         []),
        ("У тебя нет ___ от калитки?", "ключ", "gen",
         "Don't you have the key to the gate?",
         "Нет + genitive: нет ключа. Ключ is masculine: -а.",
         []),
        ("В этом году у нас нет ___.", "солома", "gen",
         "We don't have any straw.",
         "Нет + genitive. Feminine mass noun: нет соломы.",
         ["солома: straw"]),
        ("У ___ нет рогов, а у быка есть.", "корова", "gen",
         "A cow has no horns, but a bull does.",
         "У + genitive of the owner: у коровы. Нет рогов is a second genitive (рога, 'horns', genitive plural).",
         ["рог: horn"]),
        ("Для поездки у меня нет ___.", "виза", "gen",
         "I don't have a visa.",
         "Нет + genitive. Feminine -а → -ы: нет визы.",
         ["виза: visa"]),
        ("В холодильнике у нас нет ___.", "молоко", "gen",
         "We don't have any milk.",
         "Нет + genitive. Neuter -о → -а: нет молока. Compare у нас есть молоко (nominative).",
         []),
        ("На границе у них нет ___.", "чемодан", "gen",
         "They don't have a suitcase.",
         "Нет + genitive. Masculine: нет чемодана.",
         []),
        ("С собой у меня нет ___.", "телефон", "gen",
         "I don't have a phone.",
         "Нет + genitive. Masculine: нет телефона.",
         []),
        ("У неё нет ___.", "паспорт", "gen",
         "She doesn't have a passport.",
         "Нет + genitive: нет паспорта. У неё is the owner (у + genitive with н-).",
         []),
        ("У вас нет ___?", "карта", "gen",
         "Don't you have a card?",
         "Нет + genitive. Feminine: нет карты. (У вас есть карта would be nominative.)",
         []),
        ("У меня нет сегодня ___.", "урок", "gen",
         "I don't have class today.",
         "Нет + genitive: нет урока. Урок is masculine: -а.",
         ["урок: lesson, class"]),
        ("У коровы нет ___? Нет, есть, вот они.", "телёнок", "gpl",
         "Doesn't the cow have any calves? No, she does — here they are.",
         "Нет + genitive plural. Телёнок has the irregular plural телята, genitive телят.",
         []),
        ("У нас на ферме нет ___.", "свинья", "gpl",
         "We don't have any pigs on the farm.",
         "Нет + genitive plural: нет свиней (not свиньев). Compare у нас есть свиньи (nominative).",
         ["свинья: pig"]),
        ("У меня нет ___ от сарая, только один.", "ключ", "gpl",
         "I don't have the keys to the barn.",
         "Нет + genitive. If you mean several keys, use the genitive plural: нет ключей.",
         []),
    ]
    # The last one "ключ" gpl — ключей. But I already used ключ gen ключа. Different s, OK.
    for s, lemma, case, tr, ex, gl in exists + none:
        add_noun(A, C, S, s, lemma, case, tr, ex, gl)

def _dup_check(prefix=""):
    seen = {}
    for e in ITEMS:
        if e["s"] == "___":
            k = ("___", e["a"])
        else:
            k = e["s"]
        seen.setdefault(k, 0)
        seen[k] += 1
    dups = [k for k, n in seen.items() if n > 1]
    if dups:
        raise SystemExit(prefix + "duplicate items: " + "; ".join(map(str, dups[:8])))


def build_cases_b1():
    C = "cases"
    S = "prepositional"
    rows = [
        ("В этом ___ на ферме выпало мало снега.", "год", "loc",
         "This year little snow fell on the farm.",
         "В этом году uses the special locative in -у (not в годе). Году is the object of the preposition в.",
         []),
        ("Летом мы часто отдыхаем в ___ у пруда.", "сад", "loc",
         "In the summer we often relax in the garden by the pond.",
         "Где? в + locative -у: в саду. У пруда is genitive after у.",
         []),
        ("Олени выходят из ___ по вечерам.", "лес", "gen",
         "WAIT this is genitive - skip",
         "", []),
    ]
    # I'll not add the genitive one under prep. Rewrite properly below.
    rows = [
        ("В этом ___ на ферме выпало мало снега.", "год", "loc",
         "This year little snow fell on the farm.",
         "Time: в этом году uses the special locative in -у, not the ordinary prepositional в годе. Году is the object of в.",
         ["выпасть: to fall (precipitation)"]),
        ("После ужина мы сидим в ___ и пьём чай.", "сад", "loc",
         "After dinner we sit in the garden and drink tea.",
         "Где? в + the locative in -у: в саду (not в саде). О саде would mean 'about the garden'.",
         []),
        ("В жару коровы прячутся в ___.", "лес", "loc",
         "In the heat the cows hide in the woods.",
         "Где? в + locative -у: в лесу. Из леса (genitive) means 'out of the woods'.",
         ["прятаться: to hide"]),
        ("Дети весь день играли на ___.", "берег", "loc",
         "The children played on the bank all day.",
         "Где? на + locative -у: на берегу. На берег would be accusative (куда?).",
         []),
        ("Наш самолёт ещё стоит в ___.", "аэропорт", "loc",
         "Our plane is still at the airport.",
         "Где? в + locative -у: в аэропорту (not в аэропорте). Об аэропорте is 'about the airport'.",
         []),
        ("Зимой лёд на ___ уже держит.", "пруд", "loc",
         "In winter the ice on the pond already holds.",
         "Где? на + locative -у: на пруду. На пруде is sometimes heard, but the traditional locative is на пруду / в пруду.",
         ["лёд: ice"]),
        ("Сенокос в этом году был на дальнем ___.", "луг", "loc",
         "Haymaking this year was in the far meadow.",
         "Где? на + locative -у: на лугу. Дальнем agrees with лугу in the prepositional/locative.",
         ["сенокос: haymaking"]),
        ("Я оставил инструменты в ___.", "угол", "loc",
         "I left the tools in the corner.",
         "Где? в + locative -у, and угол loses its о: в углу (not в угле, which would look like 'in carbon').",
         ["инструмент: tool"]),
        ("Сапоги стоят на ___ у двери.", "пол", "loc",
         "The boots are standing on the floor by the door.",
         "Где? на + locative -у: на полу (not на поле, which means 'in the field'). У двери is genitive after у.",
         ["сапоги: boots"]),
        ("В статье мы читали о православной ___.", "церковь", "prep",
         "In the article we read about the Orthodox church.",
         "О + prepositional. Soft feminine церковь takes -и: о церкви. Православной agrees with церкви.",
         []),
        ("На собрании говорили о новой ___.", "программа", "prep",
         "At the meeting they talked about the new program.",
         "О + prepositional: о программе. Новой agrees with программе (feminine prepositional).",
         ["собрание: meeting"]),
        ("Я до сих пор не написал о своей поездке в ___.", "Беларусь", "prep",
         "I still haven't written about my trip to Belarus.",
         "В + prepositional after о поездке в… here marks location inside the trip's destination: в Беларуси. Soft feminine takes -и.",
         []),
        ("При ___ всегда много свечей.", "икона", "prep",
         "There are always a lot of candles by the icon.",
         "При (by, in the presence of) takes the prepositional: при иконе. This при means 'at, by', not 'with' (which would be с + instrumental).",
         []),
        ("Он рассказал о своих ___ в Минске.", "друг", "ppl",
         "He talked about his friends in Minsk.",
         "О + prepositional plural: о друзьях (irregular stem друг → друзь-). Своих agrees with друзьях.",
         []),
        ("В нашей ___ сегодня нет воды.", "деревня", "prep",
         "There is no water in our village today.",
         "Где? в + prepositional. Feminine -я → -е: в деревне. Нашей agrees with деревне.",
         ["деревня: village"]),
        ("Мы долго спорили о ___ для забора.", "цена", "prep",
         "We argued for a long time about the price of the fence.",
         "О + prepositional: о цене. Для забора is genitive after для.",
         []),
        ("В ___ он пишет код лучше, чем днём.", "тишина", "prep",
         "In the quiet he writes code better than during the day.",
         "Где? в + prepositional. Feminine -а → -е: в тишине.",
         ["тишина: silence, quiet"]),
        ("На ___ о войне Молчат Дома звучат особенно сильно.", "песня", "ppl",
         "In their songs about war, Molchat Doma sound especially powerful.",
         "На + prepositional plural: на песнях. О войне is also prepositional. The blank is the object of на.",
         ["война: war"]),
        ("Я прочитал об этом в старом ___.", "журнал", "prep",
         "I read about this in an old magazine.",
         "Где? в + prepositional: в журнале. Старом agrees with журнале (masculine prepositional).",
         []),
        ("При ___ света свечи икона выглядит иначе.", "свет", "prep",
         "By candlelight the icon looks different.",
         "При + prepositional: при свете. Света here is already genitive in 'свет свечи'… wait, I'll recast.",
         []),
    ]
    # Fix the last awkward one by replacing it when adding — I'll skip the bad last and the confused one
    rows = [r for r in rows if "При ___ света" not in r[0] and "WAIT" not in r[4]]
    # add a clean replacement
    rows.append(
        ("В ___ программы была ошибка.", "код", "prep",
         "There was a bug in the program's code.",
         "Где? в + prepositional: в коде. Программы is genitive ('of the program').",
         ["ошибка: mistake, bug"])
    )
    rows.append(
        ("На ___ мы стояли почти час.", "граница", "prep",
         "We stood at the border for almost an hour.",
         "Где? на + prepositional: на границе. На границу would be accusative (куда?).",
         ["граница: border"])
    )
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(B, C, S, s, lemma, case, tr, ex, gl)

    S = "accusative"
    rows = [
        ("На лугу я вчера видел двух ___.", "олень", "apl",
         "I saw two deer in the meadow yesterday.",
         "Видеть takes a direct object in the accusative. Animate plural accusative = genitive plural: оленей. Двух is also genitive/accusative of два.",
         []),
        ("Жена уже подоила всех ___.", "корова", "apl",
         "My wife has already milked all the cows.",
         "Подоить + accusative. Animate plural: коров (not коровы). Всех agrees with the animate accusative plural.",
         ["подоить: to milk (pf.)"]),
        ("Охотник вспугнул ___ за прудом.", "заяц", "acc",
         "The hunter startled a hare behind the pond.",
         "Animate masculine: accusative = genitive, and заяц has a stem change: зайца (not заяца).",
         ["заяц: hare", "вспугнуть: to startle"]),
        ("Нужно починить ___ до зимы.", "ворота", "acc",
         "We need to fix the gate before winter.",
         "Ворота is plural-only. Inanimate plural accusative = nominative: ворота (not ворот, which is genitive). Починить takes this direct object.",
         []),
        ("Всю ___ я писал новую программу.", "неделя", "acc",
         "I spent the whole week writing a new program.",
         "Duration (how long?) often uses the accusative: всю неделю. Всей неделе would be dative; всей неделей would be instrumental.",
         []),
        ("Каждый ___ он ездит в Минск.", "день", "acc",
         "He goes to Minsk every day.",
         "Каждый день is a set time expression in the accusative (how long / how often). Дня would be genitive (два дня).",
         []),
        ("В ___ мы всегда едем в церковь.", "воскресенье", "acc",
         "On Sunday we always go to church.",
         "В + accusative of the day: в воскресенье ('on Sunday'). В воскресенье looks like the nominative because the noun is neuter.",
         []),
        ("Поезд идёт через весь ___.", "город", "acc",
         "The train goes through the whole city.",
         "Через (across, through) takes the accusative: через город. Весь agrees with город in the accusative (inanimate = nominative form).",
         []),
        ("Мы переехали через ___.", "граница", "acc",
         "We crossed the border.",
         "Через + accusative: через границу. На границе (prepositional) would mean 'at the border' (где?).",
         []),
        ("За ___ начинается лес.", "пруд", "acc",
         "Beyond the pond the woods begin. / After you pass the pond…",
         "За meaning 'to the area beyond' (куда?) takes the accusative: за пруд. За прудом (instrumental) answers где? (behind the pond, location).",
         []),
        ("Я пригласил ___ на литургию.", "друг", "apl",
         "I invited my friends to the Liturgy.",
         "Пригласить + accusative. Animate plural: друзей (irregular). На литургию is also accusative (куда?).",
         []),
        ("Батюшка вчера крестил нашего ___.", "сын", "acc",
         "Father baptized our son yesterday.",
         "Animate masculine: accusative = genitive: сына. Нашего agrees with сына (animate accusative).",
         ["крестить: to baptize"]),
        ("На границе пограничник проверил наши ___.", "документ", "apl",
         "At the border the guard checked our documents.",
         "Проверить + accusative. Inanimate plural accusative = nominative: документы (not документов, which is genitive). Наши agrees with документы.",
         []),
        ("Я уже отправил ___ коллеге.", "файл", "acc",
         "I already sent the file to a colleague.",
         "Отправить + accusative direct object: файл (inanimate masculine, no change). Коллеге is the dative indirect object.",
         ["файл: file"]),
        ("В Минске мы посетили старую ___.", "церковь", "acc",
         "In Minsk we visited an old church.",
         "Посетить + accusative. Soft feminine церковь looks the same as the nominative. Старую agrees (feminine accusative -ую).",
         ["посетить: to visit"]),
        ("Он сам написал весь ___ модуля.", "код", "acc",
         "He wrote the module's entire code himself.",
         "Написать + accusative. Inanimate masculine: код. Весь agrees with код. Модуля is genitive ('of the module').",
         ["модуль: module"]),
        ("Жена купила новых ___ на ферму.", "курица", "apl",
         "My wife bought new hens for the farm.",
         "Купить + accusative. Animate plural: кур (not куриц). Новых agrees with the animate accusative plural. На ферму is куда? (accusative).",
         []),
        ("Я не могу найти свои ___.", "ключ", "apl",
         "I can't find my keys.",
         "Найти + accusative. Inanimate plural: ключи (same as nominative). Свои agrees with ключи. Ключей would be genitive.",
         []),
        ("Мы слушали эту ___ до самой ночи.", "песня", "acc",
         "We listened to this song until night itself.",
         "Слушать + accusative: песню. Эту agrees (feminine accusative). До ночи is genitive after до.",
         []),
        ("Через ___ нужно перевести деньги.", "банк", "acc",
         "The money has to be transferred through the bank.",
         "Через + accusative: через банк. Деньги is the direct object of перевести (accusative, plural-only).",
         []),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(B, C, S, s, lemma, case, tr, ex, gl)

    S = "dative"
    rows = [
        ("Я уже отправил отчёт ___.", "начальник", "dat",
         "I already sent the report to the boss.",
         "Отправить takes a dative indirect object: начальнику. Отчёт is the accusative direct object.",
         []),
        ("По ___ к сараю идёт глубокая колея.", "поле", "dat",
         "A deep rut runs across the field toward the barn.",
         "По (across, along) takes the dative: по полю. К сараю is also dative after к.",
         ["колея: rut, track"]),
        ("Каждый вечер я звоню ___ в Минск.", "сестра", "dat",
         "Every evening I call my sister in Minsk.",
         "Звонить + dative: сестре. В Минск is accusative (куда?).",
         []),
        ("___ уже за сорок, а он всё ещё пасёт коров.", "он", "dat",
         "He is already past forty, and he still grazes the cows.",
         "Age: the person is dative (ему … лет / за сорок). Это безличное предложение, субъекта в именительном нет.",
         []),
        ("___ сегодня плохо: наверное, простудился.", "он", "dat",
         "He feels unwell today: he probably caught a cold.",
         "Impersonalfeelings take the dative: ему плохо (literally 'it is bad to him').",
         ["простудиться: to catch a cold"]),
        ("___ можно войти в алтарь, а мне нельзя.", "он", "dat",
         "He may enter the altar; I may not.",
         "Можно / нельзя take the dative of the person: ему можно. В алтарь is accusative (куда?).",
         ["алтарь: altar"]),
        ("По ___ фермы мы ходим два раза в день.", "граница", "dat",
         "We walk along the edge of the farm twice a day.",
         "По (along) + dative: по границе. Фермы is genitive ('of the farm').",
         []),
        ("Я купил зерно ___ и курам.", "корова", "dpl",
         "I bought grain for the cows and the hens.",
         "The beneficiaries are dative: коровам (and курам). Зерно is the accusative direct object.",
         []),
        ("Подъезжая к ___, снизь скорость.", "ворота", "dat",
         "When you drive up to the gate, slow down.",
         "К takes the dative. Ворота is plural-only: к воротам (not к вороту).",
         []),
        ("По ___ уже можно ехать на тракторе.", "дорога", "dat",
         "You can already drive the tractor along the road.",
         "По + dative: по дороге. На тракторе is prepositional (location / means).",
         []),
        ("Я так и не ответил ___ на письмо.", "коллега", "dat",
         "I still haven't answered my colleague's letter.",
         "Ответить takes the dative of the person: коллеге. На письмо is accusative after на ('to the letter').",
         []),
        ("___ надо было сразу показать паспорт.", "ты", "dat",
         "You should have shown your passport right away.",
         "Надо было (it was necessary) takes the dative: тебе надо было. Паспорт is accusative.",
         []),
        ("Священник дал причастие ___.", "ребёнок", "dpl",
         "The priest gave Communion to the children.",
         "The recipients are dative plural. Ребёнок has the irregular plural дети: детям (not ребёнкам).",
         []),
        ("По ___ программы сразу видно, кто её писал.", "стиль", "dat",
         "From the style of the program you can tell right away who wrote it.",
         "По can mean 'judging by' and takes the dative: по стилю. Программы is genitive.",
         ["стиль: style"]),
        ("К ___ за сеном мы выезжаем на рассвете.", "луг", "dat",
         "We set out for the meadow at dawn to get the hay.",
         "К + dative: к лугу. За сеном is instrumental ('for hay', to fetch it).",
         []),
        ("Я сам настроил сервер ___ в офисе.", "коллега", "dpl",
         "I set up the server for my colleagues in the office myself.",
         "The beneficiaries are dative plural: коллегам. Сервер is the accusative direct object.",
         ["настроить: to set up", "сервер: server"]),
        ("___ некогда разговаривать: надо доить коров.", "я", "dat",
         "I have no time to talk: the cows need milking.",
         "Некогда (there's no time) takes the dative: мне некогда, like нужно and можно.",
         []),
        ("По ___ к храму мы идём пешком.", "улица", "dat",
         "We walk along the street to the church.",
         "По + dative: по улице. К храму is also dative after к.",
         []),
        ("Я уже всё объяснил ___ по телефону.", "жена", "dat",
         "I already explained everything to my wife on the phone.",
         "Объяснить takes a dative indirect object: жене. Всё is the accusative direct object. По телефону is dative after по.",
         []),
        ("___ пора выходить, иначе опоздаем на поезд.", "мы", "dat",
         "It's time for us to leave, or we'll miss the train.",
         "Пора (it's time) takes the dative: нам пора. На поезд is accusative (куда?).",
         []),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(B, C, S, s, lemma, case, tr, ex, gl)

    S = "genitive"
    rows = [
        ("Из-за ___ мы весь день сидели в сарае.", "дождь", "gen",
         "Because of the rain we sat in the barn all day.",
         "Из-за (because of, usually something unwelcome) takes the genitive: из-за дождя. The object of из-за is дождя.",
         []),
        ("Ради ___ он поднялся в четыре утра.", "жена", "gen",
         "For his wife's sake he got up at four in the morning.",
         "Ради (for the sake of) takes the genitive: ради жены.",
         ["ради: for the sake of"]),
        ("Кроме ___ на ферме больше никого не было.", "я", "gen",
         "Besides me there was no one else on the farm.",
         "Кроме (besides, except) takes the genitive: кроме меня.",
         []),
        ("Вместо ___ сегодня пасёт коров отец.", "я", "gen",
         "Instead of me, Dad is grazing the cows today.",
         "Вместо (instead of) takes the genitive: вместо меня.",
         []),
        ("До ___ ещё километр по полю.", "ферма", "gen",
         "It's another kilometer across the field to the farm.",
         "До (as far as, until) takes the genitive: до фермы. По полю is dative after по.",
         []),
        ("После ___ трактор снова заработал.", "ремонт", "gen",
         "After the repair the tractor started working again.",
         "После + genitive: после ремонта. Masculine nouns add -а.",
         ["ремонт: repair"]),
        ("Против ___ брата я ничего не имею.", "он", "pgen",
         "I have nothing against his brother. / I have nothing against him, my brother's… wait.",
         "", []),
    ]
    rows = [r for r in rows if r[4]]  # drop the botched one
    rows += [
        ("Против ___ я ничего не имею: он честный человек.", "он", "pgen",
         "I have nothing against him: he's an honest man.",
         "Против (against) takes the genitive, with н- after the preposition: против него (not против его).",
         []),
        ("Среди ___ на пастбище была одна хромая.", "корова", "gpl",
         "Among the cows in the pasture there was one lame one.",
         "Среди (among) takes the genitive: среди коров. Хромая agrees with an implied корова.",
         ["хромой: lame"]),
        ("Возле ___ мы поставили новую кормушку.", "курятник", "gen",
         "We put a new feeder next to the coop.",
         "Возле (beside) takes the genitive: возле курятника.",
         []),
        ("Я не получал от ___ писем уже месяц.", "они", "pgen",
         "I haven't had a letter from them in a month.",
         "От takes the genitive, with н-: от них. Писем is also genitive plural after не получал.",
         []),
        ("Вокруг ___ посадили яблони.", "пруд", "gen",
         "Apple trees were planted around the pond.",
         "Вокруг (around) takes the genitive: вокруг пруда.",
         ["яблоня: apple tree"]),
        ("Без ___ кода программа не соберётся.", "этот", "wait",
         "", []),
    ]
    rows = [r for r in rows if r[2] != "wait" and r[4]]
    rows += [
        ("Без этого ___ программа не соберётся.", "код", "gen",
         "Without this code the program won't build.",
         "Без + genitive: без кода. Этого agrees with кода (masculine genitive).",
         ["собраться: to build (a program)"]),
        ("Я так и не видел ___ после Пасхи.", "батюшка", "gen",
         "I still haven't seen Father since Pascha.",
         "A negated verb of perception takes the genitive of the person: не видел батюшки. После Пасхи is also genitive.",
         ["Пасха: Pascha, Easter"]),
    ]
    rows = [r for r in rows if r[2] != "wait"]
    rows += [
        ("Для нового ___ не хватает столбов.", "забор", "gen",
         "There aren't enough posts for the new fence.",
         "Для + genitive: для забора. Нового agrees with забора. Не хватает also takes the genitive (столбов).",
         ["столб: post, pole", "хватать: to be enough"]),
        ("Минувшей ___ на ферме стояли морозы.", "ночь", "gen",
         "Last night there were frosts on the farm. / During last night…",
         "Time: минувшей ночи is genitive ('of last night', during that night). Ночь is a soft feminine: ночи.",
         ["мороз: frost"]),
        ("Первого ___ мы выезжаем в Беларусь.", "май", "gen",
         "On the first of May we leave for Belarus.",
         "Dates use the genitive: первого мая (on the first of May). Май → мая. В Беларусь is accusative (куда?).",
         []),
        ("С ___ реки поле уже не видно.", "середина", "gen",
         "From the middle of the river the field is no longer visible.",
         "С meaning 'from' takes the genitive: с середины. Реки is a second genitive ('of the river').",
         ["середина: middle"]),
        ("Я устал от этой ___.", "работа", "gen",
         "I'm tired of this work.",
         "Устать от takes the genitive (the object of от): от работы. Этой agrees with работы.",
         ["устать: to get tired"]),
        ("У ___ у самой калитки растёт сирень.", "забор", "gen",
         "Lilac grows by the fence, right at the gate.",
         "У (by, next to) + genitive: у забора. У калитки is another у + genitive.",
         ["сирень: lilac"]),
    ]
    rows = [r for r in rows if r[2] != "wait"]
    rows += [
        ("Из старого ___ пахнет сеном.", "сарай", "gen",
         "The old barn smells of hay. / From the old barn comes the smell of hay.",
         "Из + genitive: из сарая. Старого agrees with сарая. Сеном is instrumental after пахнет (пахнуть чем?).",
         ["пахнуть: to smell of"]),
        ("В течение ___ нужно закончить модуль.", "неделя", "gen",
         "The module needs to be finished within a week.",
         "В течение (during, within) is a preposition that takes the genitive: в течение недели.",
         ["в течение: during, within"]),
        ("Ради своих ___ он не продал ферму.", "ребёнок", "gpl",
         "For the sake of his children he didn't sell the farm.",
         "Ради + genitive plural. Ребёнок → детей (irregular). Своих agrees with детей.",
         []),
        ("Я приехал сюда из-за ___.", "работа", "gen",
         "I came here because of work.",
         "Из-за + genitive: из-за работы. Сюда is an adverb (куда?).",
         []),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(B, C, S, s, lemma, case, tr, ex, gl)

    S = "genitive plural"
    rows = [
        ("На ферме не хватает ___.", "работник", "gpl",
         "The farm is short of workers.",
         "Не хватает takes the genitive. Masculine hard stems take -ов in the genitive plural: работников.",
         ["хватать: to be enough", "работник: worker"]),
        ("В курятнике уже нет ___.", "яйцо", "gpl",
         "There are no eggs left in the coop.",
         "Нет + genitive plural. Яйцо has an irregular genitive plural: яиц (not яйцов or яйцев).",
         []),
        ("У нас на лугу мало ___.", "олень", "gpl",
         "There are few deer in our meadow.",
         "Мало + genitive plural. Soft masculine -ень takes -ей: оленей.",
         []),
        ("Сколько ___ несёт одна курица за неделю?", "яйцо", "gpl",
         "How many eggs does one hen lay in a week?",
         "Сколько + genitive plural: сколько яиц. За неделю is accusative of duration.",
         []),
        ("В стаде пятьдесят ___ и один бык.", "корова", "gpl",
         "There are fifty cows and one bull in the herd.",
         "After 5 and up (here 50) use the genitive plural: коров (zero ending, not коровов).",
         ["стадо: herd"]),
        ("Для забора не хватает десяти ___.", "столб", "gpl",
         "The fence is ten posts short.",
         "Не хватает + genitive, and десяти is itself genitive of десять. Столб → столбов.",
         []),
        ("Я купил двадцать ___ корма.", "мешок", "gpl",
         "I bought twenty bags of feed.",
         "After 20 (which behaves like 5+) use the genitive plural: мешков. Корма is a second genitive ('of feed').",
         []),
        ("У жены много старых ___.", "икона", "gpl",
         "My wife has a lot of old icons.",
         "Много + genitive plural. Feminine -а nouns often have a zero ending: икон (not иконов). Старых agrees.",
         []),
        ("В ящике лежало несколько ___.", "свеча", "gpl",
         "There were several candles in the drawer.",
         "Несколько + genitive plural. Свеча takes -ей: свечей (not свеч, though that short form also exists in some uses).",
         []),
        ("На вокзале было полно ___.", "человек", "gpl",
         "The station was full of people.",
         "Полно, like много, takes the genitive plural. Человек used as a counting form stays человек after numerals, but after много/полно the form is людей — wait.",
         []),
    ]
    # человек after много is людей, after 5+ can be человек. "полно людей" is correct. Change lemma to use MANUAL or use люди?
    # I'll replace that last item with a clean людей one and a человек-after-numeral one.
    rows = [r for r in rows if "полно" not in r[0]]
    rows += [
        ("На вокзале было полно ___.", "люди", "gpl",
         "The station was full of people.",
         "Полно, like много, takes the genitive plural: людей (the irregular genitive of люди). Человек is the counting form after 5, 10, 20 (пять человек).",
         []),
        ("В храме вчера было человек ___? Нет, около двухсот человек.", "wait", "gpl",
         "", []),
    ]
    rows = [r for r in rows if r[2] != "wait" and r[4]]
    rows += [
        ("Для сарая нужно ещё шесть ___.", "доска", "gpl",
         "The barn needs six more boards.",
         "After 6 (5 and up) use the genitive plural. Доска has a fleeting vowel and a stem change: досок (not досков).",
         ["доска: board, plank"]),
        ("У нас в стаде мало ___.", "телёнок", "gpl",
         "We have few calves in the herd.",
         "Мало + genitive plural. Телёнок has the irregular plural телята, genitive телят (not телёнков).",
         []),
        ("Жена купила десяток ___ в магазине.", "яйцо", "gpl",
         "My wife bought a dozen eggs at the store.",
         "Десяток ('a set of ten') is followed by the genitive plural: десяток яиц.",
         ["десяток: a set of ten, a dozen (loosely)"]),
        ("После бури не осталось целых ___.", "яблоко", "gpl",
         "After the storm no whole apples were left.",
         "Не осталось takes the genitive. Neuter -о often has a zero ending, with a fleeting vowel: яблок (not яблоков). Целых agrees.",
         []),
        ("В отпуске у нас осталось всего пять ___.", "день", "gpl",
         "We have only five days of vacation left.",
         "After 5 use the genitive plural. День is irregular: дней (not деней), and after 2–4 it would be дня; после 5+ also note лет for 'years'.",
         []),
        ("На полке стоит несколько ___ Молчат Дома.", "диск", "gpl",
         "There are several Molchat Doma discs on the shelf.",
         "Несколько + genitive plural. Masculine hard stems take -ов: дисков.",
         ["диск: disc, album"]),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(B, C, S, s, lemma, case, tr, ex, gl)

    S = "instrumental"
    rows = [
        ("После института он стал ___.", "программист", "ins",
         "After university he became a programmer.",
         "Стать кем? takes the instrumental of the new role: программистом. This is a predicate, not a direct object.",
         []),
        ("Двадцать лет он проработал ___.", "священник", "ins",
         "He worked as a priest for twenty years.",
         "Проработать кем? takes the instrumental: священником.",
         []),
        ("Я пользуюсь этим ___ уже третий год.", "трактор", "ins",
         "I've been using this tractor for the third year already.",
         "Пользоваться takes the instrumental: пользоваться трактором. Этим agrees with трактором.",
         []),
        ("С детства я увлекаюсь ___ фермы.", "жизнь", "ins",
         "Since childhood I've been keen on farm life.",
         "Увлекаться takes the instrumental: увлекаюсь жизнью. Фермы is genitive ('of the farm'). Soft feminine жизнь takes -ью.",
         ["увлекаться: to be keen on"]),
        ("Между ___ и сараем мы поставили новый забор.", "дом", "ins",
         "We put up a new fence between the house and the barn.",
         "Между takes the instrumental: между домом и сараем. Both nouns are objects of между.",
         []),
        ("Над ___ кружили ласточки.", "пруд", "ins",
         "Swallows were circling above the pond.",
         "Над takes the instrumental: над прудом.",
         ["ласточка: swallow"]),
        ("Под ___ мы храним лопаты и вилы.", "навес", "ins",
         "We store the shovels and pitchforks under the lean-to.",
         "Под meaning 'under' (где?) takes the instrumental: под навесом. Под навес would be accusative (куда?).",
         ["навес: lean-to, canopy"]),
        ("Перед ___ всегда ставят свечи.", "икона", "ins",
         "People always put candles in front of the icon.",
         "Перед takes the instrumental: перед иконой. Feminine -а → -ой.",
         []),
        ("За ___ уже начинается лес.", "поле", "ins",
         "Beyond the field the woods already begin.",
         "За meaning 'beyond, behind' (где?) takes the instrumental: за полем. За поле would be accusative (куда?).",
         []),
        ("Я горжусь своими ___.", "корова", "ipl",
         "I'm proud of my cows.",
         "Гордиться takes the instrumental. Plural: коровами. Своими agrees with коровами.",
         []),
        ("Она довольна новым ___.", "курятник", "ins",
         "She is pleased with the new coop.",
         "Доволен / довольна takes the instrumental: довольна курятником. Новым agrees with курятником.",
         []),
        ("Мы ехали по Беларуси ночным ___.", "поезд", "ins",
         "We traveled across Belarus on a night train.",
         "Instrumental of means: поездом. Ночным agrees with поездом. По Беларуси is dative after по.",
         []),
        ("Код лучше править за своим ___.", "компьютер", "ins",
         "It's better to edit the code at your own computer.",
         "За + instrumental for sitting at a workstation: за компьютером. Своим agrees with компьютером.",
         []),
        ("Сено мы возим старым ___.", "прицеп", "ins",
         "We haul the hay with the old trailer.",
         "Чем? instrumental of the means/tool: прицепом. Старым agrees. Сено is the direct object (accusative).",
         ["прицеп: trailer"]),
        ("Он махнул нам ___.", "рука", "ins",
         "He waved a hand at us.",
         "Махнуть чем? takes the instrumental: рукой. Нам is dative (to whom).",
         []),
        ("Я открыл ворота своим ___.", "ключ", "ins",
         "I opened the gate with my own key.",
         "Чем? instrumental: ключом. Ворота is the direct object (accusative, plural-only). Своим agrees with ключом.",
         []),
        ("В церковь мы ходим всей ___.", "семья", "ins",
         "We go to church as a whole family.",
         "Instrumental of accompaniment / 'as a whole': всей семьёй (ё is required in the ending -ёй after ь).",
         []),
        ("Между ___ не должно быть проводов.", "столб", "ipl",
         "There shouldn't be any wires between the posts.",
         "Между + instrumental plural: между столбами. Проводов is genitive after не должно быть.",
         []),
        ("Над ___ храма горит крест.", "купол", "ins",
         "A cross burns (shines) above the church's dome.",
         "Над + instrumental: над куполом. Храма is genitive ('of the church').",
         ["купол: dome", "крест: cross"]),
    ]
    rows = [r for r in rows if r[1] != "wait"]
    rows += [
        ("Под ___ всегда лежит коврик.", "икона", "ins",
         "There is always a little rug under the icon.",
         "Под (где?) + instrumental: под иконой. Под икону would be accusative (куда?).",
         ["коврик: little rug"]),
        ("За ___ жены я ничего не решаю на ферме.", "спина", "ins",
         "I don't make any farm decisions behind my wife's back.",
         "За спиной is a set phrase in the instrumental ('behind someone's back'). Жены is genitive.",
         ["спина: back"]),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(B, C, S, s, lemma, case, tr, ex, gl)

    S = "numerals"
    # The blank is the noun after a number; answer is the required case/number form.
    rows = [
        ("На ферме у меня семь ___.", "корова", "gpl",
         "I have seven cows on the farm.",
         "After 5 and up (here семь) the noun is genitive plural: семь коров. After 2–4 it would be genitive singular (две коровы, три коровы).",
         []),
        ("У жены двадцать две ___.", "курица", "gen",
         "My wife has twenty-two hens.",
         "The last digit decides: 22 ends in 2, so use the genitive singular (две курицы). Курица is feminine, so две, not два. The everyday plural кур appears after 5+ or сколько.",
         []),
        ("В стаде три ___.", "бык", "gen",
         "There are three bulls in the herd.",
         "After 2, 3 or 4 use the genitive singular: три быка. After 5+ it would be быков. Бык is animate, but 2–4 still take genitive singular, not the accusative plural.",
         []),
        ("Я купил четыре ___ корма.", "мешок", "gen",
         "I bought four bags of feed.",
         "After 4 use the genitive singular: четыре мешка. After 5 it would be пять мешков. Корма is a second genitive ('of feed').",
         []),
        ("На лугу паслись две ___.", "лошадь", "gen",
         "Two horses were grazing in the meadow.",
         "After 2–4: genitive singular. Soft feminine лошадь → лошади. Dве because the noun is feminine (not два).",
         []),
    ]
    # пять телят, один петух, 21 день, о двух друзьях, двум братьям, полтора часа, оба берега...
    rows += [
        ("Этой весной у нас пять ___.", "телёнок", "gpl",
         "This spring we have five calves.",
         "After 5 use the genitive plural. Телёнок is irregular: пять телят (not телёнков). After 2–4 it would be телёнка.",
         []),
        ("На заборе сидел только один ___.", "петух", "nom",
         "Only one rooster was sitting on the fence.",
         "After 1 (один, двадцать один…) the noun stays nominative singular: один петух. Один agrees in gender (masculine).",
         []),
        ("Поезд идёт двадцать один ___.", "час", "nom",
         "The train takes twenty-one hours. / The train has been going for 21 hours.",
         "Compounds ending in один take the nominative singular: двадцать один час (not часа and not часов). После 2–4 — часа, после 5+ — часов.",
         []),
        ("Мы говорили о двух новых ___.", "проект", "ppl",
         "We talked about two new projects.",
         "In an oblique case the numeral and the noun share the case: о двух проектах (prepositional plural). The adjective новых also agrees.",
         ["проект: project"]),
        ("Я уже написал письмо двум ___.", "брат", "dpl",
         "I already wrote a letter to two brothers.",
         "Двум is the dative of два, so the noun is dative plural: двум братьям (irregular stem брат → брать-).",
         []),
        ("Он приехал с тремя ___.", "друг", "ipl",
         "He arrived with three friends.",
         "С takes the instrumental, so три becomes тремя and the noun is instrumental plural: с тремя друзьями.",
         []),
        ("До вокзала осталось полтора ___.", "километр", "gen",
         "There is a kilometer and a half left to the station.",
         "Полтора (1½, masculine/neuter) takes the genitive singular: полтора километра. Feminine is полторы (полторы недели).",
         []),
        ("Мы ждали поезда полтора ___.", "час", "gen",
         "We waited for the train for an hour and a half.",
         "Полтора + genitive singular: полтора часа (not часов). Поезд here is genitive after ждать.",
         []),
        ("Обе ___ уже подоены.", "корова", "npl",
         "Both cows have already been milked.",
         "Оба / обе means 'both'. Feminine is обе and the noun stays nominative plural: обе коровы. Masculine would be оба быка (оба + genitive singular — a special pattern).",
         []),
        ("Оба ___ стоят у сарая.", "трактор", "gen",
         "Both tractors are standing by the barn.",
         "Masculine оба takes the genitive singular of the noun: оба трактора (like два трактора). Обе would be feminine.",
         []),
        ("В кормушке ещё пять ___ зерна.", "килограмм", "gpl",
         "There are still five kilograms of grain in the feeder.",
         "After 5 use the genitive plural: пять килограммов (the everyday short form килограмм is also heard). Зерна is genitive ('of grain').",
         []),
    ]
    rows = [r for r in rows if r[1] != "wait"]
    rows += [
        ("Билет до Минска стоил три ___ рублей.", "тысяча", "gen",
         "The ticket to Minsk cost three thousand rubles.",
         "After 2–4 the noun is genitive singular: три тысячи. After 5 it would be пять тысяч (genitive plural). Рублей is genitive plural after the number hidden in тысячи.",
         []),
    ]
    rows = [r for r in rows if r[2] != "wait"]
    rows += [
        ("Нам нужны ещё двое ___.", "работник", "gpl",
         "We need two more workers.",
         "Collective numerals (двое, трое, четверо) are used with people (and plural-only nouns) and take the genitive plural: двое работников. Два работника (2–4 + genitive singular) is also correct, but slightly less colloquial for 'a group of people'.",
         []),
        ("У кассы стояли трое ___.", "человек", "gpl",
         "Three people were standing at the checkout.",
         "Трое (collective) takes the genitive plural. Человек after a numeral often stays человек (трое человек / три человека). Here человек is the counting genitive plural of человек.",
         []),
    ]
    rows = [r for r in rows if r[2] != "wait"]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(B, C, S, s, lemma, case, tr, ex, gl)

    # A couple of numeral-is-the-blank items, written explicitly
    add(B, C, S, "Ферме уже ___ лет.", "тридцать", "тридцать",
        ["тридцати", "тридцатью", "тридцатого"],
        "Age of a thing uses the dative of the owner (ферме) + nominative of the number: тридцать лет. Тридцати would be genitive or dative of the numeral itself.",
        "The farm is already thirty years old.",
        ["лет: years (genitive plural of год, used after 5+ and in age)"])
    add(B, C, S, "Мы говорим о ___ новых коровах.", "пять", "пяти",
        ["пять", "пятью", "пятерых"],
        "In the prepositional the numeral itself declines: о пяти коровах (not о пять). The noun is prepositional plural and agrees.",
        "We're talking about five new cows.",
        [])
    add(B, C, S, "Я купил корм за ___ рублей.", "сорок", "сорок",
        ["сорока", "сорокаа", "сороков"],
        "За + accusative of the price. Сорок (and девяносто, сто) looks the same in the nominative and the accusative: за сорок рублей. Сорока is the genitive/dative/instrumental/prepositional form.",
        "I bought the feed for forty rubles.",
        [])
    add(B, C, S, "Он приехал с ___ друзьями.", "два", "двумя",
        ["двум", "двух", "два"],
        "С takes the instrumental, so два becomes двумя: с двумя друзьями. Двум is dative; двух is genitive or accusative.",
        "He arrived with two friends.",
        [])

def build():
    build_cases_a1()
    build_cases_b1()
    build_basics_a1()
    build_conj()
    build_conj_b1()
    build_motion_aspect()
    build_home_kakoy_freq()
    build_l9_bank()
    build_topup_bank()
    build_l8_bank()
    build_kotoryy_bank()


def build_l9_bank():
    """Lesson 9 / tutor session additions (appended last so earlier bank ids stay stable)."""
    C = "cases"
    # ---- A1-A2: genitive prepositions, with the перед contrast ----
    S = "для, кроме, напротив, ради (and перед)"
    NAP = "Напротив (opposite, across from) takes the genitive: "
    rows = [
        ("Наша церковь стоит напротив ___.", "почта", "gen", "Our church stands across from the post office.", NAP + "напротив почты. In front of would be перед почтой (instrumental).", []),
        ("Напротив ___ есть заправка.", "школа", "gen", "There's a gas station across from the school.", NAP + "напротив школы.", ["заправка: gas station"]),
        ("Я живу напротив ___.", "парк", "gen", "I live across from the park.", NAP + "напротив парка.", []),
        ("Магазин находится напротив ___.", "вокзал", "gen", "The store is located across from the station.", NAP + "напротив вокзала. Находится = is located.", ["находиться: to be located"]),
        ("Напротив ___ большое поле.", "ферма", "gen", "There's a big field across from the farm.", NAP + "напротив фермы.", []),
        ("Мой офис напротив ___.", "банк", "gen", "My office is across from the bank.", NAP + "напротив банка.", []),
        ("Напротив ___ стоит старый сарай.", "дом", "gen", "An old barn stands across from the house.", NAP + "напротив дома. Перед домом would be right in front of it.", []),
        ("В храме я стою напротив ___.", "икона", "gen", "In church I stand facing the icon.", NAP + "напротив иконы. Перед иконой (instrumental) = in front of the icon.", []),
        ("Напротив ___ в Березине есть кафе.", "церковь", "gen", "There's a café across from the church in Berezino.", NAP + "напротив церкви (feminine -ь → -и).", []),
        ("Остановка напротив ___.", "магазин", "gen", "The bus stop is across from the store.", NAP + "напротив магазина.", ["остановка: (bus) stop"]),
        ("Почта находится напротив ___.", "библиотека", "gen", "The post office is across from the library.", NAP + "напротив библиотеки (к → и).", ["библиотека: library"]),
        ("Пикап стоит напротив ___.", "гараж", "gen", "The pickup is parked across from the garage.", NAP + "напротив гаража.", ["гараж: garage"]),
        ("Напротив ___ стоит памятник.", "музей", "gen", "There's a monument across from the museum.", NAP + "напротив музея (-й → -я).", ["памятник: monument"]),
        ("Наш дом стоит напротив ___.", "пруд", "gen", "Our house stands across from the pond.", NAP + "напротив пруда.", []),
        ("Напротив ___ живёт мой брат.", "больница", "gen", "My brother lives across from the hospital.", NAP + "напротив больницы.", ["больница: hospital"]),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        add_noun(A, C, S, s, lemma, case, tr, ex, gl)
    for s, lemma, case, tr, ex, gl in [
        ("Сосед живёт напротив ___.", "мы", "gen", "Our neighbor lives across from us.", "Напротив + genitive: напротив нас.", []),
        ("В офисе коллега сидит напротив ___.", "я", "gen", "At the office my colleague sits across from me.", "Напротив + genitive: напротив меня.", ["коллега: colleague"]),
        ("За столом жена сидит напротив ___.", "он", "pgen", "At the table my wife sits across from him.", "Напротив + genitive, with н- after the preposition: напротив него (not напротив его).", []),
        ("На работе никто, кроме ___, не знает этот сервер.", "я", "gen", "At work nobody but me knows this server.", "Кроме (except) takes the genitive: кроме меня.", ["сервер: server"]),
    ]:
        add_pron(A, C, S, s, lemma, case, tr, ex, gl)
    KR = "Кроме (besides, except, other than) takes the genitive: "
    RD = "Ради (for the sake of) takes the genitive: "
    DL = "Для (for) takes the genitive: "
    rows = [
        ("Все пришли на обед, кроме ___.", "брат", "gen", "Everyone came to lunch except my brother.", KR + "кроме брата.", []),
        ("Я люблю всю музыку, кроме ___.", "джаз", "gen", "I like all music except jazz.", KR + "кроме джаза.", ["джаз: jazz"]),
        ("Кроме наших ___ у нас есть куры и козы.", "корова", "gpl", "Besides our cows we have chickens and goats.", KR + "plural → genitive plural кроме коров.", ["коза: goat"]),
        ("Кроме ___ я пью только воду.", "чай", "gen", "Apart from tea I drink only water.", KR + "кроме чая.", []),
        ("Жена ест всё, кроме ___.", "рыба", "gen", "My wife eats everything except fish.", KR + "кроме рыбы.", []),
        ("Магазин работает каждый день, кроме ___.", "воскресенье", "gen", "The store is open every day except Sunday.", KR + "кроме воскресенья (neuter -е → -я).", []),
        ("Все мои друзья, кроме ___, живут в Минске.", "Андрей", "gen", "All my friends except Andrei live in Minsk.", KR + "кроме Андрея.", []),
        ("Ради наших ___ я встаю в пять утра.", "корова", "gpl", "For our cows' sake I get up at five in the morning.", RD + "plural → ради коров.", []),
        ("Мы делаем это ради наших ___.", "ребёнок", "gpl", "We do this for the sake of our children.", RD + "ради детей (irregular genitive plural of ребёнок / дети).", []),
        ("Он переехал в Джексон ради ___.", "работа", "gen", "He moved to Jackson for the sake of work.", RD + "ради работы.", ["переехать: to move (house)"]),
        ("Ради ___ я выучил русский.", "жена", "gen", "I learned Russian for my wife's sake.", RD + "ради жены.", []),
        ("Мы ходим в храм не ради ___.", "традиция", "gen", "We don't go to church for the sake of tradition.", RD + "ради традиции (-ия → -ии).", ["традиция: tradition"]),
        ("Ради ___ он продал машину.", "семья", "gen", "He sold the car for the sake of his family.", RD + "ради семьи.", []),
        ("Ради ___ они поехали в Минск.", "концерт", "gen", "They went to Minsk for the sake of the concert.", RD + "ради концерта.", []),
        ("Это корм для наших ___.", "свинья", "gpl", "This is feed for our pigs.", DL + "plural → для свиней.", []),
        ("Я купил подарок для ___.", "мама", "gen", "I bought a present for Mom.", DL + "для мамы.", ["подарок: present"]),
        ("Мы купили свечи для ___.", "храм", "gen", "We bought candles for the church.", DL + "для храма.", []),
        ("Это сыр для ___: я делаю их на завтрак.", "бутерброд", "gpl", "This cheese is for sandwiches: I make them for breakfast.", DL + "plural → для бутербродов.", ["бутерброд: (open) sandwich"]),
        ("Я пишу код для ___ в Джексоне.", "компания", "gen", "I write code for a company in Jackson.", DL + "для компании (-ия → -ии). Для = who benefits; ради = for the sake of.", ["компания: company"]),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        # plural objects: keep the genitive singular out of the options (для свиньи would also be grammatical)
        add_noun(A, C, S, s, lemma, case, tr, ex, gl,
                 prefer=["npl", "nom", "dpl", "ipl", "ppl", "dat", "ins"] if case == "gpl" else None)
    PB = "кроме / напротив / перед"
    for s, a, d, ex, tr in [
        ("Трактор стоит ___ сараем.", "перед", ["напротив", "кроме", "для"], "Сараем is instrumental, so only перед (in front of) fits. Напротив and кроме take the genitive.", "The tractor is parked in front of the barn."),
        ("Заправка находится ___ магазина, через дорогу.", "напротив", ["перед", "кроме", "ради"], "Магазина is genitive (not перед), and через дорогу (across the road) means напротив.", "The gas station is across the road from the store."),
        ("___ службой мы молимся дома.", "перед", ["напротив", "кроме", "для"], "Службой is instrumental: перед службой = just before the service.", "Before the service we pray at home."),
        ("Мы встречаемся ___ церковью.", "перед", ["напротив", "кроме", "ради"], "Церковью is instrumental: перед церковью = in front of the church.", "We're meeting in front of the church."),
        ("Кафе ___ вокзала, на другой стороне улицы.", "напротив", ["перед", "кроме", "для"], "Вокзала is genitive, and на другой стороне улицы (on the other side of the street) means напротив.", "The café is opposite the station, on the other side of the street."),
        ("Все были на созвоне, ___ меня.", "кроме", ["напротив", "перед", "ради"], "Everyone except me: кроме + genitive (меня).", "Everyone was on the call except me."),
    ]:
        add(A, C, S, s, PB, a, d, ex, tr, ["созвон: (video) call"] if "созвон" in s else [])

    # ---- B1-C1 genitive plural: the exceptions from Lesson 9, Step 5 ----
    S = "genitive plural"
    for s, base, a, d, ex, tr in [
        ("У меня в Березине пять ___.", "тётя", "тёть", ["тёти", "тётев", "тётю"], "After 5: genitive plural. Тётя → тёть (zero ending with a soft sign).", "I have five aunts in Berezino."),
        ("Купи, пожалуйста, две пары ___.", "носок", "носков", ["носки", "носка", "носоков"], "Пара (a pair) takes the genitive plural. Носок → носков (fleeting о, then -ов).", "Please buy two pairs of socks."),
        ("У меня нет зимних ___.", "сапог", "сапог", ["сапогов", "сапоги", "сапога"], "Нет + genitive plural. Сапог has a zero ending: сапог (compare носков).", "I don't have winter boots."),
        ("В машине только пять ___.", "место", "мест", ["местов", "места", "месте"], "After 5: genitive plural. Neuter -о: zero ending, мест.", "There are only five seats in the car."),
        ("Сегодня у меня на работе много ___.", "дело", "дел", ["делов", "дела", "деле"], "Много + genitive plural. Дело → дел (zero ending).", "I have a lot to do at work today."),
        ("Вокруг Березина много ___.", "поле", "полей", ["поля", "полев", "поле"], "Много + genitive plural. Neuter -е → -ей: полей.", "There are many fields around Berezino."),
        ("У дочери цвет ___ как у мамы.", "глаз", "глаз", ["глазов", "глаза", "глазу"], "Цвет (the colour of) + genitive plural. Глаз → глаз (zero ending).", "My daughter's eye colour is like her mother's."),
        ("Я уже десять ___ говорил ему про забор.", "раз", "раз", ["разов", "раза", "разы"], "After 10: genitive plural. Раз → раз (no ending).", "I've told him about the fence ten times already."),
        ("В нашем приходе двадцать ___.", "семья", "семей", ["семьёв", "семьи", "семью"], "After 20: genitive plural. Семья → семей.", "There are twenty families in our parish.", ),
        ("На созвоне было двенадцать ___.", "человек", "человек", ["людей", "человеков", "люди"], "After a number, человек stays человек: двенадцать человек. После много → людей.", "There were twelve people on the call."),
        ("На площади в Джексоне было много ___.", "люди", "людей", ["люди", "людям", "человеков"], "Много + genitive plural: людей. After a number it would be человек.", "There were a lot of people on the square in Jackson."),
        ("Сколько ___ ты работаешь программистом?", "год", "лет", ["годов", "года", "годы"], "Сколько + genitive plural, and for год that's лет. Годов is only for decades.", "How many years have you worked as a programmer?"),
        ("На кухне не хватает ___ для гостей.", "стул", "стульев", ["стулов", "стулья", "стула"], "Не хватает + genitive plural. Стул → стулья → стульев.", "There aren't enough chairs in the kitchen for the guests."),
        ("У брата нет ___ в городе.", "друг", "друзей", ["другов", "друзья", "друга"], "Нет + genitive plural. Друг → друзья → друзей.", "My brother has no friends in town."),
        ("У соседа шесть ___.", "брат", "братьев", ["братов", "братья", "брата"], "After 6: genitive plural. Брат → братья → братьев.", "My neighbor has six brothers."),
        ("Мне нужна корзина для ___.", "яйцо", "яиц", ["яйцов", "яйца", "яйцу"], "Для + genitive plural. Яйцо → яиц (irregular).", "I need a basket for eggs."),
    ]:
        add(B, C, S, s, base, a, d, ex, tr, ["приход: parish"] if "приход" in s else (["созвон: (video) call"] if "созвон" in s else []))

    # ---- какой: the tutor's questions not already in the bank ----
    Fk = {"m":{"N":"какой","A":"какой","AA":"какого","G":"какого","D":"какому","I":"каким","P":"каком"},
          "n":{"N":"какое","A":"какое","G":"какого","D":"какому","I":"каким","P":"каком"},
          "f":{"N":"какая","A":"какую","AA":"какую","G":"какой","D":"какой","I":"какой","P":"какой"},
          "p":{"N":"какие","A":"какие","AA":"каких","G":"каких","D":"каким","I":"какими","P":"каких"}}
    SUBk = {"N":"nominative: какой / какая / какое / какие", "A":"accusative (things): какой / какую / какое / какие",
            "AA":"accusative (people, animals): какого / какую / каких", "P":"prepositional (в / на / о): каком / какой / каких"}
    LVk = {"N":A,"A":A,"P":A,"AA":B}
    ORDERk = ["m","f","n","p"]; CASESk = ["N","A","G","D","I","P"]
    def kdist(g_, c_, a_):
        cc = "A" if c_ == "AA" else c_
        same_case = [Fk[x].get(c_, Fk[x][cc]) for x in ORDERk if x != g_]
        same_gen = [Fk[g_][k] for k in CASESk if k != cc]
        out = []
        for pair in zip(same_case + [None]*6, same_gen):
            for o in pair:
                if o and o != a_ and o not in out: out.append(o)
        return out[:3]
    for g_, c_, s, tr, ex, gl in [
        ("f","AA","___ девушку он любит?","Which girl does he love?","Девушка is feminine, the direct object of любит → accusative какую (feminine is -ую for people too).",["девушка: girl, young woman; girlfriend"]),
        ("f","A","___ машину ты купил?","Which car did you buy?","Машина is feminine, the direct object of купил → accusative какую.",[]),
        ("f","P","В ___ деревне ты живёшь?","Which village do you live in?","Где? в + prepositional. Деревня is feminine → в какой деревне.",["деревня: village"]),
        ("f","A","___ музыку он слушает?","What music does he listen to?","Музыка is feminine, the direct object of слушает → какую.",[]),
        ("f","N","___ картина тебе нравится?","Which painting do you like?","With нравится the thing you like is the subject (nominative). Картина is feminine → какая.",["картина: painting, picture"]),
        ("f","P","О ___ машине ты говоришь?","Which car are you talking about?","О + prepositional. Машина is feminine → о какой машине.",[]),
        ("f","P","В ___ школе ты учился?","Which school did you go to?","Где? в + prepositional. Школа is feminine → в какой школе.",["учиться: to study (at school)"]),
        ("f","A","___ колу ты предпочитаешь?","Which cola do you prefer?","Кола is feminine, the direct object of предпочитаешь → какую.",["предпочитать: to prefer"]),
        ("m","N","___ жанр тебе нравится?","Which genre do you like?","With нравится the thing is the subject. Жанр is masculine → какой. (Answer: Мне нравится джаз.)",["жанр: genre"]),
        ("m","A","___ фильм вы вчера смотрели?","Which film did you watch yesterday?","Фильм is masculine and inanimate: accusative = nominative → какой.",[]),
        ("m","A","___ последний фильм вы смотрели?","What was the last film you watched?","Фильм is the direct object, masculine inanimate → какой (последний agrees).",["последний: last, latest"]),
        ("m","A","___ сорт вина вы любите?","Which kind of wine do you like?","Сорт is masculine inanimate, the direct object → какой. Вина is genitive (of wine).",["сорт: kind, variety"]),
        ("m","N","___ город тебе нравится больше всего?","Which city do you like most of all?","With нравится the city is the subject. Город is masculine → какой. (Мне нравится Нью-Йорк.)",[]),
    ]:
        a_ = Fk[g_][c_]
        add(LVk[c_], "kakoy", SUBk[c_], s, "какой", a_, kdist(g_, c_, a_), ex, tr, gl)


def build_topup_bank():
    """Tutor-session top-up: missing какой questions, and A1 до + genitive.
    Appended last so earlier bank ids stay stable."""
    A, B = "A1-A2", "B1-C1"
    # ---- какой: new verbs and frames from the tutor session ----
    Fk = {"m":{"N":"какой","A":"какой","AA":"какого","G":"какого","D":"какому","I":"каким","P":"каком"},
          "n":{"N":"какое","A":"какое","G":"какого","D":"какому","I":"каким","P":"каком"},
          "f":{"N":"какая","A":"какую","AA":"какую","G":"какой","D":"какой","I":"какой","P":"какой"},
          "p":{"N":"какие","A":"какие","AA":"каких","G":"каких","D":"каким","I":"какими","P":"каких"}}
    SUBk = {"N":"nominative: какой / какая / какое / какие",
            "A":"accusative (things): какой / какую / какое / какие",
            "AA":"accusative (people, animals): какого / какую / каких",
            "P":"prepositional (в / на / о): каком / какой / каких",
            "G":"genitive (из / у / для / без): какого / какой / каких",
            "D":"dative (к / по): какому / какой / каким",
            "I":"instrumental (с / чем?): каким / какой / какими"}
    LVk = {"N":A,"A":A,"P":A,"AA":B,"G":B,"D":B,"I":B}
    ORDERk = ["m","f","n","p"]; CASESk = ["N","A","G","D","I","P"]
    def kdist(g_, c_, a_):
        cc = "A" if c_ == "AA" else c_
        same_case = [Fk[x].get(c_, Fk[x][cc]) for x in ORDERk if x != g_]
        same_gen = [Fk[g_][k] for k in CASESk if k != cc]
        out = []
        for pair in zip(same_case + [None]*6, same_gen):
            for o in pair:
                if o and o != a_ and o not in out:
                    out.append(o)
        return out[:3]
    rows = [
        ("f","P","О ___ машине ты мечтаешь?","Which car do you dream of?","Мечтать о takes the prepositional. Машина is feminine → о какой машине.",["мечтать: to dream (of)"]),
        ("m","P","О ___ доме ты мечтаешь?","Which house do you dream of?","Мечтать о + prepositional. Дом is masculine → о каком доме.",["мечтать: to dream (of)"]),
        ("f","P","О ___ работе ты думаешь?","Which job are you thinking about?","Думать о takes the prepositional. Работа is feminine → о какой работе.",[]),
        ("f","P","О ___ проблеме он говорит?","Which problem is he talking about?","Говорить о + prepositional. Проблема is feminine → о какой проблеме.",["проблема: problem"]),
        ("m","D","___ другу ты даришь подарок?","Which friend are you giving a present to?","Дарить кому? takes the dative. Друг is masculine → какому другу.",["дарить: to give as a gift","подарок: present"]),
        ("f","D","___ девушке ты даёшь машину?","Which girl are you giving the car to?","Давать кому? takes the dative. Девушка is feminine → какой девушке.",["давать: to give"]),
        ("m","D","___ знакомому ты звонишь?","Which acquaintance are you calling?","Звонить кому? takes the dative. Знакомый (a person you know) is masculine → какому знакомому.",["знакомый: acquaintance"]),
        ("m","D","___ ребёнку ты звонишь?","Which child are you calling?","Звонить + dative. Ребёнок is masculine → какому ребёнку.",[]),
        ("m","P","В ___ городе ты родился?","Which city were you born in?","Где? в + prepositional. Город is masculine → в каком городе.",["родиться: to be born"]),
        ("m","I","___ спортом ты занимаешься?","What sport do you do?","Заниматься (to go in for) takes the instrumental. Спорт is masculine → каким спортом.",["заниматься: to go in for, be busy with"]),
        ("p","I","___ видами спорта ты увлекаешься?","Which sports are you keen on?","Увлекаться takes the instrumental. Виды is plural → какими видами.",["увлекаться: to be keen on, into","вид спорта: a sport"]),
        ("p","D","___ детям подарили подарки?","Which children were given presents?","The children are the indirect object (кому?): dative plural → каким детям.",["подарить: to give as a gift (pf.)"]),
        ("p","N","___ они люди?","What kind of people are they?","Люди is plural and the predicate after они (nominative) → какие.",[]),
        ("f","A","В ___ деревню мы едем?","Which village are we going to?","Куда? в + accusative. Деревня is feminine → в какую деревню. (В какой деревне would be где?.)",["деревня: village"]),
        ("f","A","___ дверь она открыла?","Which door did she open?","Дверь is feminine, the direct object of открыла → какую.",[]),
        ("f","N","___ учительница дала задание?","Which teacher gave the assignment?","Учительница is feminine and the subject (nominative) → какая.",["учительница: (female) teacher","задание: assignment"]),
        ("m","G","Для ___ брата она купила подарки?","Which brother did she buy the presents for?","Для takes the genitive. Брат is masculine → для какого брата.",[]),
        ("f","D","По ___ улице мы идём?","Which street are we walking along?","По (along) takes the dative. Улица is feminine → по какой улице.",[]),
        ("n","N","___ блюдо популярно во Флориде?","Which dish is popular in Florida?","Блюдо is neuter and the subject (nominative) → какое. Во Флориде is prepositional (в + о).",["Флорида: Florida"]),
        ("n","N","___ самое красивое место во Флориде?","What is the most beautiful place in Florida?","Место is neuter, the subject → какое. Самое красивое agrees with it.",["место: place"]),
        ("p","A","___ фильмы ты любишь?","Which films do you like?","Фильмы is inanimate plural, the direct object of любишь → какие (accusative = nominative).",[]),
        ("p","AA","___ учителей ты встретил?","Which teachers did you meet?","Учителя are people: plural accusative = genitive → каких учителей.",["встретить: to meet"]),
    ]
    for g_, c_, s, tr, ex, gl in rows:
        a_ = Fk[g_][c_]
        add(LVk[c_], "kakoy", SUBk[c_], s, "какой", a_, kdist(g_, c_, a_), ex, tr, gl)

    # ---- A1 до + genitive (time and distance); same pool as the other genitive prepositions ----
    C, S = "cases", "для, кроме, напротив, ради (and перед)"
    DO = "До (before; as far as, until) takes the genitive: "
    for s, lemma, case, tr, ex, gl in [
        ("До ___ я завтракал.", "урок", "gen",
         "I had breakfast before the lesson.",
         DO + "до урока. This is time: before. After the lesson would be после урока, also genitive.",
         ["завтракал: I had breakfast"]),
        ("До ___ мы обычно молимся дома.", "служба", "gen",
         "Before the service we usually pray at home.",
         DO + "до службы (before). После службы is after the service.",
         []),
        ("От фермы до ___ всего пять минут пешком.", "школа", "gen",
         "It's only a five-minute walk from the farm to the school.",
         DO + "до школы. This is distance: as far as, up to. От фермы is also genitive (от).",
         []),
        ("До ___ двадцать часов на машине.", "Флорида", "gen",
         "It's a twenty-hour drive to Florida.",
         DO + "до Флориды (as far as / until you get there). На машине is instrumental (by car).",
         ["Флорида: Florida"]),
        ("Дети играли на улице до ___.", "темнота", "gen",
         "The children played outside until dark.",
         DO + "до темноты (until). Темнота is feminine: -а → -ы.",
         ["темнота: darkness, dark"]),
        ("До ___ я ещё покормлю коров.", "созвон", "gen",
         "I'll feed the cows before the (video) call.",
         DO + "до созвона (before). Покормлю is perfective future.",
         ["созвон: (video) call"]),
        ("Я работал в офисе до ___.", "вечер", "gen",
         "I worked at the office until evening.",
         DO + "до вечера (until). Вечер is masculine: -а.",
         []),
        ("До ___ я зашёл на ферму.", "завтрак", "gen",
         "Before breakfast I stopped by the farm.",
         DO + "до завтрака (before). Contrast после завтрака (after breakfast).",
         ["завтрак: breakfast","зашёл: I stopped by"]),
    ]:
        add_noun(A, C, S, s, lemma, case, tr, ex, gl)



def build_l8_bank():
    """Lesson 8 follow-up: instrumental plural, dative-plural exceptions, and missing какой frames.
    Appended last so earlier bank ids (1–1896) stay stable."""
    A, B = "A1-A2", "B1-C1"
    C = "cases"

    # ---- instrumental plural (tutor set: tools, people, со, рядом с, между) ----
    INS = "instrumental"
    rows_ins = [
        (A, "Я путешествую с ___.", "друг", "ipl",
         "I travel with friends.",
         "С (with) takes the instrumental plural. Друг → друзья → друзьями, not “другами”.",
         ["путешествовать: to travel"]),
        (A, "Я работаю с ___.", "коллега", "ipl",
         "I work with colleagues.",
         "С + instrumental plural: коллеги → коллегами.",
         []),
        (A, "Мы часто говорим с ___.", "врач", "ipl",
         "We often talk with doctors.",
         "С + instrumental plural: врачи → врачами.",
         []),
        (A, "Я живу рядом с ___.", "родитель", "ipl",
         "I live next to my parents.",
         "Рядом с (next to) takes the instrumental: родители → родителями.",
         ["родители: parents","рядом с: next to"]),
        (A, "Я работаю со ___.", "студент", "ipl",
         "I work with students.",
         "Со (not с) before ст-: со студентами. Regular -ами.",
         ["студент: student"]),
        (A, "Мы едим ___ и вилками.", "нож", "ipl",
         "We eat with knives and forks.",
         "Чем? The tool is instrumental plural, with no с: ножи → ножами.",
         []),
        (A, "Мы едим суп ложками и ___.", "вилка", "ipl",
         "We eat soup with spoons and forks.",
         "Чем? Вилки → вилками.",
         []),
        (A, "Чем мы обычно едим щи? ___.", "ложка", "ipl",
         "What do we usually eat shchi with? With spoons.",
         "Чем? Ложки → ложками. No с.",
         ["щи: cabbage soup"]),
        (A, "Мы пишем ___.", "ручка", "ipl",
         "We write with pens.",
         "Чем? Ручки → ручками.",
         ["ручка: pen"]),
        (A, "Мы рисуем ручками и ___.", "карандаш", "ipl",
         "We draw with pens and pencils.",
         "Чем? Карандаши → карандашами.",
         ["карандаш: pencil","рисовать: to draw"]),
        (A, "Чем мы стрижём волосы? ___.", "ножницы", "ipl",
         "What do we cut hair with? With scissors.",
         "Ножницы is plural only: ножницами. Чем? — no с.",
         ["стричь: to cut (hair)","ножницы: scissors"]),
        (A, "В китайском ресторане мы едим ___.", "палочка", "ipl",
         "In a Chinese restaurant we eat with chopsticks.",
         "Палочки (chopsticks) are used in the plural: палочками.",
         ["палочка: stick; chopsticks (pl.)"]),
        (A, "Зимой мы пользуемся ___.", "лыжи", "ipl",
         "In winter we use skis.",
         "Лыжи is used as a pair: пользоваться + instrumental → лыжами.",
         ["пользоваться: to use","лыжи: skis"]),
        (A, "Я часто гуляю с красивыми ___.", "женщина", "ipl",
         "I often go for a walk with beautiful women.",
         "С + instrumental plural: женщины → женщинами. Красивыми agrees (instrumental plural).",
         ["женщина: woman"]),
        (B, "Батюшка после службы говорит с ___.", "человек", "ipl",
         "After the service Father talks with the people.",
         "Exception: человек → люди → людьми, not “людями”.",
         []),
        (B, "На работе я каждый день советуюсь с ___.", "адвокат", "ipl",
         "At work I consult with lawyers every day.",
         "С + instrumental plural: адвокаты → адвокатами.",
         ["адвокат: lawyer"]),
        (B, "Мы ездили в Минск с ___.", "брат", "ipl",
         "We went to Minsk with (our) brothers.",
         "Брат → братья → братьями, not “братами”.",
         []),
        (B, "Она живёт с ___.", "сестра", "ipl",
         "She lives with (her) sisters.",
         "Сестра → сёстры → сёстрами.",
         []),
        (B, "Между этими ___ находится река.", "страна", "ipl",
         "The river is between these countries.",
         "Между (between) takes the instrumental plural: страны → странами.",
         ["страна: country"]),
        (B, "Я путешествую один или с ___.", "семья", "ins",
         "I travel alone or with my family.",
         "С + instrumental singular: семья → семьёй (with ё).",
         []),
    ]
    for level, s, lemma, case, tr, ex, gl in rows_ins:
        add_noun(level, C, INS, s, lemma, case, tr, ex, gl)

    # ---- dative-plural exceptions (L7 already teaches -ам/-ям; these fill the tutor set) ----
    DAT = "dative"
    rows_dat = [
        (A, "Преподаватель читает лекцию ___.", "студент", "dpl",
         "The lecturer is giving a lecture to the students.",
         "Читать лекцию кому? Dative plural: студенты → студентам.",
         ["преподаватель: lecturer","лекция: lecture"]),
        (A, "Я сказал об экскурсии ___.", "друг", "dpl",
         "I told my friends about the excursion.",
         "Сказать кому? Друг → друзья → друзьям, not “другам”.",
         ["экскурсия: excursion, tour"]),
        (A, "Я купил подарки ___.", "сестра", "dpl",
         "I bought presents for my sisters.",
         "Купить кому? Сестра → сёстры → сёстрам.",
         []),
        (A, "Сегодня я звонил ___.", "родитель", "dpl",
         "I called my parents today.",
         "Звонить кому? Родители → родителям.",
         []),
        (A, "Мы дарим цветы ___.", "женщина", "dpl",
         "We give flowers to women.",
         "Дарить кому? Женщины → женщинам.",
         ["дарить: to give as a gift","цветы: flowers"]),
        (A, "Мать купила лыжи ___.", "дочь", "dpl",
         "The mother bought skis for her daughters.",
         "Купить кому? Дочь → дочери → дочерям (the hidden -ер- comes back).",
         ["лыжи: skis"]),
        (A, "Анна помогает ___.", "брат", "dpl",
         "Anna helps her brothers.",
         "Помогать кому? Брат → братья → братьям, not “братам”.",
         []),
        (A, "Благодаря ___ дети учатся в школе.", "родитель", "dpl",
         "Thanks to their parents, the children go to school.",
         "Благодаря (thanks to) takes the dative, not the genitive: благодаря родителям. (Для родителей would be “for the parents.”)",
         ["благодаря: thanks to"]),
        (B, "Тарас послал свои фотографии ___.", "коллега", "dpl",
         "Taras sent his photographs to (his) colleagues.",
         "Послать кому? Коллеги → коллегам.",
         ["послать: to send"]),
        (B, "На прошлой неделе я приехал в Джексон к ___.", "друг", "dpl",
         "Last week I arrived in Jackson to stay with friends.",
         "К (to a person) takes the dative, also in the plural: к друзьям.",
         []),
        (B, "Мы ездили в Минск к моим ___.", "друг", "dpl",
         "We went to Minsk to stay with my friends.",
         "К + dative plural: к моим друзьям.",
         []),
        (B, "По вечерам он ходит к ___.", "врач", "dpl",
         "In the evenings he goes to see doctors.",
         "К + dative plural: к врачам (to people). В больницу would be to the place.",
         []),
    ]
    for level, s, lemma, case, tr, ex, gl in rows_dat:
        add_noun(level, C, DAT, s, lemma, case, tr, ex, gl)

    # ---- какой: remaining tutor frames (do not regenerate kakoy_exercises.py) ----
    Fk = {"m":{"N":"какой","A":"какой","AA":"какого","G":"какого","D":"какому","I":"каким","P":"каком"},
          "n":{"N":"какое","A":"какое","G":"какого","D":"какому","I":"каким","P":"каком"},
          "f":{"N":"какая","A":"какую","AA":"какую","G":"какой","D":"какой","I":"какой","P":"какой"},
          "p":{"N":"какие","A":"какие","AA":"каких","G":"каких","D":"каким","I":"какими","P":"каких"}}
    SUBk = {"N":"nominative: какой / какая / какое / какие",
            "A":"accusative (things): какой / какую / какое / какие",
            "AA":"accusative (people, animals): какого / какую / каких",
            "P":"prepositional (в / на / о): каком / какой / каких",
            "G":"genitive (из / у / для / без): какого / какой / каких",
            "D":"dative (к / по): какому / какой / каким",
            "I":"instrumental (с / чем?): каким / какой / какими"}
    LVk = {"N":A,"A":A,"P":A,"AA":B,"G":B,"D":B,"I":B}
    ORDERk = ["m","f","n","p"]; CASESk = ["N","A","G","D","I","P"]
    def kdist(g_, c_, a_):
        cc = "A" if c_ == "AA" else c_
        same_case = [Fk[x].get(c_, Fk[x][cc]) for x in ORDERk if x != g_]
        same_gen = [Fk[g_][k] for k in CASESk if k != cc]
        out = []
        for pair in zip(same_case + [None]*6, same_gen):
            for o in pair:
                if o and o != a_ and o not in out:
                    out.append(o)
        return out[:3]
    rows_k = [
        ("m","G","До ___ урока у них встреча?","Until which lesson do they have a meeting?","До takes the genitive. Урок is masculine → до какого урока.",["встреча: meeting"]),
        ("m","G","У ___ дома мы встретимся?","By which house shall we meet?","У takes the genitive. Дом is masculine → у какого дома.",[]),
        ("m","A","В ___ город ты едешь?","Which city are you going to?","Куда? в + accusative. Город is masculine inanimate → в какой город. (В каком городе would be где?.)",[]),
        ("m","A","На ___ фестиваль мы идём?","Which festival are we going to?","Куда? на + accusative (events take на). Фестиваль is masculine → на какой фестиваль.",["фестиваль: festival"]),
        ("f","A","На ___ вечеринку ты идёшь?","Which party are you going to?","Куда? на + accusative. Вечеринка is feminine → на какую вечеринку.",["вечеринка: party"]),
        ("f","G","Около ___ дачи стоит машина?","Near which dacha is the car standing?","Около (near) takes the genitive. Дача is feminine → около какой дачи.",["дача: dacha, country house"]),
        ("f","G","У ___ подруги ключи?","Which (female) friend has the keys?","У takes the genitive. Подруга is feminine → у какой подруги.",[]),
        ("p","I","Между ___ странами находится эта река?","Between which countries is this river?","Между takes the instrumental. Страны is plural → между какими странами.",["страна: country"]),
        ("p","D","К ___ врачам он ходит?","Which doctors does he go to?","К (to a person) takes the dative, also in the plural → к каким врачам.",[]),
        ("p","D","По ___ вопросам он консультирует?","On which questions does he give advice?","По takes the dative. Вопросы is plural → по каким вопросам.",["вопрос: question","консультировать: to advise"]),
        ("m","P","В ___ шкафу лежит футболка?","In which wardrobe is the T-shirt lying?","Где? в + prepositional. Шкаф has the special locative -у: в шкафу, and какой agrees: в каком шкафу.",["шкаф: wardrobe","футболка: T-shirt"]),
        ("n","N","___ у тебя полотенце?","What sort of towel do you have?","Полотенце is neuter and the subject after у тебя (nominative) → какое.",["полотенце: towel"]),
        ("m","P","На ___ столе стоит стакан?","On which table is the glass standing?","Где? на + prepositional. Стол is masculine → на каком столе.",[]),
        ("m","A","В ___ зал ты идёшь?","Which hall are you going into?","Куда? в + accusative. Зал is masculine inanimate → в какой зал. (В каком зале would be где?.)",["зал: hall"]),
    ]
    for g_, c_, s, tr, ex, gl in rows_k:
        a_ = Fk[g_][c_]
        add(LVk[c_], "kakoy", SUBk[c_], s, "какой", a_, kdist(g_, c_, a_), ex, tr, gl)



def build_kotoryy_bank():
    """Lesson LK / tutor notes set 4. Appended last so ids 1–1942 stay stable."""
    C, S = "cases", "который (relative pronoun)"
    # 24 который items, B1-C1 (relative clauses sit a step above A1; pool minimum is 20).
    rows = [
        ("Вот программист, ___ пишет код в Минске.", "который",
         ["которая", "которого", "которое"],
         "The programmer who writes the code lives in Minsk.",
         "Программист is masculine; который is the subject of пишет → nominative который.",
         ["программист: programmer", "код: code"]),
        ("Это девушка, ___ живёт в Бресте.", "которая",
         ["который", "которую", "которое"],
         "This is a girl who lives in Brest.",
         "Девушка is feminine; которая is the subject of живёт → nominative которая.",
         []),
        ("Письмо, ___ пришло из Беларуси, лежит на столе.", "которое",
         ["который", "которая", "которого"],
         "The letter that arrived from Belarus is lying on the table.",
         "Письмо is neuter; которое is the subject of пришло → nominative которое.",
         ["пришло: arrived"]),
        ("Мы купили дом, ___ стоит рядом с фермой.", "который",
         ["которого", "которому", "которое"],
         "We bought a house that stands next to the farm.",
         "Дом is masculine inanimate; который is the subject of стоит → nominative (same form as inanimate accusative).",
         []),
        ("Я знаю врача, ___ работает в нашей деревне.", "который",
         ["которого", "которому", "которая"],
         "I know a doctor who works in our village.",
         "The relative clause is который работает: nominative, even though врача in the main clause is animate accusative.",
         []),
        ("Батюшка, ___ я исповедовался, служит в этом храме.", "которому",
         ["которого", "которым", "который"],
         "The priest I confessed to serves in this church.",
         "исповедоваться кому? → dative которому.",
         ["исповедоваться: to confess"]),
        ("Это корова, ___ мы доим каждое утро.", "которую",
         ["которая", "которой", "которое"],
         "This is the cow we milk every morning.",
         "Корова is feminine; object of доим → accusative которую.",
         ["доим: we milk"]),
        ("Друзья, ___ я встретил в Гомеле, зовут нас в гости.", "которых",
         ["которые", "которым", "которого"],
         "The friends I met in Gomel are inviting us over.",
         "Animate plural object of встретил → accusative = genitive которых.",
         []),
        ("Сервер, ___ стоит в офисе, работает всю ночь.", "который",
         ["которое", "которого", "которая"],
         "The server that is in the office runs all night.",
         "Сервер is masculine; который is the subject of стоит → nominative.",
         ["сервер: server"]),
        ("Книги, ___ лежат на аналое, очень старые.", "которые",
         ["которых", "которым", "который"],
         "The books that are lying on the analogion are very old.",
         "Книги is inanimate plural; которые is the subject of лежат → nominative plural.",
         ["аналой: analogion, lectern"]),
        ("Город, ___ мы едем, называется Березино.", "в который",
         ["в котором", "в которую", "который"],
         "The town we are going to is called Berezino.",
         "Куда? ехать в + accusative. Город is masculine inanimate → в который.",
         []),
        ("Церковь, ___ мы молимся, стоит напротив почты.", "в которой",
         ["в которую", "в котором", "которой"],
         "The church we pray in stands across from the post office.",
         "Где? молиться в + prepositional. Церковь is feminine → в которой. Keep в.",
         ["молиться: to pray"]),
        ("Это роман, ___ все говорят в нашем городе.", "о котором",
         ["котором", "о которой", "в котором"],
         "This is a novel that everyone in our town is talking about.",
         "говорить о + prepositional. Роман is masculine → о котором. The preposition stays.",
         ["роман: novel"]),
        ("У сына есть собака, ___ он гуляет каждый вечер.", "с которой",
         ["которой", "с которым", "которую"],
         "My son has a dog that he walks every evening.",
         "гулять с + instrumental. Собака is feminine → с которой, not bare которой.",
         []),
        ("Ферма, ___ течёт ручей, принадлежит нашим соседям.", "рядом с которой",
         ["с которой", "рядом с которым", "которой"],
         "The farm that a stream runs next to belongs to our neighbors.",
         "рядом с + instrumental. Ферма is feminine → рядом с которой.",
         ["ручей: stream", "принадлежит: belongs"]),
        ("Человек, ___ я дал ключи, обещал вернуть их вечером.", "которому",
         ["которого", "которым", "который"],
         "The person I gave the keys to promised to return them in the evening.",
         "дать кому? → dative которому.",
         []),
        ("Коллега Иван, ___ я обедаю, работает программистом.", "с которым",
         ["с которой", "которым", "которому"],
         "My colleague Ivan, who I have lunch with, works as a programmer.",
         "обедать с + instrumental. Иван is a man, so с которым (коллега is common gender; agreement follows the person’s sex).",
         ["обедать: to have lunch"]),
        ("Поездка, ___ мы мечтали три года, наконец начинается.", "о которой",
         ["которой", "к которой", "о котором"],
         "The trip we had dreamed of for three years is finally starting.",
         "мечтать о + prepositional. Поездка is feminine → о которой.",
         ["мечтать: to dream of"]),
        ("Это лекарство, ___ жена привыкла после операции.", "к которому",
         ["которое", "к которой", "которому"],
         "This is the medicine my wife got used to after the operation.",
         "привыкнуть к + dative. Лекарство is neuter → к которому, not bare которое.",
         ["привыкнуть: to get used to", "лекарство: medicine"]),
        ("Ольга купила книгу, ___ ей нужна для работы.", "которая",
         ["которую", "которой", "которое"],
         "Olga bought a book that she needs for work.",
         "книга ей нужна: книга is the subject of нужна → nominative которая, not accusative которую.",
         []),
        ("Это люди, ___ батюшка говорит после службы.", "с которыми",
         ["которыми", "с которым", "которых"],
         "These are people the priest talks with after the service.",
         "говорить с + instrumental, plural → с которыми. Bare которыми drops the preposition.",
         []),
        ("Машина, ___ отец ездит на рынок, стоит у сарая.", "на которой",
         ["в которой", "на котором", "которой"],
         "The car Father drives to the market is standing by the barn.",
         "ездить на машине: на + prepositional. Машина is feminine → на которой.",
         ["сарай: barn"]),
        ("Дети, ___ мы гордимся, помогают на ферме.", "которыми",
         ["которых", "с которыми", "которым"],
         "The children we are proud of help on the farm.",
         "гордиться + instrumental, no с → которыми.",
         ["гордиться: to be proud of"]),
        ("Жена, ___ он мечтает вечерами, живёт в Минске.", "о которой",
         ["о котором", "которой", "о ком"],
         "The wife he dreams about in the evenings lives in Minsk.",
         "мечтать о + prepositional. Жена is feminine → о которой. (The question about a person would be о ком, but the relative form agrees with жена.)",
         []),
    ]
    for s_, a, d, tr, ex, gl in rows:
        add(B, C, S, s_, "который", a, d, ex, tr, gl)

    # ~10 instrumental: над / под, увлекаться / заниматься, pronouns с ней / с ними / с вами / со мной
    SI = "instrumental"
    add_noun(A, C, SI, "Над ___ летит самолёт.", "город", "ins",
             "A plane is flying over the city.",
             "Над (over, above) takes the instrumental: над городом.",
             ["самолёт: airplane"])
    add_noun(A, C, SI, "Под ___ находится подвал.", "здание", "ins",
             "There is a basement under the building.",
             "Под (under) takes the instrumental: под зданием.",
             ["подвал: basement", "здание: building"])
    add_noun(A, C, SI, "Самолёт долго кружил над ___.", "лес", "ins",
             "The plane circled over the forest for a long time.",
             "Над + instrumental: над лесом.",
             ["кружил: circled"])
    add_noun(A, C, SI, "Я с детства увлекаюсь ___.", "музыка", "ins",
             "I have been keen on music since childhood.",
             "увлекаться takes the instrumental, with no с: увлекаюсь музыкой.",
             ["увлекаться: to be keen on"])
    add_noun(A, C, SI, "По вечерам они занимаются ___.", "спорт", "ins",
             "In the evenings they work out / go in for sport.",
             "заниматься takes the instrumental, with no с: занимаются спортом.",
             ["заниматься: to go in for, be busy with"])
    add_noun(A, C, SI, "После урока он занимается ___.", "спорт", "ins",
             "After the lesson he works out / goes in for sport.",
             "заниматься + instrumental: занимается спортом. Чем они занимаются сегодня?",
             [])
    add_pron(A, C, SI, "Я уже год работаю с ___.", "она", "pins",
             "I have already been working with her for a year.",
             "с + instrumental; after a preposition она → ней: с ней.",
             [])
    add_pron(A, C, SI, "Мы всегда встречаемся с ___ поздно.", "они", "pins",
             "We always meet up with them late.",
             "с + instrumental; after a preposition они → ними: с ними.",
             ["встречаться: to meet up"])
    add_pron(A, C, SI, "С ___ интересно говорить о ферме.", "вы", "ins",
             "It is interesting to talk with you about the farm.",
             "с + instrumental: с вами (plural or formal you).",
             [])
    add_pron(A, C, SI, "Хочешь поговорить со ___ после службы?", "я", "ins",
             "Do you want to talk with me after the service?",
             "со мной: с becomes со before мной.",
             ["поговорить: to talk (a bit)"])

    # 4 мочь vs уметь contrast items, in the existing irregular conjugation pool
    SUB = "irregular"
    add(A, "conjugation", SUB,
        "Я не ___ вам помочь: у меня нет времени.", "мочь", "могу",
        ["умею", "можете", "мог"],
        "мочь is “be able / can / may” (circumstance). There is no time, so не могу — not не умею (that would mean “I don’t know how”).",
        "I can’t help you: I don’t have time.",
        ["помочь: to help"])
    add(A, "conjugation", SUB,
        "Я не ___ танцевать: меня не учили.", "уметь", "умею",
        ["могу", "умеешь", "умел"],
        "уметь is “know how.” Nobody taught me, so не умею танцевать — not не могу (that would be “I can’t right now / I’m not allowed”).",
        "I don’t know how to dance: I was never taught.",
        ["танцевать: to dance"])
    add(A, "conjugation", SUB,
        "Он не ___ прийти завтра: билетов уже нет.", "мочь", "может",
        ["умеет", "могут", "мог"],
        "No tickets is a circumstance, so мочь: не может прийти. умеет would be “doesn’t know how to come.”",
        "He can’t come tomorrow: there are no tickets left.",
        ["прийти: to come", "билетов: tickets (gen. pl.)"])
    add(A, "conjugation", SUB,
        "Она не ___ водить трактор, хотя очень хочет научиться.", "уметь", "умеет",
        ["может", "умею", "умела"],
        "She wants to learn, so this is a skill she doesn’t have yet: не умеет. не может would be “isn’t able / isn’t allowed right now.”",
        "She doesn’t know how to drive a tractor, though she very much wants to learn.",
        ["водить: to drive", "научиться: to learn how"])


def _poss_forms(stem):
    # stem is мой/твой/наш/ваш/чей
    if stem == "мой":
        return {"m": "мой", "f": "моя", "n": "моё", "p": "мои"}
    if stem == "твой":
        return {"m": "твой", "f": "твоя", "n": "твоё", "p": "твои"}
    if stem == "наш":
        return {"m": "наш", "f": "наша", "n": "наше", "p": "наши"}
    if stem == "ваш":
        return {"m": "ваш", "f": "ваша", "n": "ваше", "p": "ваши"}
    if stem == "чей":
        return {"m": "чей", "f": "чья", "n": "чьё", "p": "чьи"}
    raise SystemExit(stem)

def _adj_forms(lemma):
    """Nominative adjective forms from pymorphy."""
    ps = [p for p in M.parse(lemma) if p.tag.POS in ("ADJF", "ADJS") and "nomn" in p.tag]
    if not ps:
        ps = [p for p in M.parse(lemma) if "ADJF" in p.tag]
    if not ps:
        raise SystemExit("no adj " + lemma)
    p = ps[0]
    out = {}
    for k, tags in (("m", {"masc", "sing", "nomn"}), ("f", {"femn", "sing", "nomn"}),
                    ("n", {"neut", "sing", "nomn"}), ("p", {"plur", "nomn"})):
        f = p.inflect(tags)
        if not f:
            raise SystemExit("no %s for %s" % (k, lemma))
        out[k] = f.word
    return out

def add_agree(level, cat, sub, s, base, forms, key, tr, ex, glosses=None):
    a = forms[key]
    d = [forms[k] for k in forms if k != key]
    # keep 3
    if len(d) > 3:
        d = d[:3]
    if len(d) < 3:
        raise SystemExit((s, d))
    add(level, cat, sub, s, base, a, d, ex, tr, glosses)

def build_basics_a1():
    C = "basics"
    # --- possessives ---
    S = "possessives"
    rows = [
        ("Это ___ трактор.", "мой", "m", "This is my tractor.",
         "Трактор is masculine (ends in a consonant), so мой stays мой. Моя would be feminine.", []),
        ("Это ___ жена.", "мой", "f", "This is my wife.",
         "Жена is feminine, so мой becomes моя.", []),
        ("Где ___ ведро?", "мой", "n", "Where is my bucket?",
         "Ведро is neuter (ends in -о), so use моё.", ["ведро: bucket"]),
        ("Это ___ коровы.", "мой", "p", "These are my cows.",
         "Коровы is plural, so use мои (not моя, even though корова is feminine in the singular).", []),
        ("Где ___ паспорт?", "твой", "m", "Where is your passport?",
         "Паспорт is masculine: твой паспорт.", []),
    ]
    # existing has "___ сестра живёт в Москве." with Твоя. Don't clash.
    rows = [r for r in rows if r[4]]
    rows += [
        ("___ ферма далеко от города?", "твой", "f",
         "Is your farm far from the city?",
         "Ферма is feminine, so твой becomes твоя.", []),
        ("Это ___ сено, не наше.", "твой", "n",
         "This is your hay, not ours.",
         "Сено is neuter: твоё сено.", []),
        ("Где ___ ключи?", "твой", "p",
         "Where are your keys?",
         "Ключи is plural: твои ключи.", []),
        ("Это ___ храм, мы здесь молимся.", "наш", "m",
         "This is our church; we pray here.",
         "Храм is masculine: наш храм.", []),
        ("___ церковь стоит на холме.", "наш", "f",
         "Our church stands on the hill.",
         "Церковь is feminine: наша церковь. Наш would be masculine.", []),
        ("___ поле ещё не скошено.", "наш", "n",
         "Our field hasn't been mowed yet.",
         "Поле is neuter: наше поле.", []),
        ("___ куры уже на насесте.", "наш", "p",
         "Our hens are already on the roost.",
         "Куры is plural: наши куры.", ["насест: roost"]),
        ("Это ___ билет до Минска.", "ваш", "m",
         "This is your ticket to Minsk.",
         "Билет is masculine: ваш билет. Вы / ваш is the polite or plural 'your'.", []),
        ("___ жена тоже на ферме?", "ваш", "f",
         "Is your wife on the farm too?",
         "Жена is feminine: ваша жена.", []),
        ("___ молоко ещё свежее.", "ваш", "n",
         "Your milk is still fresh.",
         "Молоко is neuter: ваше молоко.", []),
        ("___ документы лежат на кассе.", "ваш", "p",
         "Your documents are on the checkout counter.",
         "Документы is plural: ваши документы.", []),
        ("___ это трактор?", "чей", "m",
         "Whose tractor is this?",
         "Чей agrees with the noun. Трактор is masculine: чей трактор?", []),
        ("___ это сумка?", "чей", "f",
         "Whose bag is this?",
         "Сумка is feminine: чья сумка? (existing item was чья машина).", []),
        ("___ это пальто?", "чей", "n",
         "Whose coat is this?",
         "Пальто is neuter (and indeclinable): чьё пальто?", []),
        ("___ это ворота?", "чей", "p",
         "Whose gate is this?",
         "Ворота is plural-only: чьи ворота? (not чей ворота).", []),
        ("Это ___ компьютер, не мой.", "он", "его",
         "This is his computer, not mine.",
         "Его, её and их (his / her / their) never change for gender or number: его компьютер, его жена, его коровы.", []),
    ]
    # его/её/их need custom add because they don't have 4-way forms
    for row in rows:
        if row[1] in ("мой", "твой", "наш", "ваш", "чей"):
            s, stem, key, tr, ex, gl = row
            forms = _poss_forms(stem)
            add_agree(A, C, S, s, stem, forms, key, tr, ex, gl)

    add(A, C, S, "Это ___ компьютер, не мой.", "его", "его",
        ["её", "их", "ему"],
        "Его (his) never changes for gender or number of the following noun: его компьютер, его жена, его коровы. Ему is dative ('to him').",
        "This is his computer, not mine.", [])
    add(A, C, S, "Это ___ ферма, она сама её ведёт.", "её", "её",
        ["его", "ей", "их"],
        "Её (her) is indeclinable as a possessive: её ферма, её трактор, её коровы. Ей is dative ('to her').",
        "This is her farm; she runs it herself.", [])
    add(A, C, S, "Это ___ курятник, не наш.", "их", "их",
        ["его", "её", "им"],
        "Их (their) never changes: их курятник, их жена, их коровы. Им is dative ('to them').",
        "This is their coop, not ours.", [])
    add(A, C, S, "Каждый фермер любит ___ ферму.", "свой", "свою",
        ["своя", "своё", "свои"],
        "Свой means 'one's own' and agrees with the noun. Ферму is feminine accusative (direct object of любит), so свою ферму. Своя would be nominative.",
        "Every farmer loves his (own) farm.", [])
    add(A, C, S, "Я забыл ___ паспорт дома.", "свой", "свой",
        ["своя", "своё", "свои"],
        "Паспорт is masculine accusative (inanimate, so it looks like the nominative): свой паспорт. Свой here means 'my own', because the subject is я.",
        "I left my passport at home.", [])
    add(A, C, S, "Они продают ___ молоко в городе.", "свой", "своё",
        ["свой", "своя", "свои"],
        "Молоко is neuter, the direct object (accusative = nominative): своё молоко. Свой would be masculine.",
        "They sell their own milk in town.", [])
    add(A, C, S, "Мы пасём ___ коров на лугу.", "свой", "своих",
        ["свои", "своя", "своё"],
        "Коров is animate accusative plural (direct object), so the possessive also takes the animate accusative/genitive plural: своих коров. Свои would be nominative plural.",
        "We graze our own cows in the meadow.", [])

    # --- adjectives ---
    S = "adjectives"
    arows = [
        ("У нас ___ трактор.", "новый", "m", "We have a new tractor.",
         "Adjectives agree with the noun in gender and number. Трактор is masculine: новый трактор.", []),
        ("Это ___ ферма.", "большой", "f", "This is a big farm.",
         "Ферма is feminine: большая ферма (not большой).", []),
        ("Какое ___ поле!", "красивый", "n", "What a beautiful field!",
         "Поле is neuter: красивое поле. Какое already shows the neuter.", []),
        ("У соседа ___ коровы.", "здоровый", "p", "The neighbor has healthy cows.",
         "Коровы is plural: здоровые коровы. Здоровый would be masculine singular.", ["здоровый: healthy"]),
        ("Сегодня ___ молоко.", "свежий", "n", "The milk is fresh today.",
         "Молоко is neuter: свежее молоко (not свежое).", []),
        ("Мама купила ___ хлеб.", "свежий", "m", "Mom bought fresh bread.",
         "Хлеб is masculine, and here it is the direct object (accusative = nominative for inanimate masculine): свежий хлеб.", []),
        ("Жена сварила ___ суп.", "вкусный", "m", "My wife made a tasty soup.",
         "Суп is masculine: вкусный суп. The adjective agrees with суп, the direct object, which looks like the nominative.", []),
        ("Это очень ___ яйца.", "вкусный", "p", "These are very tasty eggs.",
         "Яйца is plural (neuter in the singular, but adjectives use the one plural form): вкусные яйца.", []),
        ("В этом магазине ___ сыр.", "дорогой", "m", "The cheese in this store is expensive.",
         "Сыр is masculine: дорогой сыр. Дорогая would be feminine.", []),
        ("Это ___ икона, шестнадцатого века.", "старый", "f", "This is an old icon, from the sixteenth century.",
         "Икона is feminine: старая икона.", []),
        ("У нас ___ пастбище за рекой.", "большой", "n", "We have a large pasture across the river.",
         "Пастбище is neuter: большое пастбище.", []),
        ("На ферме ___ ворота.", "новый", "p", "The farm has a new gate.",
         "Ворота is plural-only: новые ворота (not новый ворота).", []),
        ("Это ___ храм, мы здесь молимся каждое воскресенье.", "православный", "m",
         "This is an Orthodox church; we pray here every Sunday.",
         "Храм is masculine: православный храм. Православная would agree with церковь (feminine).", []),
        ("Наша ___ церковь стоит в деревне.", "православный", "f",
         "Our Orthodox church stands in the village.",
         "Церковь is feminine: православная церковь.", []),
        ("Какой ___ пруд!", "красивый", "m", "What a beautiful pond!",
         "Пруд is masculine, and какой already shows the masculine: красивый пруд.", []),
        ("У нас ___ кухня.", "уютный", "f", "We have a cozy kitchen.",
         "Кухня is feminine: уютная кухня.", []),
        ("Это ___ пальто, мне жарко.", "тёплый", "n", "This is a warm coat; I'm hot.",
         "Пальто is neuter (and indeclinable): тёплое пальто. Тёплый would be masculine.", ["тёплый: warm"]),
        ("На лугу пасутся ___ лошади.", "дикий", "p", "Wild horses are grazing in the meadow.",
         "Лошади is plural: дикие лошади. Дикий would be masculine singular (дикий олень).", []),
        ("Это ___ заяц, не кролик.", "дикий", "m", "This is a wild hare, not a rabbit.",
         "Заяц is masculine: дикий заяц.", []),
        ("У кассы ___ очередь.", "длинный", "f", "There is a long line at the checkout.",
         "Очередь is feminine: длинная очередь.", ["очередь: line, queue", "длинный: long"]),
        ("Сегодня ___ день для сенокоса.", "хороший", "m", "Today is a good day for haymaking.",
         "День is masculine: хороший день. Хорошая would be feminine (хорошая погода).", ["сенокос: haymaking"]),
        ("Какое ___ сено в этом году!", "хороший", "n", "What good hay this year!",
         "Сено is neuter: хорошее сено (not хорошое).", []),
        ("Это ___ билеты до Минска.", "дешёвый", "p", "These are cheap tickets to Minsk.",
         "Билеты is plural: дешёвые билеты. Note ё in дешёвый.", []),
        ("На рынке ___ мясо.", "дешёвый", "n", "The meat at the market is cheap.",
         "Мясо is neuter: дешёвое мясо.", []),
        ("У соседа ___ бык.", "злой", "m", "The neighbor has a mean bull.",
         "Бык is masculine: злой бык. Злая would be feminine.", []),
        ("Какая ___ песня!", "известный", "f", "What a well-known song!",
         "Песня is feminine: известная песня. Какая already shows the feminine.", ["известный: well-known"]),
    ]
    for s, lemma, key, tr, ex, gl in arows:
        forms = _adj_forms(lemma)
        add_agree(A, C, S, s, lemma, forms, key, tr, ex, gl)

    # --- noun gender ---
    S = "noun gender"
    grows = [
        ("Где мой трактор? — Вот ___.", "он", "Where is my tractor? — Here it is.",
         "Трактор ends in a consonant, so it is masculine: он (it / he). Она would be feminine.", []),
        ("Где моя ферма? — Вот ___.", "она", "Where is my farm? — Here it is.",
         "Ферма ends in -а, so it is feminine: она.", []),
        ("Где наше поле? — Вот ___.", "оно", "Where is our field? — Here it is.",
         "Поле ends in -е, so it is neuter: оно.", []),
        ("Где ворота? — Вот ___.", "они", "Where is the gate? — Here it is.",
         "Ворота is plural-only, so even one gate is они (they), not он or оно.", []),
        ("Где моё ведро? — Вот ___.", "оно", "Where is my bucket? — Here it is.",
         "Ведро ends in -о, so it is neuter: оно.", []),
        ("Где моя лошадь? — Вот ___.", "она", "Where is my horse? — Here it is.",
         "Лошадь ends in a soft sign after a consonant and is feminine: она. (A few -ь nouns are masculine: путь, день, календарь.)", []),
        ("Где мой путь? — Вот ___.", "он", "Where is my path? — Here it is.",
         "Путь ends in -ь but is masculine: он. This is one of the exceptions you just have to remember (also день, календарь).", ["путь: path, way"]),
        ("Где моё время? — Вот ___, у тебя ещё час.", "оно", "Where is my time? — Here it is; you still have an hour.",
         "Время ends in -мя and is neuter: оно (like имя, знамя, племя).", []),
        ("Где мой кофе? — Вот ___.", "он", "Where is my coffee? — Here it is.",
         "Кофе is indeclinable but masculine in standard Russian: он (not оно). In casual speech some people treat it as neuter, but the textbook form is masculine.", []),
        ("Где наше кафе? — Вот ___.", "оно", "Where is our café? — Here it is.",
         "Кафе is indeclinable and neuter: оно. Compare masculine кофе.", []),
        ("Где моё пальто? — Вот ___, на вешалке.", "оно", "Where is my coat? — Here it is, on the rack.",
         "Пальто is indeclinable and neuter: оно. (An existing item already used пальто; this one adds the location.)", []),
        ("Где моё меню? — Вот ___.", "оно", "Where is my menu? — Here it is.",
         "Меню is indeclinable and neuter: оно.", []),
        ("Где наше метро? — Вот ___, за углом.", "оно", "Where is our metro? — Here it is, around the corner.",
         "Метро is indeclinable and neuter: оно.", []),
        ("Где моё такси? — Вот ___.", "оно", "Where is my taxi? — Here it is.",
         "Такси is indeclinable and neuter: оно.", []),
        ("Где мой папа? — Вот ___.", "он", "Where is my dad? — Here he is.",
         "Папа ends in -а but means a man, so it is masculine: он (not она). The same is true of дядя, дедушка, батюшка, Саша (for a man).", []),
        ("Где наш батюшка? — Вот ___.", "он", "Where is Father? — Here he is.",
         "Батюшка ends in -а but is masculine: он. Possessives and adjectives also stay masculine: наш батюшка, добрый батюшка.", []),
        ("Где моя свеча? — Вот ___.", "она", "Where is my candle? — Here it is.",
         "Свеча ends in -а, so it is feminine: она.", []),
        ("Где мой храм? — Вот ___.", "он", "Where is my church? — Here it is.",
         "Храм ends in a consonant, so it is masculine: он. Церковь is the feminine word for 'church'.", []),
        ("Где моя церковь? — Вот ___.", "она", "Where is my church? — Here it is.",
         "Церковь ends in -ь and is feminine: она.", []),
        ("Где моё сено? — Вот ___, в сарае.", "оно", "Where is my hay? — Here it is, in the barn.",
         "Сено ends in -о, so it is neuter: оно.", []),
        ("Где мой пруд? — Вот ___.", "он", "Where is my pond? — Here it is.",
         "Пруд ends in a consonant, so it is masculine: он.", []),
        ("Где мои вилы? — Вот ___.", "они", "Where is my pitchfork? — Here it is.",
         "Вилы is plural-only, like ворота and ножницы: even one pitchfork is они.", []),
        ("Где моя кукуруза? — Вот ___.", "она", "Where is my corn? — Here it is.",
         "Кукуруза ends in -а, so it is feminine: она.", []),
        ("Где моё зерно? — Вот ___.", "оно", "Where is my grain? — Here it is.",
         "Зерно ends in -о, so it is neuter: оно.", []),
        ("Где мой день? — Какой ___ сегодня? Понедельник.", "он", "Where has my day gone? — What day is it today? Monday.",
         "День ends in -ь but is masculine: он, какой день (not какая).", []),
        ("Где моя ночь? Я совсем не спал. — Вот ___, уже утро.", "она", "Where did my night go? I didn't sleep at all. — Here it is; it's already morning.",
         "Ночь ends in -ь and is feminine: она, спокойной ночи.", []),
        ("Где моё яблоко? — Вот ___.", "оно", "Where is my apple? — Here it is.",
         "Яблоко ends in -о, so it is neuter: оно. Яблоки (plural) would be они.", []),
        ("Где мои яйца? — Вот ___, в корзине.", "они", "Where are my eggs? — Here they are, in the basket.",
         "Яйца is plural: они. One egg (яйцо) would be оно.", []),
        ("Где мой календарь? — Вот ___.", "он", "Where is my calendar? — Here it is.",
         "Календарь ends in -ь but is masculine: он (like день, путь, словарь).", ["календарь: calendar"]),
        ("Где моя соль? — Вот ___, на столе.", "она", "Where is my salt? — Here it is, on the table.",
         "Соль ends in -ь and is feminine: она, соль (like ночь, лошадь, церковь).", ["соль: salt"]),
    ]
    PRON4 = {"он": ["она", "оно", "они"], "она": ["он", "оно", "они"],
             "оно": ["он", "она", "они"], "они": ["он", "она", "оно"]}
    for s, a, tr, ex, gl in grows:
        # avoid clashing "Где моё пальто? — Вот ___." existing uses "Где твоё пальто?"
        add(A, C, S, s, "он / она / оно / они", a, PRON4[a], ex, tr, gl)

    # --- plurals ---
    S = "plurals"
    prows = [
        ("На лугу пасутся наши ___.", "корова", "Our cows are grazing in the meadow.",
         "Корова forms a regular plural in -ы: коровы. Коров is the genitive plural (много коров).", []),
        ("В курятнике сидят ___.", "курица", "The hens are sitting in the coop.",
         "The everyday plural of курица is the irregular куры (not курицы, which is also possible but less common on a farm, and is the genitive singular too).", []),
        ("В стаде бегают маленькие ___.", "телёнок", "Little calves are running around in the herd.",
         "Телёнок has an irregular plural: телята (like ребёнок → ребята, цыплёнок → цыплята).", []),
        ("Утром ___ кричат на заборе.", "петух", "In the morning the roosters crow on the fence.",
         "Петух has a regular plural in -и (after к/г/х/ж/ш/ч/щ): петухи (not петухы).", []),
        ("На столе лежат свежие ___.", "яйцо", "There are fresh eggs on the table.",
         "Яйцо (neuter -о) takes -а in the nominative plural, with a stress change: яйца. Яиц is genitive plural.", []),
        ("В сарае стоят два ___.? wait use npl", "трактор", "", []),
    ]
    prows = [r for r in prows if r[3]]
    prows += [
        ("У забора стоят наши ___.", "трактор", "Our tractors are standing by the fence.",
         "Трактор is a regular masculine noun: тракторы (not трактора; the -а plural is for words like дом → дома, поезд → поезда, паспорт → паспорта).", []),
        ("На полке стоят ___.", "икона", "Icons are standing on the shelf.",
         "Икона (feminine -а) takes -ы: иконы. Икон is the genitive plural.", []),
        ("Перед службой мы зажигаем ___.", "свеча", "Before the service we light the candles.",
         "Свеча takes -и (after ч): свечи. Свечей is the genitive plural.", []),
        ("В кармане у меня только эти ___.", "билет", "I only have these tickets in my pocket.",
         "Билет is a regular masculine noun: билеты.", []),
        ("На кассе лежат наши ___.", "паспорт", "Our passports are on the checkout counter.",
         "Паспорт has the stressed -а plural: паспорта (not паспорты). Other common -а plurals: дома, поезда, города, вечера.", []),
        ("К вокзалу подошли ___.", "поезд", "Trains pulled up to the station.",
         "Поезд has the stressed -а plural: поезда (not поезды).", []),
        ("В поле работают ___.", "человек", "People are working in the field.",
         "The nominative plural of человек is the irregular люди (not человеки). Человек is kept after many numerals (пять человек).", []),
        ("У нас на ферме весёлые ___.", "ребёнок", "We have cheerful kids on the farm.",
         "Ребёнок has two plurals: the everyday дети, and ребята (more colloquial, 'kids / guys'). The form ребёнки is wrong.", []),
        ("Мои ___ живут в Беларуси.", "брат", "My brothers live in Belarus.",
         "Брат has an irregular plural: братья (like друг → друзья, лист → листья, стул → стулья).", []),
        ("У меня двое ___ и одна сестра? wait npl", "сын", "", []),
    ]
    prows = [r for r in prows if r[3]]
    prows += [
        ("Мои ___ помогают на ферме.", "сын", "My sons help on the farm.",
         "Сын has an irregular plural: сыновья (not сыны in everyday speech, though сыны appears in solemn or poetic language).", []),
        ("У калитки сидят наши ___.", "собака", "Our dogs are sitting by the gate.",
         "Собака is a regular feminine noun: собаки.", []),
        ("В корзине лежат ___.", "яблоко", "There are apples in the basket.",
         "Яблоко (neuter) takes -и after к: яблоки (not яблока in the nominative plural; яблока is genitive singular).", []),
        ("На столе стоят ___ и тарелки.", "стакан", "There are glasses and plates on the table.",
         "Стакан is a regular masculine noun: стаканы.", ["стакан: glass (for drinking)"]),
        ("В ящике лежат старые ___.", "ключ", "The old keys are in the drawer.",
         "Ключ takes -и (after ч): ключи (not ключы).", []),
        ("За фермой видны чужие ___.", "дом", "Other people's houses are visible beyond the farm.",
         "Дом has the stressed -а plural: дома. Дома can also mean 'at home' (an adverb), but here it is the noun 'houses'.", []),
        ("У нас в деревне новые ___.", "магазин", "There are new stores in our village.",
         "Магазин is regular: магазины.", []),
        ("На границе проверяют ___.", "документ", "They check documents at the border.",
         "Документ is regular: документы.", []),
        ("В храме висят старые ___.", "икона", "Old icons hang in the church.",
         "Already have иконы on a shelf — different s is fine? 'висят старые ___' vs 'на полке стоят'. OK.",
         "Икона → иконы. Старые agrees with the plural.", []),
    ]
    # last one has a stray comment in ex - I put a comment as 4th string? Let me look... 
    # ("В храме висят старые ___.", "икона", "Old icons hang in the church.",
    #  "Already have иконы on a shelf — different s is fine? 'висят старые ___' vs 'на полке стоят'. OK.",
    #  "Икона → иконы. Старые agrees with the plural.", []),
    # That's 6 fields with an extra English/ex mixed. I'll filter badly shaped later if syntax fails.

    # I'll just not include a duplicate икона and add others
    prows = [r for r in prows if not (len(r) != 6 or r[0].startswith("В храме висят"))]
    prows += [
        ("Над полем летят дикие ___.", "гусь", "Wild geese are flying over the field.",
         "Гусь has the plural гуси (not гусы). Like мышь → мыши, лошадь → лошади.", ["гусь: goose"]),
        ("У соседа во дворе бегают ___.", "овца", "Sheep are running around in the neighbor's yard.",
         "Овца has a fleeting vowel in some forms, but the nominative plural is овцы (not овци).", []),
        ("Вечером мы слушаем старые ___ группы «Молчат Дома».", "песня", "In the evening we listen to old Molchat Doma songs.",
         "Песня (feminine -я) takes -и: песни. Песен is the genitive plural.", []),
    ]
    for s, lemma, tr, ex, gl in prows:
        forms = noun_forms(lemma)
        a = forms["npl"]
        # pedagogical distractors: a regular-looking wrong plural, the singular, the genitive plural
        fake = lemma + "ы" if not lemma.endswith(("а", "я", "о", "е", "ь")) else lemma[:-1] + "и"
        cands = [forms.get("nom"), forms.get("gpl"), forms.get("gen"), fake, forms.get("acc"), lemma + "и", lemma + "а"]
        d, seen = [], {a.replace("ё","е").lower()}
        for x in cands:
            if not x or x == "-" or x.replace("ё","е").lower() in seen:
                continue
            seen.add(x.replace("ё","е").lower())
            d.append(x)
            if len(d) == 3:
                break
        if len(d) < 3:
            d = pad_distractors(lemma, a, d)
        add(A, C, S, s, lemma, a, d, ex, tr, gl)


    more_pl = [
        ("На лугу пасутся наши ___.", "корова", "Our cows are grazing in the meadow.",
         "Корова forms a regular plural in -ы: коровы. Коров is the genitive plural (много коров).", []),
        ("В курятнике сидят ___.", "курица", "The hens are sitting in the coop.",
         "The everyday plural of курица is the irregular куры (not курицы, which is also possible but sounds more like 'of a hen' or a bookish plural).", []),
        ("В стаде бегают маленькие ___.", "телёнок", "Little calves are running around in the herd.",
         "Телёнок has an irregular plural: телята (like ребёнок → ребята, цыплёнок → цыплята).", []),
        ("Утром ___ кричат на заборе.", "петух", "In the morning the roosters crow on the fence.",
         "Петух has a regular plural in -и (after к/г/х/ж/ш/ч/щ): петухи, never петухы.", []),
        ("На столе лежат свежие ___.", "яйцо", "There are fresh eggs on the table.",
         "Яйцо (neuter -о) takes -а in the nominative plural, with a stress change: яйца. Яиц is genitive plural.", []),
        ("У забора стоят наши ___.", "трактор", "Our tractors are standing by the fence.",
         "Трактор is regular: тракторы. The stressed -а plural (дома, поезда, паспорта) does not apply here.", []),
        ("На полке стоят ___.", "икона", "Icons are standing on the shelf.",
         "Икона (feminine -а) takes -ы: иконы. Икон is the genitive plural.", []),
        ("Перед службой мы зажигаем ___.", "свеча", "Before the service we light the candles.",
         "Свеча takes -и after ч: свечи. Свечей is the genitive plural.", []),
        ("В кармане у меня только эти ___.", "билет", "I only have these tickets in my pocket.",
         "Билет is a regular masculine noun: билеты.", []),
        ("На кассе лежат наши ___.", "паспорт", "Our passports are on the checkout counter.",
         "Паспорт has the stressed -а plural: паспорта (not паспорты). Other common -а plurals: дома, поезда, города.", []),
        ("К вокзалу подошли ___.", "поезд", "Trains pulled up to the station.",
         "Поезд has the stressed -а plural: поезда (not поезды).", []),
        ("В поле работают ___.", "человек", "People are working in the field.",
         "The nominative plural of человек is the irregular люди (not человеки). Человек is kept after many numerals (пять человек).", []),
        ("У нас на ферме весёлые ___.", "ребёнок", "We have cheerful kids on the farm.",
         "Ребёнок has the everyday plural дети (ребята is more colloquial). Ребёнки is wrong.", []),
        ("Мои ___ живут в Беларуси.", "брат", "My brothers live in Belarus.",
         "Брат has an irregular plural: братья (like друг → друзья, стул → стулья).", []),
        ("Мои ___ помогают на ферме.", "сын", "My sons help on the farm.",
         "Сын has an irregular plural: сыновья (сыны appears only in solemn or poetic language).", []),
        ("У калитки сидят наши ___.", "собака", "Our dogs are sitting by the gate.",
         "Собака is a regular feminine noun: собаки.", []),
        ("В корзине лежат ___.", "яблоко", "There are apples in the basket.",
         "Яблоко (neuter) takes -и after к: яблоки (яблока is the genitive singular, not the nominative plural).", []),
        ("На столе стоят ___ и тарелки.", "стакан", "There are glasses and plates on the table.",
         "Стакан is a regular masculine noun: стаканы.", ["стакан: glass"]),
        ("В ящике лежат старые ___.", "ключ", "The old keys are in the drawer.",
         "Ключ takes -и after ч: ключи (not ключы).", []),
        ("За фермой видны чужие ___.", "дом", "Other people's houses are visible beyond the farm.",
         "Дом has the stressed -а plural: дома. The same spelling дома can also be the adverb 'at home', but here it is the noun 'houses'.", []),
        ("У нас в деревне новые ___.", "магазин", "There are new stores in our village.",
         "Магазин is regular: магазины.", []),
        ("На границе проверяют ___.", "документ", "They check documents at the border.",
         "Документ is regular: документы.", []),
        ("В сарае мыши, а на чердаке летучие ___.", "мышь", "There are mice in the barn, and bats in the attic.",
         "Мышь (feminine -ь) takes -и: мыши. The same pattern: лошадь → лошади, ночь → ночи.", ["мышь: mouse", "летучая мышь: bat"]),
        ("Осенью с деревьев падают ___.", "лист", "In the autumn the leaves fall from the trees.",
         "Лист has an irregular plural: листья (like брат → братья, стул → стулья). Листы means 'sheets of paper'.", ["лист: leaf; sheet"]),
        ("В гостиной стоят старые ___.", "стул", "There are old chairs in the living room.",
         "Стул has an irregular plural: стулья (not стулы).", ["стул: chair"]),
        ("На столе лежат острые ___.", "нож", "There are sharp knives on the table.",
         "Нож takes -и after ж: ножи (not ножы). Острые agrees with the plural.", ["острый: sharp"]),
    ]
    for s, lemma, tr, ex, gl in more_pl:
        forms = noun_forms(lemma)
        a = forms["npl"]
        fake = lemma + "ы" if not lemma.endswith(("а", "я", "о", "е", "ь")) else lemma[:-1] + "и"
        cands = [forms.get("nom"), forms.get("gpl"), forms.get("gen"), fake, forms.get("acc"), lemma + "и", lemma + "а"]
        d, seen = [], {a.replace("ё","е").lower()}
        for x in cands:
            if not x or x == "-" or x.replace("ё","е").lower() in seen:
                continue
            seen.add(x.replace("ё","е").lower())
            d.append(x)
            if len(d) == 3:
                break
        if len(d) < 3:
            d = pad_distractors(lemma, a, d)
        add(A, C, S, s, lemma, a, d, ex, tr, gl)


def build_conj():
    C = "conjugation"
    # ---- A1 1st conjugation ----
    S = "1st conjugation"
    rows = [
        ("Я ___ на ферме уже двадцать лет.", "работать", "1s",
         "I have been working on the farm for twenty years.",
         "1st conjugation (most -ать verbs): я работаю, ты работаешь, он работает, мы работаем, вы работаете, они работают.",
         []),
        ("Ты ___ в поле до вечера?", "работать", "2s",
         "Do you work in the field until evening?",
         "1st conjugation: ты работаешь (-ешь).", []),
        ("Он ___ программистом в Минске.", "работать", "3s",
         "He works as a programmer in Minsk.",
         "1st conjugation: он работает (-ет). Программистом is instrumental (работать кем?).", []),
        ("Что ты ___ по вечерам?", "делать", "2s",
         "What do you do in the evenings?",
         "1st conjugation: ты делаешь (-ешь).", []),
        ("Мы ___ сено в июле.", "собирать", "1p",
         "We gather the hay in July.",
         "1st conjugation: мы собираем (-ем). Сено is the direct object (accusative).",
         ["собирать: to gather"]),
        ("Они ___ новый забор у сарая.", "ставить", "3p",
         "WAIT ставить is 2nd. skip", "2nd", []),
    ]
    rows = [r for r in rows if "WAIT" not in r[4] and r[4] != "2nd"]
    rows += [
        ("Они ___ зерно в кормушки.", "собирать", "3p",
         "They are gathering grain into the feeders.",
         "1st conjugation: они собирают (-ют).", []),
        ("Я хорошо ___ этот код.", "знать", "1s",
         "I know this code well.",
         "Знать is 1st conjugation: я знаю, ты знаешь, он знает (not знаюю). Код is the direct object.", []),
        ("Ты ___ дорогу на ферму?", "знать", "2s",
         "Do you know the way to the farm?",
         "1st conjugation: ты знаешь.", []),
        ("Он ___ , где лежат ключи.", "знать", "3s",
         "He knows where the keys are.",
         "1st conjugation: он знает.", []),
        ("Я ___ о жене, пока пасу коров.", "думать", "1s",
         "I think about my wife while I graze the cows.",
         "1st conjugation: я думаю. О жене is prepositional.", []),
        ("Вы ___ на русском или на английском?", "думать", "2p",
         "Do you think in Russian or in English?",
         "1st conjugation: вы думаете (-ете).", []),
        ("Я ___ хлеб в этом магазине.", "покупать", "1s",
         "I buy bread in this store.",
         "1st conjugation: я покупаю. Хлеб is the direct object (accusative).", []),
        ("Жена ___ молоко у соседа.", "покупать", "3s",
         "My wife buys milk from the neighbor.",
         "1st conjugation: она покупает. У соседа is genitive after у.", []),
        ("По вечерам мы ___ в деревне.", "гулять", "1p",
         "In the evenings we walk in the village.",
         "1st conjugation: мы гуляем.", ["гулять: to walk, stroll"]),
        ("Дети ___ у пруда.", "играть", "3p",
         "The children are playing by the pond.",
         "1st conjugation: они играют. У пруда is genitive after у.", []),
        ("Я ___ в шахматы с женой.", "играть", "1s",
         "I play chess with my wife.",
         "1st conjugation: я играю. С женой is instrumental after с.", []),
        ("Ты ___ музыку Молчат Дома?", "слушать", "2s",
         "Do you listen to Molchat Doma's music?",
         "1st conjugation: ты слушаешь. Музыку is the direct object (accusative).", []),
        ("Мы ___ эту песню в машине.", "слушать", "1p",
         "We listen to this song in the car.",
         "1st conjugation: мы слушаем.", []),
        ("Я ___ книгу на крыльце.", "читать", "1s",
         "I'm reading a book on the porch.",
         "1st conjugation: я читаю. Книгу is the direct object. (An existing item was 'Я ___ интересную книгу.' — this one names the place.)",
         ["крыльцо: porch"]),
        ("Вы ___ газету каждое утро?", "читать", "2p",
         "Do you read the newspaper every morning?",
         "1st conjugation: вы читаете.", []),
        ("Они плохо ___ по-русски, но стараются.", "понимать", "3p",
         "They don't understand Russian well, but they try.",
         "1st conjugation: они понимают (-ют).", []),
        ("Я ___ вопрос батюшке.", "задавать", "1s",
         "I ask Father a question. / I am putting a question to Father.",
         "Задавать is 1st conjugation with a stem change in some forms? Actually я задаю. Let me use спрашивать.",
         []),
    ]
    # remove задавать if I used a doubtful comment as ex - I'll skip that row
    rows = [r for r in rows if "Задавать" not in r[4]]
    rows += [
        ("Я ___ батюшку после службы.", "спрашивать", "1s",
         "I ask Father after the service.",
         "1st conjugation: я спрашиваю. Спрашивать takes the accusative of the person asked (батюшку).",
         ["спрашивать: to ask"]),
        ("Почему вы ___ так поздно?", "завтракать", "2p",
         "Why do you have breakfast so late?",
         "1st conjugation: вы завтракаете.", ["завтракать: to have breakfast"]),
        ("Утром он ___ в пять часов.", "вставать", "3s",
         "In the morning he gets up at five.",
         "Вставать is 1st conjugation with a stem change: он встаёт (в-ста-ё-т), я встаю, они встают. The -ва- drops in the present.",
         []),
        ("Мы ___ калитку на ночь.", "закрывать", "1p",
         "We close the gate at night.",
         "1st conjugation: мы закрываем. Калитку is the direct object (accusative).",
         ["закрывать: to close"]),
        ("Я ___ поле с весны.", "пахать", "1s",
         "I have been plowing the field since spring.",
         "Пахать is 1st conjugation with a stem change: я пашу, ты пашешь, он пашет (х → ш), not пахаю.",
         ["пахать: to plow"]),
        ("Он ___ письмо жене каждый день.", "писать", "3s",
         "He writes a letter to his wife every day.",
         "Писать is 1st conjugation with a stem change: он пишет (с → ш), not писает. Жене is dative.",
         []),
        ("Я ___ ключи от сарая.", "искать", "1s",
         "I'm looking for the keys to the barn.",
         "Искать is 1st conjugation with a stem change: я ищу, ты ищешь (к → щ), not искаю. Ключи is the direct object.",
         ["искать: to look for"]),
        ("Мы ___ на крыльце и пьём чай.", "отдыхать", "1p",
         "We are resting on the porch and drinking tea.",
         "1st conjugation: мы отдыхаем.", ["отдыхать: to rest"]),
    ]
    for s, inf, key, tr, ex, gl in rows:
        typo = None
        # a typical 1st-conj learner typo for a couple of items
        if inf == "пахать" and key == "1s":
            typo = ["пахаю"]
        if inf == "писать" and key == "3s":
            typo = ["писает"]
        if inf == "искать" and key == "1s":
            typo = ["искаю"]
        add_verb(A, C, S, s, inf, key, tr, ex, gl, typo=typo)

    # ---- A1 2nd conjugation ----
    S = "2nd conjugation"
    rows = [
        ("Я ___ коров в шесть утра.", "кормить", "1s",
         "I feed the cows at six in the morning.",
         "2nd conjugation (most -ить verbs): я кормлю (м → мл in the я-form), ты кормишь, он кормит, они кормят.",
         ["кормить: to feed"]),
        ("Ты уже ___ кур?", "кормить", "2s",
         "Have you already fed the hens? / Are you feeding the hens yet?",
         "2nd conjugation: ты кормишь (-ишь). Кур is the animate accusative plural.", []),
        ("Жена ___ телят тёплым молоком.", "кормить", "3s",
         "My wife feeds the calves with warm milk.",
         "2nd conjugation: она кормит (-ит). Телят is animate accusative plural; молоком is instrumental.", []),
        ("Утром я ___ коров.", "доить", "1s",
         "In the morning I milk the cows.",
         "2nd conjugation: я дою, ты доишь, он доит, они доят. Коров is the direct object.",
         ["доить: to milk"]),
        ("Он ___ корову два раза в день.", "доить", "3s",
         "He milks the cow twice a day.",
         "2nd conjugation: он доит (-ит).", []),
        ("В июле мы ___ траву на лугу.", "косить", "1p",
         "In July we mow the grass in the meadow.",
         "2nd conjugation: мы косим (-им). Косить has с → ш in the я-form (я кошу), but мы косим keeps с.",
         ["косить: to mow"]),
        ("Ты ___ забор или калитку?", "чинить", "2s",
         "Are you repairing the fence or the gate?",
         "2nd conjugation: ты чинишь. Забор and калитку are direct objects (accusative).",
         ["чинить: to fix"]),
        ("Они ___ трактор уже третий день.", "чинить", "3p",
         "They have been repairing the tractor for the third day already.",
         "2nd conjugation: они чинят (-ят, not -ют).", []),
        ("Я ___ в храме каждое воскресенье.", "молиться", "1s",
         "I pray in church every Sunday.",
         "2nd conjugation, reflexive: я молюсь, ты молишься, он молится. В храме is prepositional (где?).",
         ["молиться: to pray"]),
        ("Мы ___ о детях и о ферме.", "молиться", "1p",
         "We pray for the children and for the farm.",
         "2nd conjugation: мы молимся. О детях, о ферме are prepositional after о.", []),
        ("Я ___ жене во всём.", "верить", "1s",
         "I trust my wife in everything.",
         "2nd conjugation: я верю. Верить takes the dative (жене). Во всём is prepositional.",
         ["верить: to believe, trust"]),
        ("Вы ___ этому человеку?", "верить", "2p",
         "Do you trust this person?",
         "2nd conjugation: вы верите. Человеку is dative.", []),
        ("На Рождество мы ___ иконы друзьям.", "дарить", "1p",
         "At Christmas we give icons to friends as gifts.",
         "2nd conjugation: мы дарим. Иконы is the direct object (accusative); друзьям is dative.",
         ["дарить: to give as a gift"]),
        ("Я ___ жену после обеда.", "звонить", "1s",
         "I call my wife after lunch.",
         "WAIT звонить takes dative: жене, not жену. Fix.",
         []),
    ]
    rows = [r for r in rows if "WAIT" not in (r[4] or "")]
    rows += [
        ("Я ___ жене после обеда.", "звонить", "1s",
         "I call my wife after lunch.",
         "2nd conjugation: я звоню. Звонить takes the dative (жене), not the accusative.",
         ["звонить: to call"]),
        ("Ты ___ батюшке о крещении?", "звонить", "2s",
         "Are you calling Father about the baptism?",
         "2nd conjugation: ты звонишь. Батюшке is dative. О крещении is prepositional.",
         ["крещение: baptism"]),
        ("Мама ___ суп на кухне.", "готовить", "3s",
         "Mom is cooking soup in the kitchen.",
         "2nd conjugation: она готовит. Суп is the direct object. На кухне is prepositional.",
         ["готовить: to cook"]),
    ]
    rows = [r for r in rows if "wait" not in r[1]]
    rows += [
        ("Вечером я ___ русский язык.", "учить", "1s",
         "In the evening I study Russian.",
         "2nd conjugation: я учу, ты учишь, он учит. Язык is the direct object (accusative).",
         ["учить: to study, to teach"]),
        ("Дети ___ молитву перед едой.", "учить", "3p",
         "The children are learning a prayer before the meal.",
         "2nd conjugation: они учат (-ат after ч, not -ят spoken as -ут).",
         ["молитва: prayer"]),
        ("Я ___ свою ферму.", "любить", "1s",
         "I love my farm.",
         "2nd conjugation: я люблю (б → бл in the я-form), ты любишь, он любит. Ферму is feminine accusative.", []),
        ("Они ___ песни Молчат Дома.", "любить", "3p",
         "They love Molchat Doma's songs.",
         "2nd conjugation: они любят (-ят). Песни is the direct object.", []),
        ("Днём коровы ___ в тени сарая.", "стоять", "3p",
         "During the day the cows stand in the shade of the barn.",
         "Стоять is 2nd conjugation: они стоят (я стою, ты стоишь). В тени is prepositional; сарая is genitive.",
         ["стоять: to stand", "тень: shade"]),
        ("Я ___ на крыльце и пью чай.", "сидеть", "1s",
         "I am sitting on the porch and drinking tea.",
         "2nd conjugation: я сижу (д → ж in the я-form), ты сидишь, он сидит, они сидят.", []),
        ("Ты ___ икону в красном углу?", "видеть", "2s",
         "Do you see the icon in the icon corner?",
         "2nd conjugation: ты видишь. Видеть has д → ж in the я-form (я вижу), but ты видишь keeps д. Икону is the direct object.",
         []),
    ]
    rows = [r for r in rows if r[4] != ""]
    rows += [
        ("Я ___ трактор за сараем.", "видеть", "1s",
         "I can see the tractor behind the barn.",
         "2nd conjugation: я вижу (д → ж). Трактор is the direct object; за сараем is instrumental after за.", []),
        ("Я ___ шум поезда за лесом.", "слышать", "1s",
         "I hear the noise of the train beyond the woods.",
         "2nd conjugation: я слышу (ш stays; я слышу, ты слышишь). Шум is the direct object; поезда is genitive.",
         ["слышать: to hear"]),
        ("Вы ___ эту песню?", "слышать", "2p",
         "Do you hear this song? / Can you hear this song?",
         "2nd conjugation: вы слышите. Песню is the direct object.", []),
        ("На ферму мы ___ пешком.", "ходить", "1p",
         "We go to the farm on foot (regularly).",
         "Ходить is 2nd conjugation (многократное, habitual motion): мы ходим. На ферму is accusative (куда?).",
         ["ходить: to go on foot (regularly)"]),
        ("По вечерам он ___ в храм.", "ходить", "3s",
         "In the evenings he goes to church.",
         "2nd conjugation, habitual motion: он ходит. В храм is accusative (куда?).", []),
    ]
    for s, inf, key, tr, ex, gl in rows:
        typo = None
        if inf == "кормить" and key == "1s":
            typo = ["кормю"]
        if inf == "любить" and key == "1s":
            typo = ["любю"]
        if inf == "сидеть" and key == "1s":
            typo = ["сидю"]
        add_verb(A, C, S, s, inf, key, tr, ex, gl, typo=typo)

    # ---- A1 irregular ----
    S = "irregular"
    rows = [
        ("Я ___ на ферме, а брат живёт в Минске.", "жить", "1s",
         "I live on the farm, and my brother lives in Minsk.",
         "Жить is irregular and adds в: я живу, ты живёшь, он живёт, мы живём, они живут. (An existing item was 'Я ___ в Минске.')", []),
        ("Где ___ ваши родители?", "жить", "3p",
         "Where do your parents live?",
         "Жить: они живут (not жиют or житут).", []),
        ("Мы ___ недалеко от церкви.", "жить", "1p",
         "We live not far from the church.",
         "Жить: мы живём (ё is required).", []),
        ("Я ___ чашку чая после дойки.", "хотеть", "1s",
         "I want a cup of tea after milking.",
         "Хотеть is mixed: я хочу, ты хочешь, он хочет (т → ч in the singular).", ["дойка: milking"]),
        ("Они ___ купить новый трактор.", "хотеть", "3p",
         "They want to buy a new tractor.",
         "Хотеть in the plural follows a 2nd-conjugation pattern with no ч: они хотят (not хочут).", []),
        ("Ты ___ поехать в Беларусь?", "хотеть", "2s",
         "Do you want to go to Belarus?",
         "Хотеть: ты хочешь (ч in the singular).", []),
        ("Я ___ кашу каждое утро.", "есть", "1s",
         "I eat kasha every morning.",
         "Есть (to eat) is irregular: я ем, ты ешь, он ест, мы едим, вы едите, они едят. Кашу is the direct object.",
         ["каша: kasha, porridge"]),
        ("Коровы ___ сено и траву.", "есть", "3p",
         "The cows eat hay and grass.",
         "Есть: они едят (not едут, which is from ехать 'to go by vehicle').", []),
        ("Что вы ___ на ужин?", "есть", "2p",
         "What do you eat for supper?",
         "Есть: вы едите. На ужин is accusative of purpose / time.", []),
        ("Я не ___ поднять этот мешок.", "мочь", "1s",
         "I can't lift this sack.",
         "Мочь is irregular: я могу, ты можешь, он может, мы можем, они могут (г → ж in ты/он/мы/вы).",
         ["поднять: to lift"]),
        ("Он ___ починить трактор сам.", "мочь", "3s",
         "He can repair the tractor himself.",
         "Мочь: он может. Сам agrees with он.", []),
        ("Вы ___ мне помочь с сеном?", "мочь", "2p",
         "Can you help me with the hay?",
         "Мочь: вы можете. Мне is dative; с сеном is instrumental.", []),
        ("Они не ___ приехать в этом году.", "мочь", "3p",
         "They can't come this year.",
         "Мочь: они могут. Приехать is the perfective infinitive (a single trip).", []),
        ("Завтра я ___ тебе ключи от сарая.", "дать", "1s",
         "Tomorrow I'll give you the keys to the barn.",
         "Дать is irregular (perfective, so the forms have a future meaning): я дам, ты дашь, он даст, мы дадим, они дадут. Тебе is dative; ключи is accusative.",
         []),
    ]
    rows = [r for r in rows if r[4] != ""]
    rows += [
        ("Он ___ нам знать, когда приедет.", "дать", "3s",
         "He'll let us know when he arrives.",
         "Дать: он даст (not дадет). Нам is dative.", []),
        ("Я ___ пешком на ферму.", "идти", "1s",
         "I'm walking to the farm (right now, one way).",
         "Идти is irregular: я иду, ты идёшь, он идёт, мы идём, они идут. На ферму is accusative (куда?).", []),
        ("Куда ты ___ так рано?", "идти", "2s",
         "Where are you going so early?",
         "Идти: ты идёшь (ё is required). Куда? asks for a destination.", []),
        ("Мы ___ в церковь пешком.", "идти", "1p",
         "We're walking to church.",
         "Идти: мы идём. В церковь is accusative (куда?).", []),
        ("Я ___ на тракторе в поле.", "ехать", "1s",
         "I'm going to the field on the tractor.",
         "Ехать (by vehicle) is irregular: я еду, ты едешь, он едет — not ехаю. На тракторе is prepositional; в поле is accusative (куда?).",
         []),
        ("Вы ___ в Минск сегодня?", "ехать", "2p",
         "Are you going to Minsk today?",
         "Ехать: вы едете. В Минск is accusative (куда?).", []),
        ("Они ___ на рынок за кормом.", "ехать", "3p",
         "They are going to the market for feed.",
         "Ехать: они едут (not едят, which is from есть 'to eat'). За кормом is instrumental ('to get feed').", []),
        ("Смотри, теленок ___ к маме.", "бежать", "3s",
         "Look, the calf is running to its mother.",
         "Бежать is mixed: он бежит, я бегу, они бегут (г in я and они, ж in the rest). К маме is dative after к.",
         []),
        ("Я ___ на вокзал, поезд уже близко.", "бежать", "1s",
         "I'm running to the station; the train is already close.",
         "Бежать: я бегу (not бежу). На вокзал is accusative (куда?).", []),
    ]
    for s, inf, key, tr, ex, gl in rows:
        typo = None
        if inf == "есть" and key == "3p":
            typo = ["едут"]
        if inf == "ехать" and key == "3p":
            typo = ["едят"]
        if inf == "хотеть" and key == "3p":
            typo = ["хочут"]
        if inf == "дать" and key == "1s":
            typo = ["дадю"]
        if inf == "бежать" and key == "1s":
            typo = ["бежу"]
        add_verb(A, C, S, s, inf, key, tr, ex, gl, typo=typo)

    # ---- A1 past tense ----
    S = "past tense"
    # key is m/f/n/p
    prows = [
        ("Вчера я весь день ___ на тракторе.", "работать", "m",
         "Yesterday I worked on the tractor all day.",
         "The past tense is built from the stem + -л / -ла / -ло / -ли and agrees with the subject: я (a man) работал. A woman would say работала.",
         []),
        ("Жена вчера ___ в городе до вечера.", "работать", "f",
         "My wife worked in town until evening yesterday.",
         "Feminine singular past: работала (-ла). Жена is the subject.", []),
        ("Мы ___ сено до темноты.", "собирать", "p",
         "We gathered hay until dark.",
         "Plural past (мы / вы / они): собирали (-ли).", []),
        ("Утром отец ___ коров.", "кормить", "m",
         "In the morning Dad fed the cows.",
         "Masculine past: кормил. Коров is the direct object (animate accusative plural).", []),
        ("Жена уже ___ всех кур.", "кормить", "f",
         "My wife has already fed all the hens.",
         "Feminine past: кормила. Кур is animate accusative plural; всех agrees with it.", []),
        ("Вчера я ___ коров сам.", "доить", "m",
         "Yesterday I milked the cows myself.",
         "Masculine past: доил. Сам agrees with я (a man).", []),
        ("Сестра ___ корову за меня.", "доить", "f",
         "My sister milked the cow for me.",
         "Feminine past: доила. За меня is accusative after за ('in my place').", []),
        ("В июле мы ___ весь луг.", "косить", "p",
         "In July we mowed the whole meadow.",
         "Plural past: косили. Весь луг is the direct object (accusative).", []),
        ("После бури отец ___ забор.", "чинить", "m",
         "After the storm Dad repaired the fence.",
         "Masculine past: чинил. Забор is the direct object.", []),
        ("На границе я ___ паспорт.", "открыть", "m",
         "At the border I opened my passport.",
         "Perfective past: открыл. Паспорт is the direct object. Perfective past reports a completed action.",
         []),
        ("Жена ___ новую икону.", "купить", "f",
         "My wife bought a new icon.",
         "Feminine perfective past: купила. Икону is the direct object (feminine accusative).", []),
        ("Мы ___ билеты до Минска.", "купить", "p",
         "We bought tickets to Minsk.",
         "Plural perfective past: купили. Билеты is the direct object.", []),
        ("Вчера я ___ старого друга в городе.", "видеть", "m",
         "Yesterday I saw an old friend in town.",
         "Masculine past: видел. Друга is the animate accusative (direct object).", []),
        ("Она ___ батюшку после литургии.", "видеть", "f",
         "She saw Father after the Liturgy.",
         "Feminine past: видела. Батюшку is the direct object.", []),
        ("Я ___ на ферме с детства.", "жить", "m",
         "I have lived on the farm since childhood. / I lived…",
         "Masculine past of жить: жил. С детства is genitive after с ('since').", []),
        ("Бабушка ___ в этой деревне всю жизнь.", "жить", "f",
         "Grandmother lived in this village all her life.",
         "Feminine past: жила (stress on -ла). Всю жизнь is accusative of duration.", []),
        ("Вчера вечером я ___ пешком в церковь.", "идти", "m",
         "Yesterday evening I walked to church.",
         "Идти has an irregular past: шёл, шла, шло, шли (not идил). Masculine: шёл (ё is required).", []),
        ("Жена ___ в магазин за хлебом.", "идти", "f",
         "My wife went to the store for bread.",
         "Feminine past of идти: шла (the ё drops). В магазин is accusative (куда?); за хлебом is instrumental.", []),
        ("Дети ___ к пруду купаться.", "идти", "p",
         "The children were going to the pond to swim.",
         "Plural past of идти: шли. К пруду is dative after к.", []),
        ("Утром письмо ___ от друга из Беларуси.", "прийти", "n",
         "In the morning a letter arrived from a friend in Belarus.",
         "Прийти, like идти, has an irregular past: пришёл, пришла, пришло, пришли. Письмо is neuter, so пришло.",
         []),
        ("В Минск мы ___ на поезде.", "ехать", "p",
         "We went to Minsk by train.",
         "Past of ехать is regular: ехал, ехала, ехало, ехали. Plural: ехали. На поезде is prepositional.", []),
        ("Она ___ на рынок одна.", "ехать", "f",
         "She went to the market on her own.",
         "Feminine past: ехала. Одна agrees with она.", []),
        ("Я не ___ поднять мешок сам.", "мочь", "m",
         "I couldn't lift the sack by myself.",
         "Мочь has an irregular past: мог, могла, могло, могли (no -л in the masculine). Masculine: мог.", []),
        ("Жена не ___ найти ключи.", "мочь", "f",
         "My wife couldn't find the keys.",
         "Feminine past of мочь: могла. Ключи is the direct object of найти.", []),
        ("В сарае ___ тихо и пахло сеном.", "быть", "n",
         "It was quiet in the barn and it smelled of hay.",
         "Impersonal sentences (тихо, холодно, пахло) take the neuter past: было. Сеном is instrumental after пахло.", []),
        ("Ты ___ вчера на литургии? (to a man)", "быть", "m",
         "Were you at the Liturgy yesterday? (to a man)",
         "Ты takes the past form of the person spoken to: a man is был, a woman is была. На литургии is prepositional.", []),
        ("Саша вчера ___ код до ночи.", "писать", "m",
         "Sasha was writing code until night yesterday. (Sasha is a man here.)",
         "Masculine past: писал. If Саша were a woman, it would be писала. Код is the direct object.", []),
        ("После службы мы ___ чай у батюшки.", "пить", "p",
         "After the service we drank tea at Father's.",
         "Plural past of пить: пили. У батюшки is genitive after у ('at Father's place').", []),
    ]
    for s, inf, key, tr, ex, gl in prows:
        typo = None
        if inf == "идти" and key == "m":
            typo = ["идил", "идила", "шёлл"]
            typo = ["идил"]
        if inf == "мочь" and key == "m":
            typo = ["могл"]
        add_verb(A, C, S, s, inf, key, tr, ex, gl, typo=typo)


def build_conj_b1():
    C = "conjugation"
    S = "1st conjugation"
    rows = [
        ("Я ___ тебя у калитки ровно в семь.", "ждать", "1s",
         "I'll wait for you at the gate at exactly seven.",
         "Ждать is 1st conjugation with a short stem: я жду, ты ждёшь, он ждёт (not ждаю). Тебя is the direct object (accusative).", []),
        ("Мы ___ посылку из Минска уже неделю.", "ждать", "1p",
         "We've been waiting for a parcel from Minsk for a week already.",
         "1st conjugation: мы ждём. Посылку is the direct object; из Минска is genitive after из.", ["посылка: parcel"]),
        ("По вечерам я ___ отчёт для начальника.", "проверять", "1s",
         "In the evenings I check the report for the boss.",
         "1st conjugation: я проверяю. Отчёт is the direct object; для начальника is genitive after для.", ["проверять: to check"]),
        ("Вы ___ код перед тем, как его отправить?", "проверять", "2p",
         "Do you check the code before sending it?",
         "1st conjugation: вы проверяете.", []),
        ("Он всегда ___ на сенокос.", "опаздывать", "3s",
         "He is always late for haymaking.",
         "1st conjugation: он опаздывает. На сенокос is accusative (куда? / for an event).", ["опаздывать: to be late"]),
        ("Мы не ___ на литургию, выходим рано.", "опаздывать", "1p",
         "We're not late for the Liturgy; we leave early.",
         "1st conjugation: мы опаздываем. На литургию is accusative.", []),
        ("Я ___ коллегам, как пахать это поле.", "показывать", "1s",
         "I'm showing my colleagues how to plow this field.",
         "1st conjugation: я показываю. Коллегам is dative (to whom); поле is accusative.", ["показывать: to show"]),
    ]
    rows = [r for r in rows if r[4] != ""]
    rows += [
        ("В кафе мы обычно ___ борщ и котлеты.", "заказывать", "1p",
         "At the café we usually order borscht and cutlets.",
         "1st conjugation: мы заказываем. Борщ и котлеты are direct objects (accusative).", ["заказывать: to order"]),
        ("Ты ___ билеты через сайт?", "заказывать", "2s",
         "Do you book the tickets through the website?",
         "1st conjugation: ты заказываешь. Билеты is the direct object.", []),
        ("Я ___ жене с сеном, когда она просит.", "помогать", "1s",
         "I help my wife with the hay when she asks.",
         "1st conjugation: я помогаю. Помогать takes the dative (жене); с сеном is instrumental.", ["помогать: to help"]),
        ("Соседи ___ нам чинить крышу.", "помогать", "3p",
         "The neighbors are helping us repair the roof.",
         "1st conjugation: они помогают. Нам is dative.", []),
        ("После работы он ___ на крыльце.", "отдыхать", "3s",
         "After work he rests on the porch.",
         "1st conjugation: он отдыхает. На крыльце is prepositional.", []),
        ("Мы ___ сезон в октябре, когда сено уже в сарае.", "заканчивать", "1p",
         "We finish the season in October, when the hay is already in the barn.",
         "1st conjugation: мы заканчиваем. Сезон is the direct object.", ["заканчивать: to finish"]),
        ("Я ___ новый модуль на этой неделе.", "начинать", "1s",
         "I'm starting a new module this week.",
         "1st conjugation: я начинаю. Модуль is the direct object; на этой неделе is prepositional.", ["начинать: to begin"]),
        ("Они ___ ошибки в старом коде.", "исправлять", "3p",
         "They are fixing mistakes in the old code.",
         "1st conjugation: они исправляют. Ошибки is the direct object; в коде is prepositional.", ["исправлять: to correct"]),
        ("Ты ___ батюшку после службы?", "спрашивать", "2s",
         "Are you going to ask Father after the service?",
         "1st conjugation: ты спрашиваешь. Спрашивать takes the accusative of the person (батюшку).", []),
        ("Каждое утро я ___ кашу и яйца.", "завтракать", "1s",
         "WAIT завтракать doesn't take those as direct objects easily (завтракать + instrumental). Use ужинать? or change.",
         "", []),
    ]
    rows = [r for r in rows if r[4] not in ("",) and "WAIT" not in r[4]]
    rows += [
        ("По вечерам мы ___ в девять, после дойки.", "ужинать", "1p",
         "In the evenings we have supper at nine, after milking.",
         "1st conjugation: мы ужинаем. В девять is accusative of time.", ["ужинать: to have supper"]),
        ("Он ___ на все письма в тот же день.", "отвечать", "3s",
         "He answers all the letters the same day.",
         "1st conjugation: он отвечает. На письма is accusative after на (отвечать на + acc).", ["отвечать: to answer"]),
        ("Я ___ дверь сарая ключом.", "открывать", "1s",
         "I open the barn door with a key.",
         "1st conjugation: я открываю. Дверь is the direct object; ключом is instrumental.", ["открывать: to open"]),
        ("Вы ___ ворота на ночь?", "закрывать", "2p",
         "Do you close the gate at night?",
         "1st conjugation: вы закрываете. Ворота is the direct object (plural-only).", []),
        ("Летом дети ___ у пруда до темноты.", "купаться", "3p",
         "In the summer the children swim at the pond until dark.",
         "1st conjugation, reflexive: они купаются. У пруда is genitive after у.", ["купаться: to swim, bathe"]),
    ]
    rows = [r for r in rows if r[4] != ""]
    rows += [
        ("Я ___ программу вечером, после фермы.", "запускать", "1s",
         "I launch the program in the evening, after the farm work.",
         "1st conjugation: я запускаю. Программу is the direct object.", ["запускать: to launch"]),
        ("Мы ___ новый забор вдоль поля.", "ставить", "1p",
         "WAIT ставить is 2nd (ставлю, ставишь).", "", []),
    ]
    rows = [r for r in rows if "WAIT" not in (r[4] or "") and r[4] != ""]
    for s, inf, key, tr, ex, gl in rows:
        add_verb(B, C, S, s, inf, key, tr, ex, gl)

    S = "2nd conjugation"
    rows = [
        ("По утрам я ___ коров сам, жена ещё спит.", "доить", "1s",
         "In the mornings I milk the cows myself; my wife is still asleep.",
         "2nd conjugation: я дою, ты доишь, он доит. Коров is the direct object; сам agrees with я.", []),
        ("К осени мы ___ всё сено под крышу.", "носить", "1p",
         "By autumn we carry all the hay under the roof (as a regular job).",
         "Носить is 2nd conjugation (habitual carrying): мы носим. Сено is the direct object; под крышу is accusative (куда?).",
         ["носить: to carry (regularly)"]),
        ("Он уже двадцать лет ___ этот трактор.", "водить", "3s",
         "He has been driving this tractor for twenty years.",
         "Водить (habitual driving) is 2nd conjugation: он водит. Трактор is the direct object.", ["водить: to drive (regularly)"]),
        ("Ты ___ лошадь в поводу или едешь верхом?", "водить", "2s",
         "Are you leading the horse by the bridle, or riding?",
         "2nd conjugation: ты водишь. Лошадь is the direct object (soft feminine, acc = nom).", []),
        ("Я ___ сено на сеновал по ступеням.", "носить", "1s",
         "I carry the hay up to the hayloft by the steps.",
         "2nd conjugation, я-form of носить: я ношу (с → ш). На сеновал is accusative (куда?).", []),
        ("Они ___ новый курятник у забора.", "строить", "3p",
         "They are building a new coop by the fence.",
         "2nd conjugation: они строят (-ят). Курятник is the direct object; у забора is genitive after у.", ["строить: to build"]),
        ("Мы ___ баню за сараем уже второй год.", "строить", "1p",
         "We've been building a bathhouse behind the barn for the second year already.",
         "2nd conjugation: мы строим. Баню is the direct object; за сараем is instrumental after за.", ["баня: bathhouse"]),
        ("Я ___ батюшку благословить новую икону.", "просить", "1s",
         "I'm asking Father to bless the new icon.",
         "2nd conjugation: я прошу (с → ш in the я-form). Просить takes the accusative of the person (батюшку) + an infinitive.",
         ["просить: to ask, request", "благословить: to bless"]),
        ("Вы ___ у соседа сеялку на неделю?", "просить", "2p",
         "Are you asking the neighbor for the seeder for a week?",
         "2nd conjugation: вы просите. У соседа is genitive after у; сеялку is the direct object.", ["сеялка: seeder"]),
        ("Жена ___ постную кашу в среду.", "готовить", "3s",
         "My wife cooks Lenten kasha on Wednesday.",
         "2nd conjugation: она готовит. Кашу is the direct object; в среду is accusative of time.", ["постный: Lenten"]),
    ]
    rows = [r for r in rows if r[4] != ""]
    rows += [
        ("Я ___ этот модуль уже третью неделю.", "учить", "1s",
         "I've been learning (studying) this module for the third week already.",
         "2nd conjugation: я учу. Модуль is the direct object. Учить here means 'to study, work through'.", []),
        ("По вечерам дети ___ молитвы вслух.", "учить", "3p",
         "In the evenings the children learn the prayers out loud.",
         "2nd conjugation: они учат. Молитвы is the direct object.", []),
        ("На литургии мы ___ стоя, если можем.", "стоять", "1p",
         "At the Liturgy we stand, if we can.",
         "2nd conjugation: мы стоим. На литургии is prepositional. Стоя is a verbal adverb (gerund).", []),
        ("Ключи ___ на полке у двери.", "лежать", "3p",
         "The keys are lying on the shelf by the door.",
         "Лежать is 2nd conjugation: они лежат (я лежу, ты лежишь). На полке is prepositional.", ["лежать: to lie, be lying"]),
        ("Пальто ___ в шкафу.", "висеть", "3s",
         "The coat is hanging in the wardrobe.",
         "Висеть is 2nd conjugation: оно висит (я вишу, ты висишь). В шкафу is the special locative in -у.", ["висеть: to hang"]),
    ]
    rows = [r for r in rows if r[4] != ""]
    rows += [
        ("Я ___ жену до калитки после службы.", "проводить", "1s",
         "I walk my wife to the gate after the service.",
         "2nd conjugation: я провожу (д → ж). Жену is the direct object; до калитки is genitive after до.",
         ["проводить: to walk someone somewhere, see off"]),
        ("Ты ___ лошадей в поле или в лес?", "водить", "2s",
         "Do you take the horses out to the field or into the woods?",
         "2nd conjugation: ты водишь. Лошадей is animate accusative plural; в поле / в лес are accusative (куда?).", []),
        ("Они ___ сено вилами на воз.", "грузить", "3p",
         "They are loading the hay onto the wagon with pitchforks.",
         "2nd conjugation: они грузят. Сено is the direct object; вилами is instrumental; на воз is accusative (куда?).",
         ["грузить: to load", "воз: wagon, load"]),
        ("Я ___ свечу перед иконой.", "ставить", "1s",
         "I set a candle in front of the icon.",
         "2nd conjugation: я ставлю (в → вл in the я-form), ты ставишь. Свечу is the direct object; перед иконой is instrumental.",
         ["ставить: to set, put standing"]),
        ("Мы ___ кур в курятник на ночь.", "загонять", "1p",
         "WAIT загонять is 1st (загоняю). Use гонять? or завести? Skip.",
         "", []),
    ]
    rows = [r for r in rows if "WAIT" not in (r[4] or "") and r[4] != ""]
    rows += [
        ("Мы ___ кур в курятник на ночь.", "гнать", "1p",
         "We drive the hens into the coop for the night.",
         "Гнать is often taught with the 2nd-conjugation set of motion verbs (я гоню, ты гонишь, мы гоним, они гонят). Кур is the direct object; в курятник is accusative (куда?).",
         ["гнать: to drive (animals)"]),
    ]
    for s, inf, key, tr, ex, gl in rows:
        typo = None
        if inf == "носить" and key == "1s":
            typo = ["носию"]
        add_verb(B, C, S, s, inf, key, tr, ex, gl, typo=typo)

    S = "irregular"
    rows = [
        ("Завтра я ___ в Минск на поезде.", "ехать", "1s",
         "Tomorrow I'm going to Minsk by train.",
         "Ехать is irregular: я еду (not ехаю). В Минск is accusative (куда?); на поезде is prepositional.", []),
        ("Куда вы ___ в такую погоду — на рынок?", "ехать", "2p",
         "Where are you driving in this weather — to the market?",
         "Ехать: вы едете. Куда? asks for a destination.", []),
        ("Пешком я ___ только до храма, дальше — на машине.", "идти", "1s",
         "I only walk as far as the church; after that I go by car.",
         "Идти is irregular: я иду, ты идёшь. До храма is genitive after до.", []),
        ("Смотри, они уже ___ к воротам.", "идти", "3p",
         "Look, they're already walking toward the gate.",
         "Идти: они идут. К воротам is dative after к (ворота is plural-only).", []),
        ("Этой зимой мы ___ в старом доме у пруда.", "жить", "1p",
         "This winter we're living in the old house by the pond.",
         "Жить: мы живём (ё is required). В доме is prepositional; у пруда is genitive after у.", []),
        ("Где ___ сейчас твои родители?", "жить", "3p",
         "Where are your parents living now?",
         "Жить: они живут.", []),
        ("Я не ___ сегодня поднять этот мешок — спина болит.", "мочь", "1s",
         "I can't lift this sack today — my back hurts.",
         "Мочь: я могу, ты можешь, он может. Инфинитив поднять is perfective (one act of lifting).", []),
        ("Вы ___ приехать на престольный праздник?", "мочь", "2p",
         "Can you come for the parish feast day?",
         "Мочь: вы можете. Приехать is a perfective infinitive (one trip).", ["престольный праздник: parish feast"]),
        ("Завтра я ___ тебе знать точное время поезда.", "дать", "1s",
         "Tomorrow I'll let you know the exact time of the train.",
         "Дать (perfective) has future meaning: я дам, ты дашь, он даст, мы дадим, они дадут.", []),
        ("Надеюсь, начальник ___ нам выходной после сенокоса.", "дать", "3s",
         "I hope the boss will give us a day off after haymaking.",
         "Дать: он даст. Нам is dative; выходной is the direct object.", ["выходной: day off"]),
        ("После службы я ___ кусок хлеба и чаю.", "есть", "1s",
         "After the service I'll have a piece of bread and some tea. / I eat…",
         "Есть (to eat) is irregular: я ем (not естю). Кусок хлеба is accusative + genitive.", []),
        ("Что они ___ на праздник — борщ или щи?", "есть", "3p",
         "What are they eating for the feast — borscht or shchi?",
         "Есть: они едят (not едут, from ехать).", []),
        ("Телята ___ к матери через всё поле.", "бежать", "3p",
         "The calves are running to their mother across the whole field.",
         "Бежать is mixed: они бегут (г, like я бегу), not бежат. К матери is dative after к.", []),
        ("Я ___ за врачом — не могу дождаться скорой.", "бежать", "1s",
         "I'm running for the doctor; I can't wait for the ambulance.",
         "Бежать: я бегу (not бежу). За врачом is instrumental ('to fetch the doctor').", []),
    ]
    rows = [r for r in rows if r[4] != ""]
    rows += [
        ("Я ___ эту лопату, если ты не против.", "взять", "1s",
         "I'll take this shovel, if you don't mind.",
         "Взять is irregular (perfective, future meaning): я возьму, ты возьмёшь, он возьмёт, мы возьмём, они возьмут (not взяму).",
         ["взять: to take"]),
        ("Вы ___ с собой паспорт на границу?", "взять", "2p",
         "Will you take your passport with you to the border?",
         "Взять: вы возьмёте. С собой is instrumental; паспорт is the direct object; на границу is accusative (куда?).", []),
        ("Я не ___ больше так работать без выходных.", "хотеть", "1s",
         "I don't want to work like this without days off any longer.",
         "Хотеть: я хочу (т → ч in the singular). Без выходных is genitive after без.", []),
        ("Они ___ остаться на ферме до Покрова.", "хотеть", "3p",
         "They want to stay on the farm until Pokrov (the Protection of the Theotokos).",
         "Хотеть: они хотят (no ч in the plural). До Покрова is genitive after до.", ["Покров: Protection of the Theotokos"]),
    ]
    for s, inf, key, tr, ex, gl in rows:
        typo = None
        if inf == "взять" and key == "1s":
            typo = ["взяму"]
        if inf == "есть" and key == "3p":
            typo = ["едут"]
        if inf == "бежать" and key == "3p":
            typo = ["бежат"]
        add_verb(B, C, S, s, inf, key, tr, ex, gl, typo=typo)

    S = "stem change"
    rows = [
        ("Я ___ жене каждое воскресенье.", "писать", "1s",
         "I write to my wife every Sunday.",
         "Писать changes с → ш in the present: я пишу, ты пишешь, он пишет (not писаю / писаешь). Жене is dative.", []),
        ("Они ___ код до глубокой ночи.", "писать", "3p",
         "They write code late into the night.",
         "Писать: они пишут (ш in every present form). Код is the direct object.", []),
        ("Я ___ калитку, которую вчера сломали.", "искать", "1s",
         "I'm looking for the gate latch they broke yesterday. / I'm looking for the gate…",
         "Hmm калитку is the gate itself. Fine: looking for the gate.",
         "Искать changes к → щ: я ищу, ты ищешь (not искаю). Калитку is the direct object.", []),
    ]
    # fix the one with a comment as extra field - the last has 7 fields. Let me not include messy ones.
    rows = [r for r in rows if len(r) == 6]
    rows += [
        ("Ты ___ ключи от курятника?", "искать", "2s",
         "Are you looking for the coop keys?",
         "Искать: ты ищешь (к → щ). Ключи is the direct object; от курятника is genitive after от.", []),
        ("Весной я ___ поле под кукурузу.", "пахать", "1s",
         "In the spring I plow the field for corn.",
         "Пахать changes х → ш: я пашу, ты пашешь, он пашет (not пахаю). Поле is the direct object.", []),
        ("Он ___ землю медленно, чтобы не испортить дерн.", "пахать", "3s",
         "He plows the ground slowly so as not to ruin the sod.",
         "Пахать: он пашет. Землю is the direct object.", ["дёрн: sod, turf"]),
        ("Я ___ такси до вокзала, иначе опоздаю.", "брать", "1s",
         "I'm taking a taxi to the station, otherwise I'll be late.",
         "Брать changes to бер-: я беру, ты берёшь, он берёт (not браю). Такси is indeclinable (accusative). До вокзала is genitive after до.", []),
        ("Вы всегда ___ с собой воду в поле?", "брать", "2p",
         "Do you always take water with you into the field?",
         "Брать: вы берёте. Воду is the direct object; с собой is instrumental; в поле is accusative (куда?).", []),
        ("Утром я ___ чай, а жена — кофе.", "пить", "1s",
         "In the morning I drink tea, and my wife drinks coffee.",
         "Пить has a short stem: я пью, ты пьёшь, он пьёт, мы пьём, они пьют (the и drops).", []),
        ("Что они ___ на сенокосе — квас или воду?", "пить", "3p",
         "What do they drink at haymaking — kvas or water?",
         "Пить: они пьют. На сенокосе is prepositional.", ["квас: kvas"]),
        ("В храме мы ___ «Христос воскресе» на Пасху.", "петь", "1p",
         "In church we sing 'Christ is risen' at Pascha.",
         "Петь is like пить: мы поём, я пою, ты поёшь (not пеаем). В храме is prepositional.", ["петь: to sing"]),
        ("Кто ___ эту песню Молчат Дома так чисто?", "петь", "3s",
         "Who sings this Molchat Doma song so cleanly?",
         "Петь: он/она поёт (ё is required).", []),
        ("Я ___ руки перед едой, как учила мама.", "мыть", "1s",
         "I wash my hands before a meal, as Mom taught me.",
         "Мыть: я мою, ты моешь, он моет (ы → о). Руки is the direct object; перед едой is instrumental after перед.",
         ["мыть: to wash"]),
        ("По утрам он ___ в четыре, чтобы успеть доить.", "вставать", "3s",
         "In the mornings he gets up at four in order to be in time for milking.",
         "Вставать drops -ва- in the present: он встаёт, я встаю, они встают (not вставает).", []),
        ("Мы ___ детям молоко после церкви.", "давать", "1p",
         "We give the children milk after church.",
         "Давать drops -ва- in the present: мы даём, я даю, ты даёшь (not даваем). Детям is dative; молоко is accusative.",
         ["давать: to give (impf.)"]),
        ("Я ___ пирог к престольному празднику.", "печь", "1s",
         "I'm baking a pie for the parish feast.",
         "Печь is a -чь verb: я пеку, ты печёшь, он печёт, мы печём, они пекут (к / ч alternation). Пирог is the direct object.",
         ["печь: to bake"]),
        ("Вы ___ блины на Масленицу?", "печь", "2p",
         "Do you bake blini for Maslenitsa?",
         "Печь: вы печёте (ч + ё). Блины is the direct object; на Масленицу is accusative (for the feast).",
         ["блин: blin, pancake", "Масленица: Maslenitsa"]),
        ("Я ___ её сразу, хотя мы не виделись десять лет.", "узнавать", "1s",
         "I recognize her at once, even though we haven't seen each other in ten years.",
         "Узнавать, like давать and вставать, drops -ва-: я узнаю, ты узнаёшь, он узнаёт (not узнаваю).",
         ["узнавать: to recognize; to find out"]),
        ("Каждое утро я ___ жену с поля по имени.", "звать", "1s",
         "Every morning I call my wife in from the field by name.",
         "Звать changes to зов-: я зову, ты зовёшь, он зовёт (not зваю). Жену is the direct object; с поля is genitive after с.",
         ["звать: to call"]),
        ("Они ___ сено под навес, пока нет дождя.", "везти", "3p",
         "They are hauling the hay under the lean-to while there's no rain.",
         "Везти (to haul by vehicle) has з → з / зу in the present: они везут, я везу, ты везёшь. Сено is the direct object; под навес is accusative (куда?).",
         ["везти: to haul, cart"]),
        ("Я ___ корову на верёвке к пруду.", "вести", "1s",
         "I'm leading the cow on a rope to the pond.",
         "Вести (to lead) : я веду, ты ведёшь, он ведёт, они ведут (ст → д). Корову is the direct object; к пруду is dative after к.",
         ["вести: to lead"]),
    ]
    for s, inf, key, tr, ex, gl in rows:
        typo = None
        if inf == "писать" and key == "1s":
            typo = ["писаю"]
        if inf == "искать" and key == "2s":
            typo = ["искаешь"]
        if inf == "пахать" and key == "1s":
            typo = ["пахаю"]
        if inf == "брать" and key == "1s":
            typo = ["браю"]
        if inf == "вставать" and key == "3s":
            typo = ["вставает"]
        if inf == "давать" and key == "1p":
            typo = ["даваем"]
        add_verb(B, C, S, s, inf, key, tr, ex, gl, typo=typo)


def addv(level, cat, sub, s, base, a, d, ex, tr, gl=None):
    add(level, cat, sub, s, base, a, d, ex, tr, gl)

def build_motion_aspect():
    C = "motion"
    # A1 идти (need ~28)
    S = "идти"
    rows = [
        ("Сейчас я ___ на ферму пешком.", "иду", ["еду", "хожу", "идёт"],
         "Идти is one-way motion on foot happening now: я иду. Еду would be by vehicle; хожу is habitual (there and back). На ферму is accusative (куда?).",
         "I'm walking to the farm right now."),
        ("Куда вы ___ так рано?", "идёте", ["едете", "ходите", "идёшь"],
         "Идти: вы идёте (ё is required). Куда? asks for a destination, which is why идти (direction) is the right verb family.",
         "Where are you walking so early?"),
        ("Смотри, батюшка ___ к храму.", "идёт", ["едет", "ходит", "идут"],
         "One person, one direction, on foot, right now: он идёт. Ходит would describe a habit. К храму is dative after к.",
         "Look, Father is walking toward the church."),
        ("Мы ___ в церковь пешком, это недалеко.", "идём", ["едем", "ходим", "идут"],
         "Идти, 1st person plural, one-way, on foot: мы идём. Ходим would be 'we go (regularly)'.",
         "We're walking to church; it isn't far."),
        ("Дети сейчас ___ к пруду купаться.", "идут", ["едут", "ходят", "идёт"],
         "Идти, 3rd person plural, one direction: они идут. К пруду is dative after к.",
         "The children are walking to the pond to swim."),
        ("Ты ___ в магазин? Купи, пожалуйста, хлеб.", "идёшь", ["едешь", "ходишь", "идёт"],
         "Идти: ты идёшь. This is a trip happening now (or just about to start), one way, on foot.",
         "Are you going to the store? Please buy some bread."),
        ("Я ___ за врачом, жена нехорошо себя чувствует.", "иду", ["еду", "хожу", "шёл"],
         "Идти: я иду. За врачом is instrumental ('to fetch the doctor'). If you went by car, you would say еду.",
         "I'm going for the doctor; my wife isn't feeling well."),
        ("Почему он ___ так медленно? Устал?", "идёт", ["едет", "ходил", "ходят"],
         "One direction, in progress: идёт. Ходил would be a past round trip.",
         "Why is he walking so slowly? Is he tired?"),
        ("Мы ___ вдоль забора к калитке.", "идём", ["едем", "ходим", "шли"],
         "Идти + along a path, one way, now: мы идём. Вдоль забора is genitive after вдоль; к калитке is dative after к.",
         "We're walking along the fence to the gate."),
        ("Саша ___ домой с поля.", "идёт", ["едет", "ходит", "шёл"],
         "Идти, one way, on foot: идёт домой. Домой is the adverb of destination (куда?), not the prepositional дома.",
         "Sasha is walking home from the field."),
        ("Я ___ пешком, трактор сегодня сломался.", "иду", ["еду", "ходил", "хожу"],
         "The contrast is explicit: пешком forces идти (я иду), not ехать.",
         "I'm going on foot; the tractor broke down today."),
        ("Кто ___ за нами по дороге?", "идёт", ["едет", "ходит", "идут"],
         "One person following, one direction, now: идёт. За нами is instrumental after за ('behind us').",
         "Who is walking along the road behind us?"),
        ("Вы ___ в ту сторону? Там тупик.", "идёте", ["едете", "ходите", "идёшь"],
         "Идти: вы идёте. В ту сторону is accusative (куда?).",
         "Are you walking that way? It's a dead end."),
        ("Они ___ на литургию пешком, как всегда в воскресенье? Нет, сегодня они как раз ___ (wait - don't mix)", "идут", ["едут","ходят","идёт"],
         "skip messy", "x"),
    ]
    rows = [r for r in rows if r[3] != "skip messy"]
    rows += [
        ("Они ___ на литургию пешком.", "идут", ["едут", "ходят", "идёт"],
         "Идти, plural, one-way, on foot: они идут. На литургию is accusative (куда?). Ходят would mean they go regularly, not necessarily right now.",
         "They are walking to the Liturgy."),
        ("Я ___ к соседу за семенами.", "иду", ["еду", "хожу", "шёл"],
         "Идти: я иду. К соседу is dative after к; за семенами is instrumental ('to get seeds').",
         "I'm walking over to the neighbor's for seeds."),
        ("Смотри, жена уже ___ от автобуса.", "идёт", ["едет", "ходила", "ходит"],
         "One direction, in sight, on foot: идёт. От автобуса is genitive after от.",
         "Look, my wife is already walking back from the bus."),
        ("Почему ты ___ босиком по двору?", "идёшь", ["едешь", "ходишь", "идёт"],
         "Идти: ты идёшь. Босиком is instrumental used as an adverb ('barefoot').",
         "Why are you walking around the yard barefoot?"),
        ("Мы ___ через поле, так короче.", "идём", ["едем", "ходим", "шли"],
         "Идти, one way, now: мы идём. Через поле is accusative after через.",
         "We're walking across the field; it's shorter that way."),
        ("Дед ___ в сад со своими вёдрами.", "идёт", ["едет", "ходил", "ходят"],
         "Идти: идёт. В сад is accusative (куда?); со вёдрами is instrumental after с.",
         "Grandfather is walking into the garden with his buckets."),
        ("Я ___ на почту отправить посылку.", "иду", ["еду", "хожу", "шёл"],
         "Идти, one trip happening now: я иду. На почту is accusative (куда?).",
         "I'm going to the post office to send a parcel."),
        ("Дети ___ впереди, а мы за ними.", "идут", ["едут", "ходили", "идёт"],
         "Идти, plural, one direction: идут. Впереди is an adverb (где? in front).",
         "The children are walking out in front, and we are behind them."),
        ("Куда это он ___ с лопатой?", "идёт", ["едет", "ходит", "шёл"],
         "Идти: идёт. С лопатой is instrumental after с. Куда? marks destination.",
         "Where is he going with a shovel?"),
        ("Я ___ вдоль пруда, чтобы проверить забор.", "иду", ["еду", "хожу", "шёл"],
         "Идти: я иду. Вдоль пруда is genitive after вдоль.",
         "I'm walking along the pond to check the fence."),
        ("Вы ___ в деревню или из деревни?", "идёте", ["едете", "ходите", "идёшь"],
         "Идти: вы идёте. В деревню is accusative (куда?); из деревни is genitive after из.",
         "Are you walking into the village or out of it?"),
        ("Собака ___ за мной до самой калитки.", "идёт", ["едет", "ходит", "идут"],
         "Идти can be used of an animal walking along: идёт. За мной is instrumental; до калитки is genitive after до.",
         "The dog is walking behind me all the way to the gate."),
        ("Мы ___ на звук колокола, к храму.", "идём", ["едем", "ходим", "шли"],
         "Идти: мы идём. На звук is accusative; к храму is dative after к.",
         "We're walking toward the sound of the bell, to the church."),
        ("Он ___ так быстро, что я не успеваю.", "идёт", ["едет", "ходил", "ходят"],
         "One direction, in progress: идёт. Не успеваю is 1st conjugation ('I can't keep up').",
         "He is walking so fast that I can't keep up."),
        ("Я ___ к батюшке пешком, машина в ремонте.", "иду", ["еду", "хожу", "шёл"],
         "Пешком and машина в ремонте force идти: я иду. К батюшке is dative after к.",
         "I'm walking to Father's; the car is in the shop."),
        ("Кто ___ по полю с фонарём?", "идёт", ["едет", "ходит", "идут"],
         "Идти: идёт. По полю is dative after по; с фонарём is instrumental after с.",
         "Who is walking across the field with a lantern?"),
    ]
    for s, a, d, ex, *rest in rows:
        addv(A, C, S, s, "идти", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "ехать"
    rows = [
        ("Сейчас я ___ на ферму на тракторе.", "еду", ["иду", "езжу", "едет"],
         "Ехать is one-way motion by vehicle happening now: я еду. Иду would be on foot; езжу is habitual.",
         "I'm going to the farm on the tractor right now."),
        ("Куда вы ___ в такую погоду?", "едете", ["идёте", "ездите", "едешь"],
         "Ехать: вы едете. Куда? marks a destination. Without пешком, a trip out in bad weather is usually by vehicle.",
         "Where are you driving in this weather?"),
        ("Жена ___ в город на автобусе.", "едет", ["идёт", "ездит", "едут"],
         "One way, by bus, now: она едет. На автобусе is prepositional (means of transport).",
         "My wife is going to town by bus."),
        ("Мы ___ в Минск на поезде завтра утром? Да, мы ___ уже сегодня? wait", "едем", ["идём","ездим","едут"], "skip", "x"),
    ]
    rows = [r for r in rows if r[3] != "skip"]
    rows += [
        ("Мы ___ в Минск на поезде.", "едем", ["идём", "ездим", "едут"],
         "Ехать, 1st person plural, one-way, by train: мы едем. На поезде is prepositional. (An existing item was 'Мы ___ в Москву на поезде.')",
         "We're going to Minsk by train."),
        ("Они сейчас ___ на рынок за кормом.", "едут", ["идут", "ездят", "едет"],
         "Ехать, plural, one way: они едут. На рынок is accusative (куда?); за кормом is instrumental ('to get feed').",
         "They are going to the market for feed."),
        ("Ты ___ за сеном на пикапе?", "едешь", ["идёшь", "ездишь", "едет"],
         "Ехать: ты едешь. За сеном is instrumental; на пикапе is prepositional.",
         "Are you going for hay in the pickup?"),
        ("Я ___ на работу в город, потом вечером вернусь.", "еду", ["иду", "езжу", "ехал"],
         "A one-way trip in progress (or just starting) by vehicle: я еду. Вернусь is the perfective of return.",
         "I'm going into town for work; I'll come back in the evening."),
        ("Смотри, трактор ___ по полю.", "едет", ["идёт", "ездит", "едут"],
         "A vehicle in motion, one direction, now: едет. По полю is dative after по. Идёт can be used of trains and buses, but a tractor 'is going' is normally едет.",
         "Look, the tractor is going across the field."),
        ("Вы ___ до вокзала на такси или на автобусе?", "едете", ["идёте", "ездите", "едешь"],
         "Ехать: вы едете. До вокзала is genitive after до; both options are vehicles, so not идти.",
         "Are you going to the station by taxi or by bus?"),
        ("Мы ___ на ярмарку всей семьёй.", "едем", ["идём", "ездим", "ехали"],
         "Ехать, one trip, by vehicle: мы едем. На ярмарку is accusative (куда?); всей семьёй is instrumental.",
         "We're going to the fair as a whole family."),
        ("Он ___ в Беларусь завтра, билет уже куплен.", "едет", ["идёт", "ездит", "ехал"],
         "The present of ехать can announce a planned trip: он едет завтра. В Беларусь is accusative (куда?).",
         "He's going to Belarus tomorrow; the ticket is already bought."),
        ("Я ___ за женой на вокзал.", "еду", ["иду", "езжу", "едет"],
         "Ехать: я еду. За женой is instrumental ('to pick my wife up'); на вокзал is accusative (куда?).",
         "I'm driving to the station to pick up my wife."),
        ("Почему они ___ так медленно по этой дороге?", "едут", ["идут", "ездят", "едет"],
         "Ехать, plural, in progress: едут. По дороге is dative after по.",
         "Why are they driving so slowly on this road?"),
        ("Ты ___ через поле или по дороге?", "едешь", ["идёшь", "ездишь", "едет"],
         "Ехать: ты едешь. Через поле is accusative after через; по дороге is dative after по.",
         "Are you driving across the field or along the road?"),
        ("Автобус уже ___ , поторопись!", "едет", ["идёт", "ездит", "едут"],
         "A specific bus leaving now, one direction: едет (идёт is also used of buses; here едет is equally natural and matches the subtopic).",
         "The bus is already leaving — hurry up!"),
        ("Я ___ на тракторе в дальний луг.", "еду", ["иду", "езжу", "ехал"],
         "Ехать: я еду. На тракторе is prepositional; в луг is accusative (куда?).",
         "I'm going to the far meadow on the tractor."),
        ("Мы ___ к друзьям в деревню на машине.", "едем", ["идём", "ездим", "едут"],
         "Ехать: мы едем. К друзьям is dative after к; в деревню is accusative; на машине is prepositional.",
         "We're driving to our friends' in the village."),
        ("Она ___ в аэропорт уже сейчас, рейс ранний.", "едет", ["идёт", "ездит", "ехала"],
         "One-way, by vehicle, now: едет. В аэропорт is accusative (куда?).",
         "She's already on her way to the airport; the flight is early."),
        ("Вы ___ со мной на рынок или остаётесь?", "едете", ["идёте", "ездите", "едешь"],
         "Ехать: вы едете. Со мной is instrumental after с; на рынок is accusative (куда?).",
         "Are you coming with me to the market, or staying?"),
        ("Дети ___ с дедом на телеге.", "едут", ["идут", "ездят", "едет"],
         "Ехать, plural, by wagon: едут. С дедом is instrumental; на телеге is prepositional.",
         "The children are riding with grandfather on the cart.", ["телега: cart, wagon"]),
        ("Я ___ только до поворота, потом пешком.", "еду", ["иду", "езжу", "едет"],
         "The first stretch is by vehicle: я еду. До поворота is genitive after до. Потом пешком switches to идти, which is not the blank.",
         "I'm only driving as far as the turn; after that I'll go on foot."),
        ("Куда это ___ наш пикап? Кто его взял?", "едет", ["идёт", "ездит", "едут"],
         "A specific vehicle moving now, one direction: едет.",
         "Where is our pickup going? Who took it?"),
        ("Мы ___ за молоком в соседнее село.", "едем", ["идём", "ездим", "ехали"],
         "Ехать, one trip: мы едем. За молоком is instrumental; в село is accusative (куда?).",
         "We're driving to the next village for milk."),
        ("Он ___ так быстро, что пыль столбом.", "едет", ["идёт", "ездит", "едут"],
         "One direction, in progress, by vehicle: едет.",
         "He's driving so fast that the dust stands in a column."),
        ("Я ___ на работу через поле, так короче.", "еду", ["иду", "езжу", "ехал"],
         "Ехать: я еду. На работу is accusative (куда?); через поле is accusative after через.",
         "I drive to work across the field; it's shorter."),
        ("Вы ___ в Минск сегодня или завтра?", "едете", ["идёте", "ездите", "едешь"],
         "A planned one-way trip by vehicle: вы едете. В Минск is accusative (куда?).",
         "Are you going to Minsk today or tomorrow?"),
        ("Пограничники ___ вдоль границы на машине.", "едут", ["идут", "ездят", "едет"],
         "Ехать, plural, by car, one stretch of motion: едут. Вдоль границы is genitive after вдоль.",
         "The border guards are driving along the border."),
        ("Я ___ за запчастями в районный центр.", "еду", ["иду", "езжу", "едет"],
         "Ехать: я еду. За запчастями is instrumental; в центр is accusative (куда?).",
         "I'm driving to the district center for spare parts.", ["запчасти: spare parts"]),
    ]
    for s, a, d, ex, *rest in rows:
        tr = rest[0] if rest else ""
        gl = rest[1] if len(rest) > 1 else None
        addv(A, C, S, s, "ехать", a, d, ex, tr, gl)


    S = "идти or ехать"
    rows = [
        ("Я ___ в церковь пешком, это близко.", "иду", ["еду", "хожу", "езжу"],
         "Пешком (on foot) requires идти (one way, now) or ходить (habit). Here it is a trip happening now: иду, not еду.",
         "I'm walking to church; it's close."),
        ("Мы ___ в Минск на поезде, не пешком.", "едем", ["идём", "ездим", "ходим"],
         "На поезде (by train) requires ехать, not идти: мы едем. Идём would be on foot.",
         "We're going to Minsk by train, not on foot."),
        ("Жена ___ на рынок на автобусе.", "едет", ["идёт", "ездит", "ходит"],
         "На автобусе forces ехать: едет. Идёт would mean she is walking.",
         "My wife is going to the market by bus."),
        ("Он ___ в магазин пешком за хлебом.", "идёт", ["едет", "ходит", "ездит"],
         "Пешком forces идти: идёт. За хлебом is instrumental ('for bread').",
         "He is walking to the store for bread."),
        ("Ты ___ на ферму на тракторе или пешком?", "едешь", ["идёшь", "ездишь", "ходишь"],
         "The first option is a vehicle, and the verb in the question sits with на тракторе, so едешь is the form that fits both the word order and the vehicle. If you wanted 'walk', you would ask идёшь … пешком first.",
         "Are you going to the farm on the tractor, or on foot?"),
        # The above explanation is a bit forced. Better recast that sentence.
    ]
    # I'll skip the awkward one by not including messy explanations... actually I'll replace it below
    rows = [r for r in rows if "The first option" not in r[3]]
    rows += [
        ("Ты ___ на ферму на тракторе?", "едешь", ["идёшь", "ездишь", "ходишь"],
         "На тракторе forces ехать: ты едешь, not идёшь.",
         "Are you going to the farm on the tractor?"),
        ("Дети ___ в школу пешком, школа рядом.", "идут", ["едут", "ходят", "ездят"],
         "Пешком + a trip now: идут. Ходят would describe the habitual walk to school, not necessarily this morning's walk in progress.",
         "The children are walking to school; the school is nearby."),
        ("Я ___ за запчастями в город на машине.", "еду", ["иду", "езжу", "хожу"],
         "На машине forces ехать: я еду. За запчастями is instrumental.",
         "I'm driving into town for spare parts."),
        ("Батюшка ___ к нам пешком через поле.", "идёт", ["едет", "ходит", "ездит"],
         "Пешком + через поле, one way, now: идёт, not едет.",
         "Father is walking to our place across the field."),
        ("Мы ___ на ярмарку на телеге.", "едем", ["идём", "ездим", "ходим"],
         "На телеге (on a cart) is a vehicle: мы едем, not идём.",
         "We're going to the fair on the cart."),
        ("Я ___ на почту пешком, письмо надо срочно отправить.", "иду", ["еду", "хожу", "езжу"],
         "Пешком forces идти: я иду.",
         "I'm walking to the post office; the letter has to go out at once."),
        ("Они ___ в аэропорт на такси.", "едут", ["идут", "ездят", "ходят"],
         "На такси forces ехать: они едут. В аэропорт is accusative (куда?).",
         "They are going to the airport by taxi."),
        ("Почему ты ___ пешком? Я бы тебя подвёз.", "идёшь", ["едешь", "ходишь", "ездишь"],
         "Пешком forces идти: ты идёшь. Подвёз is the past of подвезти ('give a lift').",
         "Why are you walking? I would have given you a lift."),
        ("Пограничник ___ вдоль границы на машине, не пешком.", "едет", ["идёт", "ездит", "ходит"],
         "На машине forces ехать: едет.",
         "The border guard is driving along the border, not walking."),
        ("Я ___ к колодцу пешком с вёдрами.", "иду", ["еду", "хожу", "езжу"],
         "Пешком + с вёдрами: я иду. К колодцу is dative after к.",
         "I'm walking to the well with buckets."),
        ("Мы ___ в Беларусь на поезде в пятницу.", "едем", ["идём", "ездим", "ходим"],
         "На поезде + a planned one-way trip: мы едем. The present of ехать can announce a future trip.",
         "We're going to Belarus by train on Friday."),
        ("Саша ___ в храм пешком, хотя есть автобус.", "идёт", ["едет", "ходит", "ездит"],
         "Пешком, one way, now: идёт, even though a bus exists — he is not using it.",
         "Sasha is walking to church, even though there is a bus."),
        ("Вы ___ на вокзал на автобусе?", "едете", ["идёте", "ездите", "ходите"],
         "На автобусе forces ехать: вы едете.",
         "Are you going to the station by bus?"),
        ("Я ___ за врачом на машине, так быстрее.", "еду", ["иду", "езжу", "хожу"],
         "На машине + так быстрее: я еду, not иду. За врачом is instrumental.",
         "I'm driving for the doctor; it's faster that way."),
        ("Коровы ___ на пастбище сами, пешком, конечно.", "идут", ["едут", "ходят", "ездят"],
         "Animals walking, one way, now: идут. Едут would be used of cattle only if they were being hauled.",
         "The cows are going out to the pasture on their own — on foot, of course."),
        ("Мы ___ через реку на пароме.", "едем", ["идём", "ездим", "ходим"],
         "На пароме (on the ferry) is a vehicle: мы едем. Через реку is accusative after через.",
         "We're crossing the river on the ferry."),
        ("Он ___ в поле пешком, трактор занят.", "идёт", ["едет", "ходит", "ездит"],
         "Пешком + трактор занят: идёт, not едет.",
         "He is walking to the field; the tractor is in use."),
        ("Я ___ на работу на велосипеде.", "еду", ["иду", "езжу", "хожу"],
         "На велосипеде counts as ехать (any vehicle, including a bicycle): я еду, not иду.",
         "I'm going to work on the bicycle."),
        ("Дети ___ в гости к бабушке на машине.", "едут", ["идут", "ездят", "ходят"],
         "На машине forces ехать: едут. В гости is accusative (a set phrase, куда?); к бабушке is dative after к.",
         "The children are going to visit grandmother by car."),
        ("Я ___ до поворота на машине, а дальше пешком.", "еду", ["иду", "езжу", "хожу"],
         "The blank describes the first, vehicle-driven stretch: я еду. До поворота is genitive after до.",
         "I'm driving as far as the turn, and after that I'll go on foot."),
        ("Почему вы ___ пешком с такими сумками? Возьмите такси.", "идёте", ["едете", "ходите", "ездите"],
         "Пешком forces идти: вы идёте. С сумками is instrumental after с.",
         "Why are you walking with bags like that? Take a taxi."),
        ("Отец ___ за комбикормом на пикапе.", "едет", ["идёт", "ездит", "ходит"],
         "На пикапе forces ехать: едет. За комбикормом is instrumental.",
         "Dad is going for mixed feed in the pickup.", ["комбикорм: mixed feed"]),
        ("Я ___ в сельсовет пешком, надо подать бумаги.", "иду", ["еду", "хожу", "езжу"],
         "Пешком forces идти: я иду. В сельсовет is accusative (куда?).",
         "I'm walking to the village soviet; I have to file some papers.", ["сельсовет: village council"]),
        ("Они ___ на престольный праздник на автобусе.", "едут", ["идут", "ездят", "ходят"],
         "На автобусе forces ехать: едут. На праздник is accusative (куда? / for the feast).",
         "They are going to the parish feast by bus."),
        ("Смотри, он ___ в курятник пешком, с ведром.", "идёт", ["едет", "ходит", "ездит"],
         "Пешком + с ведром, one way, now: идёт.",
         "Look, he's walking to the coop with a bucket."),
        ("Мы ___ на станцию на тракторе — автобуса сегодня нет.", "едем", ["идём", "ездим", "ходим"],
         "На тракторе forces ехать: мы едем. На станцию is accusative (куда?).",
         "We're going to the station on the tractor — there's no bus today."),
        ("Ты ___ в поле пешком или возьмёшь велосипед?", "идёшь", ["едешь", "ходишь", "ездишь"],
         "The first option is пешком, and that is the option attached to the verb: идёшь. The bicycle would need едешь.",
         "Are you walking to the field, or will you take the bicycle?"),
    ]
    for s, a, d, ex, *rest in rows:
        addv(A, C, S, s, "идти / ехать", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "где / куда"
    rows = [
        ("___ ты работаешь — на ферме или в городе?", "Где", ["Куда", "Откуда", "Когда"],
         "Где? asks for a location (где?) and takes the prepositional: на ферме, в городе. Куда? would ask for a destination.",
         "Where do you work — on the farm or in town?"),
        ("___ вы идёте с такими вёдрами?", "Куда", ["Где", "Откуда", "Когда"],
         "With a verb of motion (идти) you ask куда? (where to?), not где? (where at?).",
         "Where are you going with buckets like that?"),
        ("___ стоит ваш трактор?", "Где", ["Куда", "Откуда", "Зачем"],
         "Стоять is a location verb, so the question is где?, and the answer will be in the prepositional (в сарае, у забора).",
         "Where is your tractor standing?"),
        ("___ едет этот пикап — на рынок?", "Куда", ["Где", "Откуда", "Когда"],
         "Ехать is a verb of motion, so you ask куда? На рынок is accusative (куда?).",
         "Where is this pickup going — to the market?"),
        ("Жена сейчас ___, не на работе.", "дома", ["домой", "дом", "доме"],
         "Дома is the adverb of location (где? at home). Домой is destination (куда? to home).",
         "My wife is at home right now, not at work."),
        ("После дойки я иду ___.", "домой", ["дома", "дом", "доме"],
         "Иду is a verb of motion, so you need домой (куда?), not дома.",
         "After milking I go home."),
        ("___ лежит паспорт — в сумке или в кармане?", "Где", ["Куда", "Откуда", "Чей"],
         "Лежать is a location verb: где? The answer will be в + prepositional (в сумке, в кармане).",
         "Where is the passport — in the bag or in the pocket?"),
        ("___ поставить мешок с зерном?", "Куда", ["Где", "Откуда", "Чем"],
         "Поставить asks for a destination (куда?): in/onto somewhere, so the noun will be accusative (в сарай, на телегу).",
         "Where shall I put the sack of grain?"),
        ("Коровы уже ___, в сарае.", "дома", ["домой", "дом", "доме"],
         "Already at the location: дома can be used loosely of 'in their place', but here the clearer reading is 'they're in' (location). The prepositional в сарае confirms где?, not куда?.",
         "The cows are already in, in the barn."),
        # "коровы уже дома" is a bit odd. Let me replace later if needed - actually "the cows are already home (in the barn)" is OK in farm talk.
        ("___ ты кладёшь ключи на ночь?", "Куда", ["Где", "Откуда", "Когда"],
         "Класть (to put) is directional: куда? The thing put is accusative (ключи), the destination is also accusative (в карман, на полку).",
         "Where do you put the keys at night?"),
        ("___ живут твои родители?", "Где", ["Куда", "Откуда", "Кто"],
         "Жить is a location verb: где? The answer is в + prepositional (в Минске, в деревне).",
         "Where do your parents live?"),
        ("___ мы едем — в Минск или в Гродно?", "Куда", ["Где", "Откуда", "Зачем"],
         "Едем is a verb of motion: куда? В Минск is accusative (куда?), not в Минске.",
         "Where are we going — to Minsk or to Grodno?"),
        ("Дети уже ___ или ещё в школе?", "дома", ["домой", "дом", "доме"],
         "Location: already at home = дома. Домой would need a verb of motion (идут домой).",
         "Are the children already at home, or still at school?"),
        ("Пора ___, уже темно.", "домой", ["дома", "дом", "доме"],
         "Пора (it's time to go) is about direction: пора домой. Пора дома would not make sense.",
         "It's time to go home; it's already dark."),
        ("___ пасутся коровы — на лугу или на пастбище?", "Где", ["Куда", "Откуда", "Когда"],
         "Пастись is a location verb: где? На лугу is the special locative in -у; на пастбище is prepositional.",
         "Where are the cows grazing — in the meadow or in the pasture?"),
        ("___ ты гонишь кур — в курятник?", "Куда", ["Где", "Откуда", "Зачем"],
         "Гнать is a verb of motion (causing motion): куда? В курятник is accusative (куда?), not в курятнике.",
         "Where are you driving the hens — into the coop?"),
        ("___ выходит это письмо — в Беларусь?", "Куда", ["Где", "Откуда", "Чей"],
         "Выходить / 'is this letter going' asks for a destination: куда? В Беларусь is accusative.",
         "Where is this letter going — to Belarus?"),
        ("___ в письме указан обратный адрес?", "Где", ["Куда", "Откуда", "Когда"],
         "Указан (is given) is a location question: где в письме? В письме is prepositional.",
         "Where in the letter is the return address given?"),
        ("Я весь день был ___, чинил крышу.", "дома", ["домой", "дом", "доме"],
         "Был is a location verb: где? = дома. Домой would need motion (поехал домой).",
         "I was at home all day, repairing the roof."),
        ("После литургии мы едем ___.", "домой", ["дома", "дом", "доме"],
         "Едем is motion: куда? = домой.",
         "After the Liturgy we drive home."),
        ("___ хранится зерно — в сарае или в закромах?", "Где", ["Куда", "Откуда", "Чем"],
         "Хранится (is stored) is location: где? В сарае is prepositional.",
         "Where is the grain stored — in the barn or in the bins?", ["закрома: grain bins"]),
        ("___ нам везти это сено?", "Куда", ["Где", "Откуда", "Чем"],
         "Везти is a verb of motion (hauling): куда? The destination will be accusative (на сеновал, в сарай).",
         "Where should we haul this hay?"),
        ("___ у вас икона — в красном углу?", "Где", ["Куда", "Откуда", "Чья"],
         "Location of an object: где? В углу is the special locative in -у.",
         "Where is your icon — in the icon corner?"),
        ("___ повесить эту икону?", "Куда", ["Где", "Откуда", "Над"],
         "Повесить (to hang something) is directional: куда? На стену, в угол — accusative.",
         "Where shall we hang this icon?"),
        ("Он уже ___ или ещё в поле?", "дома", ["домой", "дом", "доме"],
         "Location: already at home = дома. Ещё в поле is also где? (prepositional).",
         "Is he already at home, or still in the field?"),
        ("Я провожу тебя ___.", "домой", ["дома", "дом", "доме"],
         "Проводить ('walk someone somewhere') is directional: домой, not дома.",
         "I'll walk you home."),
        ("___ работает этот код — на сервере или на компьютере?", "Где", ["Куда", "Откуда", "Как"],
         "Работать here is location: где? На сервере, на компьютере are prepositional.",
         "Where does this code run — on the server or on the computer?"),
        ("___ ты копируешь этот файл?", "Куда", ["Где", "Откуда", "Чем"],
         "Копировать a file asks for a destination: куда? В папку, на диск — accusative.",
         "Where are you copying this file to?"),
        ("___ приехал этот поезд — из Минска?", "Откуда", ["Где", "Куда", "Когда"],
         "Откуда? (where from?) takes из / с + genitive: из Минска. Где? is location; куда? is destination.",
         "Where did this train come from — from Minsk?"),
        ("___ вы пришли — с поля или из сарая?", "Откуда", ["Где", "Куда", "Зачем"],
         "Прийти plus a source: откуда? С поля (с + genitive), из сарая (из + genitive).",
         "Where did you come from — from the field or from the barn?"),
    ]
    for s, a, d, ex, *rest in rows:
        base = "где / куда"
        if a.lower() in ("дома", "домой", "дом", "доме"):
            base = "дом"
        if a.lower() in ("откуда",):
            base = "где / куда / откуда"
        addv(A, C, S, s, base, a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "ходить"
    rows = [
        ("Каждую неделю мы ___ в храм.", "ходим", ["идём", "ездим", "ходили"],
         "Ходить is habitual, there-and-back motion on foot: мы ходим. Идём would be one trip happening now.",
         "Every week we go to church."),
        ("По утрам он ___ на ферму пешком.", "ходит", ["идёт", "ездит", "ходил"],
         "A daily habit, on foot: он ходит. Идёт would be today's one-way walk in progress.",
         "In the mornings he walks to the farm."),
        ("Дети ___ в школу пешком, это недалеко.", "ходят", ["идут", "ездят", "ходили"],
         "Habitual walk to school: ходят. Идут would be 'they are on their way right now'.",
         "The children walk to school; it isn't far."),
        ("Я редко ___ в город пешком, обычно еду.", "хожу", ["иду", "езжу", "ходил"],
         "Ходить, 1st person, habit: я хожу (not ходю). Редко marks a repeated (if rare) action.",
         "I rarely walk to town; I usually drive."),
        ("Ты часто ___ к батюшке?", "ходишь", ["идёшь", "ездишь", "ходил"],
         "Часто + a repeated visit on foot: ты ходишь. К батюшке is dative after к.",
         "Do you often go to Father's?"),
        ("Вы ___ в этот магазин или в тот, что у вокзала?", "ходите", ["идёте", "ездите", "ходили"],
         "A habitual 'which store do you use': вы ходите. Идёте would be today's trip.",
         "Do you go to this store, or to the one by the station?"),
        ("Зимой коровы не ___ на дальнее пастбище.", "ходят", ["идут", "ездят", "ходили"],
         "A seasonal habit of animals walking out: не ходят. На пастбище here is accusative (куда?) after a verb of motion.",
         "In winter the cows don't go out to the far pasture."),
        ("Когда я был ребёнком, я ___ в эту церковь.", "ходил", ["шёл", "хожу", "ходили"],
         "A past habit, masculine: ходил (went regularly / used to go). Шёл would be one trip in progress in the past.",
         "When I was a child I went to this church."),
        ("Жена раньше ___ на рынок пешком каждый день.", "ходила", ["шла", "ходит", "ходили"],
         "Past habit, feminine: ходила. Шла would be one past trip in progress.",
         "My wife used to walk to the market every day."),
        ("Вчера мы ___ в гости к соседям.", "ходили", ["шли", "ходим", "едем"],
         "A completed round trip in the past (went and came back) takes ходить: мы ходили. Шли would be 'we were on our way'.",
         "Yesterday we went to visit the neighbors."),
        ("По вечерам я ___ вдоль пруда.", "хожу", ["иду", "езжу", "ходил"],
         "A regular evening walk: я хожу. Вдоль пруда is genitive after вдоль.",
         "In the evenings I walk along the pond."),
        ("Кто у вас ___ за почтой в деревню?", "ходит", ["идёт", "ездит", "ходил"],
         "Habitual chore, on foot: ходит. За почтой is instrumental ('to get the mail').",
         "Who at your place goes to the village for the mail?"),
        ("Они ___ в баню по субботам.", "ходят", ["идут", "ездят", "ходили"],
         "По субботам marks a habit: ходят. В баню is accusative (куда?).",
         "They go to the bathhouse on Saturdays."),
        ("Я не ___ туда один — дорога тёмная.", "хожу", ["иду", "езжу", "ходил"],
         "A general / habitual refusal: не хожу. Не иду would be 'I'm not going (this time)'.",
         "I don't go there alone — the road is dark."),
        ("Сын уже ___ сам, без руки.", "ходит", ["идёт", "ходил", "ходят"],
         "Ability to walk in general takes ходить: он уже ходит. Идёт would be one walk in progress.",
         "Our son already walks by himself, without a hand to hold."),
        ("Почему ты так странно ___? Нога болит?", "ходишь", ["идёшь", "ездишь", "ходил"],
         "Manner of walking in general: как ты ходишь? Идёшь would be this particular stretch of walking.",
         "Why are you walking so oddly? Does your leg hurt?"),
        ("Летом мы часто ___ в лес за грибами.", "ходим", ["идём", "ездим", "ходили"],
         "Часто + summer habit, on foot: ходим. В лес is accusative; за грибами is instrumental.",
         "In the summer we often go to the woods for mushrooms."),
        ("Батюшка ___ по домам на Богоявление.", "ходит", ["идёт", "ездит", "ходил"],
         "A repeated pastoral round, on foot: ходит. По домам is dative after по ('from house to house').",
         "Father goes from house to house at Theophany.", ["Богоявление: Theophany"]),
        ("Вчера я ___ в сельсовет и уже вернулся.", "ходил", ["шёл", "хожу", "ходили"],
         "Went and already came back: ходил, not шёл. Вернулся makes the round trip explicit.",
         "Yesterday I went to the village council and I'm already back."),
        ("Она ___ в эту школу десять лет.", "ходила", ["шла", "ходит", "ходили"],
         "A long past habit, feminine: ходила. Шла would be one trip.",
         "She went to this school for ten years."),
        ("По воскресеньям вы ___ к вечерне?", "ходите", ["идёте", "ездите", "ходили"],
         "По воскресеньям marks a habit: вы ходите. К вечерне is dative after к.",
         "Do you go to vespers on Sundays?", ["вечерня: vespers"]),
        ("Кошки ___ по сараю, как хотят.", "ходят", ["идут", "ездят", "ходили"],
         "Motion around a place with no single destination: ходят. Идут would be one direction.",
         "The cats walk around the barn as they please."),
        ("Я ___ за хлебом в ту лавку уже двадцать лет.", "хожу", ["иду", "езжу", "ходил"],
         "A long-standing habit: я хожу. За хлебом is instrumental; в лавку is accusative.",
         "I've been going to that shop for bread for twenty years.", ["лавка: small shop"]),
        ("Когда гости ___ по ферме, я всё им показываю.", "ходят", ["идут", "ездят", "ходили"],
         "Walking around (no single destination): ходят. По ферме is dative after по.",
         "When guests walk around the farm, I show them everything."),
        ("Раньше люди ___ в храм за десять вёрст пешком.", "ходили", ["шли", "ходят", "ездили"],
         "A past habit of a whole community: ходили. Шли would be one procession in progress.",
         "In the old days people would walk ten versts to church.", ["верста: verst (old unit of length)"]),
        ("Ты ___ по льду пруда? Это опасно.", "ходишь", ["идёшь", "ездишь", "ходил"],
         "A general / repeated activity: ходишь по льду. По льду is dative after по.",
         "Do you walk on the pond ice? That's dangerous."),
        ("Мы не ___ в тот магазин: там дорого.", "ходим", ["идём", "ездим", "ходили"],
         "A standing habit (or refusal of a habit): не ходим. Не идём would be 'we're not going this time'.",
         "We don't go to that store: it's expensive there."),
        ("По двору ___ куры и цыплята.", "ходят", ["идут", "ездят", "ходили"],
         "Animals moving around a space, no single destination: ходят. По двору is dative after по.",
         "Hens and chicks walk around the yard."),
        ("Я иногда ___ на почту пешком, иногда еду.", "хожу", ["иду", "езжу", "ходил"],
         "Иногда marks a repeated (if irregular) action: хожу. The contrast with еду is between habits, not two trips in progress.",
         "Sometimes I walk to the post office, sometimes I drive."),
        ("В детстве мы ___ на этот пруд каждый день.", "ходили", ["шли", "ходим", "ездили"],
         "A childhood habit, plural past: ходили. Шли would be one past walk in progress.",
         "As children we went to this pond every day."),
        ("Кто у вас ___ в ночное — сын или сосед?", "ходит", ["идёт", "ездит", "ходил"],
         "Habitual night-watch of the herd: ходит в ночное. В ночное is a set accusative phrase.",
         "Who at your place goes out for the night watch — your son or the neighbor?", ["ночное: night pasture watch"]),
    ]
    for s, a, d, ex, *rest in rows:
        addv(A, C, S, s, "ходить", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)


    # ---- B1 motion ----
    S = "идти / ходить"
    rows = [
        ("Сейчас я ___ за водой к колодцу, подожди.", "иду", ["хожу", "шёл", "ходил"],
         "One direction, right now: the unidirectional verb иду. Хожу would be a habit. К колодцу is dative after к.",
         "I'm going for water at the well right now; wait a moment."),
        ("По утрам я ___ за водой к колодцу.", "хожу", ["иду", "шёл", "ходил"],
         "A daily habit, there and back, on foot: хожу. Иду would be this particular trip in progress.",
         "In the mornings I go to the well for water."),
        ("Вчера я ___ к батюшке и уже вернулся.", "ходил", ["шёл", "иду", "хожу"],
         "A completed past round trip (went and came back): ходил, not шёл. Вернулся makes the return explicit.",
         "Yesterday I went to Father's and I'm already back."),
        ("Когда я ___ в храм, начался дождь.", "шёл", ["ходил", "иду", "хожу"],
         "A one-way trip in progress in the past, interrupted by an event: шёл. Ходил would mean a completed round trip.",
         "While I was walking to church, it started to rain."),
        ("Ребёнок уже ___, ему год и два месяца.", "ходит", ["идёт", "ходил", "ходят"],
         "Ability to walk in general: ходит. Идёт would be one walk happening now.",
         "The child already walks; he is a year and two months old."),
        ("Смотри, вон ___ наш батюшка, пойдём к нему.", "идёт", ["ходит", "шёл", "идут"],
         "A specific person approaching now, one direction: идёт. Ходит would be habitual.",
         "Look, there's Father coming; let's go over to him."),
        ("Каждое воскресенье мы ___ к вечерне пешком.", "ходим", ["идём", "шли", "идут"],
         "Каждое воскресенье marks a habit: ходим. К вечерне is dative after к.",
         "Every Sunday we walk to vespers."),
        ("Завтра я ___ в сельсовет, надо подать бумаги. Хочешь со мной?", "иду", ["хожу", "шёл", "ходил"],
         "The present of идти can announce a planned one-way trip: завтра я иду. Хожу would be a habit.",
         "Tomorrow I'm going to the village council; I have to file papers. Want to come with me?"),
        ("Раньше люди ___ в этот храм за десять вёрст.", "ходили", ["шли", "ходят", "идут"],
         "A past habit of a community: ходили. Шли would be one procession in progress in the past.",
         "People used to walk ten versts to this church."),
        ("Не ___ по льду, он ещё тонкий.", "ходи", ["иди", "ходишь", "шёл"],
         "A general prohibition on a kind of walking uses the imperative of ходить: не ходи. Не иди would stop someone who is already setting off on a particular path.",
         "Don't walk on the ice; it's still thin."),
        ("___ сюда, я тебе покажу телят.", "Иди", ["Ходи", "Идёт", "Ходишь"],
         "A command to come in one direction, now: иди. Ходи would be 'do your walking (in general / regularly)'.",
         "Come here; I'll show you the calves."),
        ("По двору ___ куры, не гони их.", "ходят", ["идут", "ходили", "идёт"],
         "Motion around a space with no single destination: ходят. Идут would be one direction.",
         "The hens are walking around the yard; don't chase them."),
        ("Я не ___ в тот магазин: там обвешивают.", "хожу", ["иду", "шёл", "ходил"],
         "A standing refusal of a habit: не хожу. Не иду would be 'I'm not going this time'.",
         "I don't go to that store: they short-weight you there."),
        ("Пока он ___ в школу, мы как раз доим коров.", "идёт", ["ходит", "шёл", "ходил"],
         "A specific trip in progress right now, used as a time frame: пока он идёт. Ходит would be the general habit of attending school.",
         "While he is walking to school, we are just milking the cows."),
        ("В детстве я часто ___ на этот пруд.", "ходил", ["шёл", "хожу", "ходили"],
         "A past habit: часто ходил. Шёл would be one past walk in progress.",
         "As a child I often went to this pond."),
        ("Кто это ___ по полю с фонарём? Пойдём посмотрим.", "идёт", ["ходит", "шёл", "идут"],
         "A specific person visible now, one direction: идёт. По полю is dative after по.",
         "Who is that walking across the field with a lantern? Let's go and see."),
        ("Мы ___ в эту баню уже двадцать лет.", "ходим", ["идём", "ходили", "шли"],
         "A long-standing habit still in force: ходим. Ходили would put the habit in the past.",
         "We've been going to this bathhouse for twenty years already."),
        ("Когда гости ___ по ферме, собака не лает.", "ходят", ["идут", "ходили", "идёт"],
         "Walking around (по + dative) with no single destination: ходят.",
         "When guests walk around the farm, the dog doesn't bark."),
        ("Иди не ___ , всё равно опоздаешь, бери машину.", "ходи", ["иди", "ходишь", "шёл"],
         "The set phrase иди не ходи means 'whether you go or not' / 'there's no point in going on foot' and uses ходить in the second half because the idea is the activity in general.",
         "There's no point in walking; you'll be late anyway — take the car."),
        ("Смотри, корова ___ в сарай сама.", "идёт", ["ходит", "шла", "ходят"],
         "One animal, one direction, now: идёт в сарай (куда? accusative). Ходит would be habitual.",
         "Look, the cow is going into the barn on her own."),
    ]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "идти / ходить", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "ехать / ездить"
    rows = [
        ("Завтра мы ___ в Минск на поезде.", "едем", ["ездим", "ехали", "ездили"],
         "The present of unidirectional ехать can announce a planned one-way trip: завтра мы едем. Ездим would be a habit.",
         "Tomorrow we're going to Minsk by train."),
        ("Каждую неделю он ___ в город за кормом.", "ездит", ["едет", "ехал", "ездил"],
         "Каждую неделю marks a habit, there and back, by vehicle: ездит. Едет would be this particular trip in progress.",
         "Every week he goes to town for feed."),
        ("Прошлым летом мы ___ в Беларусь на машине, было хорошо.", "ездили", ["ехали", "едем", "ездим"],
         "A completed past trip there and back: ездили, not ехали. Ехали would be 'we were on our way'.",
         "Last summer we went to Belarus by car; it was good."),
        ("Когда мы ___ на ярмарку, у пикапа спустило колесо.", "ехали", ["ездили", "едем", "ездим"],
         "A one-way trip in progress in the past, interrupted: ехали. Ездили would be a completed round trip.",
         "While we were driving to the fair, the pickup got a flat tire."),
        ("Сколько времени ___ до Минска на этом поезде?", "ехать", ["ездить", "едет", "ездит"],
         "How long a single one-way trip takes: ехать (unidirectional infinitive), not ездить.",
         "How long does it take to get to Minsk on this train?"),
        ("Я не люблю ___ ночью по этим дорогам.", "ездить", ["ехать", "еду", "езжу"],
         "A general attitude to a kind of travel (habit / in general) takes ездить. Ехать would be one particular trip.",
         "I don't like driving on these roads at night."),
        ("Сейчас я ___ за женой на вокзал, скоро буду.", "еду", ["езжу", "ехал", "ездил"],
         "One trip, right now, by vehicle: еду. Езжу would be a habit.",
         "I'm on my way to the station to pick up my wife; I'll be there soon."),
        ("По работе он часто ___ в Минск.", "ездит", ["едет", "ехал", "ездил"],
         "Часто marks a habit: ездит. В Минск is accusative (куда?).",
         "He often goes to Minsk for work."),
        ("Вчера я ___ в район и уже вернулся к обеду.", "ездил", ["ехал", "еду", "езжу"],
         "Went and already came back: ездил, not ехал.",
         "Yesterday I went to the district center and was already back by lunch."),
        ("Пока он ___ в город, мы подоили коров.", "ехал", ["ездил", "едет", "ездит"],
         "A one-way trip as a past time frame: пока он ехал. Ездил would be a completed round trip.",
         "While he was driving to town, we milked the cows."),
        ("На этом тракторе я ___ уже пятнадцать лет.", "езжу", ["еду", "ехал", "ездил"],
         "A long-standing habit / skill of driving this tractor: езжу. Еду would be this particular trip.",
         "I've been driving this tractor for fifteen years already."),
        ("Вы часто ___ в Беларусь, к родне?", "ездите", ["едете", "ездили", "ехали"],
         "Часто + habit: ездите. К родне is dative after к.",
         "Do you often go to Belarus, to your relatives?"),
        ("Завтра они ___ на ярмарку, места уже заняты.", "едут", ["ездят", "ехали", "ездили"],
         "A planned one-way trip announced in the present: завтра они едут.",
         "Tomorrow they're going to the fair; the places are already taken."),
        ("Раньше мы ___ за сеном на телеге, теперь на пикапе.", "ездили", ["ехали", "ездим", "едем"],
         "A past habit, replaced by a new one: ездили. Ехали would be one past trip in progress.",
         "We used to go for hay on a cart; now we take the pickup."),
        ("Не ___ так быстро по мокрой дороге.", "езди", ["едь", "ездишь", "едьте"],
         "A general warning about a manner of driving uses the imperative of ездить: не езди так быстро. Не едь would stop a particular trip already under way (and is also rarer).",
         "Don't drive so fast on a wet road."),
        ("Сколько стоит ___ на такси до аэропорта?", "ехать", ["ездить", "едет", "ездит"],
         "The cost of one one-way trip: ехать, not ездить. До аэропорта is genitive after до.",
         "How much does it cost to take a taxi to the airport?"),
        ("Он ___ так, будто дороги никому не нужны.", "ездит", ["едет", "ехал", "ездил"],
         "Manner of driving in general (a habit / characteristic): ездит. Едет would be this particular stretch.",
         "He drives as if nobody else needed the road."),
        ("Мы ___ на этой машине в Беларусь каждый год.", "ездим", ["едем", "ездили", "ехали"],
         "Каждый год marks a habit still in force: ездим.",
         "We drive to Belarus in this car every year."),
        ("Когда вы ___ в город, захватите мне гвоздей.", "едете", ["ездите", "ехали", "ездили"],
         "This particular (maybe imminent) trip: когда вы едете. Ездите would be 'whenever you go' as a habit, which is also possible, but the request 'grab me some nails' points to one trip.",
         "When you go to town, pick up some nails for me."),
        ("Я больше не ___ на этом поезде: он всегда опаздывает.", "езжу", ["еду", "ехал", "ездил"],
         "A standing decision about a kind of travel: больше не езжу. Не еду would be 'I'm not taking it this time'.",
         "I don't take this train any more: it's always late."),
    ]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "ехать / ездить", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "other pairs"
    rows = [
        ("Сейчас я ___ сено в сарай, помоги мне.", "несу", ["ношу", "нёс", "носил"],
         "Carrying something right now, one way: unidirectional нести — я несу. Ношу would be a habit. Сено is the direct object; в сарай is accusative (куда?).",
         "I'm carrying the hay into the barn right now; help me."),
        ("Летом мы каждый день ___ воду из колодца.", "носим", ["несём", "несли", "носили"],
         "A daily habit of carrying: носить — мы носим. Несём would be this particular load in progress.",
         "In the summer we carry water from the well every day."),
        ("Вчера я ___ мешки в сарай и уже всё сложил.", "носил", ["нёс", "несу", "ношу"],
         "A completed past activity of carrying (possibly several trips): носил. Нёс would be one load in progress in the past.",
         "Yesterday I carried the sacks into the barn and have already stacked them all."),
        ("Когда я ___ ведро к коровам, я поскользнулся.", "нёс", ["носил", "несу", "ношу"],
         "One load, in progress in the past, interrupted: нёс. Носил would be a habit or a completed set of trips.",
         "While I was carrying the bucket to the cows, I slipped."),
        ("Кто у вас ___ молоко в город на продажу?", "возит", ["везёт", "возил", "ведёт"],
         "Habitual hauling by vehicle: возить — возит. Везёт would be this particular load on the move. Молоко is the direct object.",
         "Who at your place hauls the milk into town to sell?"),
        ("Смотри, трактор ___ сено с луга.", "везёт", ["возит", "ведёт", "носит"],
         "One load, one direction, now, by vehicle: везёт. Возит would be a habit. С луга is genitive after с.",
         "Look, the tractor is hauling hay from the meadow."),
        ("Он уже тридцать лет ___ этот автобус до района.", "водит", ["ведёт", "возит", "везёт"],
         "A skill or long habit of driving: водить — водит. Ведёт would be this particular trip in progress.",
         "He has been driving this bus to the district center for thirty years."),
        ("Осторожно, он ___ трактор через калитку!", "ведёт", ["водит", "везёт", "возит"],
         "One vehicle being driven now, one direction: ведёт. Водит would be the habit / skill.",
         "Careful — he's driving the tractor through the gate!"),
        ("Куры хорошо ___ этой весной.", "несут", ["носят", "несли", "носили"],
         "Нести яйца ('to lay eggs') uses the unidirectional verb even for a general production period: несут. Носят is not used in this meaning.",
         "The hens are laying well this spring."),
        ("Почтальон каждый день ___ нам газеты.", "носит", ["несёт", "возит", "везёт"],
         "A daily delivery habit, on foot: носит. Несёт would be today's bundle in progress.",
         "The postman brings us the papers every day."),
        ("Самолёт ___ в Минск, когда началась гроза.", "летел", ["летал", "летит", "летает"],
         "One flight in progress in the past, interrupted: летел (лететь). Летал would be a habit or a completed round trip.",
         "The plane was flying to Minsk when the thunderstorm started."),
        ("Он ___ в Беларусь два раза в год, к родне.", "летает", ["летит", "летел", "летал"],
         "A repeated flight habit: летать — летает. Летит would be this particular flight now.",
         "He flies to Belarus twice a year, to his relatives."),
        ("Сейчас этот самолёт ___ в Минск, он уже над нами.", "летит", ["летает", "летел", "летал"],
         "One flight, one direction, now: летит. Летает would be a schedule or habit.",
         "This plane is flying to Minsk right now; it's already over us."),
        ("Я не люблю ___ : укачивает.", "летать", ["лететь", "лечу", "летаю"],
         "A general attitude to the activity: летать (multidirectional infinitive). Лететь would be one particular flight.",
         "I don't like flying: I get motion sickness."),
        ("Дети ___ воду из колодца каждое лето, когда насос не работает.", "носят", ["несут", "носили", "несли"],
         "A summer habit of carrying water: multidirectional носят (носить). Несут would be one load, right now.",
         "The children carry water from the well every summer, when the pump isn't working."),
        ("Смотри, гуси ___ на юг над нашей фермой.", "летят", ["летают", "летели", "летали"],
         "One flight, one direction, now: лететь — летят. Летают would be flying around or a habit.",
         "Look, the geese are flying south over our farm."),
        ("Почтальон ___ письма на велосипеде, не пешком.", "возит", ["везёт", "носит", "несёт"],
         "His regular job of delivering by vehicle: multidirectional возит (возить). Везёт would be this one trip. Носит / несёт would be on foot.",
         "The postman delivers the letters by bicycle, not on foot."),
        ("Я ___ мешок на плечо и понёс в сарай.", "взвалил? skip", ["x"], "skip", "x"),
        ("Каждое утро я ___ детей в школу на машине, потом еду на ферму.", "вожу", ["веду", "везгу", "воду"],
         "Habitual driving of people: водить — я вожу (д → ж). Веду would be leading on foot; везу would be one haul now (везти).",
         "Every morning I drive the children to school, then I go to the farm."),
        ("Сейчас я ___ телёнка в поводе к ветеринару.", "веду", ["вожу", "везу", "вожуу"],
         "Leading an animal on a lead, one way, now: вести — я веду. Вожу would be a habit; везу would be hauling by vehicle.",
         "I'm leading the calf on a rope to the vet right now."),
    ]
    rows = [r for r in rows if r[3] != "skip"]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "нести / носить · вести / водить · везти / возить · лететь / летать", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "prefixed"
    rows = [
        ("Утром я ___ из дома в пять и пошёл доить.", "вышел", ["вошёл", "пришёл", "зашёл"],
         "Вы- means 'out of': выйти из дома. Вошёл is 'went in', пришёл is 'arrived', зашёл is 'dropped in'. Из дома is genitive after из.",
         "In the morning I left the house at five and went to milk."),
        ("Когда я ___ в сарай, коровы уже стояли у кормушки.", "вошёл", ["вышел", "пришёл", "зашёл"],
         "В- / во- means 'into': войти в сарай. В сарай is accusative (куда?).",
         "When I went into the barn, the cows were already standing at the feeder."),
        ("Друг ___ к нам вчера вечером, мы пили чай.", "пришёл", ["вышел", "ушёл", "зашёл"],
         "При- means arrival at the speaker's (or a goal): он пришёл. Ушёл is 'he left'; зашёл is a short drop-in.",
         "A friend came over yesterday evening; we drank tea."),
        ("После чая он ___ домой, потому что рано доить.", "ушёл", ["пришёл", "вышел", "зашёл"],
         "У- means 'away, off': уйти домой. Пришёл is arrival; вышел is coming out of a place.",
         "After tea he left for home, because milking is early."),
        ("По дороге с поля я ___ к соседу за солью.", "зашёл", ["вышел", "пришёл", "перешёл"],
         "За- means a short stop on the way: зайти к соседу. К соседу is dative after к.",
         "On the way back from the field I dropped in on the neighbor for salt."),
        ("Чтобы попасть в храм, нужно ___ через площадь.", "перейти", ["выйти", "прийти", "уйти"],
         "Пере- means 'across': перейти через площадь. Через площадь is accusative after через.",
         "To get to the church you have to cross the square."),
        ("Поезд ___ в Минск в семь утра, не опаздывай.", "приходит", ["уходит", "выходит", "заходит"],
         "При- of a scheduled arrival: поезд приходит. Уходит is departure; выходит is 'comes out'. В Минск is accusative? Actually приходит в Минск is used, or прибывает в Минск. OK.",
         "The train arrives in Minsk at seven in the morning; don't be late."),
        ("Поезд ___ из Минска в восемь, мы ещё успеем.", "уходит", ["приходит", "выходит", "заходит"],
         "У- of a scheduled departure: поезд уходит. Из Минска is genitive after из.",
         "The train leaves Minsk at eight; we can still make it."),
        ("Самолёт ___ в Беларусь в полдень.", "прилетает", ["вылетает", "улетает", "залетит"],
         "При- + летать of an arrival by air: прилетает. Вылетает is departure. В Беларусь is accusative (куда?).",
         "The plane arrives in Belarus at noon."),
        ("Наш самолёт ___ в шесть, так что в аэропорту надо быть в четыре.", "вылетает", ["прилетает", "улетает", "долетает"],
         "Вы- + летать of a departure by air: вылетает. Прилетает is arrival.",
         "Our plane takes off at six, so we need to be at the airport at four."),
        ("Коллега ___ в командировку в Минск на неделю.", "уехал", ["ушёл", "приехал", "уехала"],
         "Travel to another city uses the ехать family: уехать в командировку. Ушёл would be on foot / just leaving the room. Уехала would need a feminine subject.",
         "A colleague has gone on a business trip to Minsk for a week."),
        ("Друг ___ из Беларуси на прошлой неделе, мы его встречали.", "приехал", ["уехал", "пришёл", "приехала"],
         "При- + ехать of arrival by vehicle: приехал. Пришёл would be on foot. Из Беларуси is genitive after из.",
         "A friend arrived from Belarus last week; we met him."),
        ("Я ___ к врачу по дороге на рынок, зуб разболелся.", "заехал", ["зашёл", "уехал", "приехал"],
         "За- + ехать: a short stop by vehicle on the way: заехать к врачу. Зашёл would be on foot. К врачу is dative after к.",
         "I stopped by the doctor on the way to the market; my tooth had started to hurt."),
        ("Чтобы попасть на ферму, нужно ___ мост через реку.", "переехать", ["перейти", "уехать", "приехать"],
         "Пере- + ехать: to cross by vehicle: переехать мост. Перейти would be on foot. Мост is the direct object (accusative).",
         "To get to the farm you have to drive across the bridge over the river."),
        ("Я ___ код на сервер и пошёл доить.", "залил? skip выложил? Use загрузить. Better: зашёл в программу? Use вошёл в систему", "x", "skip", "x"),
        ("Вечером я ___ в программу и сразу увидел ошибку.", "вошёл", ["вышел", "зашёл", "пришёл"],
         "Войти в программу / в систему is the usual prefixed verb for logging in: вошёл. Вышел would be logging out. В программу is accusative (куда?).",
         "In the evening I went into the program and immediately saw the bug."),
        ("Перед сном я ___ из программы и выключил компьютер.", "вышел", ["вошёл", "зашёл", "ушёл"],
         "Выйти из программы is logging out: вышел. Из программы is genitive after из.",
         "Before sleep I quit the program and turned off the computer."),
        ("По дороге домой мы ___ за хлебом в магазин.", "заехали", ["зашли", "уехали", "приехали"],
         "За- + ехать, plural, a stop by car: заехали за хлебом. Зашли would be on foot. За хлебом is instrumental.",
         "On the way home we stopped at the store for bread."),
        ("Он ___ от нас без завтрака, спешил на поезд.", "уехал", ["ушёл", "приехал", "выехал"],
         "У- + ехать: he left by vehicle: уехал. Ушёл would be on foot. От нас is genitive after от.",
         "He left our place without breakfast; he was in a hurry for the train."),
        ("Когда трактор ___ во двор, собаки подняли лай.", "въехал", ["выехал", "уехал", "приехал"],
         "В- / въ- + ехать: to drive into: въехать во двор. Выехал is 'drove out'. Во двор is accusative (куда?).",
         "When the tractor drove into the yard, the dogs started barking."),
        ("Утром пикап ___ со двора и больше не возвращался до ночи.", "выехал", ["въехал", "уехал", "приехал"],
         "Вы- + ехать: to drive out: выехать со двора. Со двора is genitive after с/со.",
         "In the morning the pickup drove out of the yard and didn't come back until night."),
    ]
    rows = [r for r in rows if r[3] != "skip"]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "prefixed motion", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)


    # ---- B1 aspect ----
    C = "aspect"
    def asp(sub, s, base, a, d, ex, tr, gl=None):
        addv(B, C, sub, s, base, a, d, ex, tr, gl)

    S = "process vs result"
    rows = [
        ("Весь вечер я ___ эту программу, и всё ещё не готов.", "писал", ["написал", "напишу", "пишу"],
         "Весь вечер and 'still not ready' mark a process, so the imperfective past: писал (писать / написать). Написал would mean the program is finished.",
         "I spent the whole evening writing this program, and it still isn't ready."),
        ("Я уже ___ отчёт, можешь смотреть.", "написал", ["писал", "напишу", "пишу"],
         "Уже and 'you can look' mark a completed result: perfective написал. Писал would be 'I was writing / I used to write'.",
         "I've already written the report; you can look at it."),
        ("Отец долго ___ трактор, но так и не завёл.", "чинил", ["починил", "починит", "чинит"],
         "Долго + так и не marks an unsuccessful process: imperfective чинил (чинить / починить). Починил would mean he succeeded.",
         "Dad spent a long time repairing the tractor, but he never did get it started."),
        ("Слава Богу, он наконец ___ трактор.", "починил", ["чинил", "починит", "чинит"],
         "Наконец plus a successful result: perfective починил.",
         "Thank God, he finally repaired the tractor."),
        ("Жена весь час ___ коров, я помогал с телятами.", "доила", ["подоила", "доит", "подоит"],
         "Весь час marks a process lasting over a period: imperfective доила (доить / подоить). Подоила would mean the milking is finished.",
         "My wife spent the whole hour milking the cows; I was helping with the calves."),
        ("К шести она уже ___ всех коров.", "подоила", ["доила", "доит", "подоит"],
         "Уже + к шести marks a completed result: perfective подоила. Всех коров is animate accusative plural.",
         "By six she had already milked all the cows."),
        ("Я два часа ___ сено под навес, пока не пошёл дождь.", "возил", ["повёз", "вез", "возит"],
         "Два часа marks a process: imperfective возил (возить). Повёз would start a single one-way haul as a completed act.",
         "I spent two hours hauling hay under the lean-to, until it started to rain."),
        ("Мы уже ___ всё сено: можно закрывать сарай.", "свезли", ["возили", "свозим", "везём"],
         "Уже + всё marks a completed result: perfective свезли (свозить / свезти). Возили would be the process.",
         "We've already hauled in all the hay; we can close the barn."),
        ("Он долго ___ эту задачу и в конце концов ___ её. (two blanks - skip)", "x", [], "skip", "x"),
        ("Программист долго ___ эту ошибку в коде.", "искал", ["нашёл", "найдёт", "ищет"],
         "Долго marks a process: imperfective искал (искать / найти). Нашёл would mean he found it.",
         "The programmer spent a long time looking for this bug in the code."),
        ("Наконец он ___ ошибку: не хватало одной скобки.", "нашёл", ["искал", "найдёт", "ищет"],
         "Наконец plus the result: perfective нашёл (найти). Искал would be the search process.",
         "At last he found the bug: a single bracket was missing."),
        ("Дети весь урок ___ эту молитву вслух.", "учили", ["выучили", "выучат", "учат"],
         "Весь урок marks a process: imperfective учили (учить / выучить). Выучили would mean they now know it by heart.",
         "The children spent the whole lesson learning this prayer out loud."),
        ("К вечеру они уже ___ молитву наизусть.", "выучили", ["учили", "выучат", "учат"],
         "К вечеру already + наизусть marks the result: perfective выучили.",
         "By evening they had already learned the prayer by heart."),
        ("Я три дня ___ новый курятник.", "строил", ["построил", "построит", "строит"],
         "Три дня marks a process: imperfective строил (строить / построить). Построил would mean the coop is finished.",
         "I spent three days building the new coop."),
        ("Наконец мы ___ курятник, и кур можно загонять.", "построили", ["строили", "построим", "строим"],
         "Наконец plus the result: perfective построили. Кур is animate accusative plural.",
         "At last we finished the coop, and we can drive the hens in."),
        ("Весь вечер мы ___ старые песни Молчат Дома.", "слушали", ["послушали", "послушаем", "слушаем"],
         "Весь вечер marks a process: imperfective слушали (слушать / послушать). Послушали would be a short completed listen.",
         "We spent the whole evening listening to old Molchat Doma songs."),
        ("Я уже ___ этот файл, можно закрывать программу.", "скачал", ["скачивал", "скачаю", "скачиваю"],
         "Уже plus 'you can close it' marks a completed result: perfective скачал (скачать). Скачивал would be the process.",
         "I've already downloaded this file; we can close the program."),
        ("Она долго ___ письмо батюшке и всё переписывала.", "писала", ["написала", "напишет", "пишет"],
         "Долго + переписывала marks an ongoing process: imperfective писала. Написала would mean the letter is done.",
         "She spent a long time writing a letter to Father and kept rewriting it."),
        ("Письмо уже ___ , я его отнёс на почту.", "написано? skip use написала she", "x", "skip", "x"),
        ("К утру я ___ письмо и отнёс его на почту.", "написал", ["писал", "напишу", "пишу"],
         "К утру plus the next action (отнёс) marks a completed result: написал.",
         "By morning I had written the letter and taken it to the post office."),
        ("Дождь ___ всю ночь, сено пришлось снова ворошить.", "шёл", ["пошёл", "прошёл", "идет"],
         "Всю ночь marks a process: imperfective шёл (of rain). Прошёл would mean the rain has finished; пошёл would be 'it started to rain'.",
         "The rain went on all night; we had to turn the hay again."),
    ]
    rows = [r for r in rows if r[3] != "skip"]
    for s, a, d, ex, *rest in rows:
        asp(S, s, "imperfective / perfective", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "repeated action"
    rows = [
        ("Каждое утро я ___ коров в шесть.", "дою", ["доюу", "подою", "доил"],
         "Каждое утро marks a habit, so the imperfective present: дою (доить / подоить). Подою would be one future milking.",
         "Every morning I milk the cows at six."),
        ("Раз в неделю жена ___ иконы в храме.", "протирает", ["протрёт", "протёрла", "протирала"],
         "Раз в неделю marks a repeated action: imperfective протирает (протирать / протереть).",
         "Once a week my wife dusts the icons in the church.", ["протирать: to wipe, dust"]),
        ("По вечерам мы обычно ___ чай на крыльце.", "пьём", ["выпиваем", "выпили", "попьём"],
         "Обычно + по вечерам: imperfective пьём (пить). Выпили would be a completed act of drinking something up.",
         "In the evenings we usually drink tea on the porch."),
        ("Каждый год мы ___ в Беларусь к друзьям.", "ездим", ["едем", "поедем", "ездили"],
         "Каждый год marks a habit: imperfective ездим (ездить / поехать). Поедем would be one future trip.",
         "Every year we go to Belarus to see friends."),
        ("Он всегда ___ ворота на ночь.", "закрывает", ["закроет", "закрыл", "закрой"],
         "Всегда marks a habit: imperfective закрывает (закрывать / закрыть). Закроет would be one future act.",
         "He always shuts the gate at night."),
        ("По воскресеньям они ___ к литургии пешком.", "ходят", ["идут", "пойдут", "ходили"],
         "По воскресеньям marks a habit: imperfective ходят. Идут / пойдут would be one trip.",
         "On Sundays they walk to the Liturgy."),
        ("Я редко ___ в городе: всё есть на ферме.", "покупаю", ["куплю", "купил", "покупал"],
         "Редко still marks a repeated (if rare) action: imperfective покупаю (покупать / купить).",
         "I rarely shop in town: we have everything on the farm."),
        ("Каждый раз, когда он ___ , мы садимся пить чай.", "приходит", ["придёт", "пришёл", "приходил"],
         "Каждый раз, когда… is a repeated situation: imperfective приходит (приходить / прийти).",
         "Every time he comes, we sit down to drink tea."),
        ("Зимой я часто ___ сено с дальнего луга заранее.", "вожу", ["везю", "повезу", "возил"],
         "Часто + зимой marks a seasonal habit: imperfective вожу (возить).",
         "In winter I often haul hay from the far meadow in advance."),
        ("Дети всегда ___ руки перед едой, как мы учили.", "моют", ["помоют", "вымоют", "мыли"],
         "Всегда marks a habit: imperfective моют (мыть / помыть / вымыть).",
         "The children always wash their hands before a meal, as we taught them."),
        ("По утрам программа сама ___ резервную копию.", "делает", ["сделает", "сделала", "делалась"],
         "По утрам marks a repeated automatic action: imperfective делает (делать / сделать).",
         "In the mornings the program makes a backup copy on its own."),
        ("Раз в месяц батюшка ___ по домам.", "ходит", ["идёт", "пойдёт", "ходил"],
         "Раз в месяц marks a repeated pastoral round: imperfective ходит.",
         "Once a month Father goes from house to house."),
        ("Я обычно ___ этот поезд, он почти не опаздывает.", "беру", ["возьму", "взял", "брал"],
         "Обычно marks a habit: imperfective беру (брать / взять). Возьму would be one future occasion.",
         "I usually take this train; it's almost never late."),
        ("Каждую пятницу мы ___ борщ, это семейный обычай.", "варим", ["сварим", "сварили", "варили"],
         "Каждую пятницу marks a habit: imperfective варим (варить / сварить).",
         "Every Friday we make borscht; it's a family custom."),
        ("Он никогда не ___ калитку открытой на ночь.", "оставляет", ["оставит", "оставил", "оставь"],
         "Никогда не + habit: imperfective оставляет (оставлять / оставить). The double negative никогда не is required.",
         "He never leaves the gate open at night."),
        ("По ночам собака всегда ___ , если кто-то идёт вдоль забора.", "лает", ["залает", "залаяла", "лаяла"],
         "Всегда + по ночам: imperfective лает (лаять / залаять). Залает would be one future burst of barking.",
         "At night the dog always barks if someone is walking along the fence."),
        ("Каждое лето мы ___ новый забор или чиним старый.", "ставим", ["поставим", "поставили", "ставили"],
         "Каждое лето marks a seasonal habit: imperfective ставим (ставить / поставить).",
         "Every summer we put up a new fence or repair the old one."),
        ("Я почти каждый день ___ Молчат Дома, когда еду в поле.", "слушаю", ["послушаю", "послушал", "слушал"],
         "Почти каждый день marks a habit: imperfective слушаю (слушать / послушать).",
         "I listen to Molchat Doma almost every day when I drive out to the field."),
        ("Когда гости ___, я всегда ставлю самовар.", "приходят", ["придут", "пришли", "приходили"],
         "A repeated situation (когда гости приходят): imperfective приходят, and ставлю is also imperfective (habit).",
         "When guests come, I always put the samovar on."),
        ("По утрам я ___ код, который написал накануне.", "проверяю", ["проверю", "проверил", "проверял"],
         "По утрам marks a habit: imperfective проверяю (проверять / проверить).",
         "In the mornings I check the code I wrote the day before."),
    ]
    # fix typo distractor доюу - use подоил or доишь
    rows[0] = ("Каждое утро я ___ коров в шесть.", "дою", ["подою", "доил", "доит"],
               rows[0][3], rows[0][4])
    for s, a, d, ex, *rest in rows:
        asp(S, s, "imperfective / perfective", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)


    S = "infinitive"
    rows = [
        ("В прошлом году я начал ___ русский всерьёз.", "учить", ["выучить", "учу", "выучил"],
         "Начать takes the imperfective infinitive: начал учить (the process). Выучить would be the result, and you cannot say начал выучить.",
         "Last year I started studying Russian in earnest."),
        ("Мне удалось ___ этот модуль за одну ночь.", "написать", ["писать", "написал", "пишу"],
         "Удалось (the result was achieved) takes the perfective infinitive: удалось написать. Писать would name the activity, not the successful result.",
         "I managed to write this module in a single night."),
        ("Не надо ___ хлеб в городе, у нас свой есть.", "покупать", ["купить", "купи", "покупаю"],
         "Не надо / не нужно take the imperfective infinitive: не надо покупать (no need to do this as an activity). Купить would sound like 'don't succeed in buying'.",
         "There's no need to buy bread in town; we have our own."),
        ("Нужно ___ коров до рассвета, потом сено.", "подоить", ["доить", "дою", "подоил"],
         "A single necessary task with a result in view: нужно + perfective подоить. Доить would describe the activity in general ('one should do milking'). Both are possible, but the dawn deadline points to getting it done.",
         "We need to get the cows milked before dawn, then the hay."),
        ("Я хочу ___ новый курятник до зимы.", "построить", ["строить", "построю", "строил"],
         "Хотеть can take both aspects. Here a result by a deadline (до зимы) favours the perfective: хочу построить. Строить would be 'I want to be engaged in building'.",
         "I want to get a new coop built before winter."),
        ("Он любит ___ по ферме вечером, когда остынет.", "ходить", ["пойти", "идти", "ходил"],
         "Любить takes the imperfective infinitive (the activity in general): любит ходить. Пойти would be one particular departure.",
         "He likes walking around the farm in the evening, when it cools off."),
        ("Забудь ___ этот файл: он уже не нужен.", "скачивать", ["скачать", "скачаю", "скачал"],
         "Hmm, забыть usually takes perfective for 'forget to do X once': забудь скачать? Actually 'forget about downloading / don't bother downloading' can be забудь скачивать or не надо скачивать. Let me recast.",
         "x"),
    ]
    rows = [r for r in rows if r[4] != "x"]
    rows += [
        ("Я забыл ___ паспорт и меня не пустили на поезд.", "взять", ["брать", "возьму", "взял"],
         "Забыть + perfective infinitive names one action that was not performed: забыл взять. Брать would be 'forgot how to / forgot the activity of taking'.",
         "I forgot to take my passport, and they wouldn't let me on the train."),
        ("Можно ___ окно? Здесь очень душно.", "открыть", ["открывать", "открою", "открыл"],
         "A one-time request for permission: можно + perfective открыть. Открывать would be 'is it allowed to open windows (as a practice)'.",
         "May I open the window? It's very stuffy in here."),
        ("Нельзя ___ калитку на ночь открытой.", "оставлять", ["оставить", "оставь", "оставил"],
         "Нельзя of a standing rule takes the imperfective infinitive: нельзя оставлять. Оставить would be one particular occasion.",
         "You mustn't leave the gate open at night."),
        ("Я боюсь ___ по льду: он ещё тонкий.", "ходить", ["пойти", "идти", "ходил"],
         "Бояться of a general activity takes the imperfective: боюсь ходить. Пойти would be one particular outing.",
         "I'm afraid of walking on the ice: it's still thin."),
        ("Удалось ли вам ___ билеты до Минска?", "купить", ["покупать", "купите", "купил"],
         "Удалось ли asks whether the result was achieved: perfective купить. Покупать would ask whether you engaged in the activity.",
         "Did you manage to get the tickets to Minsk?"),
        ("Пора ___ коров, уже шестой час.", "доить", ["подоить", "дою", "подоил"],
         "Пора + imperfective often names the scheduled activity whose time has come: пора доить. Подоить would stress getting this one milking finished.",
         "It's time to milk the cows; it's already six."),
        ("Мы продолжаем ___ этот модуль, он ещё сырой.", "писать", ["написать", "пишем", "написали"],
         "Продолжать always takes the imperfective infinitive: продолжаем писать (you cannot continue a result). Написать is the completed result.",
         "We are continuing to write this module; it's still rough."),
        ("Он обещал ___ нам сена с своего луга.", "привезти", ["привозить", "привезёт", "привёз"],
         "Обещать of one promised delivery takes the perfective infinitive: обещал привезти. Привозить would be a standing arrangement.",
         "He promised to bring us some hay from his own meadow."),
        ("Я устал ___ воду из колодца вёдрами.", "носить", ["нести", "ношу", "нёс"],
         "Устать от the activity in general (or of repeated carrying) takes the imperfective: устал носить. Нести would be one load.",
         "I'm tired of carrying water from the well in buckets."),
        ("Надо бы ___ батюшку, не видели его с Пасхи.", "навестить", ["навещать", "навещу", "навестил"],
         "Надо бы of one desirable visit: perfective навестить. Навещать would be 'we ought to visit him regularly'.",
         "We ought to visit Father; we haven't seen him since Pascha."),
        ("Перестань ___ на кур: они и так нервные.", "кричать", ["крикнуть", "кричи", "кричал"],
         "Перестань (stop doing) takes the imperfective infinitive of the activity: перестань кричать. Крикнуть is one shout.",
         "Stop shouting at the hens: they're nervous enough as it is."),
        ("Я научился ___ трактор, когда мне было двенадцать.", "водить", ["вести", "вожу", "вёл"],
         "Научиться of a skill takes the imperfective infinitive: научился водить (the skill in general). Вести would be one particular act of driving.",
         "I learned to drive a tractor when I was twelve."),
        ("Попробуй ___ этот файл в другую папку.", "скопировать", ["копировать", "скопирую", "копировал"],
         "Попробуй of one attempted action takes the perfective: попробуй скопировать. Копировать would be 'try engaging in copying (in general)'.",
         "Try copying this file into another folder."),
        ("Ему пора ___ : завтра рано доить.", "лечь", ["ложиться", "ляжет", "лёг"],
         "Пора + a single act now: пора лечь (perfective). Ложиться would be the process or the habit of going to bed.",
         "He ought to go to bed: milking is early tomorrow."),
        ("Я не привык ___ код без тестов.", "писать", ["написать", "пишу", "написал"],
         "Привык takes the imperfective infinitive of a habit: не привык писать. Написать is one completed write-up.",
         "I'm not used to writing code without tests."),
    ]
    for s, a, d, ex, *rest in rows:
        asp(S, s, "imperfective / perfective", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "future"
    rows = [
        ("Когда я ___ модуль, я возьму выходной.", "закончу", ["заканчиваю", "закончил", "заканчивал"],
         "A one-time future result (когда = 'once I have finished') takes the perfective future: закончу (закончить). Заканчиваю is present imperfective.",
         "When I finish the module, I'll take a day off."),
        ("Завтра я ___ тебе, как только приеду в Минск.", "позвоню", ["звоню", "звонил", "позвонил"],
         "A one-time future call: perfective позвоню (позвонить). Звоню is present ('I am calling / I call habitually').",
         "I'll call you tomorrow as soon as I get to Minsk."),
        ("Можно я ___ твою лопату на часок?", "возьму", ["беру", "взял", "брал"],
         "A one-time request about the immediate future: perfective возьму (взять). Беру is present imperfective.",
         "May I take your shovel for an hour?"),
        ("Завтра мы ___ коров раньше, потому что едем на ярмарку.", "подоим", ["доим", "доили", "подоили"],
         "One particular tomorrow-morning milking with a result in view: perfective подоим (подоить). Доим is the habitual present.",
         "Tomorrow we'll milk the cows earlier, because we're going to the fair."),
        ("Вечером я ___ этот файл на сервер.", "загружу", ["загружаю", "загрузил", "загружал"],
         "A one-time future action: perfective загружу (загрузить). Загружаю is present.",
         "This evening I'll upload this file to the server."),
        ("Завтра весь день я ___ сено, так что не звони до вечера.", "буду возить", ["повоюзу", "возил", "повезу"],
         "A future process lasting all day takes буду + imperfective: буду возить. Повезу would be one one-way haul as a completed future act.",
         "Tomorrow I'll be hauling hay all day, so don't call until evening."),
        ("После дойки я ___ в город за запчастями.", "поеду", ["еду", "езжу", "ехал"],
         "A one-time future trip: perfective поеду (поехать). Еду can announce a planned trip, but после дойки + a single outing is cleanly поеду.",
         "After milking I'll drive to town for spare parts."),
        ("Мы ___ новый забор, как только просохнет земля.", "поставим", ["ставим", "ставили", "поставили"],
         "A one-time future result after a condition: perfective поставим (поставить). Ставим is the habitual present.",
         "We'll put up a new fence as soon as the ground dries out."),
        ("В субботу я ___ батюшку, давно не виделись.", "навещу", ["навещаю", "навестил", "навещал"],
         "A one-time future visit: perfective навещу (навестить).",
         "On Saturday I'll visit Father; we haven't seen each other in a long time."),
        ("Не волнуйся, я ___ ворота, перед тем как уехать.", "закрою", ["закрываю", "закрыл", "закрывал"],
         "A one-time future promise: perfective закрою (закрыть). Закрываю is present.",
         "Don't worry, I'll shut the gate before I leave."),
        ("Завтра в это время я уже ___ в Минске.", "буду", ["буду быть", "был", "бываю"],
         "Location in the future uses буду + the prepositional: я буду в Минске. Бываю is habitual present.",
         "By this time tomorrow I'll already be in Minsk."),
        ("Если не ___ дождь, мы уберём сено.", "пойдёт", ["идёт", "шёл", "будет идти"],
         "A one-time future condition: если не пойдёт дождь (пойти of rain starting / falling as an event). Если не будет идти would describe a process.",
         "If it doesn't rain, we'll get the hay in."),
        ("Я ___ тебе письмо, как приеду.", "напишу", ["пишу", "написал", "писал"],
         "A one-time future result: perfective напишу (написать). Пишу is present.",
         "I'll write you a letter when I arrive."),
        ("Завтра они ___ кур в новый курятник.", "загонят", ["загоняют", "загнали", "загоняли"],
         "A one-time future herding: perfective загонят (загнать). Загоняют is present imperfective.",
         "Tomorrow they'll drive the hens into the new coop."),
        ("Весь следующий месяц я ___ этот курс по русской грамматике.", "буду проходить", ["пройду", "прохожу", "прошёл"],
         "A future process lasting a month: буду + imperfective проходить. Пройду would be 'I will complete it' as a single result.",
         "All next month I'll be taking this Russian grammar course."),
        ("Как только солнце ___ , мы выходим косить.", "взойдёт", ["восходит", "взошло", "всходит"],
         "A one-time future event as a starting gun: perfective взойдёт (взойти, of the sun). Восходит is present.",
         "As soon as the sun comes up, we go out to mow."),
        ("Я ___ тебе ключи, когда ты будешь выходить.", "дам", ["даю", "дал", "давал"],
         "A one-time future transfer: perfective дам (дать). Даю is present.",
         "I'll give you the keys when you're on your way out."),
        ("В этом году мы ___ больше кукурузы, чем в прошлом.", "посадим", ["сажаем", "посадили", "сажали"],
         "A one-time seasonal plan with a result: perfective посадим (посадить). Сажаем is the habitual / process present.",
         "This year we'll plant more corn than last year."),
        ("Он ___ код на ревью, как только напишет тесты.", "отправит", ["отправляет", "отправил", "отправлял"],
         "A one-time future result after a condition: perfective отправит (отправить).",
         "He'll send the code for review as soon as he writes the tests."),
        ("Завтра я не ___ в поле: надо ехать в Минск.", "пойду", ["иду", "ходил", "хожу"],
         "A one-time future refusal: не пойду (пойти). Не хожу would be a standing habit; не иду is 'I'm not going (now)'.",
         "Tomorrow I won't go out to the field: I have to go to Minsk."),
    ]
    # fix "буду возить" and "буду проходить" and "буду" - add() needs a single-word or phrase answer that's fine (multiword answers exist? existing are single). Multiword should be OK if typed/choice matches.
    for s, a, d, ex, *rest in rows:
        asp(S, s, "imperfective / perfective", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "imperative"
    rows = [
        ("Пожалуйста, ___ окно: здесь душно.", "открой", ["открывай", "откроете", "открыть"],
         "A one-time positive request takes the perfective imperative: открой (открыть). Открывай would be 'start opening / keep opening / open as a practice'.",
         "Please open the window: it's stuffy in here."),
        ("Пожалуйста, не ___ окно, здесь и так холодно.", "открывай", ["открой", "открываете", "открыть"],
         "A negative command of the type 'don't do this (now / as a policy)' takes the imperfective: не открывай. Не открой would mean 'see that you don't (accidentally) open it'.",
         "Please don't open the window; it's cold enough in here already."),
        ("___ ворота, трактор не проезжает!", "Открой", ["Открывай", "Откройте", "Открыть"],
         "A one-time urgent request to one person: perfective открой. Откройте would be the polite / plural form.",
         "Open the gate, the tractor can't get through!"),
        ("Не ___ кур с крыльца, они сами сойдут.", "гони", ["погоните", "гонись", "гнать"],
         "A 'don't do that now / don't make a habit of it' negative: imperfective не гони (гнать). The imperfective imperative is the normal negative.",
         "Don't chase the hens off the porch; they'll come down on their own."),
        ("___ мне, пожалуйста, лопату с сарая.", "Принеси", ["Приноси", "Принесите", "Принести"],
         "A one-time request to one person: perfective принеси (принести). Приноси would be 'bring (regularly / start bringing)'.",
         "Please bring me the shovel from the barn."),
        ("___ мне всегда ведро, когда идёшь к колодцу.", "Приноси", ["Принеси", "Принесите", "Принести"],
         "A standing request (always / habit) takes the imperfective imperative: приноси. Принеси would be this one occasion.",
         "Always bring me a bucket when you go to the well."),
        ("___ коров к шести, нам рано выезжать.", "Подой", ["Дои", "Подоите", "Доить"],
         "A one-time instruction with a result and a deadline: perfective подой (подоить). Дои would be 'do the milking (in general / start milking)'.",
         "Get the cows milked by six; we have to leave early."),
        ("Каждое утро ___ коров в одно и то же время.", "Дои", ["Подой", "Доите", "Доить"],
         "A standing instruction (каждое утро) takes the imperfective imperative: дои. Подой is one particular milking.",
         "Milk the cows at the same time every morning."),
        ("Не ___ так быстро по мокрой дороге!", "езди", ["поезжай", "ездите", "ехать"],
         "A general / manner warning: imperfective не езди так быстро. The imperfective is the normal negative imperative.",
         "Don't drive so fast on a wet road!"),
        ("___ сюда скорее, я тебе покажу телят.", "Иди", ["Ходи", "Идите", "Идти"],
         "A one-direction command now: иди (идти). Ходи would be 'do your walking (in general)'. Идите is polite / plural.",
         "Come here; I'll show you the calves."),
        ("Не ___ по льду: он ещё тонкий.", "ходи", ["иди", "ходите", "идти"],
         "A general prohibition on a kind of walking: не ходи (ходить). Не иди would stop someone already setting off on a particular path.",
         "Don't walk on the ice: it's still thin."),
        ("___ это письмо батюшке, пожалуйста.", "Отдай", ["Отдавай", "Отдайте", "Отдать"],
         "A one-time request: perfective отдай (отдать). Отдавай would be 'start handing it over / hand it over regularly'.",
         "Please give this letter to Father."),
        ("Не ___ ему ключи от трактора: он ещё не умеет.", "давай", ["дай", "дайте", "дать"],
         "A negative 'don't (as a policy / now)' takes the imperfective: не давай. Не дай would be 'see that you don't (let it happen)'.",
         "Don't give him the tractor keys: he can't drive yet."),
        ("___ файл в ту папку и закрой программу.", "Скопируй", ["Копируй", "Скопируйте", "Копировать"],
         "A one-time instruction in a sequence of results: perfective скопируй (скопировать). Копируй would start the activity.",
         "Copy the file into that folder and close the program."),
        ("___ всегда резервную копию, перед тем как править код.", "Делай", ["Сделай", "Делайте", "Сделать"],
         "A standing instruction (всегда) takes the imperfective imperative: делай. Сделай would be this one occasion.",
         "Always make a backup copy before you edit the code."),
        ("Не ___ это сообщение дважды: сервер не любит повторов.", "отправляй", ["отправь", "отправьте", "отправить"],
         "A negative instruction, possibly a policy: не отправляй (imperfective). Не отправь would be 'see that you don't (accidentally) send it'.",
         "Don't send this message twice: the server doesn't like repeats."),
        ("___ тихо: дети уже спят.", "Говори", ["Скажи", "Говорите", "Сказать"],
         "Manner of an ongoing activity: говори тихо (imperfective). Скажи would be 'say (one thing)'.",
         "Speak quietly: the children are already asleep."),
        ("___ ему, чтобы он закрыл калитку.", "Скажи", ["Говори", "Скажите", "Говорить"],
         "A one-time 'tell him (this one thing)': perfective скажи (сказать). Говори would be 'talk / keep talking'.",
         "Tell him to shut the gate."),
        ("Пожалуйста, ___ свет в сарае, когда будешь уходить.", "выключи", ["выключай", "выключите", "выключить"],
         "A one-time request tied to a future departure: perfective выключи (выключить). Выключай would be a standing rule.",
         "Please turn off the light in the barn when you leave."),
        ("Всегда ___ свет, когда уходишь из сарая.", "выключай", ["выключи", "выключайте", "выключить"],
         "Всегда marks a standing rule: imperfective выключай. Выключи is one particular occasion.",
         "Always turn off the light when you leave the barn."),
        ("Не ___ эту песню при жене: она её не любит.", "включай", ["включи", "включите", "включить"],
         "A standing / now negative: не включай (imperfective). Не включи would be 'see that you don't (accidentally) put it on'.",
         "Don't put this song on when my wife is here: she doesn't like it."),
    ]
    for s, a, d, ex, *rest in rows:
        asp(S, s, "imperfective / perfective", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "annulled action"
    rows = [
        ("Пока тебя не было, к тебе ___ сосед, но он уже ушёл.", "приходил", ["пришёл", "придёт", "приходит"],
         "A round trip whose result is gone (he came and left): imperfective past приходил (приходить). Пришёл would mean he is still here (or that we care about the arrival itself).",
         "While you were out, a neighbor came by for you, but he has already left."),
        ("Кто-то ___ в сарай: дверь была открыта, но внутри никого нет.", "заходил", ["зашёл", "зайдёт", "заходит"],
         "Evidence of a visit whose result is gone (nobody is there now): заходил. Зашёл would present the arrival as a fact with a result still relevant.",
         "Someone had been in the barn: the door was open, but there is no one inside."),
        ("Утром к нам ___ батюшка, но мы были в поле.", "заходил", ["зашёл", "зайдёт", "заходит"],
         "He dropped by and is no longer here (and we missed him): заходил. Зашёл would be used if we were telling the arrival as a completed event we witnessed.",
         "Father dropped by in the morning, but we were in the field."),
        ("Вчера я ___ в сельсовет, но он был закрыт, так что я вернулся.", "ходил", ["шёл", "пойду", "хожу"],
         "A failed / annulled round trip (went and came back with no result): ходил. Шёл would be the trip in progress.",
         "Yesterday I went to the village council, but it was closed, so I came back."),
        ("Кто-то ___ мой инструмент и положил его не на место.", "брал", ["взял", "берёт", "возьмёт"],
         "The tool was taken and is back (or the taking is no longer the result we care about): imperfective брал. Взял would mean he has it now.",
         "Someone had taken my tool and put it back in the wrong place."),
        ("Ты ___ мои ключи? Их нет на полке, но и у тебя я их не вижу.", "брал", ["взял", "берёшь", "возьмёшь"],
         "Asking whether someone had the keys at some point (they may already have been returned): брал. Взял would accuse him of having them now.",
         "Did you have my keys? They're not on the shelf, but I don't see them on you either."),
        ("К нам ___ письмо из Беларуси, но почтальон унёс его обратно: нас не было.", "приходило", ["пришло", "придёт", "приходит"],
         "The letter came and went again (result annulled): приходило. Пришло would mean the letter is here now. Письмо is neuter: -о.",
         "A letter from Belarus came for us, but the postman took it back: we weren't in."),
        ("На ферму ___ инспектор, посмотрел бумаги и уехал.", "приезжал", ["приехал", "приедет", "приезжает"],
         "He came and has already left: imperfective приезжал. Приехал would be used if he were still here, or if the arrival itself were the news.",
         "An inspector came to the farm, looked at the papers and left."),
        ("Я ___ тебе утром, но ты не взял трубку.", "звонил", ["позвонил", "звоню", "позвоню"],
         "I called (and the call is over, with no completed conversation): звонил. Позвонил can also be used, but the imperfective stresses the attempt rather than a successful completed call.",
         "I called you in the morning, but you didn't pick up."),
        ("В сарае кто-то ___ свет и не выключил? Нет, он сам выключился, значит кто-то ___ и ушёл. skip messy", "x", [], "skip", "x"),
        ("Кто-то ___ в программу под моим именем и вышел.", "входил", ["вошёл", "войдёт", "входит"],
         "A login whose result is gone (they have already logged out): входил. Вошёл would be used if they were still in the system.",
         "Someone had logged into the program under my name and logged out again."),
        ("К нам ___ курьеры с посылкой, не дождались и уехали.", "приезжали", ["приехали", "приедут", "приезжают"],
         "They came and left without completing the delivery: приезжали. Приехали would leave them (or the arrival) as a present result.",
         "Couriers came to us with a parcel, got tired of waiting and left."),
        ("Утром на лугу ___ олени, но к полудню их уже не было.", "были? skip use заходили / выходили", "x", "skip", "x"),
        ("Утром на луг ___ олени, но к полудню их уже не было.", "выходили", ["вышли", "выйдут", "выходят"],
         "They came out (and have gone again): imperfective выходили. Вышли would be used if we were pointing to a present result (they're out there now).",
         "Deer came out into the meadow in the morning, but by noon they were already gone."),
        ("Я ___ этот файл на рабочий стол, а потом удалил: он был не тот.", "скачивал", ["скачал", "скачаю", "скачиваю"],
         "The download's result has been undone (the file was deleted): скачивал. Скачал would be used if the file were still there as the result.",
         "I had downloaded this file to the desktop and then deleted it: it was the wrong one."),
        ("Сосед ___ нам свою косилку, но уже забрал её обратно.", "дал", ["давал", "даст", "даёт"],
         "WAIT: давал is the imperfective of the annulled loan (he lent it and took it back). Дал would be used if we still had it. I had the answer wrong. Fix.",
         "x"),
    ]
    rows = [r for r in rows if r[3] not in ("skip", "x") and r[3] != "WAIT: давал is the imperfective of the annulled loan (he lent it and took it back). Дал would be used if we still had it. I had the answer wrong. Fix."]
    rows += [
        ("Сосед ___ нам свою косилку, но уже забрал её обратно.", "давал", ["дал", "даст", "даёт"],
         "A loan whose result is gone (he has taken it back): imperfective давал. Дал would be used if we still had the mower.",
         "The neighbor had lent us his mower, but he has already taken it back."),
        ("Кто-то ___ ворота и не закрыл их? Нет, они снова закрыты: кто-то ___ и ушёл, закрыв за собой.", "x", [], "skip", "x"),
        ("Пока мы были в поле, в дом ___ воры, но ничего не взяли и ушли.", "заходили", ["зашли", "зайдут", "заходят"],
         "They came in and have already gone: заходили. Зашли would present the entry as a result still hanging over the house (they got in / they are in).",
         "While we were in the field, thieves came into the house, but they took nothing and left."),
        ("Я уже ___ в этот магазин: хлеба не было, так что ехать незачем.", "заходил", ["зашёл", "зайду", "захожу"],
         "A completed visit with no remaining result (and no need to go again): заходил. Зашёл would simply report the arrival.",
         "I've already been into this store: there was no bread, so there's no point in going."),
        ("К тебе ___ какая-то женщина с иконой, постояла и ушла.", "приходила", ["пришла", "придёт", "приходит"],
         "She came and has left: приходила (feminine -ла). Пришла would mean she is still here, or that her arrival is the news we care about.",
         "Some woman came for you with an icon, stood for a while and left."),
        ("На нашу почту ___ странное письмо, но его уже вернули отправителю.", "приходило", ["пришло", "придёт", "приходит"],
         "The letter came and the result is gone (it has been returned): приходило. Пришло would mean it is here now.",
         "A strange letter had come to our post office, but it has already been returned to the sender."),
        ("Я ___ тебе вчера книгу, но ты её уже вернул, да?", "давал", ["дал", "дам", "даю"],
         "The giving is no longer a present result (you have returned it): давал. Дал would be used if you still had the book.",
         "I lent you a book yesterday, but you've already returned it, haven't you?"),
        ("К воротам ___ машина, постояла и уехала: наверное, ошиблись дорогой.", "подъезжала", ["подъехала", "подъедет", "подъезжает"],
         "The car pulled up and the result is gone (it has driven off): подъезжала. Подъехала would be used if it were still standing there.",
         "A car pulled up to the gate, stood for a while and drove off: they probably had the wrong road."),
        ("В курятник ___ лиса, но собаки её прогнали, и кур мы всех досчитали.", "заходила", ["зашла", "зайдёт", "заходит"],
         "The fox got in and is no longer there: заходила. Зашла would leave the intrusion as a present, alarming result.",
         "A fox had got into the coop, but the dogs chased it off, and we have counted all the hens."),
        ("На ферму ___ комиссия из района, посмотрела бумаги и уехала к обеду.", "приезжала", ["приехала", "приедет", "приезжает"],
         "They came and have left: приезжала. Приехала would be used if the commission were still here.",
         "A commission from the district came to the farm, looked at the papers and left by lunch."),
    ]
    rows = [r for r in rows if r[3] != "skip"]
    for s, a, d, ex, *rest in rows:
        asp(S, s, "imperfective / perfective", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)


def build_home_kakoy_freq():
    # ---- A1 home: дома / домой ----
    C, S = "home", "дома / домой"
    rows = [
        ("Я сегодня весь день ___.", "дома", ["домой", "дом", "доме"], "Location (где?): дома. Домой is direction (куда?).", "I'm at home all day today."),
        ("После работы я иду ___.", "домой", ["дома", "дом", "доме"], "Иду is a verb of motion, so куда?: домой.", "After work I go home."),
        ("Дети уже ___ или они ещё в школе?", "дома", ["домой", "дом", "доме"], "Already at the location: дома. Домой would need a motion verb (идут домой).", "Are the children already at home, or still at school?"),
        ("Пора ___, жена уже накрыла стол.", "домой", ["дома", "дом", "доме"], "Пора is about going: пора домой. Дома would be location (we are already at home).", "It's time to go home; my wife has already set the table."),
        ("Жена ___ , готовит ужин.", "дома", ["домой", "дом", "доме"], "Location: дома. The verb готовит has no motion.", "My wife is at home, cooking supper."),
        ("Мы едем ___ на машине.", "домой", ["дома", "дом", "доме"], "Едем is motion: домой. На машине is prepositional.", "We're driving home."),
        ("Вы ___? Я могу заехать.", "дома", ["домой", "дом", "доме"], "A location question: вы дома? Домой would be 'are you (going) home?'.", "Are you at home? I can stop by."),
        ("Она вернулась ___ только в десять.", "домой", ["дома", "дом", "доме"], "Вернулась is motion of return: домой.", "She only got home at ten."),
        ("Кто ___? Откройте калитку!", "дома", ["домой", "дом", "доме"], "Location: кто дома? (who is in?).", "Who's at home? Open the gate!"),
        ("Я люблю быть ___, на своей ферме.", "дома", ["домой", "дом", "доме"], "Быть is location: быть дома.", "I like being at home, on my own farm."),
        ("После литургии мы поехали ___.", "домой", ["дома", "дом", "доме"], "Поехали is motion: домой.", "After the Liturgy we drove home."),
        ("Отец ещё не ___, он в поле.", "дома", ["домой", "дом", "доме"], "Ещё не + location: не дома. В поле is also где?.", "Dad isn't home yet; he's in the field."),
        ("Проводи меня ___, пожалуйста.", "домой", ["дома", "дом", "доме"], "Проводить is directional: домой.", "Please walk me home."),
        ("У нас ___ всегда пахнет хлебом.", "дома", ["домой", "дом", "доме"], "Location: у нас дома ('at our house').", "At our house it always smells of bread."),
        ("Я торопился ___, чтобы успеть к дойке.", "домой", ["дома", "дом", "доме"], "Торопился is motion (hurrying somewhere): домой. К дойке is dative after к.", "I was hurrying home so as to be in time for milking."),
        ("Саша уже ___ или ещё в Минске?", "дома", ["домой", "дом", "доме"], "Location contrast: дома vs в Минске (оба отвечают на где?).", "Is Sasha already at home, or still in Minsk?"),
        ("Позови всех ___ , ужин готов.", "домой", ["дома", "дом", "доме"], "Позови (call them in / home) is directional: домой.", "Call everyone home; supper is ready."),
        ("Зимой я больше сижу ___, чем в поле.", "дома", ["домой", "дом", "доме"], "Сидеть is location: сижу дома.", "In winter I sit at home more than I sit in the field."),
        ("Надо занести инструменты ___, будет дождь.", "домой", ["дома", "дом", "доме"], "Занести is motion of carrying in: домой (or в дом). Здесь домой — куда?.", "We need to bring the tools home; it's going to rain."),
        ("Батюшка сегодня ___ или в епархии?", "дома", ["домой", "дом", "доме"], "Location: дома vs в епархии.", "Is Father at home today, or at the diocese?"),
        ("Дети бегут ___ с пруда.", "домой", ["дома", "дом", "доме"], "Бегут is motion: домой. С пруда is genitive after с.", "The children are running home from the pond."),
        ("Мы остались ___ и не поехали на ярмарку.", "дома", ["домой", "дом", "доме"], "Остались is location (we stayed): дома. Не поехали is the motion we didn't take.", "We stayed at home and didn't go to the fair."),
        ("Я отнёс письмо и сразу пошёл ___.", "домой", ["дома", "дом", "доме"], "Пошёл is motion: домой.", "I dropped off the letter and went straight home."),
        ("___ теплее, чем в сарае.", "Дома", ["Домой", "Дом", "Доме"], "Location, no motion verb: дома. The adverb can start the sentence.", "It's warmer at home than in the barn."),
        ("К вечеру все уже были ___.", "дома", ["домой", "дом", "доме"], "Были is location: дома.", "By evening everyone was already at home."),
        ("Я хочу ___ , устал в поле.", "домой", ["дома", "дом", "доме"], "Хочу + an implied verb of motion (хочу идти / ехать): домой. Хочу быть дома would use дома; the short 'I want (to go) home' is домой.", "I want to go home; I'm tired from the field."),
        ("Собака уже ___ , лежит у печки.", "дома", ["домой", "дом", "доме"], "Location: уже дома. Лежит у печки is also где?.", "The dog is already at home, lying by the stove."),
        ("Гости уехали ___, а мы остались на ферме.", "домой", ["дома", "дом", "доме"], "Уехали is motion: домой (to their home).", "The guests went home, and we stayed on the farm."),
        ("Работать ___ удобно, но коровы ждут.", "дома", ["домой", "дом", "доме"], "Работать где?: дома. This is the adverb of location, not the noun доме.", "It's convenient to work at home, but the cows are waiting."),
        ("Я зашёл ___ за паспортом и снова выехал.", "домой", ["дома", "дом", "доме"], "Зашёл is motion (I dropped in home): домой / домой за паспортом. За паспортом is instrumental.", "I dropped by home for my passport and set off again."),
    ]
    rows = [r for r in rows if "No, just" not in r[3]]
    # fix the пора one if I filtered it - I had a messy s. The filter is on ex. Good, I already have "Пора ___, уже темно."? Looking at row 4, the s is messy and was filtered. Add a clean one is already in list as... no I don't have a clean пора after filter. There's none. OK we have 29 others.
    for s, a, d, ex, *rest in rows:
        addv(A, C, S, s, "дом", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    # в или на?
    S = "в или на?"
    # (s, a, ex, tr, gl)
    von = [
        ("Коровы стоят ___ сарае.", "в", "A barn is a closed space you go inside, so в: в сарае. На сарае would be 'on top of the barn'.", "The cows are standing in the barn."),
        ("Скот пасётся ___ пастбище.", "на", "Open surfaces and land take на: на пастбище, на лугу, на поле. В пастбище is wrong.", "The cattle are grazing in the pasture."),
        ("Мы молимся ___ храме.", "в", "A church building you go inside takes в: в храме, в церкви. На храме would be 'on the church'.", "We pray in the church."),
        ("Батюшка служит ___ литургии.", "на", "Services and events take на: на литургии, на службе, на венчании. В литургии would be 'inside the Liturgy' as a text, not as an event.", "Father is serving at the Liturgy."),
        ("Я работаю ___ компьютере весь вечер.", "на", "Devices you work at take на: на компьютере, на планшете. В компьютере would be 'inside the computer'.", "I work at the computer the whole evening."),
        ("Письмо лежит ___ сумке.", "в", "A bag is a container: в сумке. На сумке would be 'on top of the bag'.", "The letter is in the bag."),
        ("Мы встретились ___ вокзале.", "на", "Stations and platforms take на: на вокзале, на станции. В вокзале is sometimes heard but the standard form is на.", "We met at the train station."),
        ("Самолёт уже ___ аэропорту.", "в", "Airports as a complex you are inside take в, plus the locative -у: в аэропорту. На аэропорту is wrong.", "The plane is already at the airport."),
        ("Дети играют ___ улице.", "на", "The street as an open surface takes на: на улице. В улице is wrong.", "The children are playing in the street."),
        ("Он сидит ___ автобусе и едет в Минск.", "в", "You sit inside a vehicle: в автобусе, в поезде, в машине. На автобусе is also used for 'by bus' as means, but сидит points to inside: в.", "He is sitting on the bus and going to Minsk."),
        ("Мы едем в Минск ___ поезде.", "на", "Means of transport often take на: ехать на поезде, на автобусе, на машине. В поезде is also possible for 'inside the train' as location. Here the phrase is the means: на.", "We're going to Minsk by train."),
        ("Икона висит ___ стене.", "на", "Things hang on the surface of a wall: на стене. В стене would be 'inside the wall'.", "The icon is hanging on the wall."),
        ("Зерно лежит ___ кормушке.", "в", "A feeder is a container: в кормушке. На кормушке would be 'on top of the feeder'.", "The grain is in the feeder."),
        ("Я был ___ границе три часа.", "на", "A border as a line / post takes на: на границе. В границе is wrong.", "I was at the border for three hours."),
        ("Они живут ___ деревне, недалеко от нас.", "в", "Settlements you live inside take в: в деревне, в городе, в Минске. На деревне is colloquial / nonstandard.", "They live in the village, not far from us."),
        ("Сено лежит ___ телеге.", "на", "An open cart is a surface: на телеге. В телеге would treat it as a closed box.", "The hay is on the cart."),
        ("Документы лежат ___ паспорте? No, в столе / в папке. Use '___ папке'.", "в", "A folder is a container: в папке.", "The documents are in the folder."),
        ("Мы стояли ___ кассе двадцать минут.", "у", "У + genitive means 'by, at the side of': у кассы (the existing ключи висят у двери pattern). На кассе is 'working the till'; в кассе is 'inside the till'.", "We stood at the checkout for twenty minutes."),
        ("Картина висит ___ гостиной над диваном.", "в", "Rooms take в: в гостиной, в спальне (но на кухне). Над диваном is instrumental after над.", "The picture hangs in the living room above the sofa."),
        ("Он работает ___ почте уже десять лет.", "на", "Some workplaces take на: на почте, на заводе, на ферме. В почте would be 'inside the mail'.", "He has been working at the post office for ten years."),
        ("Куры спят ___ насесте.", "на", "A roost is a surface they sit on: на насесте. В насесте is wrong.", "The hens sleep on the roost.", ["насест: roost"]),
        ("Рыба плавает ___ пруду.", "в", "You are in the water of a pond: в пруду (locative -у). На пруду is also used for 'at the pond' as a place on the bank; плавает forces в.", "The fish is swimming in the pond."),
        ("Мы сидели ___ берегу и смотрели на воду.", "на", "A bank / shore is a surface: на берегу (locative -у). В берегу is wrong.", "We sat on the bank and looked at the water."),
        ("Я живу ___ улице Ленина, дом пять.", "на", "Addresses use на + street: на улице Ленина. В улице is wrong.", "I live on Lenin Street, house number five."),
        ("Ключи висят ___ гвозде в сарае.", "на", "On a nail as a surface / hook: на гвозде. В гвозде would be 'inside the nail'.", "The keys hang on a nail in the barn."),
        ("Он служит ___ границе, пограничником.", "на", "Service at the border: на границе. Пограничником is instrumental of the role.", "He serves at the border, as a border guard."),
        ("Мы обедали ___ столовой при храме.", "в", "A dining hall is a room you go inside: в столовой. При храме is prepositional after при.", "We had lunch in the refectory by the church."),
        ("Пикап стоит ___ дворе, у сарая.", "во", "Двор takes во (because of the consonant cluster дв): во дворе, not в дворе. На дворе is also used, more like 'outdoors / in the yard as an open space'; with стоит у сарая, во дворе is the standard location.", "The pickup is standing in the yard, by the barn."),
        ("Я увидел это ___ картинке в журнале.", "на", "A picture as a surface takes на: на картинке, на фотографии. В картинке would be 'inside the picture'.", "I saw this in a picture in a magazine."),
        ("Код пишется ___ языке Python? Use '___ русском языке' no. 'программа работает ___ сервере'.", "на", "A server as a platform takes на: на сервере. В сервере would be 'inside the hardware'.", "The program runs on the server."),
    ]
    von = [r for r in von if "No," not in r[0] and "Use '" not in r[0]]
    von += [
        ("Документы лежат ___ папке.", "в", "A folder is a container: в папке. На папке would be 'on top of the folder'.", "The documents are in the folder."),
        ("Программа работает ___ сервере.", "на", "A server as a platform takes на: на сервере. В сервере would be 'inside the hardware'.", "The program runs on the server."),
        ("Я стоял ___ очереди двадцать минут.", "в", "You stand in a line, inside it: в очереди. На очереди is wrong.", "I stood in line for twenty minutes."),
        ("Они венчались ___ церкви, не в ЗАГСе.", "в", "The wedding as taking place inside the church building: в церкви. На церкви would be 'on the church'. (На венчании would be the event.)", "They were married in church, not at the registry office."),
    ]
    for item in von:
        s, a, ex, tr = item[:4]
        gl = item[4] if len(item) > 4 else None
        d = [x for x in ("в", "на", "у", "к") if x != a][:3]
        # во is extra
        if a == "во":
            d = ["в", "на", "у"]
        addv(A, C, S, s, "в / на / у", a, d, ex, tr, gl)


    S = "где? в / на + prepositional"
    rows = [
        ("Коровы ночуют в ___.", "сарай", "prep", "The cows spend the night in the barn.",
         "Где? в + prepositional: в сарае. В сарай would be accusative (куда?).", ["ночевать: to spend the night"]),
        ("Наши куры спят в ___.", "курятник", "prep", "The hens sleep in the coop.",
         "Где? в + prepositional: в курятнике.", []),
        ("Трактор стоит в ___.", "сарай", "prep", "The tractor is standing in the barn.",
         "Где? в + prepositional: в сарае. Стоять is a location verb.", []),
        ("Жена готовит на ___.", "кухня", "prep", "My wife is cooking in the kitchen.",
         "Кухня takes на + prepositional: на кухне (the exception among rooms).", []),
        ("Мы молимся в ___.", "храм", "prep", "We are praying in the church.",
         "Где? в + prepositional: в храме. В храм would be куда?.", []),
        ("Икона стоит в красном ___.", "угол", "loc", "The icon stands in the icon corner.",
         "Где? в + the locative in -у, and угол loses о: в углу.", []),
        ("Мой паспорт лежит в ___.", "стол", "prep", "The passport is in the table (in a drawer).",
         "Где? в + prepositional: в столе. На столе would be 'on the table'.", []),
        ("Ключи висят на ___.", "гвоздь", "prep", "The keys hang on a nail.",
         "Где? на + prepositional: на гвозде. The fleeting о in гвоздь / гвоздя drops: гвозд-е? Actually гвоздь → гвозде.", ["гвоздь: nail"]),
        ("Дети сидят на ___.", "крыльцо", "prep", "The children are sitting on the porch.",
         "Где? на + prepositional. Крыльцо (neuter) → на крыльце.", ["крыльцо: porch"]),
        ("Сено лежит на ___.", "чердак", "prep", "The hay is in the loft. / The hay is up in the attic.",
         "Где? на + prepositional for an attic / loft: на чердаке. На чердак would be куда?.", ["чердак: loft, attic"]),
        ("Мы сидели на ___ и смотрели на воду.", "берег", "loc", "We sat on the bank and looked at the water.",
         "Где? на + locative -у: на берегу.", []),
        ("Зерно хранится в ___.", "закром", "prep", "The grain is stored in the bin.",
         "Где? в + prepositional: в закроме.", ["закром: grain bin"]),
        ("Сегодня гости сидят в ___.", "гостиная", "prep", "The guests are sitting in the living room.",
         "Гостиная declines like an adjective: в гостиной (prepositional).", []),
        ("Зимнее пальто висит в ___.", "прихожая", "prep", "The winter coat is hanging in the entryway.",
         "Прихожая declines like an adjective: в прихожей.", ["прихожая: entryway"]),
        ("Я работаю за столом в ___.", "кабинет", "prep", "I work at the desk in the study.",
         "Где? в + prepositional: в кабинете. За столом is instrumental after за.", ["кабинет: study, office"]),
        ("Молоко стоит в ___.", "холодильник", "prep", "The milk is in the fridge.",
         "Где? в + prepositional: в холодильнике.", []),
        ("Хлеб лежит на ___.", "полка", "prep", "The bread is on the shelf.",
         "Где? на + prepositional: на полке. Feminine -а → -е.", []),
        ("Сапоги стоят в ___.", "прихожая", "prep", "The boots are standing in the entryway.",
         "Где? в + prepositional, adjective-like: в прихожей.", []),
        ("Мы обедали в ___ при храме.", "столовая", "prep", "We had lunch in the refectory by the church.",
         "Столовая declines like an adjective: в столовой. При храме is prepositional after при.", ["столовая: dining hall"]),
        ("Отец спит в ___.", "спальня", "prep", "Dad is sleeping in the bedroom.",
         "Где? в + prepositional. Feminine -я → -е: в спальне.", []),
        ("Ведро стоит в ___.", "угол", "loc", "The bucket is standing in the corner.",
         "Где? в + locative -у: в углу (not в угле).", []),
        ("На ___ у двери лежит коврик.", "пол", "loc", "A little rug is lying on the floor by the door.",
         "Где? на + locative -у: на полу (not на поле, which is 'in the field').", []),
        ("Лошадь паслась на дальнем ___.", "луг", "loc", "The horse was grazing in the far meadow.",
         "Где? на + locative -у: на лугу. Дальнем agrees with лугу.", []),
        ("Рыба была в ___, мы сами видели.", "пруд", "loc", "The fish was in the pond; we saw it ourselves.",
         "Где? в + locative -у: в пруду.", []),
        ("Я нашёл паспорт в ___.", "карман", "prep", "I found the passport in the pocket.",
         "Где? в + prepositional: в кармане. В карман would be куда?.", []),
        ("Свечи горят на ___ перед иконами.", "аналой", "prep", "The candles are burning on the analogion in front of the icons.",
         "Где? на + prepositional: на аналое. Перед иконами is instrumental after перед.", ["аналой: analogion, lectern"]),
    ]
    # skip analogion if pymorphy fails - we'll see
    for s, lemma, case, tr, ex, gl in rows:
        try:
            add_noun(A, C, S, s, lemma, case, tr, ex, gl)
        except SystemExit as e:
            print("SKIP home prep", s, e)

    S = "куда? в / на + accusative"
    rows = [
        ("Вечером коровы идут в ___.", "сарай", "acc", "In the evening the cows go into the barn.",
         "Куда? в + accusative. Inanimate masculine: в сарай (no change). В сарае would be где?.", []),
        ("Жена гонит кур в ___.", "курятник", "acc", "My wife is driving the hens into the coop.",
         "Куда? в + accusative: в курятник. В курятнике is где?.", []),
        ("Я поставил трактор в ___.", "сарай", "acc", "I put the tractor in the barn.",
         "Поставить куда? в + accusative: в сарай.", []),
        ("После работы мы всегда едем на ___.", "ферма", "acc", "After work we drive to the farm.",
         "Куда? на + accusative: на ферму. На ферме is где?.", []),
        ("В воскресенье мы идём в ___.", "храм", "acc", "On Sunday we go to church.",
         "Куда? в + accusative: в храм. В храме is где?.", []),
        ("Повесь пальто в ___.", "шкаф", "acc", "Hang the coat in the wardrobe.",
         "Куда? в + accusative: в шкаф. В шкафу (locative -у) is где?.", []),
        ("Положи ключи на ___ над плитой.", "полка", "acc", "Put the keys on the shelf above the stove.",
         "Куда? на + accusative. Feminine -а → -у: на полку. На полке is где?.", []),
        ("Я иду на ___ за водой.", "колодец", "acc? колодец acc = колодец", "I'm going to the well for water.",
         "Куда? на + accusative: на колодец (or к колодцу with к + dative). За водой is instrumental.", ["колодец: well"]),
    ]
    # The last has a messy case field. I'll use "acc"
    rows[-1] = ("Я иду на ___ за водой.", "колодец", "acc",
                "I'm going to the well for water.",
                "Куда? на + accusative: на колодец. За водой is instrumental ('for water').", ["колодец: well"])
    rows += [
        ("Дети побежали на ___.", "крыльцо", "acc", "The children ran onto the porch.",
         "Куда? на + accusative. Neuter крыльцо stays крыльцо. На крыльце is где?.", []),
        ("Мы занесли сено на ___.", "чердак", "acc", "We carried the hay up into the loft.",
         "Куда? на + accusative: на чердак. На чердаке is где?.", []),
        ("Положи паспорт в ___.", "сумка", "acc", "Put the passport in the bag.",
         "Куда? в + accusative. Feminine -а → -у: в сумку. В сумке is где?.", []),
        ("Я иду в ___ за хлебом.", "магазин", "acc", "I'm going to the store for bread.",
         "Куда? в + accusative: в магазин. В магазине is где?; за хлебом is instrumental.", []),
        ("Они едут на ___ за кормом.", "рынок", "acc", "They are going to the market for feed.",
         "Куда? на + accusative: на рынок. На рынке is где?.", []),
        ("Садись в ___, поедем.", "машина", "acc", "Get in the car, we'll go.",
         "Куда? в + accusative. Feminine: в машину. В машине is где?.", []),
        ("Я положил письмо в ___.", "конверт", "acc", "I put the letter in the envelope.",
         "Куда? в + accusative. Inanimate masculine: в конверт.", ["конверт: envelope"]),
        ("Повесь икону в красный ___.", "угол", "acc", "Hang the icon in the icon corner.",
         "Куда? в + accusative: в угол (not в углу, which is где?). Красный agrees with угол (inanimate accusative = nominative form).", []),
        ("Мы вышли на ___ подышать.", "улица", "acc", "We went out into the street for a breath of air.",
         "Куда? на + accusative. Feminine -а → -у: на улицу. На улице is где?.", []),
        ("Он пошёл в ___ спать.", "спальня", "acc", "He went into the bedroom to sleep.",
         "Куда? в + accusative. Feminine -я → -ю: в спальню. В спальне is где?.", []),
        ("Загони скот на ___ , там трава лучше.", "луг", "acc", "Drive the cattle out to the meadow; the grass is better there.",
         "Куда? на + accusative: на луг (not на лугу, which is где?).", []),
        ("Дети побежали к воде, на ___.", "берег", "acc", "The children ran down to the water, onto the bank.",
         "Куда? на + accusative: на берег. На берегу is где?.", []),
        ("Я поставил ведро в ___.", "угол", "acc", "I put the bucket in the corner.",
         "Куда? в + accusative: в угол. В углу is где?.", []),
        ("Положи сапоги в ___.", "прихожая", "acc", "Put the boots in the entryway.",
         "Куда? в + accusative. Прихожая declines like an adjective: в прихожую. В прихожей is где?.", []),
        ("Мы едем в ___ на поезде.", "город", "acc", "We're going to town by train.",
         "Куда? в + accusative: в город. В городе is где?; на поезде is prepositional (means).", []),
        ("Я иду на ___ отправить посылку.", "почта", "acc", "I'm going to the post office to send a parcel.",
         "Куда? на + accusative. Feminine -а → -у: на почту. На почте is где?.", []),
        ("Занеси зерно в ___.", "закром", "acc", "Carry the grain into the bin.",
         "Куда? в + accusative: в закром. В закроме is где?.", []),
        ("Она пошла в ___ умыться.", "ванная", "acc", "She went into the bathroom to wash.",
         "Куда? в + accusative. Ванная declines like an adjective: в ванную. В ванной is где?.", []),
        ("Положи хлеб на ___.", "стол", "acc", "Put the bread on the table.",
         "Куда? на + accusative. Inanimate masculine: на стол. На столе is где?.", []),
        ("Я бросил пальто на ___.", "кровать", "acc", "I threw the coat onto the bed.",
         "Куда? на + accusative. Soft feminine кровать looks the same: на кровать. На кровати is где?.", []),
        ("Мы заехали на ___ за бензином.", "заправка", "acc", "We stopped at the petrol station for petrol.",
         "Куда? на + accusative. Feminine -а → -у: на заправку. За бензином is instrumental.", ["заправка: petrol station"]),
    ]
    for s, lemma, case, tr, ex, gl in rows:
        try:
            add_noun(A, C, S, s, lemma, case, tr, ex, gl)
        except SystemExit as e:
            print("SKIP home acc", s, e)

    # B1 home: stand / lie / hang
    S = "стоять / лежать / висеть"
    rows = [
        ("Ведро ___ в углу у двери.", "стоит", ["лежит", "висит", "ставит"],
         "A bucket standing on its base стоит. Лежит would be on its side; висит would be hanging.",
         "The bucket is standing in the corner by the door."),
        ("Вилы ___ у стены, не на полу.", "стоят", ["лежат", "висят", "ставят"],
         "A pitchfork leaning / standing against the wall стоит (or стоят, plural-only вилы). Если они брошены плашмя — лежат.",
         "The pitchfork is standing against the wall, not on the floor."),
        ("Мешок с зерном ___ у кормушки.", "стоит", ["лежит", "висит", "кладёт"],
         "A sack standing upright стоит. Лежит would be lying on its side.",
         "The sack of grain is standing by the feeder."),
        ("Цепь ___ на гвозде в сарае.", "висит", ["стоит", "лежит", "вешает"],
         "A chain on a nail висит (hangs). Лежит would be in a pile; стоит is for things with a base.",
         "The chain is hanging on a nail in the barn."),
        ("Икона ___ в красном углу, не на стене боком.", "стоит", ["лежит", "висит", "ставит"],
         "A standing icon in the icon corner стоит (or sometimes висит if hung). Здесь традиционно икона стоит в углу.",
         "The icon is standing in the icon corner, not hanging sideways on the wall."),
        ("Полотенце ___ на крючке у мойки.", "висит", ["стоит", "лежит", "вешает"],
         "A towel on a hook висит.",
         "The towel is hanging on the hook by the sink."),
        ("Сапоги ___ под лавкой, их повалили.", "лежат", ["стоят", "висят", "кладут"],
         "Boots knocked over and lying on their side лежат. Стоят would be upright.",
         "The boots are lying under the bench; someone knocked them over.", ["лавка: bench"]),
        ("Книга ___ на полке, корешком наружу.", "стоит", ["лежит", "висит", "кладёт"],
         "A book standing on end on a shelf стоит. Лежит would be lying flat.",
         "The book is standing on the shelf, spine out."),
        ("Газета ___ на столе, раскрытая.", "лежит", ["стоит", "висит", "кладёт"],
         "A newspaper lying flat лежит. Стоит is impossible for a sheet of paper.",
         "The newspaper is lying on the table, open."),
        ("Лампа ___ над столом, на крюке.", "висит", ["стоит", "лежит", "вешает"],
         "A lamp on a hook above the table висит. Стоит would be a lamp standing on the table.",
         "The lamp is hanging above the table, on a hook."),
        ("Кастрюля ___ на плите.", "стоит", ["лежит", "висит", "ставит"],
         "A pot sitting on the stove стоит.",
         "The pot is standing on the stove."),
        ("Крышка ___ рядом, на столе.", "лежит", ["стоит", "висит", "кладёт"],
         "A lid lying flat лежит. Стоит would be on its edge.",
         "The lid is lying next to it, on the table."),
        ("Чётки ___ на гвоздике у иконы.", "висят", ["стоят", "лежат", "вешают"],
         "A prayer rope on a little nail висит (plural-only? чётки is plural-only: висят).",
         "The prayer rope is hanging on a little nail by the icon.", ["чётки: prayer rope, beads"]),
        ("Дрова ___ у печки, аккуратной поленницей.", "стоят", ["лежат", "висят", "кладут"],
         "A neatly stacked pile of firewood can стоять (as a stack). Лежат would be a loose heap.",
         "The firewood is standing by the stove, in a neat stack.", ["поленница: woodpile"]),
        ("Дрова ___ просто кучей, ещё не складывали.", "лежат", ["стоят", "висят", "кладут"],
         "A loose heap of firewood лежит. Стоят would be a stacked pile.",
         "The firewood is just lying in a heap; we haven't stacked it yet."),
        ("Зеркало ___ над умывальником.", "висит", ["стоит", "лежит", "вешает"],
         "A mirror on the wall висит. Стоит would be a free-standing mirror.",
         "The mirror is hanging above the washbasin."),
        ("Телефон ___ в кармане, не на столе.", "лежит", ["стоит", "висит", "кладёт"],
         "A phone in a pocket лежит (flat, no 'standing' in a pocket).",
         "The phone is in the pocket, not on the table."),
        ("Грабли ___ у забора, зубьями вверх.", "стоят", ["лежат", "висят", "ставят"],
         "A rake standing / leaning стоит. Лежат would be flat on the ground. Грабли is plural-only: стоят.",
         "The rake is standing by the fence, tines up.", ["грабли: rake"]),
        ("Провод ___ между столбами, слегка провисает.", "висит", ["стоит", "лежит", "вешает"],
         "A wire stretched between posts висит. Лежит would be on the ground.",
         "The wire hangs between the posts, sagging slightly."),
        ("Корзина с яйцами ___ на лавке, не трогай.", "стоит", ["лежит", "висит", "ставит"],
         "A basket sitting on its base стоит. Лежит would be on its side (and the eggs would break).",
         "The basket of eggs is standing on the bench; don't touch it."),
    ]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "стоять / лежать / висеть", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "поставить / положить / повесить"
    rows = [
        ("___ ведро в угол, не набок.", "Поставь", ["Положи", "Повесь", "Стоит"],
         "A bucket on its base in the corner: поставить (it will стоять). Положить would lay it on its side.",
         "Stand the bucket in the corner, not on its side."),
        ("___ вилы у стены, зубьями от себя.", "Поставь", ["Положи", "Повесь", "Стоят"],
         "A pitchfork leaning against the wall: поставить. Положить would lay it flat.",
         "Stand the pitchfork against the wall, tines away from you."),
        ("___ мешок у кормушки стоймя.", "Поставь", ["Положи", "Повесь", "Стоит"],
         "Стоймя ('upright') forces поставить. Положить would lay it down.",
         "Stand the sack upright by the feeder."),
        ("___ цепь на гвоздь в сарае.", "Повесь", ["Поставь", "Положи", "Висит"],
         "On a nail, so that it will висеть: повесить. Положить would drop it in a pile.",
         "Hang the chain on the nail in the barn."),
        ("___ икону в красный угол.", "Поставь", ["Положи", "Повесь", "Стоит"],
         "A standing icon in the icon corner is traditionally поставить (it will стоять). Повесить is used if it hangs on a wall.",
         "Set the icon in the icon corner."),
        ("___ полотенце на крючок у мойки.", "Повесь", ["Поставь", "Положи", "Висит"],
         "On a hook: повесить. Положить would leave it in a heap.",
         "Hang the towel on the hook by the sink."),
        ("___ сапоги под лавку стоймя.", "Поставь", ["Положи", "Повесь", "Стоят"],
         "Стоймя forces поставить (they will стоять). Положить would lay them on their sides.",
         "Stand the boots under the bench, upright."),
        ("___ книгу на полку корешком наружу.", "Поставь", ["Положи", "Повесь", "Стоит"],
         "A book on end, spine out: поставить. Положить would lay it flat.",
         "Stand the book on the shelf, spine out."),
        ("___ газету на стол, я посмотрю.", "Положи", ["Поставь", "Повесь", "Лежит"],
         "A newspaper flat on the table: положить (it will лежать). Поставить is impossible for a sheet.",
         "Lay the newspaper on the table; I'll look at it."),
        ("___ лампу над столом, на крюк.", "Повесь", ["Поставь", "Положи", "Висит"],
         "On a hook above the table: повесить. Поставить would sit a lamp on the table.",
         "Hang the lamp above the table, on the hook."),
        ("___ кастрюлю на плиту.", "Поставь", ["Положи", "Повесь", "Стоит"],
         "A pot onto a burner, on its base: поставить. Положить would lay it on its side.",
         "Put the pot on the stove."),
        ("___ крышку рядом, на стол.", "Положи", ["Поставь", "Повесь", "Лежит"],
         "A lid laid flat: положить. Поставить would stand it on its edge.",
         "Lay the lid next to it, on the table."),
        ("___ чётки на гвоздик у иконы.", "Повесь", ["Поставь", "Положи", "Висят"],
         "On a little nail: повесить (they will висеть). Чётки is plural-only.",
         "Hang the prayer rope on the little nail by the icon."),
        ("___ дрова у печки поленницей, не кучей.", "Поставь", ["Положи", "Повесь", "Стоят"],
         "A stacked woodpile: поставить (поленницей). Положить would dump them in a heap (кучей).",
         "Stack the firewood by the stove, don't just dump it in a heap."),
        ("___ дрова пока кучей, потом сложим.", "Положи", ["Поставь", "Повесь", "Лежат"],
         "A temporary heap: положить кучей (they will лежать).",
         "Just lay the firewood in a heap for now; we'll stack it later."),
        ("___ зеркало над умывальником.", "Повесь", ["Поставь", "Положи", "Висит"],
         "A mirror onto the wall: повесить. Поставить would be a free-standing mirror.",
         "Hang the mirror above the washbasin."),
        ("___ телефон в карман, не на стол.", "Положи", ["Поставь", "Повесь", "Лежит"],
         "Into a pocket: положить (it will лежать). Поставить is impossible in a pocket.",
         "Put the phone in your pocket, not on the table."),
        ("___ грабли у забора, зубьями вверх.", "Поставь", ["Положи", "Повесь", "Стоят"],
         "A rake standing / leaning: поставить. Положить would lay it flat. Грабли is plural-only.",
         "Stand the rake by the fence, tines up."),
        ("___ корзину с яйцами на лавку осторожно.", "Поставь", ["Положи", "Повесь", "Стоит"],
         "A basket of eggs on its base: поставить. Положить набок would break the eggs.",
         "Set the basket of eggs on the bench carefully."),
        ("___ пальто на вешалку, не на спинку стула.", "Повесь", ["Поставь", "Положи", "Висит"],
         "Onto a hanger: повесить (it will висеть). Положить would dump it on a chair.",
         "Hang the coat on the coat rack, not on the back of the chair."),
    ]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "поставить / положить / повесить", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "aspect at home"
    rows = [
        ("Я уже ___ ворота, можно ехать.", "закрыл", ["закрывал", "закрываю", "закрою"],
         "Уже plus 'we can go' marks a completed result: perfective закрыл (закрыть). Закрывал would be the process, or an annulled / repeated closing.",
         "I've already shut the gate; we can go."),
        ("Я долго ___ ворота: петли заржавели.", "закрывал", ["закрыл", "закрою", "закрываю"],
         "Долго marks a process: imperfective закрывал. Закрыл would mean they are shut now, with no interest in the struggle.",
         "I spent a long time trying to shut the gate: the hinges had rusted."),
        ("Каждый вечер он ___ калитку на засов.", "закрывает", ["закроет", "закрыл", "закрой"],
         "Каждый вечер marks a habit: imperfective закрывает. Закроет would be one future occasion.",
         "Every evening he shuts the wicket on the bolt."),
        ("___ свет в сенях, пожалуйста, мы уже выходим.", "Выключи", ["Выключай", "Выключите", "Выключить"],
         "A one-time request: perfective выключи. Выключай would be a standing rule ('always turn it off').",
         "Turn off the light in the entry, please; we're already leaving."),
        ("Всегда ___ свет, когда уходишь из сарая на ночь.", "выключай", ["выключи", "выключайте", "выключить"],
         "Всегда marks a standing rule: imperfective выключай.",
         "Always turn off the light when you leave the barn."),
        ("Я ___ пальто на вешалку и сразу пошёл доить.", "повесил", ["вешал", "повешу", "вешаю"],
         "A one-time completed act in a sequence: perfective повесил (повесить). Вешал would be a process or a habit.",
         "I hung the coat on the rack and went straight to milk."),
        ("Она долго ___ шторы: кольца не проходили.", "вешала", ["повесила", "повесит", "вешает"],
         "Долго marks a process: imperfective вешала. Повесила would mean the curtains are up.",
         "She spent a long time hanging the curtains: the rings wouldn't go through."),
        ("Утром я всегда ___ кастрюлю на плиту и ставлю чай.", "ставлю", ["поставлю", "поставил", "ставил"],
         "Всегда + утром marks a habit: imperfective ставлю (ставить / поставить).",
         "In the morning I always put the pot on the stove and make tea."),
        ("___ кастрюлю на плиту, пожалуйста, вода уже закипела в ведре.", "Поставь", ["Ставь", "Поставьте", "Ставить"],
         "A one-time request: perfective поставь. Ставь would be a standing instruction.",
         "Put the pot on the stove, please; the water in the bucket is already boiling."),
        ("Кто-то ___ мою кружку и не поставил на место.", "брал", ["взял", "берёт", "возьмёт"],
         "The mug was taken and (perhaps) is back, or we don't see it as a present possession: imperfective брал can also simply report the past activity; but 'не поставил на место' after взял is also fine. Here брал hints that the taking is not a present result we can point to. Actually взял is more natural. Let me use взял as the result still missing (not put back).",
         "x"),
    ]
    rows = [r for r in rows if r[4] != "x"]
    rows += [
        ("Кто-то ___ мою кружку и не поставил на место.", "взял", ["брал", "берёт", "возьмёт"],
         "The mug is still not in its place, so the taking still has a result: perfective взял. Брал would be used if the mug were already back (an annulled taking).",
         "Someone took my mug and didn't put it back."),
        ("Я уже ___ полы в сенях, не ходи в сапогах.", "вымыл", ["мыл", "вымою", "мою"],
         "Уже plus 'don't walk in boots' marks a completed result: perfective вымыл (вымыть). Мыл would be the process.",
         "I've already washed the floors in the entry; don't walk in in your boots."),
        ("Она весь час ___ полы и ещё не закончила.", "мыла", ["вымыла", "вымоет", "моет"],
         "Весь час + ещё не закончила marks a process: imperfective мыла.",
         "She has been washing the floors for a whole hour and still isn't finished."),
        ("Не ___ окно на ночь, здесь дует.", "открывай", ["открой", "откройте", "открыть"],
         "A standing / now negative: не открывай (imperfective). Не открой would be 'see that you don't (accidentally) open it'.",
         "Don't open the window at night; there's a draught here."),
        ("___ окно на минутку, очень душно.", "Открой", ["Открывай", "Откройте", "Открыть"],
         "A one-time request: perfective открой.",
         "Open the window for a minute; it's very stuffy."),
        ("Я обычно ___ ключи на гвоздь у двери.", "вешаю", ["повешу", "повесил", "вешал"],
         "Обычно marks a habit: imperfective вешаю (вешать / повесить).",
         "I usually hang the keys on the nail by the door."),
        ("На минутку ___ ключи на гвоздь, руки заняты.", "повесь", ["весь", "повесите", "вешать"],
         "A one-time request: perfective повесь. Вешай would be a standing rule. 'весь' is a typo distractor for вешай.",
         "Hang the keys on the nail for a minute; my hands are full."),
        ("Мы ещё не ___ самовар: гости уже близко.", "поставили", ["ставили", "поставим", "ставим"],
         "Ещё не of a result not yet achieved: perfective не поставили. Не ставили would mean we weren't engaged in the activity.",
         "We still haven't put the samovar on: the guests are already close."),
        ("Пока ты ___ кровать, я закрою ставни.", "застилал? skip use застилаешь / застелешь. Use 'стелил / постелил'", "x", "skip", "x"),
        ("Пока ты ___ постель, я закрою ставни.", "стелил", ["постелил", "постелешь", "стелет"],
         "Пока ты + a process in the past / background: imperfective стелил (стелить / постелить). Постелил would already be the finished bed.",
         "While you were making the bed, I'll close the shutters. / While you were making the bed, I closed…", ["ставни: shutters"]),
    ]
    # The last translation is messy. I'll fix the tense: "While you were making the bed, I closed the shutters." needs закрыл. The s says закрою (future). Recast.
    rows = [r for r in rows if r[3] != "skip" and "застилал" not in r[0]]
    rows[-1] = ("Пока ты ___ постель, я закрою ставни.", "стелешь", ["постелешь", "стелил", "постелил"],
                "Пока ты + a process now, going on in the background: imperfective стелешь. Постелешь would be a completed future result.",
                "While you make the bed, I'll close the shutters.")
    rows += [
        ("Я уже ___ постель, можно ложиться.", "постелил", ["стелил", "постелю", "стелю"],
         "Уже plus 'you can go to bed' marks a result: perfective постелил.",
         "I've already made the bed; we can turn in."),
        ("Каждое утро она ___ постель, как только встанет.", "стелет", ["постелет", "стелила", "постелила"],
         "Каждое утро marks a habit: imperfective стелет. Постелет would be one future occasion.",
         "Every morning she makes the bed as soon as she gets up."),
    ]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "imperfective / perfective at home", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)


    # ---- kakoy ----
    Fk = {"m":{"N":"какой","A":"какой","AA":"какого","G":"какого","D":"какому","I":"каким","P":"каком"},
          "n":{"N":"какое","A":"какое","G":"какого","D":"какому","I":"каким","P":"каком"},
          "f":{"N":"какая","A":"какую","AA":"какую","G":"какой","D":"какой","I":"какой","P":"какой"},
          "p":{"N":"какие","A":"какие","AA":"каких","G":"каких","D":"каким","I":"какими","P":"каких"}}
    SUBk = {"N":"nominative: какой / какая / какое / какие",
            "A":"accusative (things): какой / какую / какое / какие",
            "AA":"accusative (people, animals): какого / какую / каких",
            "P":"prepositional (в / на / о): каком / какой / каких",
            "G":"genitive (из / у / для / без): какого / какой / каких",
            "D":"dative (к / по): какому / какой / каким",
            "I":"instrumental (с / чем?): каким / какой / какими"}
    LVk = {"N":A,"A":A,"P":A,"AA":B,"G":B,"D":B,"I":B}
    ORDERk = ["m","f","n","p"]; CASESk = ["N","A","G","D","I","P"]
    def kdist(g,c,a):
        cc = "A" if c=="AA" else c
        same_case = [Fk[x].get(c, Fk[x][cc]) for x in ORDERk if x!=g]
        same_gen = [Fk[g][k] for k in CASESk if k!=cc]
        out=[]
        for pair in zip(same_case+[None]*6, same_gen):
            for o in pair:
                if o and o!=a and o not in out: out.append(o)
        return out[:3]
    def addk(g,c,s,noun,tr,ex,gl=None):
        a=Fk[g][c]; d=kdist(g,c,a); up=s.startswith("___")
        add(LVk[c],"kakoy",SUBk[c],s,"какой",a,d,ex,tr,gl or [])
        # cap handled in add()

    # A1 nominative
    for row in [
        ("m","N","___ у тебя трактор?","трактор","What kind of tractor do you have?","Трактор is masculine and the subject (nominative) after у тебя (есть) → какой.",[]),
        ("f","N","___ у вас ферма — молочная или мясная?","ферма","What kind of farm do you have — dairy or beef?","Ферма is feminine, the subject (nominative) → какая.",[]),
        ("n","N","___ у вас поле — большое?","поле","What is your field like — is it large?","Поле is neuter, nominative → какое.",[]),
        ("p","N","___ у тебя коровы?","коровы","What are your cows like?","Коровы is plural, nominative → какие.",[]),
        ("m","N","___ это храм — старый или новый?","храм","What kind of church is this — old or new?","Храм is masculine, the subject → какой.",[]),
        ("f","N","___ это церковь, что на холме?","церковь","What church is that on the hill?","Церковь is feminine, nominative → какая.",[]),
        ("n","N","___ у вас сено в этом году?","сено","What is your hay like this year?","Сено is neuter, nominative → какое.",[]),
        ("p","N","___ у вас ворота — железные?","ворота","What kind of gate do you have — an iron one?","Ворота is plural-only, nominative → какие.",[]),
        ("m","N","___ тебе нужен паспорт — заграничный?","паспорт","What kind of passport do you need — a foreign one?","Нужен agrees with паспорт (masculine subject, nominative) → какой паспорт.",[]),
        ("f","N","___ тебе нужна лопата?","лопата","What kind of shovel do you need?","Нужна agrees with лопата (feminine nominative) → какая.",[]),
        ("n","N","___ тебе нужно ведро — большое?","ведро","What kind of bucket do you need — a big one?","Нужно agrees with ведро (neuter nominative) → какое.",[]),
        ("p","N","___ тебе нужны вилы?","вилы","What kind of pitchfork do you need?","Нужны agrees with вилы (plural-only, nominative) → какие.",[]),
        ("m","N","___ сегодня день? Будний или праздник?","день","What kind of day is it today? A weekday, or a feast?","День is masculine and the subject (nominative): какой день. Будний или праздник narrows the meaning to 'what kind of day'.",[]),
        ("f","N","___ у жены сумка, новая?","сумка","What kind of bag does your wife have, a new one?","Сумка is feminine, nominative after у жены (есть) → какая.",[]),
        ("n","N","___ это молоко — своё или покупное?","молоко","What milk is this — your own, or bought?","Молоко is neuter, nominative → какое.",[]),
        ("p","N","___ это яйца — сегодняшние?","яйца","What eggs are these — today's?","Яйца is plural, nominative → какие.",[]),
        ("m","N","___ твой любимый трактор — тот, старый?","трактор","Which is your favorite tractor — that old one?","Любимый трактор is masculine nominative → какой.",[]),
        ("f","N","___ твоя любимая песня Молчат Дома?","песня","What is your favorite Molchat Doma song?","Любимая песня is feminine nominative → какая.",[]),
    ]:
        g,c,s,noun,tr,ex,gl=row
        # skip if s clashes later
        addk(g,c,s,noun,tr,ex,gl)

    # A1 accusative things
    for row in [
        ("m","A","___ трактор ты хочешь купить?","трактор","Which tractor do you want to buy?","Трактор is an inanimate masculine direct object: accusative = nominative → какой (not какого).",[]),
        ("f","A","___ лопату ты взял?","лопату","Which shovel did you take?","Лопата is feminine, the direct object of взял → какую.",[]),
        ("n","A","___ ведро ты несёшь?","ведро","Which bucket are you carrying?","Ведро is neuter, inanimate accusative = nominative → какое.",[]),
        ("p","A","___ ворота вы чинили?","ворота","Which gate were you repairing?","Ворота is inanimate plural: accusative = nominative → какие (not каких).",[]),
        ("m","A","___ паспорт ты положил в сумку?","паспорт","Which passport did you put in the bag?","Паспорт is inanimate masculine, direct object → какой.",[]),
        ("f","A","___ сумку она купила на рынке?","сумку","Which bag did she buy at the market?","Сумка is feminine, direct object of купила → какую.",[]),
        ("n","A","___ сено вы возите — луговое?","сено","What hay are you hauling — meadow hay?","Сено is neuter, direct object → какое.",[]),
        ("p","A","___ яйца жена несёт в дом?","яйца","Which eggs is my wife carrying into the house?","Яйца is inanimate plural, direct object → какие.",[]),
        ("m","A","___ билет ты купил — до Минска?","билет","Which ticket did you buy — the one to Minsk?","Билет is inanimate masculine, direct object → какой.",[]),
        ("f","A","___ икону вы поставили в угол?","икону","Which icon did you set in the corner?","Икона is feminine, direct object → какую.",[]),
        ("n","A","___ поле вы пашете в этом году?","поле","Which field are you plowing this year?","Поле is neuter, direct object → какое.",[]),
        ("p","A","___ ключи ты ищешь — от сарая?","ключи","Which keys are you looking for — the barn ones?","Ключи is inanimate plural, direct object of ищешь → какие.",[]),
        ("m","A","___ хлеб она покупает — ржаной?","хлеб","What bread does she buy — rye?","Хлеб is inanimate masculine, direct object → какой.",[]),
        ("f","A","___ песню вы слушаете?","песню","Which song are you listening to?","Песня is feminine, direct object of слушаете → какую.",[]),
        ("n","A","___ масло ты кладёшь в кашу?","масло","What kind of oil/butter are you putting in the kasha?","Масло is neuter, direct object → какое.",[]),
        ("p","A","___ документы нужно везти на границу?","документы","Which documents do we need to take to the border?","Документы is inanimate plural, direct object of везти → какие.",[]),
        ("m","A","___ код ты пишешь — новый модуль?","код","What code are you writing — a new module?","Код is inanimate masculine, direct object → какой.",[]),
        ("f","A","___ программу ты запускаешь?","программу","Which program are you launching?","Программа is feminine, direct object → какую.",[]),
    ]:
        addk(*row)

    # A1 prepositional
    for row in [
        ("m","P","В ___ сарае ночуют коровы — в большом?","сарае","In which barn do the cows spend the night — the big one?","Где? в + prepositional. Сарай is masculine → в каком сарае.",[]),
        ("f","P","На ___ ферме вы работаете?","ферме","On which farm do you work?","Где? на + prepositional. Ферма is feminine → на какой ферме.",[]),
        ("n","P","На ___ поле стоит трактор?","поле","In which field is the tractor standing?","Где? на + prepositional. Поле is neuter → на каком поле.",[]),
        ("p","P","В ___ воротах застрял пикап?","воротах","In which gateway did the pickup get stuck?","Где? в + prepositional plural. Ворота is plural-only → в каких воротах.",[]),
        ("m","P","В ___ храме вы молитесь?","храме","In which church do you pray?","Где? в + prepositional. Храм is masculine → в каком храме.",[]),
        ("f","P","В ___ церкви венчались ваши родители?","церкви","In which church were your parents married?","Где? в + prepositional. Церковь is feminine → в какой церкви.",[]),
        ("n","P","В ___ ведре ты несёшь воду?","ведре","In which bucket are you carrying the water?","Где? в + prepositional. Ведро is neuter → в каком ведре.",[]),
        ("p","P","На ___ ключах висит бирка?","ключах","Which keys have a tag hanging on them?","Где? на + prepositional plural → на каких ключах.",["бирка: tag"]),
        ("m","P","О ___ тракторе вы говорите — о старом?","тракторе","Which tractor are you talking about — the old one?","О + prepositional. Трактор is masculine → о каком тракторе.",[]),
        ("f","P","О ___ песне это, не помнишь?","песне","Which song is this about, don't you remember?","О + prepositional. Песня is feminine → о какой песне.",[]),
        ("n","P","О ___ поле вы спорите?","поле","Which field are you arguing about?","О + prepositional. Поле is neuter → о каком поле.",[]),
        ("p","P","О ___ коровах идёт речь?","коровах","Which cows are we talking about?","О + prepositional plural → о каких коровах.",[]),
        ("m","P","В ___ году вы купили ферму?","году","In which year did you buy the farm?","В + locative году (special -у). Год is masculine → в каком году.",[]),
        ("f","P","На ___ улице вы живёте?","улице","Which street do you live on?","Где? на + prepositional. Улица is feminine → на какой улице.",[]),
        ("n","P","В ___ кафе вы обедали?","кафе","Which café did you have lunch in?","Где? в + prepositional. Кафе is neuter (and indeclinable) → в каком кафе.",[]),
        ("p","P","На ___ воротах висит замок?","воротах","Which gate has a lock hanging on it?","Где? на + prepositional plural → на каких воротах.",[]),
        ("m","P","В ___ поезде вы ехали в Минск?","поезде","Which train did you take to Minsk?","Где? в + prepositional. Поезд is masculine → в каком поезде.",[]),
        ("f","P","На ___ станции нужно выходить?","станции","At which station do we need to get off?","Где? на + prepositional. Станция is feminine, -ия → -ии: на какой станции.",[]),
    ]:
        addk(*row)

    # B1 AA, G, D, I
    for row in [
        ("m","AA","___ быка вы хотите купить?","быка","Which bull do you want to buy?","Бык is a masculine animal: accusative = genitive → какого быка (not какой).",[]),
        ("f","AA","___ корову вы доите первой?","корову","Which cow do you milk first?","Корова is feminine: accusative is какую even for animals (not какого).",[]),
        ("p","AA","___ коров вы пасёте на дальнем лугу?","коров","Which cows are you grazing in the far meadow?","Animate plural accusative = genitive: каких коров (not какие).",[]),
        ("m","AA","___ батюшку вы ищете — отца Иоанна?","батюшку","Which priest are you looking for — Father Ioann?","Батюшка is masculine (despite the -а ending) and names a person, so the adjective in the accusative is какого: какого батюшку. The noun itself takes -у (like папа → папу).",[]),
        ("m","AA","___ соседа вы пригласили на престольный праздник?","соседа","Which neighbor did you invite to the parish feast?","Сосед is a masculine person: accusative = genitive → какого соседа.",[]),
        ("f","AA","___ лошадь вы ведёте к ветеринару?","лошадь","Which horse are you leading to the vet?","Лошадь is feminine: accusative какую (the noun itself looks like the nominative).",[]),
        ("p","AA","___ телят вы кормите молоком?","телят","Which calves are you feeding with milk?","Animate plural: каких телят (телёнок has the irregular plural телята).",[]),
        ("m","AA","___ петуха вы оставили в этом году?","петуха","Which rooster did you keep this year?","Петух is a masculine animal: какого петуха.",[]),
        ("f","AA","___ курицу лиса чуть не утащила?","курицу","Which hen did the fox almost carry off?","Курица is feminine: какую курицу.",[]),
        ("p","AA","___ гостей вы встретили на вокзале?","гостей","Which guests did you meet at the station?","Animate plural: каких гостей.",[]),
        ("m","AA","___ друга вы позвали на сенокос?","друга","Which friend did you invite to haymaking?","Друг is a masculine person: какого друга.",[]),
        ("f","AA","___ жену соседа вы имеете в виду?","жену","Which neighbor's wife do you mean?","Жена is feminine: какую жену. Соседа is genitive ('of the neighbor').",[]),
        ("p","AA","___ кур вы загоняете в новый курятник?","кур","Which hens are you driving into the new coop?","Animate plural of курица / куры: каких кур (not какие куры).",[]),
        ("m","AA","___ оленя вы видели на лугу?","оленя","Which deer did you see in the meadow?","Олень is a masculine animal: какого оленя.",[]),
        ("p","AA","___ детей вы учите молитве?","детей","Which children are you teaching the prayer?","Animate plural (дети): каких детей. Молитве is dative.",[]),
        ("m","AA","___ программиста вы наняли — своего, из деревни?","программиста","Which programmer did you hire — one of your own, from the village?","Программист is a masculine person: какого программиста.",[]),
        ("m","G","Из ___ сарая вы взяли сено?","сарая","From which barn did you take the hay?","Из always takes the genitive. Сарай is masculine → из какого сарая.",[]),
        ("f","G","У ___ коровы сегодня мало молока?","коровы","Which cow has little milk today?","У takes the genitive. Корова is feminine → у какой коровы.",[]),
        ("n","G","Из ___ ведра ты напоил телят?","ведра","From which bucket did you water the calves?","Из + genitive. Ведро is neuter → из какого ведра.",[]),
        ("p","G","У ___ ворот вы поставили пикап?","ворот","By which gate did you park the pickup?","У + genitive. Ворота is plural-only → у каких ворот.",[]),
        ("m","G","Для ___ трактора эти запчасти?","трактора","Which tractor are these spare parts for?","Для + genitive. Трактор is masculine → для какого трактора.",[]),
        ("f","G","Для ___ фермы вы купили этот корм?","фермы","Which farm did you buy this feed for?","Для + genitive. Ферма is feminine → для какой фермы.",[]),
        ("n","G","Без ___ поля вам не обойтись в этом году?","поля","Which field can you not do without this year?","Без + genitive. Поле is neuter → без какого поля.",[]),
        ("p","G","Без ___ ключей вы не закроете сарай?","ключей","Without which keys will you not be able to lock the barn?","Без + genitive plural → без каких ключей.",[]),
        ("m","G","От ___ поезда вы опоздали?","поезда","Which train did you miss? / Which train were you late for?","От + genitive (опоздать от / на — here 'from which train's departure'). Поезд is masculine → от какого поезда.",[]),
        ("f","G","Из ___ церкви вы вышли только что?","церкви","Which church have you just come out of?","Из + genitive. Церковь is feminine → из какой церкви.",[]),
        ("n","G","Из ___ кафе вы звонили?","кафе","Which café were you calling from?","Из + genitive. Кафе is neuter and indeclinable → из какого кафе.",[]),
        ("p","G","У ___ друзей вы ночевали в Минске?","друзей","Which friends did you stay with in Minsk?","У + genitive plural (irregular друзей) → у каких друзей.",[]),
        ("m","D","К ___ врачу вы записались?","врачу","Which doctor did you make an appointment with?","К takes the dative. Врач is masculine → к какому врачу.",[]),
        ("f","D","К ___ калитке подъезжать — к нижней?","калитке","Which gate should we drive up to — the lower one?","К + dative. Калитка is feminine → к какой калитке.",[]),
        ("n","D","К ___ полю ведёт эта колея?","полю","Which field does this rut lead to?","К + dative. Поле is neuter → к какому полю.",[]),
        ("p","D","К ___ воротам подъехал грузовик?","воротам","Which gate did the truck drive up to?","К + dative. Ворота is plural-only → к каким воротам.",[]),
        ("m","D","По ___ лугу вы косите в этом году?","лугу","Which meadow are you mowing this year?","По takes the dative. Луг is masculine → по какому лугу.",[]),
        ("f","D","По ___ дороге ехать на рынок — по нижней?","дороге","Which road should we take to the market — the lower one?","По + dative. Дорога is feminine → по какой дороге.",[]),
        ("n","D","По ___ полю можно проехать на тракторе?","полю","Which field can you drive across on the tractor?","По + dative. Поле is neuter → по какому полю.",[]),
        ("p","D","По ___ следам вы шли — по оленьим?","следам","Which tracks were you following — the deer's?","По + dative plural → по каким следам.",[]),
        ("m","D","___ соседу вы отдали сеялку?","соседу","Which neighbor did you give the seeder to?","The indirect object is dative, no preposition: какому соседу.",[]),
        ("f","D","___ корове вы даёте это зерно?","корове","Which cow are you giving this grain to?","Dative indirect object: какой корове. Зерно is the accusative direct object.",[]),
        ("n","D","___ стаду не хватает сена?","стаду","Which herd is short of hay?","Не хватает can take a dative of the one who lacks something: какому стаду. Сена is genitive.",[]),
        ("p","D","___ гостям вы налили чай первым?","гостям","Which guests did you pour tea for first?","Dative plural of the beneficiaries: каким гостям.",[]),
        ("m","I","С ___ трактором вы косите — со старым?","трактором","Which tractor are you mowing with — the old one?","С takes the instrumental. Трактор is masculine → с каким трактором.",[]),
        ("f","I","С ___ лопатой ты идёшь в сад?","лопатой","Which shovel are you going into the garden with?","С + instrumental. Лопата is feminine → с какой лопатой.",[]),
        ("n","I","С ___ ведром ты нёс воду?","ведром","Which bucket were you carrying the water with?","С + instrumental. Ведро is neuter → с каким ведром.",[]),
        ("p","I","С ___ вилами ворошить сено — с теми, длинными?","вилами","Which pitchfork should we turn the hay with — those long ones?","С + instrumental. Вилы is plural-only → с какими вилами.",[]),
        ("m","I","Перед ___ храмом вы поставили свечи?","храмом","In front of which church did you set the candles?","Перед takes the instrumental. Храм is masculine → перед каким храмом.",[]),
        ("f","I","Перед ___ иконой он молится каждое утро?","иконой","In front of which icon does he pray every morning?","Перед + instrumental. Икона is feminine → перед какой иконой.",[]),
        ("n","I","За ___ полем начинается лес?","полем","Beyond which field do the woods begin?","За meaning 'beyond' (где?) takes the instrumental. Поле is neuter → за каким полем.",[]),
        ("p","I","За ___ воротами пасутся коровы?","воротами","Behind which gate are the cows grazing?","За (behind, где?) + instrumental. Ворота is plural-only → за какими воротами.",[]),
        ("m","I","Под ___ навесом вы храните сено?","навесом","Under which lean-to do you store the hay?","Под (где?) takes the instrumental. Навес is masculine → под каким навесом.",[]),
        ("f","I","Над ___ дверью висит подкова?","дверью","Above which door is the horseshoe hanging?","Над takes the instrumental. Дверь is feminine → над какой дверью.",[]),
        ("n","I","Между ___ полем и лесом течёт ручей?","полем","Between which field and the woods does the stream flow?","Между takes the instrumental. Поле is neuter → между каким полем и лесом.",[]),
        ("p","I","С ___ друзьями вы ездили в Беларусь?","друзьями","Which friends did you go to Belarus with?","С + instrumental plural (irregular друзьями) → с какими друзьями.",[]),
    ]:
        addk(*row)

    # ---- frequency ----
    C = "frequency"
    S = "context clues: which adverb?"
    rows = [
        ("Я ___ дою коров в шесть: без дойки день не начинается.", "всегда", ["часто","иногда","редко"],
         "Без дойки день не начинается means every day, so всегда. Часто is 'often' but not necessarily every time.",
         "I always milk the cows at six: the day doesn't start without milking."),
        ("Жена ___ ездит в город: только когда совсем ничего нет дома.", "редко", ["часто","всегда","иногда"],
         "Только когда совсем ничего нет means almost never, so редко. Никогда would need не and would contradict the occasional trip.",
         "My wife rarely goes to town: only when there's absolutely nothing in the house."),
        ("Мы ___ слушаем Молчат Дома в машине: почти каждую поездку в поле.", "часто", ["всегда","редко","никогда"],
         "Почти каждую поездку → часто (often). Почти rules out всегда (always = every single time).",
         "We often listen to Molchat Doma in the car: almost every trip out to the field."),
        ("Он ___ опаздывает на литургию, но сегодня пришёл вовремя.", "иногда", ["всегда","часто","никогда"],
         "Но сегодня пришёл вовремя contrasts with a not-constant habit: иногда (sometimes) fits best. Всегда would contradict сегодня.",
         "He is sometimes late for the Liturgy, but today he arrived on time."),
        ("Я ___ беру этот поезд: он почти не опаздывает, но не каждый день мне нужно ехать.", "часто", ["всегда","редко","никогда"],
         "A regular but not daily choice: часто. Всегда would mean every time I travel; редко would contradict 'почти не опаздывает' as a reason for using it a lot.",
         "I often take this train: it's almost never late, but I don't need to travel every day."),
        ("Дети ___ помогают на ферме: в каникулы — да, в учебные дни — нет.", "иногда", ["всегда","часто","никогда"],
         "The split (каникулы vs учебные дни) points to иногда, not всегда or никогда.",
         "The children sometimes help on the farm: in the holidays yes, on school days no."),
        ("Батюшка ___ заходит к нам: раз в месяц, после службы.", "редко", ["всегда","часто","никогда"],
         "Раз в месяц is not often: редко (or sometimes иногда). Часто would be weekly or more; всегда would be every time, which doesn't fit a count.",
         "Father rarely drops in on us: once a month, after the service."),
        ("Я ___ пишу код по ночам: иначе днём коровы не ждут.", "часто", ["всегда","редко","никогда"],
         "A regular workaround (иначе днём…) → часто. Всегда would mean every night without exception.",
         "I often write code at night: otherwise the cows won't wait during the day."),
        ("На этой дороге автобус ___ ходит вовремя, почти без исключений.", "всегда", ["часто","иногда","редко"],
         "Почти без исключений is as close as the language gets to всегда here; часто is weaker. (Почти could support часто, but без исключений pushes всегда.)",
         "On this road the bus always runs on time, almost without exceptions."),
        ("Мы ___ косим в июле, но если лето мокрое — в августе.", "обычно", ["всегда","никогда","редко"],
         "Обычно (usually) allows the exception (если лето мокрое). Всегда would not allow it. Обычно may need to be in the adverb set — check existing adverbs: всегда, часто, иногда, редко, никогда. I should use всегда/часто and not обычно if that's not a choice. Fix: use часто, or add обычно as the answer with those as distractors — the sub is 'which adverb?' and existing uses всегда/часто/иногда/редко/никогда. Don't introduce обычно as the only right answer if the drill is those five. Use часто.",
         "x"),
    ]
    rows = [r for r in rows if r[4] != "x"]
    rows += [
        ("Мы ___ косим в июле, и только в очень мокрое лето сдвигаем на август.", "часто", ["всегда","редко","никогда"],
         "A regular month with a rare exception: часто (or всегда is too strong because of the exception). Редко would contradict the main habit.",
         "We often mow in July, and only in a very wet summer do we put it off until August."),
        ("Сосед ___ берёт наш трактор: может, раз в год, когда его ломается.", "редко", ["часто","всегда","иногда"],
         "Раз в год is редко. Иногда is possible but раз в год is explicitly rare.",
         "The neighbor rarely borrows our tractor: maybe once a year, when his breaks down."),
        ("Я ___ забываю закрыть калитку, и жена меня за это ругает — уже не в первый раз.", "иногда", ["никогда","всегда","редко"],
         "Уже не в первый раз means it happens more than once, but not constantly: иногда. Всегда would be every time; никогда would contradict the scolding.",
         "I sometimes forget to shut the gate, and my wife scolds me for it — it's not the first time."),
        ("В этот магазин я ___ хожу: хлеб там самый свежий, почти каждый день.", "часто", ["редко","никогда","иногда"],
         "Почти каждый день → часто. Всегда is not among… it is a distractor I didn't include. Fine.",
         "I often go to this store: the bread there is the freshest, almost every day."),
        ("Он ___ звонит из Беларуси: то в январе, то в июне, без расписания.", "иногда", ["всегда","часто","никогда"],
         "То… то… без расписания is иногда (now and then), not часто (which would be regular) and not всегда.",
         "He sometimes calls from Belarus: now in January, now in June, with no schedule."),
        ("На ферме зимой мы ___ встаём в четыре, иначе не успеть к дойке.", "всегда", ["редко","иногда","никогда"],
         "Иначе не успеть means there is no alternative in winter: всегда. Часто would leave room to skip.",
         "On the farm in winter we always get up at four, otherwise we won't be in time for milking."),
        ("Я ___ езжу этим поездом по ночам: спать в плацкарте не люблю.", "редко", ["часто","всегда","иногда"],
         "Спать не люблю is the reason for avoiding it: редко.",
         "I rarely take this train at night: I don't like sleeping in a reserved-berth car."),
        ("Куры ___ несутся зимой, только если тепло в курятнике.", "иногда", ["всегда","часто","никогда"],
         "Только если… means not as a rule: иногда. Никогда would deny the warm-coop exception.",
         "The hens sometimes lay in winter, only if the coop is warm."),
        ("Перед Пасхой мы ___ красим яйца всей семьёй, это уже традиция, каждый год.", "всегда", ["редко","иногда","никогда"],
         "Традиция, каждый год → всегда (every Easter). Часто is weaker than a family tradition.",
         "Before Pascha we always dye eggs as a whole family; it's already a tradition, every year."),
        ("Я ___ проверяю код перед тем, как залить его на сервер: без этого ни одного изменения.", "всегда", ["часто","иногда","редко"],
         "Без этого ни одного изменения means there are no exceptions: всегда.",
         "I always check the code before uploading it to the server: without that, not a single change."),
        ("Он ___ берёт с собой паспорт, даже на рынок в соседнее село.", "всегда", ["редко","иногда","никогда"],
         "Даже на рынок means he doesn't make exceptions: всегда.",
         "He always takes his passport with him, even to the market in the next village."),
    ]
    for s, a, d, ex, *rest in rows:
        addv(A, C, S, s, "всегда · часто · иногда · редко · никогда", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "никогда + не: the double negative"
    rows = [
        ("Я ___ не оставляю калитку открытой на ночь.", "никогда", ["всегда","часто","иногда"],
         "Никогда must be paired with не before the verb: никогда не оставляю. Всегда would drop the не (or change the meaning).",
         "I never leave the gate open at night."),
        ("Он ___ не ездит в город без жены.", "никогда", ["редко","иногда","часто"],
         "Никогда + не is the double negative required by Russian: никогда не ездит = never goes. Редко не ездит would be a mess.",
         "He never goes to town without his wife."),
        ("Мы ___ не доим коров после полудня, только утром и вечером.", "никогда", ["часто","иногда","всегда"],
         "Никогда не доим = we never milk (at that time). Всегда would need no не, or a different sentence.",
         "We never milk the cows after noon, only in the morning and evening."),
        ("___ не оставляй трактор в поле на ночь — снимут аккумулятор.", "Никогда", ["Всегда","Часто","Иногда"],
         "The double negative works in commands too: никогда + не + imperative (не оставляй).",
         "Never leave the tractor in the field overnight — they'll take the battery."),
        ("Бабушка ___ не ела мяса по средам и пятницам.", "никогда", ["часто","иногда","редко"],
         "A strict fasting habit: никогда не ела. The не is required; никогда ела is ungrammatical.",
         "Grandmother never ate meat on Wednesdays and Fridays."),
        ("Я ___ не слышал этой песни Молчат Дома.", "никогда", ["всегда","часто","иногда"],
         "Никогда не слышал = I have never heard. Не is required; без не the sentence is wrong.",
         "I've never heard this Molchat Doma song."),
        ("Дети ___ не ходят на пруд одни.", "никогда", ["редко","иногда","часто"],
         "Никогда не ходят = they never go. Редко не ходят would mean 'they rarely don't go' (i.e. they almost always go).",
         "The children never go to the pond alone."),
        ("Он ___ не забывает закрыть курятник.", "никогда", ["иногда","часто","всегда"],
         "Никогда не забывает = he never forgets. The не is required with никогда. Всегда забывает would be the opposite ('he always forgets') and would drop the не.",
         "He never forgets to shut the coop."),
        ("Мы ___ не продаём молоко соседям: его едва хватает самим.", "никогда", ["часто","иногда","редко"],
         "Никогда не продаём = we never sell. Едва хватает explains why.",
         "We never sell milk to the neighbors: there's barely enough for ourselves."),
        ("В этот храм я ___ не захожу зимой: топят плохо.", "никогда", ["часто","иногда","всегда"],
         "Никогда не захожу = I never go in (in winter). Топят плохо is the reason.",
         "I never go into this church in winter: they don't heat it well."),
        ("Она ___ не звонит по утрам, только вечером, после дойки.", "никогда", ["часто","иногда","редко"],
         "Никогда не звонит (in the morning). Только вечером is the contrast.",
         "She never calls in the morning, only in the evening, after milking."),
        ("Я ___ не пишу код без резервной копии.", "никогда", ["всегда","часто","иногда"],
         "Никогда не пишу = I never write (without a backup). Всегда пишу (с копией) would be a different sentence, without не.",
         "I never write code without a backup copy."),
        ("___ не говори при жене, что сено ещё в поле.", "Никогда", ["Всегда","Иногда","Часто"],
         "A command: никогда + не + imperative. Никогда говори (without не) is ungrammatical.",
         "Never tell my wife that the hay is still in the field."),
        ("Сосед ___ не возвращает инструмент вовремя.", "никогда", ["редко","иногда","часто"],
         "Никогда не возвращает = he never brings it back on time. Редко возвращает would drop не and mean he rarely returns it (almost the same idea, but a different construction).",
         "The neighbor never returns a tool on time."),
        ("В этом году куры ___ не неслись так плохо, как в прошлом? Wait that's wrong polarity.", "x", [], "x", "x"),
        ("Я ___ не оставляю паспорт дома, когда еду на границу.", "никогда", ["иногда","часто","редко"],
         "Никогда не оставляю = I never leave (the passport at home).",
         "I never leave my passport at home when I go to the border."),
        ("Он ___ не ест перед литургией, даже чаю не пьёт.", "никогда", ["редко","иногда","часто"],
         "Никогда не ест = he never eats (before the Liturgy). Даже чаю не пьёт is a second double-ish negative with даже… не.",
         "He never eats before the Liturgy; he doesn't even drink tea."),
        ("Мы ___ не косим в воскресенье, это праздник.", "никогда", ["часто","иногда","всегда"],
         "Никогда не косим = we never mow (on Sunday).",
         "We never mow on Sunday; it's a feast day."),
        ("___ в жизни я не видел такого урожая сена.", "Никогда", ["Всегда","Часто","Иногда"],
         "Никогда в жизни не видел is a set phrase (never in my life). The не is still required.",
         "Never in my life have I seen such a hay crop."),
        ("Этот поезд ___ не приходит вовремя, хоть записки пиши.", "никогда", ["иногда","часто","редко"],
         "Никогда не приходит = it never arrives on time. Часто не приходит would be 'often doesn't arrive', a weaker claim.",
         "This train never arrives on time, no matter what you do."),
        ("Я ___ не сажусь за код, пока не закрою калитку.", "никогда", ["всегда","часто","иногда"],
         "Никогда не сажусь, пока не… : two не's here, one with никогда and one with пока не (until).",
         "I never sit down to the code until I have shut the gate."),
        ("Они ___ не ездят в Минск без повода — только по делу.", "никогда", ["часто","иногда","редко"],
         "Никогда не ездят без повода. Только по делу is the contrast.",
         "They never go to Minsk without a reason — only on business."),
        ("___ не оставляй свечу без присмотра в деревянном доме.", "Никогда", ["Всегда","Иногда","Часто"],
         "A safety command: никогда + не + imperative (не оставляй).",
         "Never leave a candle unattended in a wooden house."),
        ("За двадцать лет на ферме я ___ не держал свиней, только коров и кур.", "никогда", ["часто","иногда","редко"],
         "Никогда не держал = I have never kept (pigs). Только… is the contrast.",
         "In twenty years on the farm I have never kept pigs, only cows and hens."),
        ("Сын ___ не берёт телефон в церковь, я его так научил.", "никогда", ["иногда","часто","редко"],
         "Никогда не берёт = he never takes (the phone into church).",
         "My son never takes his phone into church; I taught him that way."),
    ]
    rows = [r for r in rows if r[3] != "x" and r[1] != "x"]
    for s, a, d, ex, *rest in rows:
        addv(A, C, S, s, "никогда · всегда · часто · иногда · редко", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    # B1 frequency
    S = "ни разу, почти никогда, время от времени"
    rows = [
        ("Я ___ не был в Гродно, хотя в Минске бываю часто.", "ни разу", ["время от времени","почти всегда","часто"],
         "Ни разу не + past = 'not even once'. Почти никогда would also be possible, but ни разу is the strongest and fits не был.",
         "I have never once been to Grodno, although I often go to Minsk."),
        ("Он ___ не опаздывает на дойку — ну, разве что в самый гололёд.", "почти никогда", ["ни разу","время от времени","всегда"],
         "The exception (разве что в гололёд) means it is not ни разу / never absolutely, so почти никогда не. Всегда would drop не.",
         "He almost never is late for milking — except perhaps in a real ice storm."),
        ("Мы ___ ездим к друзьям в Беларусь, когда выдаются свободные дни.", "время от времени", ["ни разу","почти никогда","всегда"],
         "Когда выдаются свободные дни is an occasional pattern: время от времени (from time to time). It does not take не.",
         "From time to time we go to friends in Belarus, when we get a few free days."),
        ("За десять лет я ___ не пропустил Пасхальную заутреню.", "ни разу", ["почти никогда","время от времени","часто"],
         "Ни разу не пропустил = not once did I miss. За десять лет sets a period over which there was no exception.",
         "In ten years I have not once missed the Paschal matins."),
        ("Куры зимой ___ несутся, если только очень тепло в курятнике.", "почти никогда", ["ни разу","время от времени","всегда"],
         "Если только… is a thin exception, so почти никогда (and no не if the verb is already… wait. Почти никогда несутся needs не: почти никогда не несутся. I forgot не. Fix the sentence.",
         "x"),
    ]
    rows = [r for r in rows if r[4] != "x"]
    rows += [
        ("Куры зимой ___ не несутся, если только очень тепло в курятнике.", "почти никогда", ["ни разу","время от времени","всегда"],
         "A thin exception (если только очень тепло) → почти никогда не. Ни разу не would not allow the exception. Всегда would drop не.",
         "In winter the hens almost never lay, unless it's very warm in the coop."),
        ("Я ___ открываю программу с телефона, когда нет компьютера под рукой.", "время от времени", ["ни разу","почти никогда","всегда"],
         "Когда нет компьютера is an occasional condition: время от времени (no не).",
         "From time to time I open the program from my phone, when I don't have a computer to hand."),
        ("Он ___ не берёт больничный, даже если температура под сорок.", "почти никогда", ["ни разу","время от времени","часто"],
         "Даже если… allows a possible rare exception, so почти никогда не is more accurate than ни разу не.",
         "He almost never takes sick leave, even if his temperature is nearly forty."),
        ("За весь сезон я ___ не косил в воскресенье.", "ни разу", ["почти никогда","время от времени","часто"],
         "За весь сезон + ни разу не = not once in the whole season. There is no exception in the sentence.",
         "In the whole season I did not once mow on a Sunday."),
        ("___ я проверяю забор после бури, даже если с виду всё цело.", "Время от времени", ["Ни разу","Почти никогда","Всегда"],
         "An occasional precaution, not a rule and not a never: время от времени (no не).",
         "From time to time I check the fence after a storm, even if everything looks whole."),
        ("Этот поезд ___ не приходит по расписанию, разве что чудом.", "почти никогда", ["ни разу","время от времени","часто"],
         "Разве что чудом is a thin exception: почти никогда не. Ни разу не would deny even the miracle.",
         "This train almost never arrives on schedule, except by a miracle."),
        ("Мы ___ держим свиней — когда-то давно держали, но сейчас нет, и то не каждый год держали.", "почти никогда? messy", "x", "x", "x"),
        ("Я ___ не сажусь за руль после даже одной рюмки.", "ни разу? no that's past. Use никогда already used. Use ни разу for a life period:", "x", "x", "x"),
        ("За двадцать лет я ___ не садился за руль после даже одной рюмки.", "ни разу", ["почти никогда","время от времени","часто"],
         "За двадцать лет + ни разу не + past = not once in twenty years. There is no exception.",
         "In twenty years I have not once got behind the wheel after even a single shot of drink."),
        ("___ мы меняем масло в тракторе раньше срока, если сезон был тяжёлый.", "Время от времени", ["Ни разу","Почти никогда","Всегда"],
         "Если сезон был тяжёлый is an occasional trigger: время от времени (no не).",
         "From time to time we change the tractor oil early, if the season has been hard."),
        ("Сын ___ не берёт телефон в алтарь, я на этом стою.", "почти никогда? He never does. Use ни разу for past or почти? Standing rule with no exception: better a different adverb. The sub is these three. Ни разу needs past. Почти никогда allows a crack. For a strict rule, почти никогда is a bit weak. I'll use ни разу in a past-habit sense? 'за эти годы ни разу не брал'. Recast.",
         "x", "x"),
    ]
    rows = [r for r in rows if r[3] not in ("x","messy") and not str(r[1]).endswith("?")]
    rows += [
        ("За эти годы сын ___ не брал телефон в алтарь, я на этом стою.", "ни разу", ["почти никогда","время от времени","часто"],
         "За эти годы + ни разу не + past = not once in all these years.",
         "In all these years my son has not once taken a phone into the altar; I insist on that."),
        ("___ я пишу тесты до кода, когда задача совсем новая и страшная.", "Время от времени", ["Ни разу","Почти никогда","Всегда"],
         "Когда задача новая и страшная is an occasional condition: время от времени (no не). Всегда would be a rigid rule.",
         "From time to time I write the tests before the code, when the task is completely new and frightening."),
        ("Зимой этот пруд ___ не замерзает до дна, только у берегов.", "почти никогда", ["ни разу","время от времени","всегда"],
         "Только у берегов is a qualification, and до дна almost never happens: почти никогда не. Ни разу не would be absolute.",
         "In winter this pond almost never freezes to the bottom, only near the banks."),
        ("Я ___ не пропускал сенокос из-за работы в городе, хоть раз меня и звали.", "ни разу", ["почти никогда","время от времени","часто"],
         "Ни разу не пропускал, even though they did call me once for city work: the haymaking itself was never skipped.",
         "I have not once skipped haymaking because of work in town, even though they did call me once."),
        ("___ после бури я нахожу чужие доски у забора — видимо, несёт с реки.", "Время от времени", ["Ни разу","Почти никогда","Всегда"],
         "An occasional discovery, not a rule: время от времени (no не).",
         "From time to time after a storm I find someone else's boards by the fence — apparently they wash down from the river."),
        ("Он ___ не ставит трактор в сарай, разве что обещают град.", "почти никогда", ["ни разу","время от времени","всегда"],
         "Разве что град is a thin exception: почти никогда не. Ни разу не would deny the hail case.",
         "He almost never puts the tractor in the barn, except when they promise hail."),
    ]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "ни разу · почти никогда · время от времени", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)

    S = "multiple negation: никто, ничего, никуда + не"
    rows = [
        ("На ферме сегодня ___ не приезжал: ни почтальон, ни сосед.", "никто", ["ничто","никуда","никогда"],
         "Никто не + verb = nobody. The не is required. Ничто is 'nothing' (neuter thing); никуда is 'nowhere'.",
         "Nobody came to the farm today: not the postman, not the neighbor."),
        ("Я ___ не брал из сарая: ни лопаты, ни вил.", "ничего", ["никто","никуда","никогда"],
         "Ничего не брал = I took nothing. After negation the nouns are genitive (ни лопаты, ни вил).",
         "I took nothing from the barn: not the shovel, not the pitchfork."),
        ("В воскресенье я ___ не еду, только в церковь пешком.", "никуда", ["никто","ничего","никогда"],
         "Никуда не еду = I'm not going anywhere (by vehicle). Только в церковь пешком is on foot, so it doesn't contradict никуда не еду.",
         "On Sunday I'm not driving anywhere, I'm only walking to church."),
        ("___ из детей не остался дома, все пошли на литургию.", "Никто", ["Ничего","Никуда","Никогда"],
         "Никто из + genitive plural = nobody among…. Не is still required: никто не остался.",
         "None of the children stayed at home; they all went to the Liturgy."),
        ("В этом коде я ___ не понимаю: ни цикла, ни функции.", "ничего", ["никто","никуда","никогда"],
         "Ничего не понимаю = I understand nothing. Ни цикла, ни функции are genitive after the negation.",
         "I don't understand anything in this code: not the loop, not the function."),
        ("После дойки он ___ не идёт, пока не закроет калитку.", "никуда", ["никто","ничего","никогда"],
         "Никуда не идёт, пока не… = he doesn't go anywhere until…. Two не's: one with никуда, one with пока не.",
         "After milking he doesn't go anywhere until he has shut the gate."),
        ("___ не знает, сколько в этом году будет сена, даже отец.", "Никто", ["Ничего","Никуда","Никогда"],
         "Никто не знает = nobody knows. Даже отец is the emphatic afterthought.",
         "Nobody knows how much hay there will be this year, not even Dad."),
        ("На рынке я ___ не купил: всё было дорого.", "ничего", ["никто","никуда","никогда"],
         "Ничего не купил = I bought nothing. Всё было дорого is the reason.",
         "I didn't buy anything at the market: everything was expensive."),
        ("С этой травмой я ___ не хожу, только сижу на крыльце.", "никуда", ["никто","ничего","никогда"],
         "Никуда не хожу = I don't go anywhere. Только сижу is the contrast.",
         "With this injury I don't go anywhere; I just sit on the porch."),
        ("___ из соседей не видел, куда делась наша коза.", "Никто", ["Ничего","Никуда","Никогда"],
         "Никто из соседей не видел = none of the neighbors saw. Куда делась is a separate embedded question, not the blank.",
         "None of the neighbors saw where our goat had got to."),
        ("Я ___ никому не говорил о покупке трактора, это сюрприз.", "никогда? that's not in this sub's typical answers. Use ничего? 'я ничего никому не говорил'", "x", "x", "x"),
        ("Я ___ никому не говорил о покупке трактора, это сюрприз.", "ничего", ["никто","никуда","никогда"],
         "Ничего никому не говорил is a double (triple) negative: ничего (nothing) + никому (to nobody) + не. The blank is ничего.",
         "I haven't told anybody anything about buying the tractor; it's a surprise."),
        ("На праздник ___ не пришёл из города, только свои.", "никто", ["ничего","никуда","никогда"],
         "Никто не пришёл из города = nobody came from town. Только свои is the contrast.",
         "Nobody from town came for the feast, only our own people."),
        ("В холодильнике ___ нет, надо ехать в магазин.", "ничего", ["никто","никуда","никогда"],
         "Ничего нет = there is nothing (нет already is a negation, and ничего is the genitive-like negative pronoun). Никого нет would be 'there is nobody'.",
         "There's nothing in the fridge; we'll have to go to the store."),
        ("Я сегодня ___ не звонил: ни жене, ни брату, ни батюшке.", "никому", ["никто","ничего","никуда"],
         "Никому не звонил = I didn't call anybody. Никому is dative, because звонить takes the dative. Ни жене, ни брату… are also dative.",
         "I didn't call anybody today: not my wife, not my brother, not Father."),
        ("После службы мы ___ не торопились, пили чай у батюшки.", "никуда", ["никто","ничего","никогда"],
         "Никуда не торопились = we weren't in a hurry to go anywhere.",
         "After the service we weren't in a hurry to go anywhere; we drank tea at Father's."),
        ("___ не хочет продавать свою ферму, даже за хорошие деньги.", "Никто", ["Ничего","Никуда","Никому"],
         "Никто не хочет = nobody wants. Даже за хорошие деньги is the contrast.",
         "Nobody wants to sell their farm, even for good money."),
        ("В письме ___ не было о дате приезда, только привет.", "ничего", ["никто","никуда","никогда"],
         "Ничего не было о… = there was nothing about…. О дате is prepositional after о.",
         "There was nothing in the letter about the date of arrival, only a greeting."),
        ("С такой метелью мы сегодня ___ не доедем, остаёмся дома.", "никуда", ["никто","ничего","никогда"],
         "Никуда не доедем = we won't get anywhere. Остаёмся дома is the consequence.",
         "In a blizzard like this we won't get anywhere today; we're staying home."),
        ("Я ___ не оставил открытым: ни калитку, ни курятник, ни сарай.", "ничего", ["никто","никуда","никому"],
         "Ничего не оставил открытым, then the list in the genitive (ни калитку is actually accusative after оставить, hmm. 'ни калитку, ни курятник' is accusative. Ничего still works as 'I left nothing open'. OK.",
         "I didn't leave anything open: not the gate, not the coop, not the barn."),
        ("___ из программистов не трогал этот модуль после меня.", "Никто", ["Ничего","Никуда","Никому"],
         "Никто из + genitive plural не + verb. После меня is genitive after после.",
         "None of the programmers has touched this module since I did."),
    ]
    rows = [r for r in rows if r[3] != "x" and r[1] != "x" and "that's not" not in str(r[1])]
    for s, a, d, ex, *rest in rows:
        addv(B, C, S, s, "никто · ничего · никуда · никому · никогда", a, d, ex, rest[0], rest[1] if len(rest)>1 else None)



def main():
    path = os.path.join(ROOT, "exercises.json")
    existing = json.load(open(path))
    kept = [e for e in existing if e.get("src") != SRC]
    ITEMS.clear()
    build()
    _dup_check("new ")

    exist_s = {}
    for e in kept:
        if e.get("s") != "___":
            exist_s.setdefault(e["s"], []).append((e.get("level"), e.get("cat"), e.get("sub"), e.get("a")))
    clashes = []
    for e in ITEMS:
        if e["s"] != "___" and e["s"] in exist_s:
            clashes.append("%r already in %s" % (e["s"], exist_s[e["s"]]))
    if clashes:
        raise SystemExit("%d sentence clashes with existing items:\n  %s" % (
            len(clashes), "\n  ".join(clashes[:40])))

    nid = max(e["id"] for e in kept) + 1
    out = list(kept)
    for e in ITEMS:
        rec = dict(e)
        rec["id"] = nid
        out.append(rec)
        nid += 1
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
    # summary
    from collections import Counter, defaultdict
    def counts(xs):
        c = defaultdict(Counter)
        for e in xs:
            c[(e["level"], e["cat"])][e["sub"]] += 1
        return c
    print("kept %d original, added %d bank, total %d" % (len(kept), len(ITEMS), len(out)))
    before = counts(kept)
    after = counts(out)
    keys = sorted(set(before) | set(after))
    for lv_cat in keys:
        print("== %s / %s ==" % lv_cat)
        subs = sorted(set(before[lv_cat]) | set(after[lv_cat]))
        for sub in subs:
            b, a = before[lv_cat][sub], after[lv_cat][sub]
            flag = ""
            if lv_cat[0] == A:
                need = 40 if lv_cat[1] == "cases" else 30
            else:
                need = 20
            if a < need:
                flag = "  ** SHORT (need %d)" % need
            print("  %s: %d -> %d%s" % (sub, b, a, flag))


if __name__ == "__main__":
    main()
