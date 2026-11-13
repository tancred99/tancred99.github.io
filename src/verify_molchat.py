# Checks the "Молчат Дома" song word lists in vocab.json against pymorphy3 (OpenCorpora).
# Run with: /workspace/venv-morph/bin/python src/verify_molchat.py
#  - every noun's hand-written forms (src/forms_table.json) match the dictionary, ё included (колёса, слёзы, перья…)
#  - every verb's aspect and stored conjugation forms (present for impf., future for pf.) match the dictionary
#  - every sentence frame has exactly one blank, every verb/adj/adverb is a real dictionary word
import json, sys
import pymorphy3
M = pymorphy3.MorphAnalyzer()
V = json.load(open("vocab.json")); T = json.load(open("src/forms_table.json"))
W = [w for w in V if w["theme"].startswith("Молчат Дома: ")]
errs = []
NC = {"gen": {"sing", "gent"}, "dat": {"sing", "datv"}, "acc": {"sing", "accs"}, "ins": {"sing", "ablt"},
      "prep": {"sing", "loct"}, "npl": {"plur", "nomn"}, "gpl": {"plur", "gent"}}
PERS = {"1s": {"1per", "sing"}, "2s": {"2per", "sing"}, "3s": {"3per", "sing"}, "1p": {"1per", "plur"}, "2p": {"2per", "plur"}, "3p": {"3per", "plur"}}
GEN = {"m": "masc", "f": "femn", "n": "neut"}
# стоить: OpenCorpora has no present-tense paradigm linked to the infinitive, so check its forms by lemma instead
HAND_VERBS = {"стоить": {"3s": "стоит", "3p": "стоят"}}
def known(word):
    return any(p.is_known for p in M.parse(word))
counts = {}
for w in W:
    counts[w["theme"]] = counts.get(w["theme"], 0) + 1
    if not w.get("en"): errs.append(w["ru"] + ": no English")
    if w["pos"] == "noun":
        ps = [p for p in M.parse(w["ru"]) if p.tag.POS == "NOUN" and "nomn" in p.tag and p.tag.gender == GEN[w["g"]]]
        if not ps: errs.append(w["ru"] + ": not a " + w["g"] + " noun in the dictionary"); continue
        p = ps[0]; t = T[w["ru"]]
        for k, g in NC.items():
            if t[k] == "-": continue
            f = p.inflect(g)
            if not f or f.word != t[k]: errs.append("%s.%s table=%s dict=%s" % (w["ru"], k, t[k], f and f.word))
        for k, v in (w.get("forms") or {}).items():
            if v != t.get(k): errs.append("%s: override %s=%s differs from table %s" % (w["ru"], k, v, t.get(k)))
    elif w["pos"] == "verb":
        inf = w["ru"].split()[0]; tail = w["ru"][len(inf):]
        ps = [p for p in M.parse(inf) if p.tag.POS == "INFN"]
        if not ps: errs.append(w["ru"] + ": not an infinitive"); continue
        asp = "impf" if ps[0].tag.aspect == "impf" else "pf"
        if w.get("asp") != asp: errs.append("%s: aspect %s, dictionary says %s" % (w["ru"], w.get("asp"), asp))
        if ("(" + asp + ".)") not in w["en"] and ("(" + asp + ".)") not in w["en"].replace(") +", ")"): errs.append(w["ru"] + ": English doesn't mark aspect " + asp)
        if not w.get("conj"): errs.append(w["ru"] + ": no conjugation forms"); continue
        for k, v in w["conj"].items():
            if inf in HAND_VERBS:
                exp = HAND_VERBS[inf][k]
                ok = v == exp and any(p.normal_form == inf and PERS[k] <= set(p.tag.grammemes) for p in M.parse(v))
                if not ok: errs.append("%s.%s=%s not confirmed" % (w["ru"], k, v))
                continue
            f = ps[0].inflect(PERS[k] | {"indc", "pres" if asp == "impf" else "futr"})
            if not f or f.word + tail != v: errs.append("%s.%s stored=%s dict=%s" % (w["ru"], k, v, f and f.word + tail))
        if len(w["conj"]) < 2: errs.append(w["ru"] + ": need at least 2 persons for distractors")
        for k, fr in (w.get("frames") or {}).items():
            if fr.count("{}") != 1: errs.append(w["ru"] + ": frame " + k + " needs one {}")
            if k not in w["conj"]: errs.append(w["ru"] + ": frame for missing person " + k)
    else:
        if not known(w["ru"]): errs.append(w["ru"] + ": unknown word")
print(counts, "total", len(W))
print("errors", len(errs)); [print(" ", e) for e in errs]
sys.exit(1 if errs else 0)
