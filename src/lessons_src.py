# Source for lessons.json. Run: python3 src/lessons_src.py  (build.py runs it too)
# Lesson text is trusted HTML written here; exercises use the same shape as the drill items.
import json, os

def t(head, rows, cls=""):
    h = '<div class="tw"><table class="lt %s"><thead><tr>%s</tr></thead><tbody>' % (cls, "".join("<th>%s</th>" % x for x in head))
    for r in rows:
        h += "<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>"
    return h + "</tbody></table></div>"

def ru(s): return '<span lang="ru" class="r">%s</span>' % s
def exl(pairs):  # example lines: Russian, English
    return '<ul class="exl">' + "".join('<li><span lang="ru" class="r">%s</span><span class="g">%s</span></li>' % p for p in pairs) + "</ul>"

COURSE = [
  {"n": 1, "id": "L1", "title": "Noun gender + the prepositional case", "topic": "где? в/на — saying where something is"},
  {"n": 2, "id": "L2", "title": "Accusative (things) + куда? в/на", "topic": "saying where you're going"},
  {"n": 3, "id": "L3", "title": "Present tense: 1st and 2nd conjugation", "topic": "я читаю, ты говоришь"},
  {"n": 4, "id": "L4", "title": "Genitive: у меня есть / нет", "topic": "having and not having"},
  {"review": True, "id": "R1", "title": "Review 1", "topic": "mixed practice on lessons 1–4"},
  {"n": 5, "id": "L5", "title": "Past tense", "topic": "я был, она была"},
  {"n": 6, "id": "L6", "title": "Accusative: people and animals", "topic": "я вижу брата"},
  {"n": 7, "id": "L7", "title": "Dative", "topic": "to whom? мне нравится"},
  {"n": 8, "id": "L8", "title": "Instrumental", "topic": "with whom? чай с молоком"},
  {"review": True, "id": "R2", "title": "Review 2", "topic": "mixed practice on lessons 5–8"},
  {"n": 9, "id": "L9", "title": "Plurals", "topic": "один билет, два билета, пять билетов"},
  {"n": 10, "id": "L10", "title": "Adjective agreement", "topic": "новый храм, новая церковь"},
  {"n": 11, "id": "L11", "title": "Aspect: an introduction", "topic": "делать / сделать"},
  {"n": 12, "id": "L12", "title": "Verbs of motion: an introduction", "topic": "идти / ходить, ехать / ездить"},
  {"review": True, "id": "R3", "title": "Review 3", "topic": "mixed practice on lessons 9–12"},
]

SECTIONS = [
 {"h": "Step 1 · Every noun has a gender", "open": True, "html":
  "<p>Every Russian noun is <b>masculine</b>, <b>feminine</b> or <b>neuter</b>. It's grammar, not meaning: a church can be masculine (" + ru("храм") + ") or feminine (" + ru("церковь") + "). The good news: the <b>last letter of the dictionary form</b> almost always tells you.</p>"
  + t(["Ends in", "Gender", "Examples"], [
    ["a consonant", "masculine (он)", ru("магазин") + " store · " + ru("храм") + " church · " + ru("паспорт") + " passport · " + ru("Минск")],
    [ru("-й"), "masculine (он)", ru("музей") + " museum · " + ru("чай") + " tea · " + ru("трамвай") + " tram"],
    [ru("-а"), "feminine (она)", ru("касса") + " checkout · " + ru("улица") + " street · " + ru("граница") + " border · " + ru("работа") + " work"],
    [ru("-я"), "feminine (она)", ru("таможня") + " customs · " + ru("деревня") + " village · " + ru("Россия") + " Russia"],
    [ru("-о"), "neuter (оно)", ru("окно") + " window · " + ru("место") + " place, seat · " + ru("молоко") + " milk"],
    [ru("-е"), "neuter (оно)", ru("море") + " sea · " + ru("здание") + " building · " + ru("расписание") + " timetable"],
    [ru("-ь"), "either", "see Step 2"],
  ])
  + '<p class="tip"><b>One exception to know now:</b> men are masculine even when the word ends in ' + ru("-а/-я") + ": " + ru("папа") + " (dad), " + ru("дедушка") + " (grandpa), " + ru("батюшка") + " (Father, the priest), " + ru("мужчина") + " (man).</p>"
  + '<p class="tip"><b>Habit:</b> learn every noun with он, она or оно: ' + ru("магазин — он, касса — она, окно — оно") + ".</p>"},
 {"h": "Step 2 · Nouns ending in -ь", "open": False, "html":
  "<p>The soft sign " + ru("ь") + " doesn't tell you the gender by itself. A few clues help:</p>"
  + t(["Ending", "Gender", "Examples"], [
    [ru("-чь, -шь, -щь, -жь"), "always feminine", ru("ночь") + " night · " + ru("дочь") + " daughter · " + ru("вещь") + " thing (masculine words with these sounds have no " + ru("ь") + ": " + ru("врач") + " doctor, " + ru("нож") + " knife)"],
    [ru("-ость"), "feminine", ru("новость") + " news · " + ru("радость") + " joy"],
    [ru("-тель"), "masculine", ru("учитель") + " teacher · " + ru("водитель") + " driver · " + ru("житель") + " resident"],
  ])
  + "<p>For everything else, just learn it with он or она. Common ones:</p>"
  + t(["Masculine (он)", "Feminine (она)"], [
    [ru("рубль") + " ruble", ru("церковь") + " church"],
    [ru("день") + " day", ru("очередь") + " line, queue"],
    [ru("Гомель") + " (the city)", ru("Беларусь") + " Belarus"],
    ["", ru("площадь") + " square · " + ru("дверь") + " door"],
  ])},
 {"h": "Step 3 · What the prepositional case is for", "open": False, "html":
  "<p>Russian nouns change their ending depending on their job in the sentence. These forms are called <b>cases</b>. This lesson is about the <b>prepositional case</b> (" + ru("предложный падеж") + "). It gets its name because it's only used after a preposition.</p>"
  + "<p>After " + ru("в") + " (in) or " + ru("на") + " (on, at), it answers the question " + ru("где?") + " (where?):</p>"
  + exl([("Где батюшка? — Батюшка в храме.", "Where's Father? — Father is in the church."),
         ("Где ты? — Я на вокзале.", "Where are you? — I'm at the train station."),
         ("Где вы живёте? — Я живу в Минске.", "Where do you live? — I live in Minsk.")])
  + '<p class="tip">Russian has no "is / am / are" in the present tense. ' + ru("Я в храме") + " is simply “I (am) in the church.”</p>"
  + "<p>The same endings are used after " + ru("о") + " (about): " + ru("Я думаю о Минске") + " (I'm thinking about Minsk).</p>"},
 {"h": "Step 4 · The endings: -е or -и", "open": False, "html":
  "<p>Take the dictionary form, look at the ending, and apply one of two rules.</p>"
  + "<h4>Rule 1 · Most nouns take -е</h4>"
  + t(["Dictionary form", "What happens", "Где?"], [
    [ru("храм"), "add " + ru("-е"), ru("в храме")],
    [ru("Минск"), "add " + ru("-е"), ru("в Минске")],
    [ru("магазин"), "add " + ru("-е"), ru("в магазине")],
    [ru("музей"), ru("-й") + " → " + ru("-е"), ru("в музее")],
    [ru("работа"), ru("-а") + " → " + ru("-е"), ru("на работе")],
    [ru("граница"), ru("-а") + " → " + ru("-е"), ru("на границе")],
    [ru("деревня"), ru("-я") + " → " + ru("-е"), ru("в деревне")],
    [ru("таможня"), ru("-я") + " → " + ru("-е"), ru("на таможне")],
    [ru("место"), ru("-о") + " → " + ru("-е"), ru("на месте") + " (in place, on the spot)"],
    [ru("море"), "stays " + ru("-е"), ru("на море") + " (at the seaside)"],
    [ru("Гомель") + " (masc.)", ru("-ь") + " → " + ru("-е"), ru("в Гомеле")],
  ])
  + "<h4>Rule 2 · Two groups take -и</h4>"
  + t(["Group", "Dictionary form", "Где?"], [
    ["feminine " + ru("-ь"), ru("церковь"), ru("в церкви") + " (the о drops out)"],
    ["", ru("Беларусь"), ru("в Беларуси")],
    ["", ru("очередь"), ru("в очереди") + " (in line)"],
    ["", ru("площадь"), ru("на площади")],
    [ru("-ия"), ru("Россия"), ru("в России")],
    ["", ru("литургия"), ru("на литургии")],
    [ru("-ие"), ru("здание"), ru("в здании")],
    ["", ru("расписание"), ru("в расписании")],
    [ru("-ий"), ru("санаторий") + " (health resort)", ru("в санатории")],
  ])
  + '<p class="tip"><b>Memory hook:</b> feminine ' + ru("-ь") + ", and anything with " + ru("и") + " just before the ending (" + ru("-ия, -ие, -ий") + "), takes " + ru("-и") + ". Everything else takes " + ru("-е") + ". So it's " + ru("в России") + ", never “в Россие”, and " + ru("в Гомеле") + " (masculine), but " + ru("в Беларуси") + " (feminine).</p>"
  + "<h4>Around Belarus</h4>"
  + t(["City / country", "Где?"], [
    [ru("Минск"), ru("в Минске")], [ru("Брест"), ru("в Бресте")], [ru("Витебск"), ru("в Витебске")],
    [ru("Могилёв"), ru("в Могилёве")], [ru("Гомель"), ru("в Гомеле")],
    [ru("Березино"), ru("в Березине") + " (in everyday speech you'll also hear " + ru("в Березино") + ")"],
    [ru("Беларусь"), ru("в Беларуси")],
  ])},
 {"h": "Step 5 · в or на?", "open": False, "html":
  "<p><b>" + ru("в") + " = in, inside.</b> Use it for buildings and rooms, and for cities and countries: " + ru("в храме, в церкви, в магазине, в Минске, в Беларуси") + ".</p>"
  + "<p><b>" + ru("на") + " = on, at.</b> Use it for surfaces (" + ru("на столе") + ", on the table), for events and activities (" + ru("на литургии, на службе, на работе") + "), and for a set of places you just have to learn:</p>"
  + t(["Word", "Где?", "Meaning"], [
    [ru("рынок"), ru("на рынке"), "at the market (the о drops out)"],
    [ru("вокзал"), ru("на вокзале"), "at the train station"],
    [ru("работа"), ru("на работе"), "at work"],
    [ru("почта"), ru("на почте"), "at the post office"],
    [ru("улица"), ru("на улице"), "in the street; outside"],
    [ru("граница"), ru("на границе"), "at the border"],
    [ru("касса"), ru("на кассе"), "at the checkout (for a ticket office you'll also hear " + ru("в кассе") + ")"],
    [ru("остановка"), ru("на остановке"), "at the (bus) stop"],
    [ru("таможня"), ru("на таможне"), "at customs"],
    [ru("площадь"), ru("на площади"), "in the square"],
  ])
  + '<p class="tip"><b>Habit:</b> learn new place words together with their preposition: ' + ru("в магазине, на вокзале") + ". " + ru("на улице") + " also just means “outside”: " + ru("На улице холодно") + " (It's cold outside).</p>"},
 {"h": "Step 6 · во and об", "open": False, "html":
  "<p>Two small spelling helpers make words easier to say:</p>"
  + "<p><b>" + ru("в → во") + "</b> before a word starting with " + ru("в") + " or " + ru("ф") + " plus another consonant: " + ru("во Франции") + " (in France), " + ru("во Владимире") + " (in Vladimir). But: " + ru("в Минске, в Витебске") + " (a vowel follows the в).</p>"
  + "<p><b>" + ru("о → об") + "</b> (about) before a vowel sound (" + ru("а, о, у, э, и") + "): " + ru("Я думаю об Америке") + " (I'm thinking about America). But: " + ru("о Минске") + ".</p>"
  + "<p>" + ru("на") + " never changes.</p>"},
 {"h": "Step 7 · A few exceptions", "open": False, "html":
  "<p>A small group of masculine nouns take a stressed <b>" + ru("-у") + "</b> after " + ru("в / на") + " when they mean location. Learn these as set phrases:</p>"
  + t(["Word", "Где?"], [
    [ru("аэропорт") + " airport", ru("в аэропорту")], [ru("лес") + " forest", ru("в лесу")], [ru("мост") + " bridge", ru("на мосту")],
    [ru("сад") + " garden", ru("в саду")], [ru("пол") + " floor", ru("на полу")], [ru("шкаф") + " wardrobe", ru("в шкафу")],
  ])
  + "<p>After " + ru("о") + " (about) they're regular: " + ru("о лесе, об аэропорте") + ". You'll hear " + ru("в аэропорте") + " in casual speech, but " + ru("в аэропорту") + " is the standard form.</p>"
  + "<p>Also good to know: <b>at home</b> is " + ru("дома") + " (not “в доме”). Foreign words like " + ru("кафе, метро, такси") + " never change: " + ru("в кафе, в метро, в такси") + ".</p>"},
 {"h": "Summary", "open": False, "html":
  '<ul class="sum">'
  + "<li>Gender: consonant or " + ru("-й") + " → masculine; " + ru("-а / -я") + " → feminine; " + ru("-о / -е") + " → neuter; " + ru("-ь") + " → learn it. Men are masculine.</li>"
  + "<li>" + ru("Где?") + " = " + ru("в / на") + " + prepositional.</li>"
  + "<li>Endings: " + ru("-е") + ", except feminine " + ru("-ь") + " and " + ru("-ия / -ие / -ий") + " → " + ru("-и") + ".</li>"
  + "<li>" + ru("на") + " for events and for " + ru("рынок, вокзал, работа, почта, улица, граница, касса, остановка") + ".</li>"
  + "<li>" + ru("во / об") + " before awkward clusters and vowels; " + ru("в аэропорту, в лесу, на мосту") + ".</li>"
  + "</ul>"},
]

G = ["masculine", "feminine", "neuter"]
def gq(word, en, ans, ex):
    return {"part": "A", "sub": "A · gender", "s": word + " — ___", "base": en, "a": ans,
            "d": [x for x in G if x != ans], "ex": ex, "translation": "", "glosses": [], "choiceOnly": True}
def pq(s, base, ans, d, ex, tr, gl=None):
    return {"part": "B", "sub": "B · prepositional", "s": s, "base": base, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def cq(s, base, ans, d, ex, tr, gl=None):
    return {"part": "C", "sub": "C · в or на", "s": s, "base": base + " · в or на?", "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}

EX = [
 gq("магазин", "store", "masculine", "It ends in a consonant (н), so it's masculine: он. (Step 1)"),
 gq("касса", "checkout", "feminine", "It ends in -а, so it's feminine: она. (Step 1)"),
 gq("окно", "window", "neuter", "It ends in -о, so it's neuter: оно. (Step 1)"),
 gq("таможня", "customs", "feminine", "It ends in -я, so it's feminine: она. (Step 1)"),
 gq("музей", "museum", "masculine", "It ends in -й, so it's masculine: он. (Step 1)"),
 gq("здание", "building", "neuter", "It ends in -е (here -ие), so it's neuter: оно. (Step 1)"),
 gq("ночь", "night", "feminine", "-ь after ч, ш, щ or ж is always feminine: ночь, дочь, вещь. (Step 2)"),
 gq("учитель", "teacher", "masculine", "Nouns in -тель are masculine: учитель, водитель, житель. (Step 2)"),
 gq("церковь", "church", "feminine", "A -ь word you just have to learn: церковь is feminine. That's why it's в церкви. (Step 2)"),
 gq("батюшка", "Father (the priest)", "masculine", "It ends in -а, but men are masculine: папа, дедушка, батюшка. (Step 1)"),

 pq("Я в ___.", "храм", "храме", ["храми", "храм", "храма"], "Rule 1: a consonant adds -е. храм → в храме. (Step 4)", "I'm in the church."),
 pq("Я живу в ___.", "Минск", "Минске", ["Мински", "Минск", "Минска"], "Rule 1: a consonant adds -е. Минск → в Минске. (Step 4)", "I live in Minsk.", ["живу: I live"]),
 pq("Батюшка в ___.", "церковь", "церкви", ["церкве", "церковь", "церкови"], "Rule 2: feminine -ь takes -и, and the о drops out. церковь → в церкви. (Step 4)", "Father is in the church."),
 pq("Мой друг живёт в ___.", "Россия", "России", ["Россие", "Россия", "Росси"], "Rule 2: -ия becomes -ии. Россия → в России, never “в Россие”. (Step 4)", "My friend lives in Russia.", ["мой друг: my friend", "живёт: lives"]),
 pq("Мы в ___.", "здание", "здании", ["здание", "здания", "зданию"], "Rule 2: -ие becomes -ии. здание → в здании. (Step 4)", "We're in the building.", ["мы: we"]),
 pq("Мы в ___.", "музей", "музее", ["музеи", "музей", "музея"], "Rule 1: -й becomes -е. музей → в музее. (Step 4)", "We're in the museum.", ["мы: we"]),
 pq("Бабушка живёт в ___.", "деревня", "деревне", ["деревни", "деревня", "деревню"], "Rule 1: -я becomes -е. деревня → в деревне. (Step 4)", "Grandma lives in the village.", ["бабушка: grandma", "живёт: lives"]),
 pq("Я на ___.", "работа", "работе", ["работи", "работа", "работу"], "Rule 1: -а becomes -е. работа → на работе. (Step 4)", "I'm at work."),
 pq("Мой друг в ___.", "Гомель", "Гомеле", ["Гомели", "Гомель", "Гомеля"], "Гомель is masculine, so Rule 1 applies: -ь becomes -е. Only feminine -ь takes -и. (Steps 2 and 4)", "My friend is in Gomel.", ["мой друг: my friend"]),
 pq("Мама в ___.", "санаторий", "санатории", ["санаторие", "санаторий", "санатория"], "Rule 2: -ий becomes -ии. санаторий → в санатории. (Step 4)", "Mom is at the health resort.", ["санаторий: health resort"]),

 cq("Мы сейчас ___.", "магазин", "в магазине", ["на магазине", "в магазини", "на магазини"], "в: a store is a building you're inside. Rule 1: магазин + е. (Steps 4 and 5)", "We're at the store now.", ["сейчас: now"]),
 cq("Паспорта проверяют ___.", "граница", "на границе", ["в границе", "на граници", "в граници"], "граница is on the на-list. Rule 1: -а becomes -е. (Steps 4 and 5)", "They check passports at the border.", ["паспорта: passports", "проверяют: (they) check"]),
 cq("Я жду автобус ___.", "остановка", "на остановке", ["в остановке", "на остановки", "в остановки"], "остановка is on the на-list. Rule 1: -а becomes -е. (Steps 4 and 5)", "I'm waiting for the bus at the stop.", ["жду: I'm waiting for", "автобус: bus"]),
 cq("Свечи продают ___.", "храм", "в храме", ["на храме", "в храми", "на храми"], "в: inside a building. Rule 1: храм + е. (Steps 4 and 5)", "They sell candles in the church.", ["свечи: candles", "продают: (they) sell"]),
 cq("Я живу ___.", "Беларусь", "в Беларуси", ["в Беларусе", "на Беларуси", "на Беларусе"], "в for countries and cities. Rule 2: feminine -ь takes -и. (Steps 4 and 5)", "I live in Belarus.", ["живу: I live"]),
 cq("Овощи дешевле ___.", "рынок", "на рынке", ["в рынке", "на рыноке", "в рыноке"], "рынок is on the на-list, and its о drops out: на рынке. (Step 5)", "Vegetables are cheaper at the market.", ["овощи: vegetables", "дешевле: cheaper"]),
 cq("Я ___.", "почта", "на почте", ["в почте", "на почти", "в почти"], "почта is on the на-list. Rule 1: -а becomes -е. (Steps 4 and 5)", "I'm at the post office."),
 cq("Мы встретились ___.", "вокзал", "на вокзале", ["в вокзале", "на вокзали", "в вокзали"], "вокзал is on the на-list. Rule 1: вокзал + е. (Steps 4 and 5)", "We met at the train station.", ["встретились: (we) met"]),
 cq("Я сейчас ___.", "аэропорт", "в аэропорту", ["в аэропорте", "на аэропорту", "на аэропорте"], "аэропорт is an exception: в аэропорту. You'll hear в аэропорте in casual speech, but в аэропорту is standard. (Step 7)", "I'm at the airport now.", ["сейчас: now"]),
 cq("Сегодня ___ холодно.", "улица", "на улице", ["в улице", "на улици", "в улици"], "на улице means in the street, or simply outside. Rule 1: -а becomes -е. (Steps 4 and 5)", "It's cold outside today.", ["сегодня: today", "холодно: (it's) cold"]),
 cq("Мой друг живёт ___.", "Франция", "во Франции", ["в Франции", "во Франце", "на Франции"], "в becomes во before ф + a consonant. Rule 2: -ия becomes -ии. (Steps 4 and 6)", "My friend lives in France.", ["мой друг: my friend", "живёт: lives"]),
]


# ---------------- Lesson 2 ----------------
SECTIONS2 = [
 {"h": "Step 1 · Где? or куда?", "open": True, "html":
  "<p>In Lesson 1, " + ru("где?") + " (where?) used " + ru("в / на") + " + the prepositional: " + ru("Я в храме") + ". When you're <b>moving toward</b> a place, Russian asks " + ru("куда?") + " (where to?) and uses a different case: the <b>accusative</b> (" + ru("винительный падеж") + ").</p>"
  + t(["Где? · being somewhere", "Куда? · going somewhere"], [
    [ru("Я в храме.") + "<br>I'm in church.", ru("Я иду в храм.") + "<br>I'm going to church."],
    [ru("Я на работе.") + "<br>I'm at work.", ru("Я еду на работу.") + "<br>I'm driving to work."],
    [ru("Жена в магазине.") + "<br>My wife is at the store.", ru("Жена идёт в магазин.") + "<br>My wife is going to the store."],
    [ru("Я был в Джексоне.") + "<br>I was in Jackson.", ru("Я ездил в Джексон.") + "<br>I went to Jackson."],
  ])
  + '<p class="tip"><b>The test:</b> is someone moving toward the place? Then it\'s ' + ru("куда?") + " + accusative. Being, living, working, waiting somewhere is " + ru("где?") + " + prepositional.</p>"
  + t(["Где? verbs", "Куда? verbs"], [
    [ru("быть") + " be · " + ru("жить") + " live · " + ru("работать") + " work · " + ru("стоять") + " stand", ru("идти") + " go on foot · " + ru("ехать") + " go by vehicle · " + ru("ходить / ездить") + " go (and come back) · " + ru("лететь") + " fly"],
  ])},
 {"h": "Step 2 · The accusative endings for things", "open": False, "html":
  "<p>Good news: for things and places, <b>only feminine " + ru("-а") + " and " + ru("-я") + " change.</b> Everything else stays in the dictionary form.</p>"
  + t(["Dictionary form", "Accusative", "Examples"], [
    ["masc. consonant, " + ru("-й") + ", " + ru("-ь"), "no change", ru("магазин → в магазин") + " · " + ru("Минск → в Минск") + " · " + ru("музей → в музей") + " · " + ru("Гомель → в Гомель")],
    ["neuter " + ru("-о / -е"), "no change", ru("Березино → в Березино") + " · " + ru("море → на море")],
    [ru("-а"), ru("-а → -у"), ru("работа → на работу") + " · " + ru("граница → на границу") + " · " + ru("Америка → в Америку")],
    [ru("-я"), ru("-я → -ю"), ru("деревня → в деревню") + " · " + ru("таможня → на таможню") + " · " + ru("Россия → в Россию")],
    ["feminine " + ru("-ь"), "no change", ru("церковь → в церковь") + " · " + ru("Беларусь → в Беларусь") + " · " + ru("площадь → на площадь")],
  ])
  + '<p class="tip"><b>Memory hook:</b> ' + ru("-а → -у, -я → -ю") + ". Everything else stays the same. Compare the prepositional: " + ru("в церкви") + " (where?) but " + ru("в церковь") + " (where to?).</p>"
  + "<p>Foreign words like " + ru("кафе, метро, такси, кофе") + " never change: " + ru("Я иду в кафе. Я беру такси.") + "</p>"
  + '<p class="tip">This lesson is about <b>things and places</b>. People and animals work differently in the masculine (' + ru("я вижу брата") + "). That's Lesson 6.</p>"},
 {"h": "Step 3 · The accusative for things you buy, see and want", "open": False, "html":
  "<p>The accusative has a second job, with no preposition at all: it marks the <b>direct object</b>, the thing you buy, see, want or order. The endings are the same as in Step 2.</p>"
  + exl([("В магазине я покупаю хлеб и воду.", "At the store I'm buying bread and water. (хлеб stays, вода → воду)"),
         ("Я ищу кассу.", "I'm looking for the checkout. (касса → кассу)"),
         ("Покажите, пожалуйста, паспорт.", "Show your passport, please. (паспорт stays)"),
         ("В ресторане я заказываю рыбу.", "At the restaurant I order fish. (рыба → рыбу)"),
         ("Я ставлю свечу.", "I'm putting up a candle. (свеча → свечу)"),
         ("Я вижу церковь.", "I see the church. (церковь stays)")])
  + t(["Useful verbs (I …)", "Meaning"], [
    [ru("покупаю"), "I buy, I'm buying"], [ru("беру"), "I take"], [ru("хочу"), "I want"], [ru("ищу"), "I'm looking for"],
    [ru("вижу"), "I see"], [ru("люблю"), "I love"], [ru("заказываю"), "I order"], [ru("читаю"), "I read"],
  ])
  + '<p class="tip"><b>Gender still decides everything.</b> It\'s also why we say ' + ru("моя работа") + " (feminine, ends in " + ru("-а") + ") but " + ru("мой паспорт") + " (masculine) and " + ru("моё место") + " (neuter): " + ru("мой / моя / моё") + " matches the noun. So: " + ru("Мне нравится моя работа.") + "</p>"},
 {"h": "Step 4 · в or на: same as Lesson 1", "open": False, "html":
  "<p>The preposition doesn't change. If a place takes " + ru("в") + " for " + ru("где?") + ", it takes " + ru("в") + " for " + ru("куда?") + ". The same goes for " + ru("на") + ". Only the ending changes.</p>"
  + t(["Word", "Где?", "Куда?"], [
    [ru("храм"), ru("в храме"), ru("в храм")],
    [ru("церковь"), ru("в церкви"), ru("в церковь")],
    [ru("магазин"), ru("в магазине"), ru("в магазин")],
    [ru("Джексон"), ru("в Джексоне"), ru("в Джексон")],
    [ru("Беларусь"), ru("в Беларуси"), ru("в Беларусь")],
    [ru("Россия"), ru("в России"), ru("в Россию")],
    [ru("работа"), ru("на работе"), ru("на работу")],
    [ru("граница"), ru("на границе"), ru("на границу")],
    [ru("таможня"), ru("на таможне"), ru("на таможню")],
    [ru("вокзал"), ru("на вокзале"), ru("на вокзал")],
    [ru("рынок"), ru("на рынке"), ru("на рынок") + " (the о is back)"],
    [ru("почта"), ru("на почте"), ru("на почту")],
    [ru("литургия"), ru("на литургии"), ru("на литургию")],
    [ru("аэропорт"), ru("в аэропорту"), ru("в аэропорт") + " (the -у exception is only for где?)"],
    [ru("Франция"), ru("во Франции"), ru("во Францию")],
  ])
  + '<p class="tip"><b>Home</b> has its own two words: ' + ru("дома") + " (at home, где?) and " + ru("домой") + " (home, куда?): " + ru("Я дома. Вечером я иду домой.") + "</p>"},
 {"h": "Step 5 · Going: on foot or by vehicle", "open": False, "html":
  "<p>Russian picks the verb by <b>how</b> you go. The full story is in Lesson 12. For now, learn these forms as phrases.</p>"
  + t(["", "On foot", "By vehicle"], [
    ["right now, today", ru("я иду · ты идёшь · он, она идёт · мы идём"), ru("я еду · ты едешь · он, она едет · мы едем")],
    ["went and came back", ru("я ходил · я ходила (f) · мы ходили"), ru("я ездил · я ездила (f) · мы ездили")],
  ])
  + "<p>In Jackson you drive almost everywhere, so it's " + ru("Я еду в магазин") + " even for a short trip by car. Walking to the church next door is " + ru("Я иду в храм") + ". A flight is " + ru("Мы летим в Минск") + " (We're flying to Minsk).</p>"
  + '<p class="tip"><b>Two ways to say the same trip:</b> ' + ru("Я ездил в Джексон") + " (motion → куда? → accusative) = " + ru("Я был в Джексоне") + " (being → где? → prepositional). Both mean you went there. Just match the case to the verb.</p>"},
 {"h": "Summary", "open": False, "html":
  '<ul class="sum">'
  + "<li>" + ru("Где?") + " (being) → " + ru("в / на") + " + prepositional. " + ru("Куда?") + " (going) → " + ru("в / на") + " + accusative.</li>"
  + "<li>Accusative of things: " + ru("-а → -у") + ", " + ru("-я → -ю") + ". Everything else (masculine, neuter, feminine " + ru("-ь") + ") stays the same.</li>"
  + "<li>The same accusative marks the thing you buy, see or want: " + ru("Я покупаю воду.") + "</li>"
  + "<li>" + ru("в") + " stays " + ru("в") + ", " + ru("на") + " stays " + ru("на") + ". " + ru("дома") + " = at home, " + ru("домой") + " = (going) home.</li>"
  + "<li>" + ru("иду / ходил") + " on foot; " + ru("еду / ездил") + " by vehicle. " + ru("Я ездил в Джексон = Я был в Джексоне.") + "</li>"
  + "</ul>"},
]

def aq(s, base, ans, d, ex, tr, gl=None):
    return {"part": "A", "sub": "A · accusative (things)", "s": s, "base": base, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def bq(s, base, ans, d, ex, tr, gl=None):
    return {"part": "B", "sub": "B · куда? в or на", "s": s, "base": base + " · в or на?", "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def wq(k, s, base, ans, d, ex, tr, gl=None):  # k: "where" (prepositional) or "whereto" (accusative)
    return {"part": "C", "sub": "C · где or куда?", "k": k, "s": s, "base": base + " · где or куда?", "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}

EX2 = [
 aq("В магазине я покупаю ___.", "хлеб", "хлеб", ["хлебом", "хлебе", "хлебу"], "Masculine thing: no change. хлеб → хлеб. (Steps 2 and 3)", "At the store I'm buying bread.", ["покупаю: I'm buying"]),
 aq("Я покупаю ___.", "вода", "воду", ["вода", "воде", "водой"], "Feminine -а → -у. вода → воду. (Steps 2 and 3)", "I'm buying water.", ["покупаю: I'm buying"]),
 aq("Жена любит ___.", "молоко", "молоко", ["молоку", "молоке", "молоком"], "Neuter -о: no change. молоко → молоко. (Steps 2 and 3)", "My wife loves milk.", ["жена: wife", "любит: loves"]),
 aq("Я ищу ___.", "касса", "кассу", ["касса", "кассе", "кассой"], "Feminine -а → -у. касса → кассу. (Steps 2 and 3)", "I'm looking for the checkout.", ["ищу: I'm looking for"]),
 aq("В ресторане я заказываю ___.", "рыба", "рыбу", ["рыба", "рыбе", "рыбой"], "Feminine -а → -у. рыба → рыбу. (Steps 2 and 3)", "At the restaurant I order fish.", ["заказываю: I order"]),
 aq("Покажите, пожалуйста, ___.", "паспорт", "паспорт", ["паспортом", "паспорте", "паспорту"], "Masculine thing: no change. паспорт → паспорт. (Steps 2 and 3)", "Show your passport, please.", ["покажите: show", "пожалуйста: please"]),
 aq("Я ставлю ___.", "свеча", "свечу", ["свеча", "свече", "свечой"], "Feminine -а → -у. свеча → свечу. (Steps 2 and 3)", "I'm putting up a candle.", ["ставлю: I put (up), I place"]),
 aq("Батюшка читает ___.", "молитва", "молитву", ["молитва", "молитве", "молитвой"], "Feminine -а → -у. молитва → молитву. (Steps 2 and 3)", "Father is reading the prayer.", ["батюшка: Father (the priest)", "читает: reads"]),
 aq("Я вижу ___.", "церковь", "церковь", ["церкове", "церкву", "церковью"], "Feminine -ь: no change in the accusative. церковь → церковь. (Steps 2 and 3)", "I see the church.", ["вижу: I see"]),
 aq("Я люблю ___.", "Беларусь", "Беларусь", ["Беларуси", "Беларусю", "Беларусу"], "Feminine -ь: no change. Беларусь → Беларусь. (Steps 2 and 3)", "I love Belarus.", ["люблю: I love"]),

 bq("Я иду ___.", "храм", "в храм", ["в храме", "на храм", "на храме"], "Going → куда? храм takes в, and a masculine thing doesn't change. (Steps 1, 2 and 4)", "I'm going to church.", ["иду: I'm going (on foot)"]),
 bq("Завтра я еду ___.", "Минск", "в Минск", ["в Минске", "на Минск", "на Минске"], "Going → куда? в for cities, and Минск doesn't change. (Steps 1, 2 and 4)", "Tomorrow I'm going to Minsk.", ["завтра: tomorrow", "еду: I'm going (by vehicle)"]),
 bq("Мы едем ___.", "граница", "на границу", ["на границе", "в границу", "в границе"], "Going → куда? граница takes на, and -а → -у. (Steps 1, 2 and 4)", "We're driving to the border.", ["мы едем: we're going (by vehicle)"]),
 bq("Утром я еду ___.", "работа", "на работу", ["на работе", "в работу", "в работе"], "Going → куда? работа takes на, and -а → -у. (Steps 1, 2 and 4)", "In the morning I drive to work.", ["утром: in the morning", "еду: I'm going (by vehicle)"]),
 bq("Жена идёт ___.", "магазин", "в магазин", ["в магазине", "на магазин", "на магазине"], "Going → куда? магазин takes в and doesn't change. (Steps 1, 2 and 4)", "My wife is going to the store.", ["жена: wife", "идёт: is going (on foot)"]),
 bq("Сегодня мы идём ___.", "церковь", "в церковь", ["в церкви", "на церковь", "на церкви"], "Going → куда? Feminine -ь doesn't change: в церковь. Compare where?: в церкви. (Steps 1, 2 and 4)", "Today we're going to church.", ["сегодня: today", "мы идём: we're going (on foot)"]),
 bq("Я еду ___.", "вокзал", "на вокзал", ["на вокзале", "в вокзал", "в вокзале"], "Going → куда? вокзал takes на and doesn't change. (Steps 1, 2 and 4)", "I'm going to the train station.", ["еду: I'm going (by vehicle)"]),
 bq("Мой друг едет ___.", "Березино", "в Березино", ["в Березине", "на Березино", "на Березине"], "Going → куда? в for towns, and neuter -о doesn't change. (Steps 1, 2 and 4)", "My friend is going to Berezino.", ["мой друг: my friend", "едет: is going (by vehicle)"]),
 bq("В субботу мы идём ___.", "рынок", "на рынок", ["на рынке", "в рынок", "в рынке"], "Going → куда? рынок takes на, and it doesn't change (the о stays). (Steps 1, 2 and 4)", "On Saturday we're going to the market.", ["в субботу: on Saturday", "мы идём: we're going (on foot)"]),
 bq("Мы едем ___.", "аэропорт", "в аэропорт", ["в аэропорту", "на аэропорт", "на аэропорту"], "Going → куда? в аэропорт. The -у form (в аэропорту) is only for where?. (Steps 1 and 4)", "We're going to the airport.", ["мы едем: we're going (by vehicle)"]),
 bq("Летом мы едем ___.", "Беларусь", "в Беларусь", ["в Беларуси", "на Беларусь", "на Беларуси"], "Going → куда? в for countries, and feminine -ь doesn't change. (Steps 1, 2 and 4)", "In the summer we're going to Belarus.", ["летом: in the summer", "мы едем: we're going (by vehicle)"]),

 wq("where", "Вчера я был ___.", "Джексон", "в Джексоне", ["в Джексон", "на Джексоне", "на Джексон"], "был = was, being somewhere → где? → prepositional: в Джексоне. (Steps 1 and 5)", "Yesterday I was in Jackson.", ["вчера: yesterday", "был: was"]),
 wq("whereto", "Вчера я ездил ___.", "Джексон", "в Джексон", ["в Джексоне", "на Джексон", "на Джексоне"], "ездил = went (and came back) → куда? → accusative: в Джексон. (Steps 1 and 5)", "Yesterday I went to Jackson.", ["вчера: yesterday", "ездил: went (by vehicle)"]),
 wq("where", "Мой друг работает ___.", "Минск", "в Минске", ["в Минск", "на Минске", "на Минск"], "работает = works, being somewhere → где? → в Минске. (Step 1)", "My friend works in Minsk.", ["мой друг: my friend", "работает: works"]),
 wq("where", "Жена сейчас ___.", "магазин", "в магазине", ["в магазин", "на магазине", "на магазин"], "No movement: she is there → где? → prepositional: в магазине. (Step 1)", "My wife is at the store now.", ["жена: wife", "сейчас: now"]),
 wq("whereto", "В воскресенье мы идём ___.", "литургия", "на литургию", ["на литургии", "в литургию", "в литургии"], "идём = going → куда? → на + accusative, -я → -ю. (Steps 1, 2 and 4)", "On Sunday we're going to the Liturgy.", ["в воскресенье: on Sunday", "мы идём: we're going (on foot)"]),
 wq("where", "Вчера мы были ___.", "литургия", "на литургии", ["на литургию", "в литургии", "в литургию"], "были = were → где? → на + prepositional: на литургии. (Steps 1 and 4)", "Yesterday we were at the Liturgy.", ["вчера: yesterday", "мы были: we were"]),
 wq("where", "Я стою ___.", "очередь", "в очереди", ["в очередь", "на очередь", "в очереде"], "стою = I'm standing, no movement → где? → в очереди. (Step 1)", "I'm standing in line.", ["стою: I'm standing"]),
 wq("whereto", "Завтра мы летим ___.", "Америка", "в Америку", ["в Америке", "на Америку", "на Америке"], "летим = we're flying → куда? → accusative, -а → -у. (Steps 1, 2 and 5)", "Tomorrow we're flying to America.", ["завтра: tomorrow", "летим: we're flying"]),
 wq("whereto", "Летом мы ездили ___.", "Россия", "в Россию", ["в России", "на Россию", "в Россие"], "ездили = went (and came back) → куда? → accusative, -я → -ю. (Steps 1, 2 and 5)", "In the summer we went to Russia.", ["летом: in the summer", "мы ездили: we went (by vehicle)"]),
 wq("where", "Паспорта проверяют ___.", "таможня", "на таможне", ["на таможню", "в таможне", "в таможню"], "They check passports there, no movement → где? → на + prepositional: на таможне. (Step 1)", "They check passports at customs.", ["паспорта: passports", "проверяют: (they) check"]),
 wq("whereto", "Сейчас я еду ___.", "почта", "на почту", ["на почте", "в почту", "в почте"], "еду = I'm going → куда? → на + accusative, -а → -у. (Steps 1, 2 and 4)", "I'm going to the post office now.", ["сейчас: now", "еду: I'm going (by vehicle)"]),
 wq("home", "Вечером я иду ___.", "дом (home)", "домой", ["дома", "в доме", "на дом"], "Going home → куда? → домой. дома means at home (где?). (Step 4)", "In the evening I go home.", ["вечером: in the evening", "иду: I'm going (on foot)"]),
]

LESSONS = {
 "L1": {
  "id": "L1", "n": 1,
  "title": "Noun gender and the prepositional case (where?)",
  "goal": "By the end you'll be able to say where you are and where things are: Я в храме. Я на вокзале. Мы в Беларуси.",
  "minutes": "15–20 min to read, then 31 exercises",
  "sections": SECTIONS,
  "parts": {"A": "Part A · Pick the gender", "B": "Part B · Form the prepositional", "C": "Part C · в or на + the right form"},
  "practice": {
    "title": "Now use it: write to your tutor",
    "text": "Write 3 short sentences to your tutor in chat saying where people or things are. Use at least one на-word and one -и ending.",
    "examples": ["Я живу в Минске.", "Батюшка в церкви.", "Мой паспорт на столе."]
  },
  "exercises": EX,
 },
 "L2": {
  "id": "L2", "n": 2,
  "title": "The accusative case (things) and куда? (where to?)",
  "goal": "By the end you'll be able to say where you're going and what you're buying: Я иду в храм. Я еду на работу. Я покупаю воду.",
  "minutes": "15–20 min to read, then 33 exercises",
  "sections": SECTIONS2,
  "parts": {"A": "Part A · Form the accusative", "B": "Part B · Куда? в or на + the accusative", "C": "Part C · Где or куда? Pick the right case"},
  "practice": {
    "title": "Now use it: write to your tutor",
    "text": "Write 3 short sentences to your tutor in chat: one about where you're going (куда?), one about where you were (где?), and one about something you're buying.",
    "examples": ["Завтра я еду на работу.", "Вчера я был в храме.", "В магазине я покупаю воду."]
  },
  "exercises": EX2,
 }
}

out = {"version": 1, "course": COURSE, "lessons": LESSONS}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "..", "lessons.json"), "w"), ensure_ascii=False, indent=1)
print("lessons.json:", len(COURSE), "roadmap entries,", sum(len(l["exercises"]) for l in LESSONS.values()), "exercises")
