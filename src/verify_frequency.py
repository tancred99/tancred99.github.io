# Checks the "frequency" drills in exercises.json (никогда / иногда / всегда / часто / редко).
# Run with: /workspace/venv-morph/bin/python src/verify_frequency.py
#  - structure: unique ids, one blank, answer not among distractors, levels/subs present
#  - every Cyrillic word in the correct sentences is in the OpenCorpora dictionary (pymorphy3)
#  - double-negative rule: in every correct sentence, each ни-word (никогда, ничего, никто, ни разу…) has не before the verb;
#    every option that keeps a ни-word but drops не is marked wrong; «всегда/часто/редко» answers never sit before a bare не
import json, re, sys
import pymorphy3
M = pymorphy3.MorphAnalyzer()
X = json.load(open("exercises.json"))
F = [e for e in X if e.get("cat") == "frequency"]
errs = []
ids = [e["id"] for e in X]
if len(ids) != len(set(ids)): errs.append("duplicate ids")
NI = re.compile(r"\b(никогда|ничего|ничто|никто|никому|никого|никуда|нигде|ни разу)\b", re.I)
WORD = re.compile(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)?")
def filled(e, opt): return e["s"].replace("___", opt)
def clauses(s): return re.split(r"[.!?:—]|, (?:а|но|когда|поэтому|кроме)\b", s)
def neg_ok(s):
    # each clause that contains a ни-word must also contain the particle не (not «ни» alone, not «не ни…»)
    for c in clauses(s):
        if NI.search(c) and not re.search(r"\bне\b", c, re.I): return False
        if re.search(r"\bне\s+(никогда|ничего|никто)\b", c, re.I): return False
        if re.search(r"\bни\s+(когда|работаю)\b", c, re.I): return False
    return True
unknown = set(); meaning = []
# self-test of the rule
assert neg_ok("Я никогда не пью водку.") and not neg_ok("Я никогда пью водку.") and not neg_ok("Я не никогда пью водку.")
assert neg_ok("Я иногда не работаю в субботу.") and not neg_ok("Я ни разу был в Москве.")
for e in F:
    if e["s"].count("___") != 1: errs.append("blank count %d" % e["id"])
    if e["a"] in e["d"] or len(set(e["d"])) != len(e["d"]) or len(e["d"]) < 2: errs.append("options %d" % e["id"])
    if e["level"] not in ("A1-A2", "B1-C1"): errs.append("level %d" % e["id"])
    for k in ("ex", "translation", "sub", "base"):
        if not e.get(k) and not (k == "translation" and e.get("choiceOnly")): errs.append("missing %s %d" % (k, e["id"]))
    good = filled(e, e["a"])
    if not neg_ok(good): errs.append("double-negative rule broken in answer %d: %s" % (e["id"], good))
    for w in WORD.findall(good):
        if len(w) > 1 and not M.word_is_known(w.lower()): unknown.add(w)
    # a positive adverb answer must not stand right before не (always/often/rarely + не is a different meaning)
    if re.search(r"\b(всегда|часто|редко)\s+не\b", good, re.I) and e["sub"].startswith("context"):
        errs.append("positive adverb + не in answer %d" % e["id"])
    # gap items whose sentence has «___ не» need a negative answer (никогда, ни разу, почти никогда) and vice versa
    if e["s"].startswith("___") is False and "___ не " in e["s"] and e["a"].lower() not in ("никогда", "ни разу", "почти никогда", "ничего", "никто"):
        errs.append("blank before не but answer is %s (%d)" % (e["a"], e["id"]))
    # any distractor that keeps a ни-word and is grammatical by this rule would be a second right answer for sentence items
    if e.get("choiceOnly"):
        for d in e["d"]:
            if NI.search(d) and neg_ok(d) and not re.search(r"(что-то|кто-то|куда-то|нигде|один раз|всегда|почти|иногда|часто)", d, re.I):
                meaning.append("%d: %s  (%s)" % (e["id"], d, e["base"]))
print("frequency items:", len(F), {lv: sum(1 for e in F if e["level"] == lv) for lv in ("A1-A2", "B1-C1")})
subs = {}
for e in F: subs[(e["level"], e["sub"])] = subs.get((e["level"], e["sub"]), 0) + 1
for k, v in sorted(subs.items()): print("  ", k, v)
print("unknown words (check by hand):", sorted(unknown))
print("grammatical distractors that are wrong by meaning (by design; check by hand):"); [print("  ", x) for x in meaning]
print("ERRORS:", len(errs)); [print("  ", x) for x in errs]
sys.exit(1 if errs else 0)
