#!/usr/bin/env python3
"""Build src/stress.json: stress positions for every Cyrillic word that appears in the site's content.

Source: OpenRussian.org dictionary data (Wiktionary-based, hand-corrected; CC BY-SA 4.0),
https://github.com/Badestrand/russian-dictionary . Stressed vowels are marked there with ' after the vowel.
A word gets a stress mark only when it is unambiguous: every dictionary form spelled that way
(across all lemmas, and with е/ё variants) puts the stress on the same vowel. Monosyllables,
words with ё, homographs (ру́ки / руки́, за́мок / замо́к) and words the dictionary lacks get nothing.
Run: python3 src/build_stress.py   (downloads the CSVs to ~/.cache/openrussian on first run)
"""
import csv, json, os, re, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CACHE = os.environ.get("OPENRUSSIAN_DIR", os.path.expanduser("~/.cache/openrussian"))
BASE = "https://raw.githubusercontent.com/Badestrand/russian-dictionary/master/"
FILES = ["nouns.csv", "adjectives.csv", "verbs.csv", "others.csv"]
VOW = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")
WORD = re.compile(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)*")
csv.field_size_limit(10**8)
# Hand-checked additions where the dictionary has a junk duplicate (e.g. "вилка'") or lacks the word.
# Only words with a single possible stress in any context; real homographs (дома, руки, двери, еду, плачу,
# стоит, другом, полу, шкафу, проходите, дорогой) are deliberately left out.
MANUAL = {"вода": "вода'", "вилка": "ви'лка", "полка": "по'лка", "стена": "стена'", "столик": "сто'лик",
          "микроволновка": "микроволно'вка", "провод": "про'вод", "двоих": "двои'х", "воскресе": "воскре'се",
          "нами": "на'ми", "него": "него'", "парке": "па'рке", "анне": "а'нне", "анну": "а'нну", "ивана": "ива'на",
          "родители": "роди'тели", "наших": "на'ших", "статей": "стате'й", "минут": "мину'т", "проволока": "про'волока"}

def fetch():
    os.makedirs(CACHE, exist_ok=True)
    for f in FILES:
        p = os.path.join(CACHE, f)
        if not os.path.exists(p):
            print("downloading", f, file=sys.stderr); urllib.request.urlretrieve(BASE + f, p)

def nvow(w): return sum(c in VOW for c in w)
def enorm(w): return w.replace("ё", "е")

def load_dict():
    """yo-normalized bare form -> set of accented variants (lowercase, ' after stressed vowel)"""
    groups = {}
    for f in FILES:
        with open(os.path.join(CACHE, f), encoding="utf-8") as fh:
            r = csv.reader(fh, delimiter="\t"); head = next(r)
            skip = {"bare", "translations_en", "translations_de", "gender", "partner", "animate", "indeclinable", "sg_only", "pl_only", "aspect"}
            cols = [i for i, h in enumerate(head) if h not in skip]
            for row in r:
                for i in cols:
                    if i >= len(row): continue
                    for v in re.split(r"[,;/]", row[i]):
                        v = v.strip().lower().replace("’", "'").replace("`", "'")
                        v = re.sub(r"[()*!?.]", "", v)
                        if not v or " " in v or not re.fullmatch(r"[а-яё'\-]+", v): continue
                        bare = v.replace("'", "")
                        if not bare: continue
                        groups.setdefault(enorm(bare), set()).add(v)
    return groups

def stress_index(word, groups):
    """index of the stressed vowel in word (lowercase), or None if not known for sure"""
    w = word.lower()
    if "ё" in w or nvow(w) < 2: return None
    vs = groups.get(enorm(w))
    if not vs: return None
    pos = set()
    for v in vs:
        bare = v.replace("'", "")
        if bare != w: return None                 # an ё-spelled homograph (все/всё, небо/нёбо): skip
        if v.count("'") != 1:
            if nvow(bare) >= 2: return None       # dictionary doesn't know (or double stress): skip
            continue
        k = v.index("'") - 1
        if k < 0 or v[k] not in VOW: return None
        pos.add(k)
    return pos.pop() if len(pos) == 1 else None

def content_words():
    words = set()
    def walk(x):
        if isinstance(x, str):
            for m in WORD.findall(x):
                for part in m.split("-"): words.add(part.lower())
                words.add(m.lower())
        elif isinstance(x, dict): [walk(v) for v in x.values()]
        elif isinstance(x, list): [walk(v) for v in x]
    for f in ["exercises.json", "vocab.json", "lessons.json"]:
        walk(json.load(open(os.path.join(ROOT, f), encoding="utf-8")))
    return words

def main():
    fetch(); groups = load_dict(); words = content_words()
    out = {}
    for w in sorted(words):
        if "-" in w: continue  # hyphenated words are stressed part by part at runtime
        k = MANUAL[w].index("'") - 1 if w in MANUAL else stress_index(w, groups)
        if k is not None: out[w] = k
    json.dump(out, open(os.path.join(HERE, "stress.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    poly = [w for w in words if "-" not in w and "ё" not in w and nvow(w) >= 2]
    print("content words", len(words), "multi-syllable without ё", len(poly), "stressed", len(out))

if __name__ == "__main__":
    main()
