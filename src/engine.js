/* Russian noun declension + vocabulary drill generator. Plain ES5 so it runs in any browser. */
var RuEngine = (function () {
  "use strict";
  var VOW = "аеёиоуыэюя", VEL = "гкх", HUSH = "жшщч";
  var KEYS = ["gen", "dat", "acc", "ins", "prep", "npl", "gpl"];
  var SAFE_CLUSTERS = ["ст", "зд", "рт", "рд", "рм", "рф", "мм", "сс", "тт", "лл", "нн", "тв", "жб", "нт", "нд", "мп", "рб", "сп", "шт"];
  var A_PLURALS = ["дом", "город", "паспорт", "поезд", "адрес", "номер", "вечер", "лес", "берег", "голос", "доктор", "профессор", "директор", "остров", "цвет", "сорт", "повар", "катер", "бок", "век", "снег", "сторож", "холод", "паспорт"];

  // common irregular plurals [nom pl, gen pl]
  var IRREG_PL = { "брат": ["братья", "братьев"], "друг": ["друзья", "друзей"], "стул": ["стулья", "стульев"], "сын": ["сыновья", "сыновей"],
    "муж": ["мужья", "мужей"], "человек": ["люди", "людей"], "ребёнок": ["дети", "детей"], "лист": ["листья", "листьев"], "дерево": ["деревья", "деревьев"],
    "сосед": ["соседи", "соседей"], "мать": ["матери", "матерей"], "дочь": ["дочери", "дочерей"], "время": ["времена", "времён"], "имя": ["имена", "имён"],
    "глаз": ["глаза", "глаз"], "раз": ["разы", "раз"], "солдат": ["солдаты", "солдат"], "господин": ["господа", "господ"], "хозяин": ["хозяева", "хозяев"],
    "гражданин": ["граждане", "граждан"], "англичанин": ["англичане", "англичан"], "белорус": ["белорусы", "белорусов"] };
  var IRREG_ALL = ["мать", "дочь", "время", "имя", "путь", "ребёнок", "человек", "гражданин", "англичанин", "церковь", "любовь", "господин"];
  function isV(c) { return VOW.indexOf(c) >= 0; }
  function L(s, n) { return s.charAt(s.length - (n || 1)).toLowerCase(); }
  function vowelCount(s) { var n = 0; for (var i = 0; i < s.length; i++) if (isV(s.charAt(i).toLowerCase())) n++; return n; }
  // zero-ending genitive plural is safe unless the stem ends in a consonant cluster that usually takes an inserted vowel
  function zeroSafe(stem) {
    var a = L(stem), b = L(stem, 2);
    if (isV(a)) return false;
    if (isV(b)) return true;
    return SAFE_CLUSTERS.indexOf(b + a) >= 0;
  }
  function dropFleeting(s) {
    // remove the vowel before the final consonant: огурец -> огурц, платок -> платк
    var i = s.length - 2;
    if (i < 1 || !isV(s.charAt(i).toLowerCase())) return null;
    return s.slice(0, i) + s.slice(i + 1);
  }

  // returns {f: forms, unc: {key:true}, note: string}
  function decline(w) {
    var ru = (w.ru || "").trim(), f = {}, unc = {}, note = "";
    var es = !!w.es, anim = !!w.anim;
    function allUnc(msg) { KEYS.forEach(function (k) { unc[k] = true; }); note = msg; }
    if (!ru || /\s/.test(ru)) { allUnc("Multi-word entries can't be declined automatically."); }
    else if (w.indecl) { KEYS.forEach(function (k) { f[k] = ru; }); }
    else if (w.g === "pl") { allUnc("Plural-only nouns need their forms typed in."); f.npl = ru; delete unc.npl; }
    else {
      var last = L(ru), stem = ru.slice(0, -1), t = L(stem);
      if (last === "а") {
        var yi = (VEL + HUSH).indexOf(t) >= 0 ? "и" : "ы";
        f.gen = stem + yi; f.dat = stem + "е"; f.acc = stem + "у";
        f.ins = stem + ((HUSH + "ц").indexOf(t) >= 0 && !es ? "ей" : "ой");
        f.prep = stem + "е"; f.npl = stem + yi; f.gpl = stem;
        if (!zeroSafe(stem) || (HUSH.indexOf(t) >= 0 && es)) unc.gpl = true;
      } else if (last === "я") {
        if (t === "и") {
          f.gen = stem + "и"; f.dat = stem + "и"; f.acc = stem + "ю"; f.ins = stem + "ей"; f.prep = stem + "и"; f.npl = stem + "и"; f.gpl = stem + "й";
        } else {
          f.gen = stem + "и"; f.dat = stem + "е"; f.acc = stem + "ю"; f.ins = stem + (es ? "ёй" : "ей"); f.prep = stem + "е"; f.npl = stem + "и";
          if (isV(t)) f.gpl = stem + "й";
          else { f.gpl = stem + "ь"; if (!isV(L(stem, 2))) unc.gpl = true; }
          if (t === "ь" || t === "й") { unc.gpl = true; }
        }
        if (w.g === "m" && anim) { /* дядя-type: acc is still -ю */ }
      } else if (last === "ь") {
        if (w.g === "f") {
          f.gen = stem + "и"; f.dat = stem + "и"; f.acc = ru; f.ins = ru + "ю"; f.prep = stem + "и"; f.npl = stem + "и"; f.gpl = stem + "ей";
        } else if (w.g === "m") {
          var st = stem;
          if (w.fleet) { st = dropFleeting(stem) || stem; }
          f.gen = st + "я"; f.dat = st + "ю"; f.acc = anim ? f.gen : ru; f.ins = st + (es ? "ём" : "ем"); f.prep = st + "е"; f.npl = st + "и"; f.gpl = st + "ей";
          if (!w.fleet && !w.noFleet && /[еёо][нл]$/.test(stem)) { KEYS.forEach(function (k) { if (k !== "acc" || anim) unc[k] = true; }); note = "This word may have a fleeting vowel (день → дня). Tick 'fleeting vowel' or type the forms."; }
        } else allUnc("Choose masculine or feminine for nouns ending in -ь.");
      } else if (last === "й") {
        f.gen = stem + "я"; f.dat = stem + "ю"; f.acc = anim ? f.gen : ru; f.ins = stem + "ем";
        f.prep = stem + (t === "и" ? "и" : "е"); f.npl = stem + "и"; f.gpl = stem + "ев";
      } else if (last === "о") {
        f.gen = stem + "а"; f.dat = stem + "у"; f.acc = ru; f.ins = stem + ((HUSH + "ц").indexOf(t) >= 0 && !es ? "ем" : "ом");
        f.prep = stem + "е"; f.npl = stem + "а"; f.gpl = stem;
        if (VEL.indexOf(t) >= 0 || HUSH.indexOf(t) >= 0) unc.npl = true;
        if (!zeroSafe(stem)) unc.gpl = true;
      } else if (last === "е") {
        if (t === "и") {
          f.gen = stem + "я"; f.dat = stem + "ю"; f.acc = ru; f.ins = stem + "ем"; f.prep = stem + "и"; f.npl = stem + "я"; f.gpl = stem + "й";
        } else if ((HUSH + "ц").indexOf(t) >= 0) {
          allUnc("Check the forms for this word.");
        } else {
          f.gen = stem + "я"; f.dat = stem + "ю"; f.acc = ru; f.ins = stem + "ем"; f.prep = stem + "е"; f.npl = stem + "я"; f.gpl = stem + "ей";
        }
      } else if (!isV(last)) {
        if (w.g && w.g !== "m") allUnc("Nouns ending in a consonant are usually masculine. Check the gender.");
        else {
          var obl = ru;
          if (w.fleet) { obl = dropFleeting(ru); if (!obl) { allUnc("Couldn't drop the fleeting vowel. Type the forms."); obl = ru; } }
          var o = L(obl);
          f.gen = obl + "а"; f.dat = obl + "у"; f.acc = anim ? f.gen : ru;
          f.ins = obl + ((HUSH + "ц").indexOf(o) >= 0 && !es ? "ем" : "ом");
          f.prep = obl + "е";
          var aPl = A_PLURALS.indexOf(ru.toLowerCase()) >= 0;
          f.npl = obl + (aPl ? "а" : ((VEL + HUSH).indexOf(o) >= 0 ? "и" : "ы"));
          f.gpl = obl + (HUSH.indexOf(o) >= 0 ? "ей" : (o === "ц" && !es ? "ев" : "ов"));
          if (!w.fleet && !w.noFleet && vowelCount(ru) > 1 && /(ок|ек|ёк|ец|ень)$/.test(ru.toLowerCase())) {
            KEYS.forEach(function (k) { if (k !== "acc" || anim) unc[k] = true; });
            note = "Words ending in -ок/-ек/-ец often lose that vowel (платок → платка). Tick 'fleeting vowel' or type the forms.";
          }
        }
      } else {
        allUnc("This ending isn't regular. It may be indeclinable (like кофе, меню). Tick 'indeclinable' or type the forms.");
      }
    }
    var lw = ru.toLowerCase();
    if (IRREG_ALL.indexOf(lw) >= 0 && !(w.forms && Object.keys(w.forms).length)) { allUnc("This word is irregular. Type its forms."); }
    if (IRREG_PL[lw]) { f.npl = IRREG_PL[lw][0]; f.gpl = IRREG_PL[lw][1]; delete unc.npl; delete unc.gpl; }
    // explicit forms always win
    var ov = w.forms || {};
    Object.keys(ov).forEach(function (k) { if (ov[k]) { f[k] = ov[k]; delete unc[k]; } });
    if (w.loc) f.loc = w.loc;
    return { f: f, unc: unc, note: note };
  }

  // forms that drills may use (certain or supplied)
  function usable(w) {
    var d = decline(w), out = {};
    KEYS.forEach(function (k) {
      if (!d.f[k] || d.unc[k]) return;
      if (w.mass && (k === "npl" || k === "gpl") && !(w.forms && w.forms[k])) return; // no invented plurals for mass nouns
      out[k] = d.f[k];
    });
    if (d.f.loc) out.loc = d.f.loc;
    return out;
  }

  // ---------- English helpers ----------
  function en1(w) { return (w.en || "").split(/[,(;]/)[0].trim(); }
  function enPl(w) {
    if (w.enp) return w.enp;
    var e = en1(w);
    if (/(s|sh|ch|x|z)$/.test(e)) return e + "es";
    if (/[^aeiou]y$/.test(e)) return e.slice(0, -1) + "ies";
    if (/fe$/.test(e)) return e.slice(0, -2) + "ves";
    return e + "s";
  }

  // preposition variants: в/во, с/со, к/ко, о/об
  function prepFix(p, word) {
    var w = word.toLowerCase(), a = w.charAt(0), b = w.charAt(1);
    var cons2 = b && !isV(b);
    if (p === "в" && (a === "в" || a === "ф") && cons2) return "во";
    if (p === "с" && ((("сзшж").indexOf(a) >= 0 && cons2) || a === "щ")) return "со";
    if (p === "о" && "аоуэи".indexOf(a) >= 0) return "об";
    return p;
  }

  // templates per kind and case: [ru, en, rule]. "{p:X}" = preposition X adjusted to the noun; {pp} = place preposition
  var T = {
    person: {
      gen: ["Сегодня нет ___.", "The {en} isn't here today.", "Нет (there is no) takes the genitive."],
      dat: ["Я сказал ___ спасибо.", "I said thank you to the {en}.", "Сказать кому? (to whom?) takes the dative."],
      acc: ["Я вижу ___.", "I see the {en}.", "A direct object goes in the accusative. Masculine nouns for people use the genitive form here."],
      ins: ["Я говорю {p:с} ___.", "I'm talking with the {en}.", "С (with) takes the instrumental."],
      prep: ["Я думаю {p:о} ___.", "I'm thinking about the {en}.", "О (about) takes the prepositional."]
    },
    place: {
      gen: ["Это далеко от ___?", "Is it far from the {en}?", "От (from) takes the genitive."],
      dat: ["Как пройти {p:к} ___?", "How do I get to the {en}?", "К (towards) takes the dative."],
      acc: ["Я иду {pp} ___.", "I'm going to the {en}.", "В/на + accusative answers 'where to?'"],
      ins: ["Встретимся перед ___.", "Let's meet in front of the {en}.", "Перед (in front of) takes the instrumental."],
      prep: ["Я сейчас {pp} ___.", "I'm {at} the {en} now.", "В/на + prepositional answers 'where?'"]
    },
    thing: {
      gen: ["У меня нет ___.", "I don't have {a} {en}.", "Нет (there is no) takes the genitive."],
      dat: ["Я подхожу {p:к} ___.", "I'm going up to the {en}.", "К (towards) takes the dative."],
      acc: ["Я ищу ___.", "I'm looking for the {en}.", "A direct object goes in the accusative."],
      ins: ["Что делать {p:с} ___?", "What should I do with the {en}?", "С (with) takes the instrumental."],
      prep: ["Я спросил {p:о} ___.", "I asked about the {en}.", "О (about) takes the prepositional."]
    },
    food: {
      gen: ["В магазине нет ___.", "The store has no {en}.", "Нет (there is no) takes the genitive."],
      acc: ["Дайте, пожалуйста, ___.", "{En}, please.", "Дайте (give me) + direct object in the accusative."],
      ins: ["Можно {p:с} ___?", "Can I have it with {en}?", "С (with) takes the instrumental."],
      prep: ["Я спросил {p:о} ___.", "I asked about the {en}.", "О (about) takes the prepositional."]
    },
    event: {
      gen: ["После ___ мы идём домой.", "After the {en} we go home.", "После (after) takes the genitive."],
      dat: ["Я готовлюсь {p:к} ___.", "I'm preparing for the {en}.", "Готовиться к (to prepare for) takes the dative."],
      acc: ["Я иду на ___.", "I'm going to the {en}.", "На + accusative answers 'where to?' for events."],
      ins: ["Что делать перед ___?", "What should I do before the {en}?", "Перед (before) takes the instrumental."],
      prep: ["Мы были на ___.", "We were at the {en}.", "На + prepositional for being at an event."]
    },
    transport: {
      gen: ["Я вышел из ___.", "I got out of the {en}.", "Из (out of) takes the genitive."],
      dat: ["Как пройти {p:к} ___?", "How do I get to the {en}?", "К (towards) takes the dative."],
      acc: ["Я опоздал на ___.", "I missed the {en}.", "Опоздать на (to be late for) takes the accusative."],
      prep: ["Я еду на ___.", "I'm going by {en}.", "Ехать на + prepositional: how you travel."]
    },
    // furniture, appliances and spots in a room: где? (в/на + prep) vs куда? (в/на + acc) vs откуда? (из/с + gen)
    home: {
      gen: ["Возьми это {from} ___.", "Take it {off} the {en}.", "Откуда? (from where?) Из (out of, the opposite of в) and с (off, the opposite of на) take the genitive."],
      acc: ["{put} это {pp} ___.", "{Put} it {into} the {en}.", "Куда? (where to?) В/на + accusative after a verb of putting (поставить, положить, повесить)."],
      ins: ["Что лежит под ___?", "What's under the {en}?", "Под (under) + instrumental answers 'where?'"],
      prep: ["Это {lie} {pp} ___.", "It's {at} the {en}.", "Где? (where?) В/на + prepositional after стоять, лежать, висеть."]
    },
    // abstract nouns (feelings, sounds, ideas): Молчат Дома song words
    abstract: {
      gen: ["Это песня без ___.", "It's a song without {a} {en}.", "Без (without) takes the genitive."],
      dat: ["Я уже привык {p:к} ___.", "I've already gotten used to the {en}.", "Привыкнуть к (to get used to) takes the dative."],
      acc: ["Я чувствую ___.", "I feel the {en}.", "A direct object goes in the accusative."],
      ins: ["Что делать {p:с} ___?", "What should I do with the {en}?", "С (with) takes the instrumental."],
      prep: ["Это песня {p:о} ___.", "It's a song about the {en}.", "О (about) takes the prepositional."]
    },
    // parts of the body
    body: {
      dat: ["Он прижал руку {p:к} ___.", "He pressed his hand to his {en}.", "К (towards, against) takes the dative."],
      acc: ["Он показал на ___.", "He pointed at his {en}.", "Показать на (to point at) takes the accusative."],
      prep: ["Что-то горит {p:в} ___.", "Something is burning in the {en}.", "В + prepositional answers 'where?' (like the song: «У неё горит в груди»)."]
    },
    money: {}, unit: {}
  };
  var CASE_NAME = { gen: "genitive", dat: "dative", acc: "accusative", ins: "instrumental", prep: "prepositional" };

  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function fill(tpl, w, form) {
    return tpl.replace(/\{put\}/g, w.put || "Положи").replace(/\{lie\}/g, w.lie || "лежит")
      .replace(/\{from\}/g, prepFix(w.pp === "на" ? "с" : "из", form))
      .replace(/\{pp\}/g, prepFix(w.pp || "в", form)).replace(/\{p:([^}]+)\}/g, function (_, p) { return prepFix(p, form); });
  }
  function fillEn(tpl, w, plural) {
    var e = plural ? enPl(w) : en1(w);
    var art = (w.mass || w.g === "pl") ? "any " : (/^[aeiou]/i.test(e) ? "an " : "a ");
    var on = w.pp === "на";
    var out = tpl.replace(/\{a\} /g, art)
      .replace(/\{Put\}/g, w.put === "Повесь" ? "Hang" : "Put")
      .replace(/\{off\}/g, on ? "off" : "out of")
      .replace(/\{into\}/g, w.enprep || (on ? "on" : "in"))
      .replace(/\{at\}/g, w.enprep || (on ? (w.kind === "home" ? "on" : "at") : "in"));
    if (w.noArt) out = out.replace(/the \{en\}/g, "{en}");
    return out.replace(/\{En\}/g, cap(e)).replace(/\{en\}/g, e);
  }
  function rnd(n) { return Math.floor(Math.random() * n); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = rnd(i + 1), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function uniq(arr, not) {
    var seen = {}, out = [];
    arr.forEach(function (x) { if (!x) return; var k = x.toLowerCase(); if (k === (not || "").toLowerCase() || seen[k]) return; seen[k] = 1; out.push(x); });
    return out;
  }
  function distractorsFrom(F, ans, w) {
    var pool = uniq([w.ru, F.gen, F.dat, F.acc, F.ins, F.prep, F.loc, F.npl, F.gpl], ans);
    return shuffle(pool).slice(0, 3);
  }

  var NUMS = {
    one: [[1, { m: "один", f: "одна", n: "одно" }], [21, { m: "двадцать один", f: "двадцать одна", n: "двадцать одно" }]],
    few: [[2, { m: "два", f: "две", n: "два" }], [3, "три"], [4, "четыре"], [22, { m: "двадцать два", f: "двадцать две", n: "двадцать два" }]],
    many: [[5, "пять"], [6, "шесть"], [10, "десять"], [25, "двадцать пять"]]
  };
  function numWord(spec, g) { return typeof spec === "string" ? spec : spec[g] || spec.m; }

  // Build exercises for one word. types: cases, plurals, numbers, cards
  var PERS = ["1s", "2s", "3s", "1p", "2p", "3p"];
  var PRON = { "1s": ["Я", "I"], "2s": ["Ты", "you"], "3s": ["Он", "he/she/it", "он/она/оно"], "1p": ["Мы", "we"], "2p": ["Вы", "you, plural/formal"], "3p": ["Они", "they"] };
  function wordExercises(w, types, pool) {
    var out = [];
    var gl = [w.ru + ": " + w.en];
    if (w.pos === "noun" && !w.indecl) {
      var F = usable(w), plOnly = w.g === "pl";
      var tk = T[w.kind || "thing"] || T.thing, skip = w.skip || [];
      if (types.cases) {
        ["gen", "dat", "acc", "ins", "prep"].forEach(function (c) {
          var tpl = tk[c];
          if (c === "gen" && w.kind === "food" && !w.mass) tpl = T.thing.gen;
          if (!tpl || skip.indexOf(c) >= 0) return;
          if (c === "dat" && (w.kind || "thing") === "thing" && !w.approach) return;
          var form = (c === "prep" && F.loc && (w.kind === "place" || w.kind === "home")) ? F.loc : F[c];
          if (!form) return;
          var rule = tpl[2];
          if (c === "acc" && w.kind !== "person" && w.anim && w.g === "m") rule += " Animate masculine nouns use the genitive form.";
          if (c === "prep" && form === F.loc && F.loc !== F.prep) rule += " " + w.ru + " takes the special ending -у after в/на for location (but о " + F.prep + ").";
          out.push({
            cat: "vocab", sub: CASE_NAME[c], s: fill(tpl[0], w, form), base: w.ru + (plOnly ? ", plural only" : ""), a: form, alt: [],
            d: distractorsFrom(F, form, w), ex: rule + " " + w.ru + " → " + form + ".",
            translation: fillEn(tpl[1], w, false), glosses: gl, word: w.ru
          });
        });
      }
      var countable = !w.mass && !plOnly && w.kind !== "event";
      var numOk = countable && !w.nonum; // nonum: adjective-type nouns (ванная) need adjective endings after 2-4
      var pluralDrill = countable && w.kind !== "unit";
      if (types.plurals && pluralDrill) {
        if (F.npl) out.push({ cat: "vocab", sub: "nominative plural", s: "Где ___?", base: w.ru + ", plural", a: F.npl, alt: [], d: distractorsFrom(F, F.npl, w),
          ex: "Nominative plural: " + w.ru + " → " + F.npl + ".", translation: "Where are the " + enPl(w) + "?", glosses: gl, word: w.ru });
        if (F.gpl) out.push({ cat: "vocab", sub: "genitive plural", s: "Здесь много ___.", base: w.ru, a: F.gpl, alt: w.gplAlt ? [w.gplAlt] : [], d: distractorsFrom(F, F.gpl, w).filter(function (x) { return x !== w.gplAlt; }),
          ex: "Много (a lot of) takes the genitive plural: " + w.ru + " → " + F.gpl + ".", translation: "There are a lot of " + enPl(w) + " here.", glosses: gl, word: w.ru });
      }
      if (types.numbers && numOk && F.gen && F.npl && F.gpl && w.g) {
        var frame = w.kind === "money" ? ["Это стоит {n} ___.", "It costs {N} {en}."] : ["Здесь {n} ___.", "There {be} {N} {en} here."];
        [["one", w.ru, "1 and numbers ending in 1 (but not 11) take the nominative singular."],
         ["few", F.gen, "2, 3, 4 (and 22, 23, 24…) take the genitive singular."],
         ["many", F.gpl, "5 and up (and 11–14) take the genitive plural."]].forEach(function (b) {
          var pick = NUMS[b[0]][rnd(NUMS[b[0]].length)], nw = numWord(pick[1], w.g), n = pick[0];
          var single = n === 1;
          out.push({ cat: "vocab", sub: "numbers", s: frame[0].replace("{n}", nw), base: w.ru, a: b[1], alt: [], d: distractorsFrom(F, b[1], w),
            ex: b[2] + " " + nw + " " + b[1] + ".", translation: frame[1].replace("{be}", single ? "is" : "are").replace("{N}", String(n)).replace("{en}", single ? en1(w) : enPl(w)),
            glosses: gl, word: w.ru });
        });
      }
    }
    // conjugation (verbs that carry their present/future forms, e.g. the Молчат Дома words)
    if (types.conj && w.pos === "verb" && w.conj) {
      var ks = PERS.filter(function (k) { return w.conj[k]; });
      var pf = w.asp === "pf", tense = pf ? "future" : "present";
      var para = ks.map(function (k) { return (PRON[k][2] || PRON[k][0].toLowerCase()) + " " + w.conj[k]; }).join(" · ");
      var enV = (w.en || "").split(" (")[0];
      ks.forEach(function (k) {
        var fr = (w.frames && w.frames[k]) || (PRON[k][0] + " {}.");
        var a = w.conj[k];
        var d = shuffle(uniq(ks.filter(function (x) { return x !== k; }).map(function (x) { return w.conj[x]; }).concat([w.ru]), a)).slice(0, 3);
        out.push({ cat: "vocab", sub: "conjugation", s: fr.replace("{}", "___"), base: w.ru + (pf ? " (pf. → future)" : " (impf. → present)"), a: a, alt: [], d: d,
          ex: (pf ? "Perfective verbs have no present tense: these endings make the future. " : "") + para + ".",
          translation: "(" + PRON[k][1] + ") " + enV + ", " + tense + " tense", glosses: gl, word: w.ru });
      });
    }
    if (types.cards && pool) {
      var same = pool.filter(function (x) { return x !== w && x.theme === w.theme; });
      var others = same.length >= 3 ? same : pool.filter(function (x) { return x !== w; });
      var enD = uniq(shuffle(others).map(function (x) { return x.en; }), w.en).slice(0, 3);
      var ruD = uniq(shuffle(others.filter(function (x) { return x.pos === w.pos; }).concat(shuffle(others))).map(function (x) { return x.ru; }), w.ru).slice(0, 3);
      out.push({ cat: "vocab", sub: "flashcard ru→en", s: "«" + w.ru + "» — ___", base: "choose the English meaning", a: w.en, alt: [], d: enD, ex: w.ru + " means \"" + w.en + "\"." + (w.note ? " " + w.note : ""), translation: "", glosses: [], word: w.ru, choiceOnly: true });
      out.push({ cat: "vocab", sub: "flashcard en→ru", s: "«" + w.en + "» — ___", base: "по-русски", a: w.ru, alt: [], d: ruD, ex: "\"" + w.en + "\" is " + w.ru + "." + (w.note ? " " + w.note : ""), translation: "", glosses: [], word: w.ru });
    }
    return out;
  }

  function buildSession(words, drill, limit) {
    var types = drill === "mixed" ? { cases: 1, plurals: 1, numbers: 1, cards: 1, conj: 1 } : {};
    if (drill !== "mixed") types[drill] = 1;
    var all = [];
    words.forEach(function (w) { all = all.concat(wordExercises(w, types, words)); });
    all = shuffle(all);
    if (drill === "mixed") {
      // keep variety: at most 2 items per word in a mixed session
      var cap = Math.max(2, Math.ceil(25 / Math.max(1, words.length))), per = {};
      all = all.filter(function (e) { per[e.word] = (per[e.word] || 0) + 1; return per[e.word] <= cap; });
    }
    return limit ? all.slice(0, limit) : all;
  }

  return { decline: decline, usable: usable, wordExercises: wordExercises, buildSession: buildSession, prepFix: prepFix, KEYS: KEYS, enPl: enPl, en1: en1 };
})();
if (typeof module !== "undefined") module.exports = RuEngine;
