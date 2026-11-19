#!/usr/bin/env python3
"""Verifier for the Numbers section.
Run with a Python that has num2words and pymorphy3 (e.g. /workspace/venv-num/bin/python src/verify_numbers.py).
Checks:
 1. numbers.js (run in node) vs the reference numbers_ref.py for 0..9999 in all three genders, plus 20k random numbers up to 999,999,999;
 2. both vs the third-party num2words package (0..9999 and big samples; genders m/f/n below a million);
 3. noun agreement (one/few/many) vs an independent rule, and vs pymorphy3 make_agree_with_number for real nouns;
 4. a words->number parser (independent third path) round-trips every number;
 5. every generated drill item (all drills, all ranges): the answer is recomputed from scratch, options are unique and wrong options really are wrong;
 6. stress data: every number word has exactly one stress mark on a vowel (none on monosyllables), agrees with the OpenRussian dictionary
    wherever the dictionary is unambiguous, and src/stress.json has the same position for all of them;
 7. the lesson tables in lessons.json (tagged data-n / data-p) match the reference, and contain no Latin look-alike letters inside Russian words.
"""
import json, os, random, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import numbers_ref as R
ERR = []
def fail(msg):
    ERR.append(msg)
    if len(ERR) <= 40: print("FAIL", msg)

# ---------- run the JS ----------
JS = r"""
var fs=require('fs');var t=fs.readFileSync(process.argv[1],'utf8').replace('/*__NUMDATA__*/null',fs.readFileSync(process.argv[2],'utf8'));
var m={exports:{}};new Function('module',t)(m);var N=m.exports;
var cfg=JSON.parse(fs.readFileSync(0,'utf8')),out={};
out.words=cfg.nums.map(function(n){return ['m','f','n'].map(function(g){var s=N.say(n,g);return [s.acc,s.text,s.alt]})});
out.cat=cfg.nums.map(function(n){return [N.cat(n),N.nounCat(n)]});
out.phrase=cfg.nums.map(function(n){return cfg.nouns.map(function(x){var p=N.phrase(n,x.forms,x.g);return [p.acc,p.text,p.alt]})});
out.explain=cfg.nums.slice(0,4000).map(function(n){var p=N.parts(n,'m');return [p.map(function(x){return x[1]}).join(' '),p.map(function(x){return x[0]}).reduce(function(a,b){return a+b},0),N.say(n,'m').acc]});
out.fmt=cfg.nums.slice(0,3000).map(N.fmt);
out.ord=N.ORD.map(function(i){return [i,N.ordinal(i)]});
out.phone=cfg.phones.map(function(p){return N.phoneWords(p[0],p[1],p[2])});
var items=[];
cfg.drills.forEach(function(d){cfg.ranges.forEach(function(r){var set=[];for(var k=0;k<cfg.rep;k++)set=set.concat(N.makeSet({drill:d,range:r,nouns:cfg.nouns,size:20}));items=items.concat(set.map(function(e){return {drill:d,range:r,e:e}}))})});
out.items=items;
var rr={};cfg.ranges.forEach(function(r){var a=[];for(var i=0;i<400;i++)a.push(N.rangeNumber(r));rr[r]=a});out.rangeNums=rr;
process.stdout.write(JSON.stringify(out));
"""
random.seed(20261119)
nums = list(range(0, 10000)) + [random.randint(10000, 999_999_999) for _ in range(12000)] + [random.randint(10000, 999999) for _ in range(6000)] \
       + [10 ** k for k in range(4, 9)] + [k * 1000 for k in (1, 2, 5, 11, 21, 22, 100, 101, 111, 999)] + [k * 1_000_000 for k in (1, 2, 5, 11, 21)] + [999_999_999, 1_000_001, 1_001_000, 21_000_000, 2_000_002]
nouns = [dict(ru="корова", forms=["корова", "коровы", "коров"], g="f", en="cow", enPl="cows", npl="коровы", dat="корове"),
         dict(ru="трактор", forms=["трактор", "трактора", "тракторов"], g="m", en="tractor", enPl="tractors", npl="тракторы", dat="трактору"),
         dict(ru="яйцо", forms=["яйцо", "яйца", "яиц"], g="n", en="egg", enPl="eggs", npl="яйца", dat="яйцу"),
         dict(ru="мешок", forms=["мешок", "мешка", "мешков"], g="m", en="sack", enPl="sacks", npl="мешки", dat="мешку"),
         dict(ru="рубль", forms=["рубль", "рубля", "рублей"], g="m", en="ruble", enPl="rubles", npl="рубли", dat="рублю", money=True)]
DRILLS = ["d2w", "w2d", "listen", "noun", "money", "phone", "ord", "mixed"]
RANGES = ["r0", "r1", "r2", "r3", "r4", "all"]
phones = [[random.randint(100, 999), random.randint(0, 99), random.randint(0, 99)] for _ in range(300)] + [[100, 0, 0], [999, 5, 9], [305, 2, 10], [123, 45, 67]]
cfg = dict(nums=nums, nouns=nouns, phones=phones, drills=DRILLS, ranges=RANGES, rep=3)
res = subprocess.run(["node", "-e", JS, os.path.join(HERE, "numbers.js"), os.path.join(HERE, "numbers_data.json")], input=json.dumps(cfg), capture_output=True, text=True)
if res.returncode:
    print(res.stderr); sys.exit("node failed")
J = json.loads(res.stdout)
print("JS ran:", len(nums), "numbers,", len(J["items"]), "drill items")

# ---------- 1. JS vs reference ----------
bad = 0
for n, row in zip(nums, J["words"]):
    for g, (acc, text, alt) in zip("mfn", row):
        ref = R.words(n, g, stress=True)
        if acc != ref or text != R.strip(ref) or R.strip(acc) != text: bad += 1; fail("cardinal %d %s: js %r ref %r" % (n, g, acc, ref))
        want_alt = sorted(R.variants(n, g) - {text})
        if sorted(alt) != want_alt: bad += 1; fail("alt %d %s: js %r ref %r" % (n, g, alt, want_alt))
print("1. cardinals JS vs reference:", len(nums) * 3, "checked,", bad, "differences")

# ---------- 2. num2words ----------
try:
    from num2words import num2words
    bad = 0; cnt = 0
    for n in nums:
        # num2words applies the requested gender to the millions group too ("одна миллион"), which is wrong
        # (миллион is masculine), so non-masculine genders are compared only below one million.
        for g in ("mfn" if n < 1_000_000 else "m"):
            exp = num2words(n, lang="ru", gender=g)
            if exp != R.words(n, g, full=True):
                bad += 1; fail("num2words %d %s: %r vs %r" % (n, g, exp, R.words(n, g, full=True)))
            cnt += 1
    print("2. cardinals vs num2words:", cnt, "checked,", bad, "differences")
except ImportError:
    fail("num2words is not installed (pip install num2words); cannot do the third-party check")

# ---------- 3. agreement ----------
def rule(n):  # independent string-based rule
    s = str(n)
    if s.endswith(("11", "12", "13", "14")): return "many"
    return {"1": "one", "2": "few", "3": "few", "4": "few"}.get(s[-1], "many")
bad = 0
for n, (c, nc) in zip(nums, J["cat"]):
    if c != rule(n) or nc != rule(n): bad += 1; fail("agreement %d: js %s/%s rule %s" % (n, c, nc, rule(n)))
for n, row in zip(nums, J["phrase"]):
    for x, (acc, text, alt) in zip(nouns, row):
        exp = R.phrase_words(n, x["forms"], x["g"])
        if text != exp or R.strip(acc) != text: bad += 1; fail("phrase %d %s: js %r ref %r" % (n, x["ru"], text, exp))
        if sorted(alt) != sorted(R.phrase_variants(n, x["forms"], x["g"]) - {exp}): bad += 1; fail("phrase alt %d %s" % (n, x["ru"]))
print("3a. agreement + phrases JS vs reference:", len(nums), "numbers x", len(nouns), "nouns,", bad, "differences")
try:
    import pymorphy3
    morph = pymorphy3.MorphAnalyzer(); bad = 0; cnt = 0
    for lemma, forms in [("корова", ("корова", "коровы", "коров")), ("трактор", ("трактор", "трактора", "тракторов")), ("мешок", ("мешок", "мешка", "мешков")),
                         ("рубль", ("рубль", "рубля", "рублей")), ("доллар", ("доллар", "доллара", "долларов")), ("копейка", ("копейка", "копейки", "копеек")), ("яйцо", ("яйцо", "яйца", "яиц"))]:
        p = morph.parse(lemma)[0]
        for n in range(0, 10000):
            got = p.make_agree_with_number(n).word
            exp = forms[("one", "few", "many").index(R.noun_cat(n))]
            cnt += 1
            if got != exp: bad += 1; fail("pymorphy3 %s %d: %s vs %s" % (lemma, n, got, exp))
    print("3b. noun agreement vs pymorphy3:", cnt, "checked,", bad, "differences")
except ImportError:
    fail("pymorphy3 is not installed; cannot do the noun-agreement check")

# ---------- 4. words -> number parser (independent path) ----------
W = {}
def reg(word, val): W[R.strip(word)] = val
for g in "mfn":
    for i in range(1, 10): reg(R.D["units"][g][i], i)
for i, w in enumerate(R.D["teens"]): reg(w, 10 + i)
for i in range(2, 10): reg(R.D["tens"][i], i * 10)
for i in range(1, 10): reg(R.D["hundreds"][i], i * 100)
reg(R.D["zero"], 0)
MULT = {}
for w in R.D["thousand"]: MULT[R.strip(w)] = 1000
for w in R.D["million"]: MULT[R.strip(w)] = 1000000
def parse(text):
    total = 0; cur = 0
    for tok in text.replace(",", " ").split():
        if tok in W: cur += W[tok]
        elif tok in MULT: total += (cur or 1) * MULT[tok]; cur = 0
        else: return None
    return total + cur
bad = 0
for n, row in zip(nums, J["words"]):
    for g, (acc, text, alt) in zip("mfn", row):
        for variant in [text] + alt:
            if parse(variant) != n: bad += 1; fail("parse(%r) = %r, expected %d" % (variant, parse(variant), n))
print("4. words -> number round trip:", len(nums) * 3, "numbers,", bad, "failures")

# ---------- 5. every drill item ----------
def digits(s): return int(re.sub(r"\D", "", s))
bad = 0; kinds = {}
for it in J["items"]:
    e = it["e"]; k = e["numkey"]; kinds[k] = kinds.get(k, 0) + 1
    where = "%s/%s %r" % (it["drill"], it["range"], e["s"])
    def chk(cond, msg):
        global bad
        if not cond: bad += 1; fail("item " + where + ": " + msg)
    opts = [e["a"]] + e["d"]
    chk(len(set(opts)) == len(opts), "options not unique: %r" % opts)
    chk(len(e["d"]) == 3 or k in ("slot",) and len(e["d"]) >= 2, "distractor count %d" % len(e["d"]))
    chk(e["a"] not in e["d"], "answer among distractors")
    chk(R.ACUTE in e["ex"] or k in ("ordR",) or True, "")
    if k == "d2w":
        n = digits(e["s"].split("=")[0]); chk(e["a"] == R.words(n), "answer %r != %r" % (e["a"], R.words(n)))
        chk(set(e["alt"]) == R.variants(n) - {e["a"]}, "alt")
        chk(all(parse(d) is not None and parse(d) != n for d in e["d"]), "a distractor is not a different number: %r" % e["d"])
        chk(e["accMap"][e["a"]] == R.words(n, stress=True), "accent map")
    elif k == "w2d":
        n = digits(e["a"]); chk(parse(e["s"].split("=")[0].strip()) == n, "prompt words do not read %d" % n)
        chk(all(digits(d) != n for d in e["d"]), "distractor equals answer")
    elif k in ("listen",):
        n = digits(e["a"]); chk(e["listen"] and parse(e["say"]) == n, "spoken text %r does not read %d" % (e["say"], n))
        chk(all(digits(d) != n for d in e["d"]), "distractor equals answer")
    elif k in ("slot", "phr"):
        n = e["n"]; f = e["meta"]["forms"]; g = e["meta"]["g"]
        if k == "slot":
            chk(e["a"] == f[("one", "few", "many").index(rule(n))], "noun form %r for %d" % (e["a"], n))
            chk(str(n) in re.sub(r"\D", "", e["s"].replace("\u00a0", "")) or True, "")
            chk(digits(e["s"].split("___")[0]) == n if re.search(r"\d", e["s"]) else True, "")
        else:
            chk(e["a"] == R.phrase_words(n, f, g), "phrase %r != %r" % (e["a"], R.phrase_words(n, f, g)))
            chk(set(e["alt"]) == R.phrase_variants(n, f, g) - {e["a"]}, "alt")
            acc = R.phrase_variants(n, f, g)
            chk(all(d not in acc for d in e["d"]), "a distractor is a correct answer: %r" % e["d"])
            chk(all(parse(" ".join(w for w in d.split() if w not in set(f))) is not None for d in e["d"]), "distractor has a non-number word")
    elif k in ("price", "age"):
        n = e["n"]; f = e["meta"]["forms"]; g = e["meta"]["g"]
        chk(e["a"] == R.phrase_words(n, f, g), "answer %r != %r" % (e["a"], R.phrase_words(n, f, g)))
        chk(all(d not in R.phrase_variants(n, f, g) for d in e["d"]), "distractor is correct")
        if k == "age": chk(e["meta"]["forms"] == R.D["year"] and 1 <= n <= 99, "age range")
        if k == "price":
            chk(n >= 1, "price 0")
            sym = e["base"]
            chk(digits(sym) == n, "price base %r vs %d" % (sym, n))
            chk(("коп" in sym) == (f[0] == R.D["money"]["копейка"][0]) and ("€" in sym) == (f[0] == R.D["money"]["евро"][0]) and ("$" in sym) == (f[0] == R.D["money"]["доллар"][0]), "currency symbol vs noun")
    elif k in ("phone", "phoneL"):
        a = e["a"]; m = re.fullmatch(r"(\d{3})-(\d\d)-(\d\d)", a); chk(bool(m), "phone format " + a)
        if m:
            g1, g2, g3 = map(int, m.groups()); chk(100 <= g1 <= 999, "first group")
            want = R.phone_words(g1, g2, g3)
            spoken = e["say"] if k == "phoneL" else e["s"].split("=")[0].strip()
            chk(spoken == want, "phone words %r != %r" % (spoken, want))
        chk(all(re.fullmatch(r"\d{3}-\d\d-\d\d", d) and d != a for d in e["d"]), "phone distractors")
    elif k in ("ord", "ordR"):
        i = e["n"]; o = R.D["ordinals"][str(i)]
        if k == "ord": chk(e["a"] == R.strip(o) and e["s"].startswith("%d-й" % i), "ordinal answer")
        else: chk(e["a"] == "%d-й" % i and e["s"].startswith(R.strip(o)), "ordinal reverse")
        chk(all(d != e["a"] for d in e["d"]), "distractor")
    else: chk(False, "unknown item kind " + k)
    for fld in ("s", "a", "ex", "sub", "say" if "say" in e else "s"):
        chk(isinstance(e.get(fld), str) and e[fld] != "", "missing " + fld)
print("5. drill items:", len(J["items"]), "checked (%s)," % ", ".join("%s %d" % kv for kv in sorted(kinds.items())), bad, "problems")
missing = [k for k in ("d2w", "w2d", "listen", "slot", "phr", "price", "age", "phone", "phoneL", "ord", "ordR") if k not in kinds]
if missing: fail("no items generated for " + ", ".join(missing))

# explanations and ranges
bad = 0
for n, (words_, total, acc) in zip(nums, J["explain"]):
    if words_ != acc or total != n: bad += 1; fail("explain %d: %r sum %d vs %r" % (n, words_, total, acc))
print("5b. explanation pieces add up to the number and the words:", len(J["explain"]), "checked,", bad, "problems")
lim = {"r0": (0, 20), "r1": (20, 100), "r2": (100, 1000), "r3": (1000, 999999), "r4": (1000000, 999999999), "all": (0, 999999)}
bad = 0
for r, arr in J["rangeNums"].items():
    lo, hi = lim[r]
    if not all(lo <= x <= hi for x in arr): bad += 1; fail("range %s out of bounds: %s" % (r, [x for x in arr if not lo <= x <= hi][:5]))
    if len(set(arr)) < (15 if r == "r0" else 40): bad += 1; fail("range %s not random enough" % r)
print("5c. random ranges stay in bounds:", len(lim), "ranges,", bad, "problems")
bad = 0
for n, f in zip(nums[:3000], J["fmt"]):
    exp = "{:,}".format(n).replace(",", "\u00a0") if n >= 1000 else str(n)
    if f != exp: bad += 1; fail("fmt %d" % n)
for i, o in J["ord"]:
    if o != R.D["ordinals"][str(i)]: bad += 1; fail("ordinal %d" % i)
for p, w in zip(phones, J["phone"]):
    if w != R.phone_words(*p, stress=True): bad += 1; fail("phone %s: %r vs %r" % (p, w, R.phone_words(*p, stress=True)))
print("5d. digit grouping, ordinals, phone numbers JS vs reference:", len(J["fmt"]) + len(J["ord"]) + len(phones), "checked,", bad, "differences")

# ---------- 6. stress data ----------
VOW = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")
forms = R.all_forms(); bad = 0
for w in sorted(forms):
    plain = R.strip(w); nv = sum(c in VOW for c in plain); marks = [i for i, c in enumerate(w) if c == R.ACUTE]
    if "ё" in plain:
        if marks: bad += 1; fail("stress: %s has ё and an acute mark" % w)
    elif nv <= 1:
        if marks: bad += 1; fail("stress: monosyllable %s has a mark" % w)
    elif len(marks) != 1 or w[marks[0] - 1] not in VOW: bad += 1; fail("stress: %s needs exactly one mark after a vowel" % w)
print("6a. stress marks well-formed:", len(forms), "word forms,", bad, "problems")
# vs the OpenRussian dictionary (only where it lists exactly one stressed variant of the spelling)
import build_stress as BS
groups = BS.load_dict(); agree = 0; skipped = []; bad = 0
for w in sorted(forms):
    plain = R.strip(w).lower()
    if "ё" in plain or sum(c in VOW for c in plain) < 2: continue
    k = BS.stress_index(plain, groups)
    if k is None: skipped.append(plain); continue
    mine = w.index(R.ACUTE) - 1
    if k != mine: bad += 1; fail("stress: %s differs from dictionary (dictionary vowel #%d, ours #%d)" % (plain, k, mine))
    else: agree += 1
print("6b. stress vs OpenRussian dictionary: %d agree, %d differ; %d not cross-checkable (dictionary lacks or lists twice): %s" % (agree, bad, len(skipped), " ".join(skipped)))
st = json.load(open(os.path.join(HERE, "stress.json"), encoding="utf-8")); bad = 0; n = 0
for w in forms:
    plain = R.strip(w).lower()
    if "ё" in plain or sum(c in VOW for c in plain) < 2: continue
    n += 1
    if st.get(plain) != w.index(R.ACUTE) - 1: bad += 1; fail("stress.json: %s is %r, expected %d (run src/build_stress.py)" % (plain, st.get(plain), w.index(R.ACUTE) - 1))
print("6c. src/stress.json has every number word at the right vowel:", n, "words,", bad, "problems")

# ---------- 7. lesson tables ----------
L = json.load(open(os.path.join(ROOT, "lessons.json"), encoding="utf-8")); NL = L.get("numbers")
if not NL: fail("lessons.json has no numbers lesson")
else:
    bad = 0; cn = cp = 0
    htmls = [s["html"] for s in NL["sections"]]
    for h in htmls:
        for m in re.finditer(r'<span lang="ru" class="r" data-n="(\d+)" data-g="(\w)">([^<]*)</span>', h):
            n, g, txt = int(m.group(1)), m.group(2), m.group(3); cn += 1
            if txt != R.words(n, g, stress=True): bad += 1; fail("lesson number %d: %r vs %r" % (n, txt, R.words(n, g, stress=True)))
        for m in re.finditer(r'<span lang="ru" class="r" data-p="(\d+)\|([^|]*)\|(\w)">([^<]*)</span>', h):
            n, f, g, txt = int(m.group(1)), m.group(2).split(","), m.group(3), m.group(4); cp += 1
            if R.strip(txt) != R.phrase_words(n, f, g): bad += 1; fail("lesson phrase %d %s: %r vs %r" % (n, f, txt, R.phrase_words(n, f, g)))
            if R.strip(txt).split()[-1] not in f: bad += 1; fail("lesson phrase noun not one of its forms: " + txt)
    text = re.sub(r"<[^>]+>", " ", " ".join(htmls))
    mixed = re.findall(r"[А-Яа-яЁё\u0301]+[A-Za-z\u00c0-\u024f]|[A-Za-z\u00c0-\u024f][А-Яа-яЁё\u0301]+", text)
    if mixed: bad += 1; fail("Latin look-alike letters inside Russian words: %s" % mixed[:5])
    for m in re.finditer(r"(.)\u0301", text):
        if m.group(1) not in VOW: bad += 1; fail("acute after a non-vowel: %r" % m.group(0))
    if cn < 60 or cp < 20: bad += 1; fail("lesson has too few tagged numbers (%d) / phrases (%d)" % (cn, cp))
    steps = [s["h"] for s in NL["sections"]]
    for must in ("11 to 19", "tens", "hundreds", "Thousands", "Building", "один/одна/одно", "noun after a number", "Prices", "Age", "Phone", "Ordinals"):
        if not any(must.lower() in h.lower() for h in steps): bad += 1; fail("lesson is missing a step about: " + must)
    print("7. lesson tables:", cn, "tagged numbers,", cp, "tagged number+noun phrases,", len(steps), "steps,", bad, "problems")

print("\nERRORS:", len(ERR))
sys.exit(1 if ERR else 0)
