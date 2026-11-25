# Lesson 9: plurals and the genitive plural, exceptions to watch, genitive prepositions (кроме / напротив / перед contrast).
# Built from the tutor session notes («Родительный падеж 2»). Imported by lessons_src.py.
# Every form here was checked with pymorphy3 (src/verify_lessons.py, check_l9).

def build(t, ru, exl):
    def rv(inner, hint="Say each word out loud first. Then check the stress:"):
        return ('<div class="rv nostress"><div class="rvbar"><span class="rvh">%s</span>'
                '<button type="button" class="sbtn" data-rv="1" aria-pressed="false">Show stress ´</button></div>%s</div>') % (hint, inner)
    def ar(a, b): return ru(a) + " → " + ru(b)

    S = []
    S.append({"h": "Step 1 · The nominative plural (a quick review)", "open": True, "html":
      "<p>Before the genitive plural, a quick look at the plain plural, the <b>nominative plural</b> (" + ru("именительный падеж, множественное число") + "). It's the form for the <b>subject</b>: " + ru("Коровы пасутся на лугу") + ".</p>"
      + rv(t(["Dictionary form", "Nominative plural", "Examples"], [
        ["masc. consonant", ru("-ы") + " (" + ru("-и") + " after г, к, х, ж, ч, ш, щ)", ar("студент", "студенты") + " · " + ar("программист", "программисты") + " · " + ar("петух", "петухи") + " · " + ar("врач", "врачи")],
        ["masc. " + ru("-й / -ь") + ", fem. " + ru("-я / -ь"), ru("-и"), ar("музей", "музеи") + " · " + ar("словарь", "словари") + " · " + ar("песня", "песни") + " · " + ar("тетрадь", "тетради")],
        ["fem. " + ru("-а"), ru("-ы / -и"), ar("корова", "коровы") + " · " + ar("улица", "улицы") + " · " + ar("подруга", "подруги")],
        ["neut. " + ru("-о / -е"), ru("-а / -я"), ar("место", "места") + " · " + ar("поле", "поля") + " · " + ar("общежитие", "общежития")],
        ["some masc. (stressed)", ru("-а"), ar("город", "города") + " · " + ar("дом", "дома") + " · " + ar("сорт", "сорта")],
      ]))
      + "<p>A handful are irregular in the plural itself. You've met most of them already:</p>"
      + t(["Singular", "Plural"], [
        [ru("человек") + " person", ru("люди")], [ru("ребёнок") + " child", ru("дети")],
        [ru("друг") + " friend", ru("друзья")], [ru("брат") + " brother", ru("братья")],
        [ru("сестра") + " sister", ru("сёстры")], [ru("жена") + " wife", ru("жёны")],
        [ru("мать") + " / " + ru("дочь"), ru("матери") + " / " + ru("дочери") + " (the hidden " + ru("-ер-") + " comes back)"],
      ])
      + '<p class="tip"><b>German:</b> German marks the plural mostly with the article (die Kühe, die Brüder). Russian has no article, so the <b>ending</b> carries all the information, and the plural has its own set of cases. This lesson is about the most-used of those cases after the nominative.</p>'})

    S.append({"h": "Step 2 · The genitive plural: masculine nouns (-ов / -ев / -ей)", "open": False, "html":
      "<p>The <b>genitive plural</b> (" + ru("родительный падеж, множественное число") + ") answers " + ru("кого? чего?") + " for more than one: " + ru("много коров") + ", " + ru("пять друзей") + ", " + ru("нет денег") + ". Unlike the other plural cases, it has <b>three</b> different endings, and the dictionary form tells you which one.</p>"
      + "<p>Masculine nouns, from your tutor's chart and your own life:</p>"
      + rv(t(["Dictionary form ends in", "Genitive plural", "Examples"], [
        ["a hard consonant", ru("-ов"), ar("студент", "студентов") + " · " + ar("город", "городов") + " · " + ar("учебник", "учебников") + " · " + ar("отец", "отцов") + " · " + ar("петух", "петухов") + " · " + ar("программист", "программистов")],
        [ru("-й"), ru("-ев"), ar("музей", "музеев") + " · " + ar("планетарий", "планетариев") + " · " + ar("сарай", "сараев")],
        [ru("ж, ч, ш, щ"), ru("-ей"), ar("этаж", "этажей") + " · " + ar("врач", "врачей") + " · " + ar("карандаш", "карандашей") + " · " + ar("товарищ", "товарищей")],
        [ru("-ь"), ru("-ей"), ar("преподаватель", "преподавателей") + " · " + ar("словарь", "словарей") + " · " + ar("рубль", "рублей") + " · " + ar("гость", "гостей")],
      ]))
      + "<p>Notice " + ru("отец → отцов") + ": the " + ru("е") + " in " + ru("отец") + " is a <b>fleeting vowel</b>. It drops out as soon as an ending is added (" + ru("отца, отцу, отцы, отцов") + "). The same happens with " + ru("петушок → петушков") + ", " + ru("огурец → огурцов") + ".</p>"
      + exl([("У нас на ферме двенадцать петухов.", "We have twelve roosters on the farm."),
             ("В нашем офисе пять программистов.", "There are five programmers in our office."),
             ("В Джексоне много музеев?", "Are there many museums in Jackson?")])
      + '<p class="tip">A memory hook: after the “hushing” sounds ' + ru("ж, ч, ш, щ") + " and after " + ru("-ь") + ", Russian wants " + ru("-ей") + ". " + ru("-ов") + " after " + ru("ж/ч/ш/щ") + " (" + ru("врачов") + ") is the most common learner mistake here.</p>"})

    S.append({"h": "Step 3 · Feminine and neuter: the zero ending", "open": False, "html":
      "<p>Most feminine nouns in " + ru("-а / -я") + " and neuter nouns in " + ru("-о") + " take <b>no ending at all</b> in the genitive plural: you just remove the last vowel. This is the “zero ending”.</p>"
      + rv(t(["Dictionary form", "Genitive plural", "Examples"], [
        ["fem. " + ru("-а"), "drop " + ru("-а"), ar("комната", "комнат") + " · " + ar("подруга", "подруг") + " · " + ar("улица", "улиц") + " · " + ar("корова", "коров") + " · " + ar("икона", "икон") + " · " + ar("школа", "школ")],
        ["neut. " + ru("-о"), "drop " + ru("-о"), ar("посольство", "посольств") + " · " + ar("место", "мест") + " · " + ar("дело", "дел")],
        ["fem. " + ru("-ия") + ", neut. " + ru("-ие"), ru("-ий"), ar("аудитория", "аудиторий") + " · " + ar("литургия", "литургий") + " · " + ar("общежитие", "общежитий") + " · " + ar("здание", "зданий")],
        ["fem. " + ru("-ь") + ", neut. " + ru("-е"), ru("-ей"), ar("тетрадь", "тетрадей") + " · " + ar("лошадь", "лошадей") + " · " + ar("море", "морей") + " · " + ar("поле", "полей")],
        [ru("мать, дочь"), ru("-ерей"), ar("мать", "матерей") + " · " + ar("дочь", "дочерей")],
      ]))
      + "<h4>The fleeting vowel comes in</h4>"
      + "<p>If removing the vowel would leave two consonants jammed together at the end, Russian <b>inserts</b> an " + ru("о") + " or " + ru("е / ё") + " to make the word pronounceable:</p>"
      + rv(t(["Dictionary form", "Without help (impossible)", "Genitive plural"], [
        [ru("тарелка"), "тарелк", ru("тарелок")], [ru("чашка"), "чашк", ru("чашек")],
        [ru("бутылка"), "бутылк", ru("бутылок")], [ru("заправка"), "заправк", ru("заправок")],
        [ru("сестра"), "сестр", ru("сестёр")], [ru("песня"), "песн", ru("песен")],
        [ru("деревня"), "деревн", ru("деревень")], [ru("письмо"), "письм", ru("писем")],
        [ru("окно"), "окн", ru("окон")],
      ]))
      + '<p class="tip"><b>Shorter, not longer:</b> German has nothing like the zero ending, so it feels odd at first. The key point is that here the genitive plural is the <b>shortest</b> form: ' + ru("коров") + " is shorter than " + ru("корова") + ". That is why " + ru("“коровов”") + " sounds so wrong to a Russian.</p>"})

    S.append({"h": "Step 4 · When to use the genitive plural", "open": False, "html":
      "<p>You'll need the genitive plural in five everyday situations:</p>"
      + t(["Trigger", "Example", "Note"], [
        ["a number of 5 or more (and 11–14)", ru("пять коров") + " · " + ru("двадцать петухов"), "the <b>Numbers</b> section, Step 8: 1 nominative, 2–4 genitive singular, 5+ genitive plural. Only the last digit counts: " + ru("двадцать две коровы") + "."],
        [ru("много, мало, сколько, несколько"), ru("много друзей") + " · " + ru("сколько яиц?"), "quantity words always take the genitive (plural if you can count it)"],
        [ru("нет") + " + plural", ru("в деревне нет школ") + " · " + ru("у нас нет свиней"), "Lesson 4's " + ru("нет") + " rule, in the plural"],
        ["a genitive preposition", ru("для коров") + " · " + ru("кроме друзей"), "Step 6"],
        ["animate direct object, plural", ru("я вижу коров") + " · " + ru("я жду друзей"), "Lesson 6: animate accusative plural = genitive plural"],
      ])
      + exl([("У нас много коров и кур.", "We have a lot of cows and chickens."),
             ("Сколько у тебя петухов? — Два петуха.", "How many roosters do you have? — Two. (2 → genitive singular)"),
             ("В Березине нет больших заправок.", "There are no big gas stations in Berezino."),
             ("На альбоме Молчат Дома десять песен.", "There are ten songs on the Molchat Doma album.")])
      + '<p class="tip"><b>Don’t over-apply it:</b> with ' + ru("есть") + " the thing is the <b>subject</b>, so it stays nominative plural: " + ru("У нас есть коровы") + " (we have cows), but " + ru("У нас много коров") + " (we have many cows). It's exactly the pair " + ru("есть / нет") + " from Lesson 4.</p>"})

    S.append({"h": "Step 5 · Exceptions to watch", "open": False, "html":
      "<p>These are the words that trip up even advanced learners, because the “regular” form you'd build from Steps 2–3 is wrong. Russians notice them instantly. If you build a genitive plural for one of these and it <b>looks regular</b>, stop and check this list.</p>"
      + rv(t(["Word", "Genitive plural", "The trap"], [
        [ru("человек") + " person", ru("людей") + " · but " + ru("пять человек"), "after <b>numbers</b>: " + ru("человек") + " (" + ru("пять человек, двадцать человек") + "); after " + ru("много / мало / сколько") + ": " + ru("людей") + ". Never " + ru("“человеков”") + "."],
        [ru("год") + " year", ru("лет"), ru("пять лет") + ", " + ru("сорок лет") + ", " + ru("много лет") + ". " + ru("годов") + " is only for decades (" + ru("девяностых годов") + ")."],
        [ru("ребёнок") + " child", ru("детей"), "from " + ru("дети") + ": " + ru("трое детей") + ", " + ru("много детей")],
        [ru("деньги") + " money", ru("денег"), "plural only, with a fleeting " + ru("е") + ": " + ru("нет денег") + ", not " + ru("“деньгов”")],
        [ru("брат") + " brother", ru("братьев"), "plural " + ru("братья") + " → " + ru("братьев") + " (also " + ru("стул → стулья → стульев") + ")"],
        [ru("друг") + " friend", ru("друзей"), "plural " + ru("друзья") + " → " + ru("друзей") + ", not " + ru("“другов”")],
        [ru("стул") + " chair", ru("стульев"), "plural " + ru("стулья") + ", like " + ru("братья")],
        [ru("раз") + " time (occasion)", ru("раз"), ru("пять раз") + ", " + ru("много раз") + ": no ending, like " + ru("глаз → глаз")],
        [ru("глаз") + " eye", ru("глаз"), ru("у неё красивые глаза") + ", but " + ru("цвет глаз")],
        [ru("солдат") + " soldier", ru("солдат"), "zero ending although it's masculine: " + ru("пять солдат") + " (the film " + ru("«Солдаты неудачи»") + ")"],
        [ru("сапог") + " boot", ru("сапог"), ru("пара сапог") + " — but " + ru("носок → носков") + " (" + ru("пара носков") + ")"],
        [ru("носок") + " sock", ru("носков"), "fleeting " + ru("о") + ", then " + ru("-ов")],
        [ru("курица") + " / " + ru("куры") + " hens", ru("кур"), "on the farm the plural is " + ru("куры") + ", genitive " + ru("кур") + " (" + ru("много кур") + "). The textbook form " + ru("куриц") + " exists too."],
        [ru("яйцо") + " egg", ru("яиц"), ru("десять яиц") + " — not " + ru("“яйцов”") + " or " + ru("“яица”") + ". (2–4: " + ru("четыре яйца") + ")"],
        [ru("семья") + " family", ru("семей"), ru("-ья → -ей") + ": " + ru("много семей")],
        [ru("тётя") + " aunt", ru("тёть"), "zero ending with a soft sign: " + ru("у меня пять тёть")],
        [ru("место") + " / " + ru("дело"), ru("мест") + " / " + ru("дел"), "neuter zero ending: " + ru("нет мест") + ", " + ru("много дел")],
        [ru("поле") + " field", ru("полей"), "neuter " + ru("-е → -ей") + ": " + ru("вокруг фермы много полей")],
      ]))
      + "<h4>The other trap: нравится or нравятся?</h4>"
      + "<p>Your tutor's sentence is a great example of where the genitive and agreement meet:</p>"
      + exl([("Мне нравятся все виды сыра, кроме бри.", "I like all kinds of cheese except Brie.")])
      + t(["Word", "Job in the sentence", "Case"], [
        [ru("мне"), "the person who likes (Lesson 7)", "dative"],
        [ru("нравятся"), "verb, plural to agree with the subject", "—"],
        [ru("все виды"), "<b>subject</b>: “all kinds”", "nominative <b>plural</b>"],
        [ru("сыра"), "“of cheese”", "genitive"],
        [ru("кроме бри"), "except Brie; " + ru("бри") + " never changes", "genitive (indeclinable)"],
      ])
      + '<p class="tip"><b>Check the subject, not the nearest noun.</b> The scratch-pad note said ' + ru("Мне нравится все виды сыра") + ", but " + ru("виды") + " is plural, so the verb must be " + ru("нравятся") + ". Compare " + ru("Мне нравится джаз") + " and " + ru("Мне нравится Нью-Йорк") + " (one thing → " + ru("нравится") + ") with " + ru("Мне нравятся песни Молчат Дома") + " (plural → " + ru("нравятся") + "). A genitive in between (" + ru("сыра") + ", " + ru("коров") + ") never decides the verb.</p>"})

    S.append({"h": "Step 6 · Prepositions that take the genitive", "open": False, "html":
      "<p>You know " + ru("у") + " from Lesson 4. A whole group of prepositions works the same way: the noun after them goes into the <b>genitive</b>, singular or plural. Grammatically, that noun is the <b>object of the preposition</b>, never the direct object.</p>"
      + rv(t(["Preposition", "Meaning · German", "Example"], [
        [ru("для"), "for (a purpose, or who benefits) · <i>für</i>", ru("Вода для моих коров.")],
        [ru("кроме"), "besides, except, other than · <i>außer</i>", ru("Я ем всё, кроме сыра.")],
        [ru("напротив"), "<b>opposite, across from</b> · <i>gegenüber</i>", ru("Моя машина стоит напротив моего дома.")],
        [ru("ради"), "for the sake of · <i>um … willen</i>", ru("Я работаю ради моей семьи.")],
        [ru("без"), "without · <i>ohne</i>", ru("Без интернета сервер не работает.")],
        [ru("из"), "from, out of (a place) · <i>aus</i>", ru("Мой друг из Березина.")],
        [ru("от"), "from (a person); away from · <i>von</i>", ru("Письмо от батюшки.")],
        [ru("после"), "after · <i>nach</i>", ru("После службы мы пьём чай.")],
        [ru("около"), "near, by · <i>bei, neben</i>", ru("Около заправки есть магазин.")],
      ]))
      + "<p>In your tutor's sentences the possessive goes into the genitive too, to agree: " + ru("мои коровы → для моих коров") + ", " + ru("мой дом → напротив моего дома") + ", " + ru("моя семья → ради моей семьи") + ". (Adjective and possessive endings are Lesson 10; for now, learn these three as phrases.)</p>"
      + "<h4>для or ради?</h4>"
      + exl([("Я работаю для компании в Джексоне.", "I work for a company in Jackson. (who benefits / the employer)"),
             ("Я работаю ради моей семьи.", "I work for the sake of my family. (why I do it, the motive)"),
             ("Это корм для кур.", "This is feed for the hens. (purpose)")])
      + '<p class="tip"><b>German makes ' + ru("ради") + " easy:</b> “um meiner Familie willen” uses the German genitive, just like " + ru("ради моей семьи") + ". " + ru("для") + " is the everyday “für”.</p>"})

    S.append({"h": "Step 7 · кроме, напротив or перед?", "open": False, "html":
      "<p>Your tutor's notes glossed " + ru("напротив") + " as “in front of”. That's a slip worth fixing now, because it's a real mix-up even for native speakers explaining in English: " + ru("напротив") + " means <b>opposite / across from</b> (facing it, usually with a street or room in between). “In front of” is " + ru("перед") + ", and it takes a <b>different case</b>.</p>"
      + t(["Preposition", "Meaning · case", "Example"], [
        [ru("кроме"), "besides, except · <b>genitive</b>", ru("Кроме меня, на ферме никого нет.")],
        [ru("напротив"), "opposite, across from · <b>genitive</b>", ru("Церковь стоит напротив почты.")],
        [ru("перед"), "in front of; just before · <b>instrumental</b>", ru("Машина стоит перед домом.")],
      ])
      + '<p class="tip"><b>German lines up neatly:</b> ' + ru("кроме") + " = außer (außer mir), " + ru("напротив") + " = gegenüber (gegenüber der Post), " + ru("перед") + " = vor (vor dem Haus). In German all three take the dative; in Russian the first two take the genitive and " + ru("перед") + " the instrumental.</p>"
      + "<p>Picture your street: the car parked " + ru("перед домом") + " is right at your door; the house " + ru("напротив моего дома") + " is on the other side of the road, facing you.</p>"
      + "<p>The <b>instrumental</b> after " + ru("перед") + " is the subject of Lesson 8. For now, recognize the endings: masculine/neuter " + ru("-ом / -ем") + " (" + ru("перед домом, перед зданием") + "), feminine " + ru("-ой / -ей") + " (" + ru("перед иконой, перед заправкой") + "), soft " + ru("-ь → -ью") + " (" + ru("перед церковью") + "). In time expressions " + ru("перед") + " means “just before”: " + ru("перед службой") + ", " + ru("перед едой") + ".</p>"
      + '<p class="tip"><b>The case is your clue.</b> If the noun is genitive (' + ru("почты, дома, школы") + "), the preposition can be " + ru("напротив") + " or " + ru("кроме") + ", never " + ru("перед") + ". If it's instrumental (" + ru("домом, иконой") + "), only " + ru("перед") + " fits. Then the meaning decides between " + ru("кроме") + " (except) and " + ru("напротив") + " (across from).</p>"})

    S.append({"h": "Summary", "open": False, "html":
      '<ul class="sum">'
      + "<li>Genitive plural, masculine: hard consonant " + ru("-ов") + " (" + ru("студентов, петухов") + "), " + ru("-й → -ев") + " (" + ru("музеев") + "), " + ru("ж, ч, ш, щ, -ь → -ей") + " (" + ru("врачей, словарей") + ").</li>"
      + "<li>Feminine " + ru("-а / -я") + " and neuter " + ru("-о") + ": <b>zero ending</b> (" + ru("коров, подруг, мест") + "), with a fleeting vowel when needed (" + ru("тарелок, чашек, сестёр, песен") + "). " + ru("-ия / -ие → -ий") + "; " + ru("-ь / -е → -ей") + " (" + ru("тетрадей, морей") + "); " + ru("матерей, дочерей") + ".</li>"
      + "<li>Use it after 5+, " + ru("много / мало / сколько / несколько") + ", " + ru("нет") + ", genitive prepositions, and for animate plural direct objects.</li>"
      + "<li>Exceptions: " + ru("людей (пять человек), лет, детей, денег, братьев, друзей, стульев, раз, глаз, солдат, сапог, носков, кур, яиц, семей, тёть, мест, дел, полей") + ".</li>"
      + "<li>The verb agrees with the <b>subject</b>: " + ru("Мне нравятся все виды сыра") + " (виды = plural).</li>"
      + "<li>Genitive prepositions: " + ru("для, кроме, напротив, ради, без, из, от, после, около") + " (and " + ru("у") + ").</li>"
      + "<li>" + ru("кроме") + " = except (gen.); " + ru("напротив") + " = opposite / across from (gen.); " + ru("перед") + " = in front of (<b>instrumental</b>).</li>"
      + "</ul>"})

    def it(part, sub, k, s, w, ans, d, ex, tr, gl=None, **extra):
        item = {"part": part, "sub": sub, "k": k, "w": w, "s": s, "base": extra.pop("base", w), "a": ans, "d": d,
                "ex": ex, "translation": tr, "glosses": gl or []}
        item.update(extra)
        return item
    PA, PB, PC = "A · genitive plural endings", "B · exceptions to watch", "C · genitive prepositions: кроме / напротив / перед"
    EX = [
     # Part A · endings
     it("A", PA, "gpl", "У нас на ферме двадцать ___.", "корова", "коров", ["коровы", "корова", "коровов"],
        "20 behaves like 5+: genitive plural. Feminine -а has a zero ending: коров (shorter than корова). (Steps 3 and 4)",
        "We have twenty cows on the farm."),
     it("A", PA, "gpl", "На работе у нас пять ___.", "программист", "программистов", ["программисты", "программиста", "программист"],
        "After 5: genitive plural. Masculine hard consonant → -ов. (Steps 2 and 4)",
        "We have five programmers at work."),
     it("A", PA, "gpl", "Сколько ___ в Джексоне?", "музей", "музеев", ["музеи", "музеей", "музея"],
        "Сколько takes the genitive plural. Masculine -й → -ев: музеев. (Steps 2 and 4)",
        "How many museums are there in Jackson?"),
     it("A", PA, "gpl", "В нашем городе мало ___.", "врач", "врачей", ["врачов", "врачи", "врача"],
        "Мало + genitive plural. After ч the ending is -ей, not -ов. (Step 2)",
        "There are few doctors in our town."),
     it("A", PA, "gpl", "У жены много ___.", "подруга", "подруг", ["подруги", "подругов", "подруге"],
        "Много + genitive plural. Feminine -а: zero ending, подруг. (Steps 3 and 4)",
        "My wife has a lot of friends."),
     it("A", PA, "gpl", "На кухне нет чистых ___.", "тарелка", "тарелок", ["тарелки", "тарелков", "тарелка"],
        "Нет + genitive plural. Zero ending; тарелк can't be said, so a fleeting о is inserted: тарелок. Чистых agrees. (Steps 3 and 4)",
        "There are no clean plates in the kitchen.", ["чистый: clean"]),
     it("A", PA, "gpl", "У меня две сестры, а у друга пять ___.", "сестра", "сестёр", ["сестры", "сестров", "сестрей"],
        "After 5: genitive plural, zero ending with an inserted ё: сестёр. After 2 it's the genitive singular сестры. (Steps 3 and 4)",
        "I have two sisters, and my friend has five."),
     it("A", PA, "gpl", "На новом альбоме Молчат Дома десять ___.", "песня", "песен", ["песни", "песнов", "песнях"],
        "After 10: genitive plural. Песня → песен (zero ending + fleeting е). (Steps 3 and 4)",
        "There are ten songs on the new Molchat Doma album."),
     it("A", PA, "gpl", "В Минске несколько ___.", "посольство", "посольств", ["посольства", "посольствов", "посольстве"],
        "Несколько + genitive plural. Neuter -о: zero ending, посольств. (Steps 3 and 4)",
        "There are several embassies in Minsk.", ["посольство: embassy"]),
     it("A", PA, "gpl", "Батюшка служит много ___ в году.", "литургия", "литургий", ["литургии", "литургией", "литургиев"],
        "Много + genitive plural. Feminine -ия → -ий: литургий. (Step 3)",
        "Father serves many liturgies a year.", ["служить: to serve (a service)"]),
     it("A", PA, "gpl", "На службе было много ___ с детьми.", "мать", "матерей", ["матери", "матей", "мать"],
        "Много + genitive plural. Мать brings back its hidden -ер-: матерей (like дочерей). (Steps 1 and 3)",
        "There were many mothers with children at the service."),

     # Part B · exceptions
     it("B", PB, "gpl_num", "На онлайн-конференции было сто ___.", "человек", "человек", ["людей", "человеков", "люди"],
        "After a number, человек stays человек: сто человек. Людей is for много / мало / сколько. (Step 5)",
        "There were a hundred people at the online conference.", ["онлайн-конференция: online conference"]),
     it("B", PB, "gpl", "В храме на Пасху было много ___.", "человек", "людей", ["человек", "человеков", "люди"],
        "After много use людей (from люди). Пять человек, but много людей. (Step 5)",
        "There were a lot of people in church at Easter.", base="человек / люди"),
     it("B", PB, "gpl", "Мне сорок пять ___.", "год", "лет", ["годов", "года", "годы"],
        "45 ends in 5: genitive plural, and for год that's лет. Годов is only for decades. (Step 5 and the Numbers section)",
        "I'm forty-five."),
     it("B", PB, "gpl", "У брата трое ___.", "ребёнок", "детей", ["ребёнков", "дети", "ребёнка"],
        "Трое (a group of three) takes the genitive plural. Ребёнок → дети → детей. (Step 5)",
        "My brother has three children."),
     it("B", PB, "gpl", "У меня нет ___ на новый трактор.", "деньги", "денег", ["деньгов", "деньги", "деньгах"],
        "Нет + genitive plural. Деньги → денег (fleeting е), never деньгов. (Step 5)",
        "I don't have money for a new tractor."),
     it("B", PB, "gpl", "У жены пять ___.", "брат", "братьев", ["братов", "братья", "брата"],
        "After 5: genitive plural. Брат → братья → братьев, not братов. (Step 5)",
        "My wife has five brothers."),
     it("B", PB, "gpl", "На мой день рождения пришло много ___.", "друг", "друзей", ["другов", "друзья", "друга"],
        "Много + genitive plural. Друг → друзья → друзей, not другов. (Step 5)",
        "A lot of friends came to my birthday."),
     it("B", PB, "gpl", "На кухне шесть ___.", "стул", "стульев", ["стулов", "стулья", "стула"],
        "After 6: genitive plural. Стул → стулья → стульев (like братьев). (Step 5)",
        "There are six chairs in the kitchen."),
     it("B", PB, "gpl", "Я звонил тебе пять ___!", "раз", "раз", ["разов", "раза", "разы"],
        "Раз (time, occasion) has no ending in the genitive plural: пять раз. Two times = два раза. (Step 5)",
        "I called you five times!"),
     it("B", PB, "gpl", "У нас много ___, но мало петухов.", "куры", "кур", ["куров", "куры", "курей"],
        "Много + genitive plural. The farm plural куры → кур. (The textbook куриц is also correct.) Петухов is regular -ов. (Step 5)",
        "We have a lot of hens but few roosters.", base="куры (курица)", alt=["куриц"]),
     it("B", PB, "gpl", "Наши куры несут десять ___ в день.", "яйцо", "яиц", ["яйцов", "яйца", "яйцев"],
        "After 10: genitive plural, and яйцо is irregular: яиц. (2–4 would be яйца.) (Step 5)",
        "Our hens lay ten eggs a day."),
     it("B", PB, "gpl", "В нашей церкви много больших ___.", "семья", "семей", ["семьёв", "семьи", "семьёй"],
        "Много + genitive plural. Семья → семей. Больших agrees with it. (Step 5)",
        "There are many big families in our church."),
     it("B", PB, "gpl", "В фильме «Солдаты неудачи» пять ___.", "солдат", "солдат", ["солдатов", "солдаты", "солдата"],
        "After 5: genitive plural. Солдат is a masculine word with a zero ending: пять солдат. (Step 5)",
        "There are five soldiers in the film Tropic Thunder.", ["«Солдаты неудачи»: the Russian title of Tropic Thunder"]),
     it("B", PB, "nslike", "Мне ___ все виды сыра, кроме бри.", "нравиться", "нравятся", ["нравится", "нравлюсь", "нравишься"],
        "The subject is все виды (plural), so the verb is plural: нравятся. Сыра is genitive and doesn't decide the verb. (Step 5)",
        "I like all kinds of cheese except Brie.", ["вид: kind, type", "бри: Brie (indeclinable)"], g="pl"),

     # Part C · prepositions
     it("C", PC, "gen", "Вода для моих ___.", "корова", "коров", ["коровы", "коровам", "корову"],
        "Для takes the genitive; plural → genitive plural коров. Моих agrees. (Step 6)",
        "Water for my cows.", base="корова · plural"),
     it("C", PC, "gen", "Я ем всё, кроме ___.", "сыр", "сыра", ["сыр", "сыру", "сыром"],
        "Кроме (except) takes the genitive: кроме сыра. (Steps 6 and 7)",
        "I eat everything except cheese."),
     it("C", PC, "gen", "Моя машина стоит напротив моего ___.", "дом", "дома", ["дом", "доме", "домом"],
        "Напротив (opposite, across from) takes the genitive: напротив моего дома. Домом would need перед. (Steps 6 and 7)",
        "My car is parked across from my house."),
     it("C", PC, "gen", "Я работаю ради моей ___.", "семья", "семьи", ["семью", "семье", "семьёй"],
        "Ради (for the sake of) takes the genitive: ради моей семьи. (Step 6)",
        "I work for the sake of my family."),
     it("C", PC, "gen", "После ___ мы пьём чай у батюшки.", "служба", "службы", ["служба", "службу", "службой"],
        "После takes the genitive: после службы. (Перед службой would be instrumental.) (Step 6)",
        "After the service we have tea at Father's."),
     it("C", PC, "gen", "Около ___ есть маленький магазин.", "заправка", "заправки", ["заправка", "заправку", "заправкой"],
        "Около (near) takes the genitive: около заправки. (Step 6)",
        "There's a small store near the gas station.", ["заправка: gas station"]),
     it("C", PC, "ins", "Мой пикап стоит перед ___.", "дом", "домом", ["дома", "доме", "дом"],
        "Перед (in front of) takes the instrumental: перед домом. Напротив дома would be across the street. (Step 7)",
        "My pickup is parked in front of the house.", ["пикап: pickup truck"]),
     it("C", PC, "prep", "Наша церковь стоит ___ почты, через дорогу.", "кроме / напротив / перед", "напротив", ["перед", "кроме", "для"],
        "Почты is genitive, so not перед; через дорогу (across the road) means напротив. (Step 7)",
        "Our church stands opposite the post office, across the road."),
     it("C", PC, "prep", "Машина стоит ___ домом.", "кроме / напротив / перед", "перед", ["напротив", "кроме", "для"],
        "Домом is instrumental, and only перед takes the instrumental here: in front of the house. (Step 7)",
        "The car is parked in front of the house."),
     it("C", PC, "prep", "На ферме никого не было, ___ меня.", "кроме / напротив / перед", "кроме", ["напротив", "перед", "ради"],
        "Nobody was there except me: кроме + genitive (меня). (Step 7)",
        "There was no one on the farm except me."),
     it("C", PC, "prep", "Жена молится ___ иконой.", "кроме / напротив / перед", "перед", ["напротив", "кроме", "для"],
        "Иконой is instrumental: перед иконой, in front of the icon. (Step 7)",
        "My wife prays in front of the icon."),
     it("C", PC, "prep", "Я живу ___ школы, прямо через улицу.", "кроме / напротив / перед", "напротив", ["перед", "кроме", "ради"],
        "Школы is genitive and через улицу tells you it's across the street: напротив школы. (Step 7)",
        "I live opposite the school, right across the street."),
     it("C", PC, "prep", "Я люблю все песни Молчат Дома, ___ одной.", "кроме / напротив / перед", "кроме", ["напротив", "перед", "для"],
        "All the songs except one: кроме + genitive (одной). (Step 7)",
        "I love all of Molchat Doma's songs except one."),
    ]
    L = {
      "id": "L9", "n": 9,
      "title": "Plurals and the genitive plural: пять коров, много друзей",
      "goal": "By the end you'll count and quantify anything: У нас двадцать коров. У жены много подруг. Мне сорок пять лет. You'll also use the genitive prepositions (для, кроме, напротив, ради…) and tell напротив from перед.",
      "minutes": "20–25 min to read, then %d exercises" % len(EX),
      "sections": S,
      "parts": {"A": "Part A · genitive plural endings", "B": "Part B · exceptions to watch", "C": "Part C · genitive prepositions: кроме / напротив / перед"},
      "practice": {
        "title": "Now use it: write to your tutor",
        "text": "Answer in chat: Что есть напротив твоего дома? Для кого ты работаешь? Кого и чего у тебя много? Write 4 sentences: one with напротив, one with для or ради, one with много / мало + genitive plural, and one with a number of 5 or more (watch the exceptions: людей / человек, лет, яиц, друзей).",
        "examples": ["Напротив моего дома большое поле.", "Я работаю ради моей семьи.", "У нас много коров и кур.", "Наши куры несут десять яиц в день."]
      },
      "exercises": EX,
    }
    return L
