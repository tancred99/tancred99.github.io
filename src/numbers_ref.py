"""Reference implementation of Russian number words, used (1) by lessons_src.py to write the Numbers lesson tables
and (2) by verify_numbers.py as the independent check on the JavaScript engine (src/numbers.js).
Word data comes from numbers_data.json ("'" after a vowel = stressed vowel; converted to U+0301 here)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ACUTE = "\u0301"
_RAW = json.load(open(os.path.join(HERE, "numbers_data.json"), encoding="utf-8"))

def _acc(x):
    if isinstance(x, str): return x.replace("'", ACUTE)
    if isinstance(x, list): return [_acc(i) for i in x]
    if isinstance(x, dict): return {k: _acc(v) for k, v in x.items()}
    return x
D = _acc({k: v for k, v in _RAW.items() if not k.startswith("_")})
def strip(s): return s.replace(ACUTE, "")

# ---- which form of the counted noun follows a number: "one" (nom. sg.), "few" (gen. sg.), "many" (gen. pl.)
def cat(n):
    if 11 <= n % 100 <= 14: return "many"
    return {1: "one", 2: "few", 3: "few", 4: "few"}.get(n % 10, "many")

def noun_cat(n):
    """form of the noun counted by the WHOLE number n: round thousands / millions take the genitive plural
    (тысяча рублей, два миллиона рублей), otherwise the last two digits decide"""
    return "many" if n > 0 and n % 1000 == 0 else cat(n)

def _pick(forms, n): return forms[("one", "few", "many").index(cat(n))]

def _hundreds_block(n, g):
    """1..999 as a list of words; g = gender of a final один/два"""
    out = []
    if n >= 100: out.append(D["hundreds"][n // 100]); n %= 100
    if n >= 20:
        out.append(D["tens"][n // 10]); n %= 10
    if 10 <= n <= 19: out.append(D["teens"][n - 10])
    elif n: out.append(D["units"][g][n])
    return out

def cardinal(n, g="m", full=False):
    """words of n as a list. full=True keeps a leading один/одна before тысяча/миллион (the formal variant)."""
    if n == 0: return [D["zero"]]
    out = []
    rest = n
    for size, forms, gen in ((10 ** 6, D["million"], "m"), (1000, D["thousand"], "f")):
        k, rest = divmod(rest, size)
        if k:
            lead_one = (k == 1 and n < size * 1000)       # exactly "one million" / "one thousand" at the start
            if not lead_one or full: out += _hundreds_block(k, gen)
            out.append(_pick(forms, k))
    if rest: out += _hundreds_block(rest, g)
    return out

def words(n, g="m", full=False, stress=False):
    s = " ".join(cardinal(n, g, full))
    return s if stress else strip(s)

def variants(n, g="m"):
    """every accepted spelling (plain): the normal form plus the formal one with один/одна"""
    return {words(n, g), words(n, g, full=True)}

def phrase_words(n, forms, g, stress=False):
    """number + counted noun, e.g. 22 корова -> двадцать две коровы. forms = (one, few, many)"""
    noun = forms[("one", "few", "many").index(noun_cat(n))]
    s = " ".join(cardinal(n, g)) + " " + noun
    return s if stress else strip(s)

def phrase_variants(n, forms, g):
    noun = forms[("one", "few", "many").index(noun_cat(n))]
    return {strip(" ".join(cardinal(n, g, f)) + " " + noun) for f in (False, True)}

def ordinal(i, g="m"):
    w = D["ordinals"][str(i)]
    if g == "m": return w
    if w.endswith("ий"): return w[:-2] + ("ья" if g == "f" else "ье")
    if w.endswith("ый"): return w[:-2] + ("ая" if g == "f" else "ое")
    if w.endswith("о" + ACUTE + "й"):                      # end-stressed: шестой -> шестая, шестое
        return w[:-3] + (("а" if g == "f" else "о") + ACUTE + ("я" if g == "f" else "е"))
    raise ValueError(w)

def phone_words(g1, g2, g3, stress=False):
    out = []
    out.append(" ".join(cardinal(g1)))
    for x in (g2, g3):
        out.append((D["zero"] + " " + " ".join(cardinal(x))) if x < 10 else " ".join(cardinal(x)))
    s = ", ".join(out)
    return s if stress else strip(s)

# ---- every word the generators can produce (for the stress checks)
def all_forms():
    f = set()
    def add(x):
        for w in re.findall(r"[А-Яа-яЁё\u0301]+", x): f.add(w)
    add(D["zero"])
    for g in "mfn":
        for w in D["units"][g]: add(w)
    for k in ("teens", "tens", "hundreds", "thousand", "million", "year"):
        for w in D[k]: add(w)
    for v in D["ordinals"].values(): add(v)
    for forms in D["money"].values():
        for w in forms: add(w)
    for i in D["ordinals"]:
        for g in "fn": add(ordinal(int(i), g))
    return f
