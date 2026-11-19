/* Russian numbers: number -> words (with stress), agreement of the counted noun, and the Numbers drill generators.
   Plain ES5. The word tables come from numbers_data.json (build.py pastes them in at the marker below).
   Exposes window.RuNumbers. Checked against an independent reference by src/verify_numbers.py. */
var RuNumbers = (function () {
  "use strict";
  var A = "\u0301", NB = "\u00a0";
  var RAW = /*__NUMDATA__*/null;
  function acc(x) {
    if (typeof x === "string") return x.replace(/'/g, A);
    if (Array.isArray(x)) return x.map(acc);
    var o = {}; Object.keys(x).forEach(function (k) { if (k.charAt(0) !== "_") o[k] = acc(x[k]); }); return o;
  }
  var D = acc(RAW);
  function strip(s) { return String(s).replace(/\u0301/g, ""); }
  function rnd(n) { return Math.floor(Math.random() * n); }
  function pick(a) { return a[rnd(a.length)]; }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = rnd(i + 1), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function between(a, b) { return a + rnd(b - a + 1); }
  function fmt(n) { var s = String(n); return n >= 1000 ? s.replace(/\B(?=(\d{3})+(?!\d))/g, NB) : s; }

  // ---------- agreement ----------
  var CATS = ["one", "few", "many"];
  function cat(n) {
    var m = n % 100; if (m >= 11 && m <= 14) return "many";
    var d = n % 10; return d === 1 ? "one" : (d >= 2 && d <= 4) ? "few" : "many";
  }
  // form of the noun counted by the whole number: round thousands/millions are nouns themselves and take the genitive plural
  function nounCat(n) { return (n > 0 && n % 1000 === 0) ? "many" : cat(n); }
  function form(forms, c) { return forms[CATS.indexOf(c)]; }

  // ---------- cardinals ----------
  function block(n, g) {
    var out = [], h = Math.floor(n / 100), r = n % 100;
    if (h) out.push(D.hundreds[h]);
    if (r >= 20) { out.push(D.tens[Math.floor(r / 10)]); r %= 10; }
    if (r >= 10) out.push(D.teens[r - 10]);
    else if (r) out.push(D.units[g][r]);
    return out;
  }
  function cardinal(n, g, full) {
    g = g || "m";
    if (n === 0) return [D.zero];
    var out = [], rest = n, steps = [[1000000, D.million, "m"], [1000, D.thousand, "f"]];
    for (var i = 0; i < steps.length; i++) {
      var size = steps[i][0], k = Math.floor(rest / size); rest -= k * size;
      if (k) {
        var lead = (k === 1 && n < size * 1000);
        if (!lead || full) out = out.concat(block(k, steps[i][2]));
        out.push(form(steps[i][1], cat(k)));
      }
    }
    if (rest) out = out.concat(block(rest, g));
    return out;
  }
  // {acc, text, alt}: stressed text, plain text, other accepted spellings (plain)
  function say(n, g) {
    var a = cardinal(n, g).join(" "), full = cardinal(n, g, true).join(" "), alt = strip(full) !== strip(a) ? [strip(full)] : [];
    return { acc: a, text: strip(a), alt: alt };
  }
  function phrase(n, forms, g) {
    var noun = form(forms, nounCat(n)), a = cardinal(n, g).join(" ") + " " + noun, full = cardinal(n, g, true).join(" ") + " " + noun;
    return { acc: a, text: strip(a), alt: strip(full) !== strip(a) ? [strip(full)] : [] };
  }
  // pieces for the explanation: [value, accented words]. The final group is split into hundreds / tens / units.
  function parts(n, g) {
    g = g || "m";
    if (n === 0) return [[0, D.zero]];
    var out = [], rest = n, steps = [[1000000, D.million, "m"], [1000, D.thousand, "f"]];
    for (var i = 0; i < steps.length; i++) {
      var size = steps[i][0], k = Math.floor(rest / size); rest -= k * size;
      if (k) {
        var lead = (k === 1 && n < size * 1000), w = lead ? [] : block(k, steps[i][2]);
        w.push(form(steps[i][1], cat(k))); out.push([k * size, w.join(" ")]);
      }
    }
    if (rest) {
      var h = Math.floor(rest / 100), r = rest % 100;
      if (h) out.push([h * 100, D.hundreds[h]]);
      if (r >= 20) { var t = Math.floor(r / 10); out.push([t * 10, D.tens[t]]); r %= 10; if (r) out.push([r, D.units[g][r]]); }
      else if (r >= 10) out.push([r, D.teens[r - 10]]);
      else if (r) out.push([r, D.units[g][r]]);
    }
    return out;
  }
  function explain(n, g) {
    var p = parts(n, g);
    if (p.length === 1) return fmt(n) + " = " + p[0][1];
    return p.map(function (x) { return fmt(x[0]) + " = " + x[1]; }).join(" + ");
  }
  function ordinal(i) { return D.ordinals[String(i)]; }
  function phoneWords(g1, g2, g3) {
    var out = [cardinal(g1).join(" ")];
    [g2, g3].forEach(function (x) { out.push((x < 10 ? D.zero + " " : "") + cardinal(x).join(" ")); });
    return out.join(", ");
  }

  // ---------- random numbers ----------
  var RANGES = [["r0", "0–20"], ["r1", "20–100"], ["r2", "100–1000"], ["r3", "1 000+"], ["r4", "1 000 000+"]];
  function roundish(n, keep) { var s = String(n); if (s.length <= keep) return n; var z = Math.pow(10, s.length - keep); return Math.round(n / z) * z; }
  function rangeNumber(key) {
    var d;
    switch (key) {
      case "r0": return between(0, 20);
      case "r1": return rnd(10) < 4 ? between(2, 10) * 10 : between(21, 99);
      case "r2": d = rnd(10); return d < 3 ? between(1, 10) * 100 : d < 4 ? between(2, 19) * 50 : between(100, 999);
      case "r3": d = pick([4, 4, 5, 6]); var n3 = between(Math.pow(10, d - 1), Math.pow(10, d) - 1);
        if (rnd(10) < 4) n3 = roundish(n3, 2); return Math.min(999999, Math.max(1000, n3));
      case "r4": var m = rnd(2) ? between(1, 20) : between(1, 999), n4 = m * 1000000;
        if (rnd(10) < 4) n4 += roundish(between(1, 999) * 1000, 2); return Math.min(999999999, n4);
      default: return rangeNumber(pick(["r0", "r1", "r1", "r2", "r2", "r3"]));
    }
  }

  // ---------- look-alike numbers for multiple choice ----------
  function similar(n, want) {
    var s = String(n), L = s.length, set = {}, hot = [], i;
    function add(m, h) { if (m >= 0 && m !== n && m < 1000000000 && String(m).length === L && !set[m]) { set[m] = 1; if (h) hot.push(m); } }
    [1, 2, 10, 100, 1000].forEach(function (st) { if (st <= n || st < 100) { add(n + st); add(n - st); } });
    for (i = 0; i < L; i++) {
      var pow = Math.pow(10, L - 1 - i), dig = +s.charAt(i);
      for (var v = (i === 0 && L > 1 ? 1 : 0); v <= 9; v++) if (v !== dig) add(n + (v - dig) * pow);
    }
    for (i = 0; i + 1 < L; i++) { var sw = s.split(""); var t = sw[i]; sw[i] = sw[i + 1]; sw[i + 1] = t; if (sw[0] !== "0" || L === 1) add(+sw.join(""), true); }
    var tail = n % 100, base = n - tail;      // teens vs tens: 13/30, 14/40 ... 19/90
    if (tail > 10 && tail < 20) add(base + (tail - 10) * 10, true);
    if (tail >= 30 && tail % 10 === 0) add(base + 10 + tail / 10, true);
    var all = Object.keys(set).map(Number), h = shuffle(hot.filter(function (m) { return set[m]; })), rest = shuffle(all.filter(function (m) { return h.indexOf(m) < 0; }));
    var out = h.slice(0, 2).concat(rest).slice(0, want || 3);
    if (out.length < (want || 3)) { for (i = 0; i < 40 && out.length < (want || 3); i++) { var m2 = n + between(-20, 20); if (m2 >= 0 && m2 !== n && out.indexOf(m2) < 0) out.push(m2); } }
    return out;
  }

  // ---------- drill items ----------
  var LABEL = "Numbers";
  function base(sub, numkey, extra) {
    var e = { cat: "numbers", catLabel: LABEL, sub: sub, numkey: numkey, alt: [], d: [], translation: "", glosses: [], accMap: {} };
    for (var k in extra) e[k] = extra[k];
    return e;
  }
  function uniqueFirst(list, a, k) { var out = []; list.forEach(function (x) { if (x !== a && out.indexOf(x) < 0) out.push(x); }); return out.slice(0, k); }

  function itemDigitsToWords(n) {
    var c = say(n), d = similar(n, 6).map(function (m) { var w = say(m); return [w.text, w.acc]; }), e;
    var ds = uniqueFirst(d.map(function (x) { return x[0]; }), c.text, 3), am = {}; am[c.text] = c.acc;
    d.forEach(function (x) { if (ds.indexOf(x[0]) >= 0) am[x[0]] = x[1]; });
    e = base("digits → words", "d2w", { s: fmt(n) + " = ___", base: "словами", a: c.text, alt: c.alt, d: ds, ph: "Type it in words", say: c.text,
      ex: explain(n) + (c.alt.length ? " (the formal style also says «" + c.alt[0] + "»)." : "."), n: n });
    e.accMap = am; if (c.alt.length) c.alt.forEach(function (x) { e.accMap[x] = x; });
    return e;
  }
  function itemWordsToDigits(n) {
    var c = say(n), d = uniqueFirst(similar(n, 6).map(fmt), fmt(n), 3);
    return base("words → digits", "w2d", { s: c.text + " = ___", base: "цифрами", a: fmt(n), d: d, digits: true, ph: "Type the digits", say: c.text,
      ex: explain(n) + " → " + c.acc + ".", n: n });
  }
  function itemListen(n) {
    var c = say(n), d = uniqueFirst(similar(n, 6).map(fmt), fmt(n), 3);
    return base("listening", "listen", { s: "___", base: "what number did you hear?", a: fmt(n), d: d, digits: true, listen: true, ph: "Type the digits you heard", say: c.text,
      translation: c.text, trLabel: "Can't hear it? Show the words", ex: "You heard " + c.acc + ". " + explain(n) + ".", n: n });
  }
  function ruleText(n) {
    var c = nounCat(n);
    if (n > 0 && n % 1000 === 0) return "a round thousand or million is itself a noun (тысяча, миллион), so what is counted goes into the genitive plural";
    if (c === "one") return "it ends in 1 (but not 11), so the noun is nominative singular";
    if (c === "few") return "it ends in 2, 3 or 4 (but not 12, 13, 14), so the noun is genitive singular";
    if (n % 100 >= 11 && n % 100 <= 14) return "11 to 14 are the exception: the noun is genitive plural";
    return "it ends in 0 or 5–9, so the noun is genitive plural";
  }
  function phraseOptions(n, forms, g, ok) {
    var wrong = [], c0 = nounCat(n), ds = [], am = {}, seen = {};
    CATS.forEach(function (c) { if (c !== c0) wrong.push(cardinal(n, g).join(" ") + " " + form(forms, c)); });   // right number, wrong noun form
    if (g !== "m") wrong.push(cardinal(n, "m").join(" ") + " " + form(forms, c0));                                 // wrong gender of один/два
    var near = similar(n, 4).map(function (m) { return phrase(m, forms, g).acc; });
    seen[ok.text] = 1;
    shuffle(wrong).concat(near).forEach(function (a) {
      var p = strip(a); if (!seen[p] && ds.length < 3) { seen[p] = 1; ds.push(p); am[p] = a; }
    });
    return { d: ds, am: am };
  }
  // noun: {ru, forms:[one,few,many], g, en, enPl, money}
  function itemNounSlot(n, N) {
    var c = nounCat(n), a = form(N.forms, c), ph = phrase(n, N.forms, N.g);
    var ds = uniqueFirst([N.forms[0], N.forms[1], N.forms[2], N.npl || "", N.dat || ""].filter(Boolean), a, 3);
    var fr = N.money ? ["Это стоит " + fmt(n) + " ___.", "It costs " + fmt(n) + " " + (n === 1 ? N.en : N.enPl) + "."] :
      (rnd(2) ? ["Здесь " + fmt(n) + " ___.", "There " + (n === 1 ? "is " : "are ") + fmt(n) + " " + (n === 1 ? N.en : N.enPl) + " here."] :
        ["У нас " + fmt(n) + " ___.", "We have " + fmt(n) + " " + (n === 1 ? N.en : N.enPl) + "."]);
    var e = base("number + noun", "slot", { s: fr[0], base: N.ru, a: a, d: ds, translation: fr[1], glosses: [N.ru + ": " + N.en],
      say: ph.text, ex: fmt(n) + ": " + ruleText(n) + ". " + ph.acc + ".", n: n, meta: { forms: N.forms, g: N.g } });
    e.accMap[a] = a;
    return e;
  }
  function itemNounPhrase(n, N) {
    var ph = phrase(n, N.forms, N.g), o = phraseOptions(n, N.forms, N.g, ph);
    var e = base("number + noun in words", "phr", { s: fmt(n) + " " + N.ru + " = ___", base: "словами, with the right noun form", a: ph.text, alt: ph.alt, d: o.d, ph: "Type the number and the noun", say: ph.text,
      translation: fmt(n) + " " + (n === 1 ? N.en : N.enPl), glosses: [N.ru + ": " + N.en],
      ex: fmt(n) + ": " + ruleText(n) + ". " + ph.acc + (N.g === "f" || N.g === "n" ? " (" + N.ru + " is " + (N.g === "f" ? "feminine" : "neuter") + ", so 1 and 2 are " + (N.g === "f" ? "одна, две" : "одно, два") + ")." : "."), n: n, meta: { forms: N.forms, g: N.g } });
    o.am[ph.text] = ph.acc; e.accMap = o.am; return e;
  }
  var CUR = { rub: { sym: " ₽", key: "рубль", g: "m", en: "ruble" }, usd: { sym: " $", key: "доллар", g: "m", en: "dollar" }, eur: { sym: " €", key: "евро", g: "n", en: "euro" }, kop: { sym: " коп.", key: "копейка", g: "f", en: "kopek" } };
  function itemPrice(range) {
    var k = pick(["rub", "rub", "usd", "usd", "eur", "kop"]), c = CUR[k], n;
    if (k === "kop") n = between(1, 99); else { n = rangeNumber(range); if (n === 0) n = between(1, 20); }
    var forms = D.money[c.key], ph = phrase(n, forms, c.g), o = phraseOptions(n, forms, c.g, ph);
    var en = c.en + (n === 1 ? "" : "s"), sym = k === "usd" ? "$" + fmt(n) : k === "eur" ? fmt(n) + " €" : fmt(n) + c.sym;
    var e = base("prices", "price", { s: "Сколько стоит? — ___.", base: sym, a: ph.text, alt: ph.alt, d: o.d, ph: "Type the price in words", say: ph.text,
      translation: "How much is it? — " + fmt(n) + " " + en + ".", ex: fmt(n) + ": " + ruleText(n) + ". " + ph.acc + (k === "eur" ? " (евро never changes.)" : ""), n: n, meta: { forms: forms, g: c.g } });
    o.am[ph.text] = ph.acc; e.accMap = o.am; return e;
  }
  function itemAge() {
    var n = rnd(10) < 4 ? between(1, 20) : between(1, 99), who = pick([["мне", "Мне", "How old am I? — I am"], ["тебе", "Тебе", "How old are you? — You are"], ["ему", "Ему", "How old is he? — He is"], ["ей", "Ей", "How old is she? — She is"]]);
    var ph = phrase(n, D.year, "m"), o = phraseOptions(n, D.year, "m", ph);
    var e = base("age", "age", { s: "Сколько " + who[0] + " лет? — " + who[1] + " ___.", base: fmt(n) + " " + (n === 1 ? "year old" : "years old"), a: ph.text, alt: ph.alt, d: o.d, ph: "Type the age in words", say: who[1] + " " + ph.text,
      translation: who[2] + " " + fmt(n) + ".", ex: fmt(n) + ": " + ruleText(n).replace("noun", "word (год / года / лет)") + ". " + who[1] + " " + ph.acc + ". (The person is in the dative: мне, тебе, ему, ей.)", n: n, meta: { forms: D.year, g: "m" } });
    o.am[ph.text] = ph.acc; e.accMap = o.am; return e;
  }
  function phoneParts() { return [between(100, 999), between(0, 99), between(0, 99)]; }
  function two(x) { return (x < 10 ? "0" : "") + x; }
  function phoneStr(p) { return p[0] + "-" + two(p[1]) + "-" + two(p[2]); }
  function itemPhone(listen) {
    var p = phoneParts(), w = phoneWords(p[0], p[1], p[2]), a = phoneStr(p), ds = [], q;
    var tweaks = shuffle([[p[0] + (rnd(2) ? 10 : -10) * rnd(5), p[1], p[2]], [p[0], p[2], p[1]], [p[0], (p[1] + 10) % 100, p[2]], [p[0], p[1], (p[2] + 1) % 100], [p[0] % 100 + 100, p[1], p[2]]]);
    tweaks.forEach(function (t) { if (t[0] >= 100 && t[0] <= 999) { var s = phoneStr(t); if (s !== a && ds.indexOf(s) < 0 && ds.length < 3) ds.push(s); } });
    while (ds.length < 3) { q = phoneParts(); var s2 = phoneStr(q); if (s2 !== a && ds.indexOf(s2) < 0) ds.push(s2); }
    var tail = " Russians read a phone number in groups (123-45-67 → 123, 45, 67); a group like 05 is ноль пять. → " + a + ".";
    if (listen) return base("phone numbers (listening)", "phoneL", { s: "___", base: "what number did you hear?", a: a, d: ds, digits: true, listen: true, ph: "Type the digits you heard", say: strip(w),
      translation: strip(w), trLabel: "Can't hear it? Show the words", ex: "You heard " + w + "." + tail, n: 0 });
    return base("phone numbers", "phone", { s: strip(w) + " = ___", base: "цифрами", a: a, d: ds, digits: true, ph: "Type the digits", say: strip(w), ex: w + "." + tail, n: 0 });
  }
  var ORD = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 100];
  function itemOrdinal(rev) {
    var i = pick(ORD), o = ordinal(i), cardW = say(i).acc;
    if (!rev) {
      var ds = uniqueFirst(shuffle(ORD.filter(function (x) { return x !== i; }).map(function (x) { return strip(ordinal(x)); })).slice(0, 2).concat([strip(cardW)]), strip(o), 3);
      var am = {}; am[strip(o)] = o;
      var e = base("ordinals", "ord", { s: i + "-й = ___", base: "ordinal, masculine", a: strip(o), d: ds, ph: "Type the ordinal", say: strip(o), translation: i + (i === 1 ? "st" : i === 2 ? "nd" : i === 3 ? "rd" : "th"),
        ex: o + " is the ordinal (" + i + "-й); the cardinal is " + cardW + ". Ordinals are adjectives, so they agree with the noun: первый урок, первая лекция, первое мая.", n: i });
      e.accMap = am; return e;
    }
    var ds2 = uniqueFirst(shuffle(ORD.filter(function (x) { return x !== i; })).map(function (x) { return x + "-й"; }), i + "-й", 3);
    return base("ordinals → digits", "ordR", { s: strip(o) + " = ___", base: "цифрами", a: i + "-й", d: ds2, digits: true, ph: "Type the digit", say: strip(o), ex: o + " = " + i + "-й; the cardinal is " + cardW + ".", n: i });
  }

  var DRILLS = [["mixed", "Mixed"], ["d2w", "Digits → words"], ["w2d", "Words → digits"], ["listen", "Listening"], ["noun", "With nouns"], ["money", "Prices & age"], ["phone", "Phone numbers"], ["ord", "Ordinals"]];
  // count items; opts: {drill, range, nouns:[noun], size}
  function makeItem(kind, range, nouns) {
    var n;
    switch (kind) {
      case "d2w": return itemDigitsToWords(rangeNumber(range));
      case "w2d": return itemWordsToDigits(rangeNumber(range));
      case "listen": return itemListen(rangeNumber(range));
      case "noun":
        if (!nouns || !nouns.length) return itemDigitsToWords(rangeNumber(range));
        n = rangeNumber(range); if (n === 0) n = between(1, 20);
        return rnd(2) ? itemNounSlot(n, pick(nouns)) : itemNounPhrase(n, pick(nouns));
      case "money": return rnd(3) ? itemPrice(range) : itemAge();
      case "phone": return itemPhone(rnd(2) === 0);
      case "ord": return itemOrdinal(rnd(2) === 0);
    }
    return null;
  }
  function makeSet(opts) {
    var drill = opts.drill || "mixed", size = opts.size || 10, out = [], seen = {}, tries = 0, kinds = ["d2w", "w2d", "listen", "noun", "money", "d2w", "w2d", "listen", "phone", "ord"];
    while (out.length < size && tries++ < size * 30) {
      var kind = drill === "mixed" ? kinds[rnd(kinds.length)] : drill;
      var it = makeItem(kind, opts.range, opts.nouns);
      if (!it) continue;
      var key = it.numkey + "|" + it.s + "|" + it.a;
      if (seen[key]) continue; seen[key] = 1; out.push(it);
    }
    return out;
  }

  return { D: D, fmt: fmt, cat: cat, nounCat: nounCat, cardinal: cardinal, say: say, phrase: phrase, parts: parts, explain: explain, ordinal: ordinal, phoneWords: phoneWords,
    rangeNumber: rangeNumber, similar: similar, makeItem: makeItem, makeSet: makeSet, strip: strip, RANGES: RANGES, DRILLS: DRILLS, ORD: ORD };
})();
if (typeof module !== "undefined") module.exports = RuNumbers;
