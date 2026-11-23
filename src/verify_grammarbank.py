#!/usr/bin/env python3
"""Verify Grammar-tab bank items in exercises.json.

Checks (all items, structurally; form checks focus on src='bank'):
  - exactly one ___ in s
  - a unique, not equal to any distractor; bank items have 3 unique distractors
  - translation and explanation present
  - no duplicate fill-in s among bank items, and no bank fill-in s that copies an original
  - for a Cyrillic lemma (or list of lemmas) in base, the answer is a valid form
    (pymorphy3 + forms_table + pronouns + дома/домой + какой + listed adverbs)

Run from the repo root:
  /workspace/venv-morph/bin/python src/verify_grammarbank.py
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pymorphy3
import grammarbank_exercises as g

M = pymorphy3.MorphAnalyzer()
EX = json.load(open(os.path.join(ROOT, "exercises.json")))

CYR = re.compile(r"[А-Яа-яЁё]")
SPLIT = re.compile(r"\s*[·/]\s*")

KAKOY = set(
    "какой какая какое какие какого какую какому каким какой какими каком каких".split()
)
DOM = set("дом дома дому домом доме домам домами домах домой".split())
# Common adverb / particle answers used with list-style bases.
ADVERBS = set(
    "всегда часто иногда редко никогда обычно "
    "никто ничто ничего никого никому ничем ничём нигде никуда никогда "
    "ни разу почти никогда время от времени "
    "в на".split()
)


def norm(w):
    return (w or "").strip().lower().replace("ё", "е")


def is_cyr(s):
    return bool(CYR.search(s or ""))


def tokens(base):
    if not base or not is_cyr(base):
        return []
    if any(x in base for x in ("Which ", "imperfective", "perfective")) and not re.search(r"[А-Яа-яЁё]{3,}", base.split("/")[0] if "/" in base else ""):
        # English contrast label, possibly with a Russian pair later
        parts = SPLIT.split(base)
        return [p.strip() for p in parts if is_cyr(p) and "imperfective" not in p.lower()]
    return [p.strip() for p in SPLIT.split(base) if p.strip() and is_cyr(p)]


def lexeme_forms(word):
    out = set()
    for p in M.parse(word):
        try:
            for x in p.lexeme:
                out.add(norm(x.word))
        except Exception:
            pass
        out.add(norm(p.normal_form))
        out.add(norm(p.word))
    return out


def lemma_forms(lemma):
    out = {norm(lemma)}
    out |= lexeme_forms(lemma)
    if lemma in g.PRONOUNS:
        out |= {norm(v) for v in g.PRONOUNS[lemma].values()}
    if lemma in g.MANUAL:
        out |= {norm(v) for v in g.MANUAL[lemma].values()}
    if lemma == "какой":
        out |= {norm(x) for x in KAKOY}
    if lemma == "дом":
        out |= {norm(x) for x in DOM}
    if norm(lemma) in {norm(x) for x in ADVERBS} or lemma in ADVERBS:
        out.add(norm(lemma))
    try:
        nf = g.noun_forms(lemma)
        out |= {norm(v) for v in nf.values() if v and v != "-"}
    except Exception:
        pass
    if any(p.tag.POS == "INFN" for p in M.parse(lemma)):
        try:
            keys = list(g.PERS) + list(g.PAST)
            out |= {norm(v) for v in g.vparadigm(lemma, keys).values() if v}
        except Exception:
            pass
    # loc2
    if lemma in g.LOC2:
        out.add(norm(g.LOC2[lemma]))
    return out


errs = []

# --- structural ---
seen_orig_s = {}
seen_bank_s = {}
seen_blank = set()  # (s, a) for s == '___'
for e in EX:
    eid = e.get("id")
    s, a, d = e.get("s") or "", e.get("a") or "", e.get("d") or []
    if s.count("___") != 1:
        errs.append("id %s: s should have exactly one ___: %r" % (eid, s))
    if not a:
        errs.append("id %s: empty answer" % eid)
    dlow = [x.lower() for x in d]
    if a and a.lower() in dlow:
        errs.append("id %s: answer %r is also a distractor" % (eid, a))
    if len(dlow) != len(set(dlow)):
        errs.append("id %s: duplicate distractors %s" % (eid, d))
    if e.get("src") == "bank":
        if len(d) < 3:
            errs.append("id %s: bank item has fewer than 3 distractors: %s" % (eid, d))
        if not (e.get("translation") or "").strip():
            errs.append("id %s: missing translation: %s" % (eid, s))
        if not (e.get("ex") or "").strip():
            errs.append("id %s: missing explanation: %s" % (eid, s))
        if s == "___":
            key = ("___", a)
            if key in seen_blank:
                errs.append("id %s: duplicate choice-only item %r" % (eid, a))
            seen_blank.add(key)
        else:
            if s in seen_bank_s:
                errs.append("id %s: duplicate bank sentence %r (also id %s)" % (eid, s, seen_bank_s[s]))
            seen_bank_s[s] = eid
    else:
        if s != "___":
            seen_orig_s.setdefault(s, eid)

for s, eid in seen_bank_s.items():
    if s in seen_orig_s:
        errs.append("id %s: bank sentence copies original id %s: %r" % (eid, seen_orig_s[s], s))

# --- form checks (bank items) ---
checked = skipped = 0
for e in EX:
    if e.get("src") != "bank":
        continue
    base, a = e.get("base") or "", e.get("a") or ""
    toks = tokens(base)
    if not toks:
        skipped += 1
        continue
    forms = set()
    for t in toks:
        forms |= lemma_forms(t)
        forms.add(norm(t))
    # listed multi-word adverbs as whole tokens
    forms |= {norm(x) for x in ADVERBS}
    if norm(a) in forms:
        checked += 1
    else:
        # last chance: any parse of the answer has a normal_form in toks
        ok = False
        for p in M.parse(a):
            if any(norm(p.normal_form) == norm(t) for t in toks):
                ok = True
                break
        if ok:
            checked += 1
        else:
            errs.append("id %s: %r is not a form of %r in %r" % (e.get("id"), a, base, e.get("s")))

# --- counts vs targets ---
from collections import defaultdict, Counter
c = defaultdict(Counter)
for e in EX:
    c[(e["level"], e["cat"])][e["sub"]] += 1
A, B = "A1-A2", "B1-C1"
short = []
for lv_cat, subs in sorted(c.items()):
    for sub, n in sorted(subs.items()):
        need = 40 if (lv_cat[0] == A and lv_cat[1] == "cases") else (30 if lv_cat[0] == A else 20)
        if n < need:
            short.append("%s / %s / %s: %d (need %d)" % (lv_cat[0], lv_cat[1], sub, n, need))
if short:
    errs.append("short pools:\n  " + "\n  ".join(short))

if errs:
    print("%d problem(s):" % len(errs))
    for x in errs[:60]:
        print(" -", x)
    if len(errs) > 60:
        print(" ... and %d more" % (len(errs) - 60))
    sys.exit(1)

print("ok", len(EX), "exercises;", sum(1 for e in EX if e.get("src") == "bank"), "bank;",
      "forms checked", checked, "skipped", skipped, "; no short pools")
