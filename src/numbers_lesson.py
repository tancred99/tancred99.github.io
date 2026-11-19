# The Numbers teaching page (shown in the Numbers tab → Learn). Built by lessons_src.py into lessons.json["numbers"].
# Number words in the tables come from numbers_ref.py (the same data the drills use), tagged data-n / data-p so verify_numbers.py can re-check them.
import html
import numbers_ref as R

def build(t, ru, exl):
    NB = "\u00a0"
    def fmt(n): return "{:,}".format(n).replace(",", NB) if n >= 1000 else str(n)
    def nw(n, g="m", full=False):          # number word(s), stressed, tagged for the verifier
        return '<span lang="ru" class="r" data-n="%d" data-g="%s">%s</span>' % (n, g, R.words(n, g, full, stress=True))
    def pw(n, forms, g):                   # number + counted noun
        return '<span lang="ru" class="r" data-p="%d|%s|%s">%s</span>' % (n, ",".join(R.strip(x) for x in forms), g, R.phrase_words(n, forms, g, stress=True))
    def say_list(items): return html.escape(", ".join(R.strip(x) for x in items), quote=True)
    def rv(inner, say_text, hint="Say each word out loud first. Then check:"):
        return ('<div class="rv nostress"><div class="rvbar"><span class="rvh">%s</span>'
                '<button type="button" class="sbtn" data-rv="1" aria-pressed="false">Show stress ´</button>'
                '<button type="button" class="sbtn" data-say="%s">🔊 Hear them</button></div>%s</div>') % (hint, say_text, inner)
    COW = ("корова", "коровы", "коров"); TRACTOR = ("трактор", "трактора", "тракторов"); SACK = ("мешок", "мешка", "мешков"); EGG = ("яйцо", "яйца", "яиц")
    RUB = R.D["money"]["рубль"]; USD = R.D["money"]["доллар"]; EUR = R.D["money"]["евро"]; KOP = R.D["money"]["копейка"]; YEAR = R.D["year"]
    def fmt_(x): return x.replace(" ", NB)

    S = []
    # ---- Step 1
    de = ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn"]
    rows = [[str(i), nw(i), de[i]] for i in range(11)]
    S.append({"h": "Step 1 · 0 to 10 (a quick review)", "open": True, "html":
      "<p>You know most of these. Say each one out loud before you look at the stress marks. The goal is to <b>say them from the digits</b>, not to recognize them on a flashcard.</p>"
      + rv(t(["Digit", "Russian", "German"], rows), say_list([R.words(i) for i in range(11)]))
      + '<p class="tip"><b>German helps:</b> ' + ru("три") + " = drei, " + ru("шесть") + " = sechs, " + ru("семь") + " = sieben, " + ru("десять") + " = zehn. The ones to drill are " + ru("восемь") + " (<i>acht</i>) and " + ru("девять") + " (<i>neun</i>): nothing in them sounds like the German.</p>"
      + "<p>" + ru("ноль") + " is zero (" + ru("нуль") + " also exists, but you'll hear " + ru("ноль") + " much more).</p>"})

    # ---- Step 2
    base = {11: "один + на + дцать", 12: "две + на + дцать", 13: "три + на + дцать", 14: "четыр(е) + на + дцать", 15: "пят(ь) + на + дцать", 16: "шест(ь) + на + дцать", 17: "сем(ь) + на + дцать", 18: "восем(ь) + на + дцать", 19: "девят(ь) + на + дцать"}
    rows = [[str(n), nw(n), ru(base[n])] for n in range(11, 20)]
    S.append({"h": "Step 2 · 11 to 19: the -надцать numbers", "open": False, "html":
      "<p>All of 11–19 follow one pattern: <b>the unit + " + ru("-надцать") + "</b>. " + ru("на") + " means “on” and " + ru("-дцать") + " is a short form of " + ru("десять") + ", so " + ru("одиннадцать") + " is literally “one-on-ten”. German does the same: <i>drei</i> + <i>zehn</i> = <i>dreizehn</i>.</p>"
      + rv(t(["Digit", "Russian", "Built from"], rows), say_list([R.words(n) for n in range(11, 20)]))
      + "<h4>Stress</h4><p>The stress sits on the syllable <b>just before -надцать</b>: " + nw(12) + ", " + nw(13) + ", " + nw(15) + ", " + nw(16) + ", " + nw(17) + ", " + nw(18) + ", " + nw(19) + ". Two numbers keep the stress of the word they're built from: " + nw(11) + " (like " + nw(1) + ") and " + nw(14) + " (like " + nw(4) + ").</p>"
      + '<p class="tip"><b>Spelling:</b> the soft sign of ' + ru("пять, шесть, семь, восемь, девять") + " disappears in the teens: " + ru("пятнадцать") + " (not “пятьнадцать”).</p>"})

    # ---- Step 3
    tbase = {20: ru("два + дцать"), 30: ru("три + дцать"), 40: ru("сорок") + " (irregular)", 50: ru("пять + десят"), 60: ru("шесть + десят"), 70: ru("семь + десят"), 80: ru("восемь + десят"), 90: ru("девяносто") + " (irregular)"}
    rows = [[str(n), nw(n), tbase[n]] for n in range(20, 100, 10)]
    conf = [[nw(14) + " / " + nw(40), "14 / 40"], [nw(15) + " / " + nw(50), "15 / 50"], [nw(16) + " / " + nw(60), "16 / 60"], [nw(17) + " / " + nw(70), "17 / 70"], [nw(18) + " / " + nw(80), "18 / 80"], [nw(19) + " / " + nw(90), "19 / 90"]]
    S.append({"h": "Step 3 · The tens: 20 to 90", "open": False, "html":
      "<p>20 and 30 end in " + ru("-дцать") + ". 50 to 80 are “unit + " + ru("десят") + "” (five tens, six tens…). <b>40 and 90 are irregular</b> and have to be memorized, like " + ru("сто") + " (100).</p>"
      + rv(t(["Digit", "Russian", "Built from"], rows), say_list([R.words(n) for n in range(20, 100, 10)]))
      + "<h4>Stress</h4><p>" + nw(50) + " and " + nw(60) + " are stressed at the <b>end</b>; " + nw(70) + " and " + nw(80) + " at the <b>start</b>. Those two long words are the hardest in this lesson: say " + nw(70) + " and " + nw(80) + " aloud a few times. Note the soft sign in the middle of 50–80: " + ru("пятьдесят") + ".</p>"
      + "<h4>Teen or ten? The pairs people mix up</h4><p>When you listen, the ending tells you: <b>" + ru("-надцать") + "</b> is a teen (14–19), while " + ru("сорок") + ", " + ru("-десят") + " and " + ru("девяносто") + " are tens.</p>"
      + rv(t(["Teen / ten", "Digits"], conf), say_list([R.words(n) for n in (14, 40, 15, 50, 16, 60, 17, 70, 18, 80, 19, 90)]), "Say both, then check which is which:")})

    # ---- Step 4
    hb = {100: ru("сто") + " (irregular)", 200: ru("две + сти"), 300: ru("три + ста"), 400: ru("четыре + ста"), 500: ru("пять + сот"), 600: ru("шесть + сот"), 700: ru("семь + сот"), 800: ru("восемь + сот"), 900: ru("девять + сот")}
    rows = [[fmt(n), nw(n), hb[n]] for n in range(100, 1000, 100)]
    S.append({"h": "Step 4 · The hundreds: 100 to 900", "open": False, "html":
      "<p>The hundreds are three small groups: <b>100</b> " + ru("сто") + " (one word, no ending), <b>200–400</b> " + ru("двести, триста, четыреста") + " (the word " + ru("сто") + " has a special form after 2, 3, 4), and <b>500–900</b> = unit + " + ru("сот") + ", where " + ru("сот") + " is the genitive plural of " + ru("сто") + " (“five of hundreds”). The 500–900 words are the long ones: " + nw(900) + ", " + nw(800) + ".</p>"
      + rv(t(["Digit", "Russian", "Built from"], rows), say_list([R.words(n) for n in range(100, 1000, 100)]))
      + "<h4>Stress</h4><p>200, 300 and 400 are stressed on the <b>first or second syllable</b> (" + nw(200) + ", " + nw(300) + ", " + nw(400) + "). 500 to 900 are all stressed on the last syllable, " + ru("-сот") + ": " + nw(500) + ", " + nw(900) + ". There's a soft sign in every one of them (" + ru("пятьсот") + ").</p>"})

    # ---- Step 5
    rows = [[fmt(n), nw(n), note] for n, note in [(1000, "<i>одна тысяча</i> is also correct, but one thousand on its own is just " + ru("тысяча")), (2000, "2–4: " + ru("тысячи")), (5000, "5 and up: " + ru("тысяч")), (21000, "ends in 1: " + ru("одна тысяча")), (1000000, "one million on its own is just " + ru("миллион") + " (" + ru("один миллион") + " is also fine)"), (2000000, ru("миллиона")), (5000000, ru("миллионов"))]]
    S.append({"h": "Step 5 · Thousands and millions", "open": False, "html":
      "<p>" + ru("тысяча") + " (1000) is a <b>feminine noun</b>, and " + ru("миллион") + " (1,000,000) is a <b>masculine noun</b>. That has two consequences: you count them like any other noun (Step 8), and " + ru("тысяча") + " needs the feminine <b>одна / две</b> (Step 7).</p>"
      + rv(t(["Digit", "Russian", "Note"], rows), say_list([R.words(n) for n in (1000, 2000, 5000, 21000, 1000000, 2000000, 5000000)]))
      + '<p class="tip"><b>Writing digits:</b> Russian puts a space in big numbers (12' + NB + '500) where English puts a comma, and uses a <b>comma as the decimal point</b> (3,5 = 3.5). The next size up is ' + ru("миллиард") + " (a billion).</p>"})

    # ---- Step 6
    ex = [(21, ""), (35, ""), (101, ""), (347, ""), (512, "the teen stays one word: " + nw(12) + ", not “десять два”"), (1985, ""), (2026, "this year"), (12500, ""), (250000, ""), (1250000, "")]
    rows = [[fmt(n), nw(n), note] for n, note in ex]
    S.append({"h": "Step 6 · Building any number", "open": False, "html":
      "<p>Say a number <b>from left to right, biggest part first</b>. There's no “and”, no hyphen, and every part is its own word: " + nw(347) + " = " + ru("триста") + " + " + ru("сорок") + " + " + ru("семь") + ". <b>German reverses the order</b> of units and tens (<i>einundzwanzig</i>, one-and-twenty); Russian doesn't: " + nw(21) + " is simply “twenty one”.</p>"
      + "<p>For big numbers, split the digits <b>from the right into groups of three</b> and read each group like a small number, adding " + ru("тысяча / тысячи / тысяч") + " or " + ru("миллион…") + " after its group:</p>"
      + t(["Digits", "Groups", "Words"], [["4" + NB + "762", "4 | 762", nw(4762)], ["250" + NB + "300", "250 | 300", nw(250300)]])
      + rv(t(["Digit", "Russian", "Note"], rows), say_list([R.words(n) for n, _ in ex]))
      + '<p class="tip"><b>Years</b> are read the same way, with the last word turned into an ordinal (Step 12): ' + ru("две тысячи двадцать шестой год") + " (2026).</p>"})

    # ---- Step 7
    U = R.D["units"]
    def one(g, noun): return '<span lang="ru" class="r">%s %s</span>' % (U[g][1], noun)
    def two(g, noun): return '<span lang="ru" class="r">%s %s</span>' % (U[g][2], noun)
    G = [[one("m", "дом") + " · " + one("m", "мешок"), one("f", "корова") + " · " + one("f", "тысяча"), one("n", "яйцо") + " · " + one("n", "окно")],
         [two("m", "дома") + " · " + two("m", "мешка"), two("f", "коровы") + " · " + two("f", "тысячи"), two("n", "яйца") + " · " + two("n", "окна")]]
    S.append({"h": "Step 7 · один/одна/одно and два/две", "open": False, "html":
      "<p>Only <b>1 and 2</b> have gender. They agree with the counted noun, like German <i>ein / eine / ein</i>. 2 has just two forms: " + ru("два") + " for masculine and neuter, " + ru("две") + " for feminine.</p>"
      + t(["Masculine", "Feminine", "Neuter"], G)
      + "<p>This applies at the end of a compound number too: " + pw(21, COW, "f") + " (21 cows), " + pw(22, COW, "f") + " (22 cows), " + pw(31, EGG, "n") + " (31 eggs). And " + ru("тысяча") + " is feminine, so 2000 is " + nw(2000) + " even if you're counting tractors.</p>"})

    # ---- Step 8
    rule = [["1 (not 11)", "<b>nominative singular</b>", pw(1, COW, "f") + " · " + pw(21, COW, "f") + " · " + pw(101, TRACTOR, "m")],
            ["2, 3, 4 (not 12–14)", "<b>genitive singular</b>", pw(2, COW, "f") + " · " + pw(4, TRACTOR, "m") + " · " + pw(22, EGG, "n")],
            ["5 to 20, and 0", "<b>genitive plural</b>", pw(5, COW, "f") + " · " + pw(7, SACK, "m") + " · " + pw(20, TRACTOR, "m")],
            ["11, 12, 13, 14", "<b>genitive plural</b> (the exception)", pw(11, COW, "f") + " · " + pw(12, TRACTOR, "m") + " · " + pw(14, EGG, "n")]]
    S.append({"h": "Step 8 · The noun after a number", "open": False, "html":
      "<p>This is the rule most beginner courses skip, and it's the most useful one in the lesson. After a number the noun is <b>not</b> in the plural nominative like English “five cows”. Instead:</p>"
      + t(["The number ends in", "The noun is in the", "Examples"], rule)
      + "<p>Why the genitive? The number is the <b>subject</b> (nominative) and the counted thing hangs off it as “of”: " + ru("пять коров") + " is literally “five <i>of cows</i>”. It's the case of " + ru("нет коров") + " in Lesson 4, and the case German uses for “of” (<i>der Kühe</i>). German is closer to Russian than to English here: <i>fünf Sack Futter</i> (five sack feed) has no plural after the number either.</p>"
      + "<h4>Compound numbers: only the last digits count</h4>"
      + t(["Number", "Looks at", "Noun form", "Example"], [
          ["21, 31, 101, 1001", "ends in 1", "nominative singular", pw(21, COW, "f") + " · " + pw(1001, TRACTOR, "m")],
          ["22, 33, 104, 2003", "ends in 2, 3, 4", "genitive singular", pw(22, COW, "f") + " · " + pw(104, TRACTOR, "m")],
          ["25, 100, 2500", "ends in 0, 5–9", "genitive plural", pw(25, COW, "f") + " · " + pw(100, TRACTOR, "m")],
          ["111, 212, 1014", "ends in 11–14", "genitive plural", pw(111, COW, "f") + " · " + pw(212, TRACTOR, "m")],
          ["2000, 21000, 5000000", "round thousands and millions", "genitive plural", pw(2000, TRACTOR, "m") + " · " + pw(21000, COW, "f")]])
      + "<h4>On the farm</h4>"
      + exl([("У нас двадцать одна корова.", "We have 21 cows. (One cow: nominative singular, feminine one.)"),
             ("Я купил семь мешков корма.", "I bought 7 sacks of feed. (мешков = genitive plural after семь; корма = genitive singular, “of feed”.)"),
             ("На ферме два трактора.", "There are two tractors on the farm. (genitive singular)"),
             ("В магазине двенадцать мешков.", "There are 12 sacks in the store. (11–14 are the exception.)")])
      + '<p class="tip"><b>Mnemonic:</b> “1 stays, 2–4 shrinks, 5+ grows”: the dictionary form for 1, the short genitive for 2–4, the long genitive plural for 5 and up. A few nouns have an irregular genitive plural (' + ru("яйцо → яиц") + ", " + ru("человек → человек") + "), but the pattern is always the same.</p>"})

    # ---- Step 9
    pr = [(1, RUB, "m", "{} ₽"), (2, RUB, "m", "{} ₽"), (5, RUB, "m", "{} ₽"), (21, RUB, "m", "{} ₽"), (11, RUB, "m", "{} ₽"), (100, RUB, "m", "{} ₽"), (1000, RUB, "m", "{} ₽"), (2500, RUB, "m", "{} ₽"),
          (12, USD, "m", "${}"), (5, EUR, "n", "{} €"), (50, KOP, "f", "{} коп.")]
    rows = [[fmt_(f.format(fmt(n))), pw(n, forms, g)] for n, forms, g, f in pr]
    S.append({"h": "Step 9 · Prices", "open": False, "html":
      "<p>Prices are just Step 8 with money nouns: " + ru("рубль / рубля / рублей") + ", " + ru("доллар / доллара / долларов") + ", " + ru("копейка / копейки / копеек") + ". " + ru("евро") + " never changes (like " + ru("кофе") + "). Belarus uses " + ru("рубли") + " too.</p>"
      + exl([("Сколько это стоит?", "How much is it?"), ("Это стоит сто двадцать рублей.", "It costs 120 rubles."), ("С вас пятьсот рублей.", "That's 500 rubles from you. (what the cashier says)")])
      + t(["Written", "Said"], rows)
      + '<p class="tip">' + ru("рубль") + " is masculine, so 21 is " + ru("двадцать один рубль") + " and 2 is " + ru("два рубля") + "; " + ru("копейка") + " is feminine: " + ru("одна копейка, две копейки") + ".</p>"})

    # ---- Step 10
    S.append({"h": "Step 10 · Age", "open": False, "html":
      "<p>To say how old someone is, Russian uses the person in the <b>dative case</b> (the indirect object: “to me”) plus the number and " + ru("год / года / лет") + ". There's no verb, and no “I am”:</p>"
      + exl([("Сколько тебе лет?", "How old are you? (literally: to you how many years?)"), ("Мне сорок один год.", "I'm 41. (literally: to me 41 years)"), ("Ей двадцать два года.", "She's 22."), ("Ему пятьдесят лет.", "He's 50.")])
      + "<p>The dative pronouns: " + ru("мне") + " (me), " + ru("тебе") + " (you), " + ru("ему") + " (him), " + ru("ей") + " (her), " + ru("нам") + " (us), " + ru("им") + " (them). Lesson 7 covers the dative properly; for now just learn these.</p>"
      + t(["Age", "Said"], [[str(n), pw(n, YEAR, "m")] for n in (1, 2, 4, 5, 11, 12, 20, 21, 22, 25, 33, 41, 64, 100)])
      + '<p class="tip"><b>' + ru("лет") + "</b> is the genitive plural of " + ru("год") + " when you talk about age or a number of years (" + ru("пять лет") + "). It's an irregular form you simply memorize, a bit like English <i>go / went</i>. " + ru("годов") + " is only used in phrases like " + ru("в девяностых годах") + ".</p>"})

    # ---- Step 11
    ph = [["123-45-67", "123 | 45 | 67", ru(R.phone_words(123, 45, 67, stress=True))], ["305-02-10", "305 | 02 | 10", ru(R.phone_words(305, 2, 10, stress=True))],
          ["+375", "Belarus", ru("плюс " + R.words(375, stress=True))], ["+7 (495)", "Moscow", ru("плюс семь, " + R.words(495, stress=True))]]
    S.append({"h": "Step 11 · Phone numbers", "open": False, "html":
      "<p>Russians read a phone number in <b>groups</b>, like small numbers, not digit by digit. A local number is usually 3 + 2 + 2: " + ru("123-45-67") + " is " + ru("сто двадцать три, сорок пять, шестьдесят семь") + ". A group such as 05 is " + ru("ноль пять") + ", and 00 is " + ru("ноль ноль") + ". Country codes are read as numbers too.</p>"
      + t(["Written", "Groups", "Said"], ph)})

    # ---- Step 12
    ords = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 100]
    rows = [[str(i) + "-й", '<span lang="ru" class="r">%s</span>' % R.ordinal(i, "m"), '<span lang="ru" class="r">%s</span>' % R.ordinal(i, "f"), '<span lang="ru" class="r">%s</span>' % R.ordinal(i, "n")] for i in ords]
    S.append({"h": "Step 12 · Ordinals, dates and years (a first look)", "open": False, "html":
      "<p>Ordinals (1st, 2nd…) are <b>adjectives</b>, so they agree with their noun in gender, number and case, like " + ru("новый / новая / новое") + ": " + ru("первый урок") + ", " + ru("первая лекция") + ", " + ru("первое мая") + ". The dictionary form is masculine nominative, ending in " + ru("-ый, -ой") + " or " + ru("-ий") + ".</p>"
      + rv(t(["Digit", "Masc.", "Fem.", "Neut."], rows), say_list([R.strip(R.ordinal(i)) for i in ords]))
      + "<p>In a compound number <b>only the last word</b> is the ordinal: " + ru("двадцать первый") + " (21st), " + ru("сто двадцатый") + " (120th).</p>"
      + "<h4>Dates</h4><p>The day is a neuter ordinal (it agrees with the unspoken " + ru("число") + ", “date”) and the month is in the <b>genitive</b>: “the 19th <i>of</i> November”.</p>"
      + exl([("Какое сегодня число?", "What's today's date?"), ("Сегодня " + R.ordinal(19, "n") + " ноября.", "Today is November 19th.")])
      + t(["Date", "Said"], [["1 мая", '<span lang="ru" class="r">%s мая</span>' % R.ordinal(1, "n")], ["8 марта", '<span lang="ru" class="r">%s марта</span>' % R.ordinal(8, "n")], ["20 июня", '<span lang="ru" class="r">%s июня</span>' % R.ordinal(20, "n")], ["25 декабря", '<span lang="ru" class="r">%s %s декабря</span>' % (R.words(20, stress=True), R.ordinal(5, "n"))]])
      + "<p>Years: the last element is an ordinal and " + ru("год") + " follows: " + ru("две тысячи двадцать шестой год") + " (2026), and “in 2026” is " + ru("в две тысячи двадцать шестом году") + ".</p>"})

    # ---- Step 13
    S.append({"h": "Step 13 · Numbers change case too (just a heads-up)", "open": False, "html":
      "<p>Numbers decline like nouns and adjectives. You don't need to produce these yet, but you'll hear them, so recognize them:</p>"
      + t(["Nominative", "Genitive", "Dative", "Instrumental"], [[ru("два / две"), ru("двух"), ru("двум"), ru("двумя́")], [ru("три"), ru("трёх"), ru("трём"), ru("тремя́")], [ru("пять"), ru("пяти́"), ru("пяти́"), ru("пятью́")], [ru("двадцать"), ru("двадцати́"), ru("двадцати́"), ru("двадцатью́")]])
      + exl([("Это корм для двух коров.", "This is feed for two cows."), ("Мне нужно пять мешков корма.", "I need five sacks of feed. (the nominative form after нужно)"), ("У нас нет пяти коров.", "We don't have five cows.")])
      + "<p>Notice that after a case change the noun goes to the <b>plural of that case</b>: " + ru("двух коров") + " (genitive plural), not the singular. In the nominative (and accusative of things) the Step 8 rule applies.</p>"})

    # ---- Step 14
    S.append({"h": "Summary", "open": False, "html":
      "<ul class='sum'>"
      "<li><b>11–19:</b> unit + " + ru("-надцать") + "; stress before " + ru("-надцать") + " (" + ru("двенадцать") + "), except " + ru("одиннадцать") + " and " + ru("четырнадцать") + ".</li>"
      "<li><b>Tens:</b> " + ru("двадцать, тридцать, сорок, пятьдесят, шестьдесят, семьдесят, восемьдесят, девяносто") + ". Irregular: " + ru("сорок, девяносто, сто") + ".</li>"
      "<li><b>Hundreds:</b> " + ru("сто, двести, триста, четыреста, пятьсот … девятьсот") + ".</li>"
      "<li><b>Big numbers:</b> left to right, groups of three, with " + ru("тысяча / тысячи / тысяч") + " (feminine) and " + ru("миллион") + " (masculine).</li>"
      "<li><b>Gender:</b> " + ru("один / одна / одно") + ", " + ru("два / две") + ", also at the end of compounds.</li>"
      "<li><b>Noun after a number:</b> ends in 1 → nominative singular; 2–4 → genitive singular; 5–20, 0, 11–14 → genitive plural. Only the last digits count.</li>"
      "<li><b>Age:</b> dative person + number + " + ru("год / года / лет") + ": " + ru("Мне сорок лет") + ". <b>Prices:</b> " + ru("рубль / рубля / рублей") + ".</li>"
      "<li><b>Ordinals</b> are adjectives. In dates, the day is a neuter ordinal and the month is genitive.</li>"
      "</ul>"})

    return {
      "id": "N1", "title": "Numbers: from 0 to a million",
      "goal": "By the end you'll be able to read, say and hear numbers up to a million and use the right noun after them: Мне сорок лет. У нас двадцать две коровы. Это стоит триста пятьдесят рублей.",
      "minutes": "20–30 min to read, then unlimited practice",
      "sections": S,
      "practice": {
        "title": "Now use it: write to your tutor",
        "text": "Answer in chat with full sentences, with the numbers written in words: Сколько у тебя коров? Сколько тебе лет? Сколько стоит мешок корма?",
        "examples": ["У нас двадцать две коровы.", "Мне сорок лет.", "Мешок корма стоит тысяча двести рублей."]
      }
    }
