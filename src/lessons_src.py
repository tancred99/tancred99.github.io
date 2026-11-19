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


# ---------------- Lesson 3 ----------------
def cj(stem, end): return stem + "<b>" + end + "</b>"
SECTIONS3 = [
 {"h": "Step 1 · What conjugation is", "open": True, "html":
  "<p>An English verb barely changes: I work, you work, he work<b>s</b>. A Russian verb changes its ending for every <b>person</b> and <b>number</b>. That's <b>conjugation</b> (" + ru("спряжение") + "). The verb <b>agrees with its subject</b>, and the subject is always in the <b>nominative</b> case.</p>"
  + t(["Person", "Singular", "Plural"], [
    ["1st", ru("я") + " I", ru("мы") + " we"],
    ["2nd", ru("ты") + " you (one friend, family)", ru("вы") + " you (polite, or more than one)"],
    ["3rd", ru("он, она, оно") + " he, she, it", ru("они") + " they"],
  ])
  + '<p class="tip"><b>You already know this from German:</b> ich arbeite, du arbeitest, er arbeitet, wir arbeiten. Russian works the same way. ' + ru("ты") + " is du; " + ru("вы") + " is both Sie (polite) and ihr (you all), and it always takes the " + ru("вы") + " form, even when you're speaking to one person.</p>"
  + "<p>Two terms you'll see: the <b>infinitive</b> is the dictionary form, which ends in " + ru("-ть") + " (" + ru("работать") + ", to work). The <b>stem</b> is what's left when you take the ending off (" + ru("работа-") + "). You add the personal endings to the stem.</p>"
  + "<p>A noun subject takes the 3rd person, just like " + ru("он / она") + " or " + ru("они") + ":</p>"
  + exl([("Жена работает.", "My wife works. (жена = она)"),
         ("Батюшка читает молитву.", "Father reads the prayer. (батюшка = он)"),
         ("Мы с женой живём в Джексоне.", "My wife and I live in Jackson. (мы с женой = мы)")])
  + '<p class="tip"><b>One present tense, like German.</b> ' + ru("Я читаю") + " covers I read, I'm reading and I do read, just as ich lese does. There's no separate “-ing” form.</p>"},
 {"h": "Step 2 · 1st conjugation: the е-verbs", "open": False, "html":
  "<p>Most verbs whose infinitive ends in " + ru("-ать") + " or " + ru("-ять") + " belong to the <b>1st conjugation</b>. Drop " + ru("-ть") + " and add these endings. Notice the " + ru("е") + " in the middle of the endings: that's why some textbooks call it the е-conjugation.</p>"
  + t(["Subject", "Ending", ru("работать") + " to work", ru("читать") + " to read"], [
    [ru("я"), ru("-ю"), ru(cj("работа", "ю")), ru(cj("чита", "ю"))],
    [ru("ты"), ru("-ешь"), ru(cj("работа", "ешь")), ru(cj("чита", "ешь"))],
    [ru("он, она"), ru("-ет"), ru(cj("работа", "ет")), ru(cj("чита", "ет"))],
    [ru("мы"), ru("-ем"), ru(cj("работа", "ем")), ru(cj("чита", "ем"))],
    [ru("вы"), ru("-ете"), ru(cj("работа", "ете")), ru(cj("чита", "ете"))],
    [ru("они"), ru("-ют"), ru(cj("работа", "ют")), ru(cj("чита", "ют"))],
  ])
  + "<p>Verbs that work exactly like this:</p>"
  + t(["Infinitive", "Meaning"], [
    [ru("делать"), "do, make"], [ru("знать"), "know"], [ru("понимать"), "understand"], [ru("думать"), "think"],
    [ru("слушать"), "listen (to)"], [ru("отдыхать"), "rest, relax"], [ru("покупать"), "buy"], [ru("гулять"), "go for a walk"],
    [ru("завтракать"), "have breakfast"], [ru("ужинать"), "have dinner"],
  ])
  + exl([("Я работаю в IT.", "I work in IT."),
         ("Что ты делаешь после работы?", "What do you do after work?"),
         ("Вы понимаете?", "Do you understand?"),
         ("В субботу мы отдыхаем.", "On Saturday we rest.")])
  + '<p class="tip">When the stem ends in a consonant, the ' + ru("я") + " ending is " + ru("-у") + " and the " + ru("они") + " ending is " + ru("-ут") + ": " + ru("живу, живут") + ". When the ending is stressed, " + ru("е") + " becomes " + ru("ё") + ": " + ru("живёшь, живёт") + ". More in Step 6.</p>"},
 {"h": "Step 3 · 2nd conjugation: the и-verbs", "open": False, "html":
  "<p>Most verbs whose infinitive ends in " + ru("-ить") + " belong to the <b>2nd conjugation</b>. Drop the " + ru("-ить") + " and add these endings. Here the vowel is " + ru("и") + ", and " + ru("они") + " ends in " + ru("-ят") + ".</p>"
  + t(["Subject", "Ending", ru("говорить") + " to speak", ru("звонить") + " to call"], [
    [ru("я"), ru("-ю"), ru(cj("говор", "ю")), ru(cj("звон", "ю"))],
    [ru("ты"), ru("-ишь"), ru(cj("говор", "ишь")), ru(cj("звон", "ишь"))],
    [ru("он, она"), ru("-ит"), ru(cj("говор", "ит")), ru(cj("звон", "ит"))],
    [ru("мы"), ru("-им"), ru(cj("говор", "им")), ru(cj("звон", "им"))],
    [ru("вы"), ru("-ите"), ru(cj("говор", "ите")), ru(cj("звон", "ите"))],
    [ru("они"), ru("-ят"), ru(cj("говор", "ят")), ru(cj("звон", "ят"))],
  ])
  + t(["Side by side", "1st conjugation", "2nd conjugation"], [
    [ru("ты"), ru("-ешь"), ru("-ишь")], [ru("он, она"), ru("-ет"), ru("-ит")], [ru("мы"), ru("-ем"), ru("-им")],
    [ru("вы"), ru("-ете"), ru("-ите")], [ru("они"), ru("-ют / -ут"), ru("-ят / -ат")],
  ])
  + exl([("Вы говорите по-английски?", "Do you speak English?"),
         ("Я звоню жене.", "I'm calling my wife. (жене: to my wife, dative, the indirect object)"),
         ("Вечером мы смотрим фильм.", "In the evening we watch a movie."),
         ("Мой друг часто звонит мне.", "My friend often calls me.")])},
 {"h": "Step 4 · Which group is a verb in?", "open": False, "html":
  "<p>The infinitive gives you a strong hint, with a few exceptions to learn:</p>"
  + t(["Infinitive ends in", "Usually", "Exceptions to know"], [
    [ru("-ить"), "2nd: " + ru("говорить, звонить, любить, учить, платить, ходить"), ru("жить") + " (live) and " + ru("пить") + " (drink) are 1st: " + ru("живёшь, пьёшь")],
    [ru("-ать, -ять"), "1st: " + ru("работать, читать, гулять"), "a few are 2nd: " + ru("слышать") + " (hear), " + ru("стоять") + " (stand), " + ru("спать") + " (sleep): " + ru("слышишь, стоишь, спишь")],
    [ru("-еть"), "the common ones are 2nd: " + ru("смотреть") + " (watch), " + ru("видеть") + " (see), " + ru("сидеть") + " (sit)", "a few are 1st: " + ru("уметь") + " (know how): " + ru("умею, умеешь")],
  ])
  + '<p class="tip"><b>The sure test is the ' + ru("ты") + " form.</b> " + ru("-ешь") + " means 1st conjugation, " + ru("-ишь") + " means 2nd. That's why good dictionaries list every verb with its " + ru("я") + " and " + ru("ты") + " forms: " + ru("читать (-аю, -аешь)") + ", " + ru("говорить (-ю, -ишь)") + ". Learn new verbs in threes: " + ru("говорить · говорю · говоришь") + ". From those you can build the whole verb.</p>"},
 {"h": "Step 5 · Two spelling rules for the я form", "open": False, "html":
  "<h4>Rule 1 · After ж, ч, ш, щ write у and а</h4>"
  + "<p>Russian spelling never puts " + ru("ю") + " or " + ru("я") + " after " + ru("ж, ч, ш, щ") + ". The sound is the same; only the letter changes: " + ru("-ю → -у") + " and " + ru("-ят → -ат") + ".</p>"
  + t(["Infinitive", ru("я"), ru("ты"), ru("они")], [
    [ru("учить") + " study, teach", ru(cj("уч", "у")), ru(cj("уч", "ишь")), ru(cj("уч", "ат"))],
    [ru("слышать") + " hear", ru(cj("слыш", "у")), ru(cj("слыш", "ишь")), ru(cj("слыш", "ат"))],
  ])
  + "<h4>Rule 2 · 2nd-conjugation consonant change in the я form</h4>"
  + "<p>In the 2nd conjugation, many stems change their last consonant <b>in the " + ru("я") + " form only</b>. Every other person keeps the stem from the infinitive.</p>"
  + t(["Change", "Infinitive", ru("я"), ru("ты · они")], [
    [ru("б, в, п, м") + " + " + ru("л"), ru("любить") + " love", ru("люблю"), ru("любишь · любят")],
    ["", ru("готовить") + " cook", ru("готовлю"), ru("готовишь · готовят")],
    [ru("д → ж"), ru("ходить") + " go (on foot), walk", ru("хожу"), ru("ходишь · ходят")],
    ["", ru("видеть") + " see", ru("вижу"), ru("видишь · видят")],
    [ru("т → ч"), ru("платить") + " pay", ru("плачу"), ru("платишь · платят")],
    [ru("с → ш"), ru("просить") + " ask (for)", ru("прошу"), ru("просишь · просят")],
  ])
  + '<p class="tip">After the change you often land on ' + ru("ж, ч, ш") + ", so Rule 1 kicks in too: " + ru("плачу") + ", never “плачю”. " + ru("На кассе я плачу картой.") + " (At the checkout I pay by card.)</p>"},
 {"h": "Step 6 · Verbs that change their stem", "open": False, "html":
  "<p>Like German strong verbs (ich lese, du liest; ich fahre, du fährst), some of the most common Russian verbs change their stem. The good news: the <b>endings are regular 1st conjugation</b>. Once you know " + ru("я") + " and " + ru("ты") + ", the rest follows.</p>"
  + t(["Infinitive", ru("я"), ru("ты"), ru("они")], [
    [ru("жить") + " live", ru("живу"), ru("живёшь"), ru("живут")],
    [ru("писать") + " write", ru("пишу"), ru("пишешь"), ru("пишут")],
    [ru("брать") + " take", ru("беру"), ru("берёшь"), ru("берут")],
    [ru("пить") + " drink", ru("пью"), ru("пьёшь"), ru("пьют")],
    [ru("искать") + " look for", ru("ищу"), ru("ищешь"), ru("ищут")],
    [ru("идти") + " go (on foot)", ru("иду"), ru("идёшь"), ru("идут")],
    [ru("ехать") + " go (by vehicle)", ru("еду"), ru("едешь"), ru("едут")],
  ])
  + '<p class="tip"><b>ё:</b> when the ending is stressed, its ' + ru("е") + " becomes " + ru("ё") + ": " + ru("живёшь, берёшь, идёшь, пьёшь") + ". When it isn't stressed it stays " + ru("е") + ": " + ru("пишешь, ищешь, едешь") + ".</p>"
  + "<h4>One mixed verb: хотеть (to want)</h4>"
  + "<p>" + ru("хотеть") + " is 1st conjugation in the singular and 2nd in the plural:</p>"
  + t(["Singular", "Plural"], [
    [ru("я хочу"), ru("мы хотим")], [ru("ты хочешь"), ru("вы хотите")], [ru("он, она хочет"), ru("они хотят")],
  ])
  + '<p class="tip">You met ' + ru("иду, еду, беру, хочу, ищу") + " in Lesson 2. Now you know they're simply the " + ru("я") + " forms of these verbs.</p>"},
 {"h": "Summary", "open": False, "html":
  '<ul class="sum">'
  + "<li>The verb agrees with its subject (nominative) in person and number. A noun subject is 3rd person; " + ru("мы с женой") + " takes the " + ru("мы") + " form.</li>"
  + "<li>1st conjugation (most " + ru("-ать / -ять") + "): " + ru("-ю, -ешь, -ет, -ем, -ете, -ют") + ".</li>"
  + "<li>2nd conjugation (most " + ru("-ить") + ", plus " + ru("смотреть, видеть, слышать, стоять") + "): " + ru("-ю, -ишь, -ит, -им, -ите, -ят") + ".</li>"
  + "<li>After " + ru("ж, ч, ш, щ") + ": " + ru("-у, -ат") + ". 2nd-conjugation " + ru("я") + " forms can change the consonant: " + ru("люблю, хожу, плачу") + ".</li>"
  + "<li>Stem changers keep 1st-conjugation endings: " + ru("живу, пишу, беру, пью, иду, еду") + ". " + ru("хочу, хочешь, хочет / хотим, хотите, хотят") + ".</li>"
  + "<li>The " + ru("ты") + " form tells you the group: " + ru("-ешь") + " = 1st, " + ru("-ишь") + " = 2nd.</li>"
  + "</ul>"},
]

def v1(p, s, base, ans, d, ex, tr, gl=None):
    return {"part": "A", "sub": "A · 1st conjugation", "p": p, "s": s, "base": base, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def v2(p, s, base, ans, d, ex, tr, gl=None):
    return {"part": "B", "sub": "B · 2nd conjugation", "p": p, "s": s, "base": base, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def v3(p, s, base, ans, d, ex, tr, gl=None):
    return {"part": "C", "sub": "C · stem changes and хотеть", "p": p, "s": s, "base": base, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}

EX3 = [
 v1("1s", "Я ___ в IT.", "работать", "работаю", ["работаешь", "работает", "работают"], "я → -ю. Stem работа- + ю = работаю. (Steps 1 and 2)", "I work in IT."),
 v1("2s", "Что ты ___ после работы?", "делать", "делаешь", ["делаю", "делает", "делаишь"], "ты → -ешь in the 1st conjugation: делаешь. -ишь belongs to the 2nd conjugation. (Step 2)", "What do you do after work?", ["после работы: after work"]),
 v1("3s", "Батюшка ___ молитву.", "читать", "читает", ["читаю", "читают", "читаит"], "The subject батюшка is a noun, so it's 3rd person singular, like он: -ет. (Steps 1 and 2)", "Father reads the prayer.", ["батюшка: Father (the priest)", "молитву: the prayer (accusative)"]),
 v1("1p", "Мы ___ по-русски.", "понимать", "понимаем", ["понимаете", "понимают", "понимаим"], "мы → -ем: понимаем. (Step 2)", "We understand Russian.", ["по-русски: (in) Russian"]),
 v1("2p", "Вы ___, где касса?", "знать", "знаете", ["знаешь", "знаем", "знаите"], "вы → -ете. Polite вы (like German Sie) always takes the вы form, even for one person. (Steps 1 and 2)", "Do you know where the checkout is?", ["касса: checkout"]),
 v1("3p", "Они ___ в парке.", "гулять", "гуляют", ["гуляет", "гуляем", "гулят"], "они → -ют in the 1st conjugation: гуляют. -ят belongs to the 2nd. (Step 2)", "They're taking a walk in the park.", ["гулять: to go for a walk", "в парке: in the park"]),
 v1("1p", "В субботу мы ___.", "отдыхать", "отдыхаем", ["отдыхают", "отдыхаете", "отдыхаим"], "мы → -ем: отдыхаем. (Step 2)", "On Saturday we rest.", ["в субботу: on Saturday", "отдыхать: to rest, relax"]),
 v1("3s", "Жена ___ продукты в магазине.", "покупать", "покупает", ["покупаю", "покупают", "покупаит"], "The subject жена is 3rd person singular, like она: -ет. (Steps 1 and 2)", "My wife buys groceries at the store.", ["жена: wife", "продукты: groceries"]),
 v1("2s", "Ты ___ музыку?", "слушать", "слушаешь", ["слушаю", "слушает", "слушишь"], "ты → -ешь: слушаешь. (Step 2)", "Do you listen to music?", ["музыку: music (accusative)"]),
 v1("1p", "Мы с женой ___ в семь часов.", "завтракать", "завтракаем", ["завтракаю", "завтракают", "завтракает"], "Мы с женой means “my wife and I”, so the verb takes the мы form: -ем. (Steps 1 and 2)", "My wife and I have breakfast at seven.", ["мы с женой: my wife and I", "в семь часов: at seven o'clock"]),
 v1("1s", "Я ___, что это правильно.", "думать", "думаю", ["думаешь", "думает", "думаем"], "я → -ю: думаю. (Step 2)", "I think that's right.", ["правильно: right, correct"]),

 v2("2p", "Вы ___ по-английски?", "говорить", "говорите", ["говорит", "говорим", "говорете"], "говорить is -ить, so 2nd conjugation: вы → -ите. -ете belongs to the 1st. (Steps 3 and 4)", "Do you speak English?", ["по-английски: (in) English"]),
 v2("1s", "Я ___ жене каждый день.", "звонить", "звоню", ["звонишь", "звонит", "звонят"], "я → -ю: звоню. (Step 3)", "I call my wife every day.", ["жене: (to) my wife (dative, the indirect object)", "каждый день: every day"]),
 v2("3s", "Мой друг ___ по-русски и по-белорусски.", "говорить", "говорит", ["говорю", "говорят", "говорет"], "The subject мой друг is 3rd person singular, like он: -ит. (Steps 1 and 3)", "My friend speaks Russian and Belarusian.", ["мой друг: my friend", "по-белорусски: (in) Belarusian"]),
 v2("1p", "Вечером мы ___ фильм.", "смотреть", "смотрим", ["смотрем", "смотрят", "смотрите"], "смотреть ends in -еть but is 2nd conjugation: мы → -им. (Steps 3 and 4)", "In the evening we watch a movie.", ["вечером: in the evening", "фильм: movie"]),
 v2("1s", "Я ___ свою работу.", "любить", "люблю", ["любю", "любит", "любишь"], "A б-stem adds л in the я form: любить → люблю. Only the я form: любишь, любит. (Step 5)", "I love my work.", ["свою работу: my (own) work (accusative)"]),
 v2("1s", "На кассе я ___ картой.", "платить", "плачу", ["плачю", "платю", "платит"], "т → ч in the я form, and after ч you write у, not ю: плачу. (Step 5)", "At the checkout I pay by card.", ["на кассе: at the checkout", "картой: by card"]),
 v2("2s", "Ты ___ русский язык?", "учить", "учишь", ["учешь", "учит", "учу"], "учить is -ить, so 2nd conjugation: ты → -ишь. (Steps 3 and 4)", "Are you learning Russian?", ["русский язык: the Russian language"]),
 v2("3p", "Они ___ в очереди.", "стоять", "стоят", ["стоют", "стоит", "стоим"], "стоять looks like 1st conjugation (-ять), but it's 2nd: они → -ят, not -ют. (Steps 3 and 4)", "They're standing in line.", ["в очереди: in line"]),
 v2("1s", "Я ___ храм.", "видеть", "вижу", ["видю", "видит", "видишь"], "д → ж in the я form: вижу. The other forms keep д: видишь, видит. (Step 5)", "I see the church.", ["храм: church"]),
 v2("1p", "По воскресеньям мы ___ в церковь.", "ходить", "ходим", ["ходем", "ходят", "хожу"], "мы → -им: ходим. The д → ж change (хожу) happens only in the я form. (Steps 3 and 5)", "On Sundays we go to church.", ["по воскресеньям: on Sundays"]),
 v2("2p", "Вы ___ меня?", "слышать", "слышите", ["слышете", "слышишь", "слышат"], "слышать is one of the -ать verbs in the 2nd conjugation: вы → -ите. (Step 4)", "Can you hear me?", ["меня: me"]),

 v3("1p", "Мы с женой ___ в Джексоне.", "жить", "живём", ["живут", "живёте", "живим"], "жить ends in -ить but is 1st conjugation with the stem жив-: мы → живём (ё because the ending is stressed). (Steps 4 and 6)", "My wife and I live in Jackson.", ["мы с женой: my wife and I"]),
 v3("3s", "Мой друг ___ в Беларуси.", "жить", "живёт", ["живит", "живут", "живу"], "жить is 1st conjugation: он → живёт, not “живит”. (Steps 4 and 6)", "My friend lives in Belarus.", ["мой друг: my friend"]),
 v3("1s", "Я ___ письмо другу.", "писать", "пишу", ["писаю", "пишет", "пишут"], "писать changes its stem to пиш-: пишу, пишешь, пишут. The endings are 1st conjugation. (Step 6)", "I'm writing a letter to my friend.", ["письмо: letter (accusative, the direct object)", "другу: to my friend (dative, the indirect object)"]),
 v3("2s", "Что ты ___? Чай или кофе?", "пить", "пьёшь", ["пишь", "пьют", "пьёт"], "пить has the stem пь- and 1st-conjugation endings: ты → пьёшь. (Steps 4 and 6)", "What are you drinking? Tea or coffee?", ["чай: tea", "или: or"]),
 v3("2s", "Ты ___ такси?", "брать", "берёшь", ["бераешь", "берёт", "беришь"], "брать changes its stem to бер-: беру, берёшь. The ending is stressed, so it's ё. (Step 6)", "Are you taking a taxi?"),
 v3("2p", "Что вы ___?", "искать", "ищете", ["искаете", "ищите", "ищут"], "искать changes its stem to ищ-: ищу, ищешь, ищете. Careful: ищите (with и) is the command “look for!”. (Step 6)", "What are you looking for?"),
 v3("1s", "Я ___ кофе.", "хотеть", "хочу", ["хотю", "хочет", "хотим"], "хотеть is mixed. Singular: хочу, хочешь, хочет. Plural: хотим, хотите, хотят. (Step 6)", "I want coffee.", ["кофе: coffee"]),
 v3("1p", "Мы ___ поехать в Минск.", "хотеть", "хотим", ["хочем", "хотят", "хочешь"], "In the plural хотеть switches to the 2nd conjugation: мы хотим. “Хочем” is a very common mistake. (Step 6)", "We want to go to Minsk.", ["поехать: to go (by vehicle)"]),
 v3("2s", "Куда ты ___?", "идти", "идёшь", ["идишь", "иду", "идут"], "идти has 1st-conjugation endings, and the ending is stressed: ты → идёшь. (Step 6)", "Where are you going?", ["куда: where to"]),
 v3("3p", "Завтра они ___ на границу.", "ехать", "едут", ["ехают", "едят", "едет"], "ехать changes its stem to ед-: еду, едешь, едут. Careful: едят means “they eat”. (Steps 2 and 6)", "Tomorrow they're driving to the border.", ["завтра: tomorrow", "на границу: to the border"]),
 v3("3s", "Жена ___ борщ.", "готовить", "готовит", ["готовлит", "готовлю", "готовет"], "готовить is 2nd conjugation: она → готовит. The л appears only in the я form (готовлю). (Steps 3 and 5)", "My wife is making borscht.", ["жена: wife", "борщ: borscht"]),
]


# ---------------- Lesson 4 ----------------
SECTIONS4 = [
 {"h": "Step 1 · How Russian says “I have”", "open": True, "html":
  "<p>Russian has a verb “to have” (" + ru("иметь") + "), but in everyday speech nobody says it about things they own. Instead Russian says <b>“by me there is …”</b>:</p>"
  + exl([("У меня есть трактор.", "I have a tractor. (literally: by me there is a tractor)"),
         ("У нас есть коровы и куры.", "We have cows and chickens."),
         ("У тебя есть время?", "Do you have time?")])
  + "<p>Diagram the first sentence and every word has a clear job:</p>"
  + t(["Word", "Job in the sentence", "Case"], [
    [ru("у"), "preposition “by, at”: always takes the genitive", "—"],
    [ru("меня"), "object of the preposition " + ru("у") + ": the <b>owner</b>", "genitive"],
    [ru("есть"), "verb “there is” (an old present-tense form of " + ru("быть") + ")", "—"],
    [ru("трактор"), "<b>subject</b>: the thing that exists", "nominative"],
  ])
  + '<p class="tip"><b>The thing you own is the subject.</b> That\'s why it stays in the dictionary form (nominative): ' + ru("У меня есть машина") + ", never “машину”. English makes the owner the subject (<i>I</i> have); Russian makes the <i>thing</i> the subject. In Lesson 5 you'll see why this matters: the past-tense verb agrees with the thing.</p>"
  + '<p class="tip"><b>German helps here:</b> ' + ru("у") + " is very close to <i>bei</i>. " + ru("у друга") + " = bei meinem Freund (at my friend's place). Russian says, in effect, “bei mir ist ein Traktor.” And " + ru("у") + " always takes the <b>genitive case</b> (" + ru("родительный падеж") + "), the same case German uses for “of”: des Bruders.</p>"},
 {"h": "Step 2 · у меня, у тебя, у него …", "open": False, "html":
  "<p>The owner after " + ru("у") + " is in the genitive. Here are the pronouns:</p>"
  + t(["Subject (nominative)", "After у (genitive)", "Example"], [
    [ru("я"), ru("у меня"), ru("У меня есть ферма.") + " I have a farm."],
    [ru("ты"), ru("у тебя"), ru("У тебя есть собака?") + " Do you have a dog?"],
    [ru("он"), ru("у него"), ru("У него есть машина.") + " He has a car."],
    [ru("она"), ru("у неё"), ru("У неё есть сестра.") + " She has a sister."],
    [ru("мы"), ru("у нас"), ru("У нас есть сарай.") + " We have a barn."],
    [ru("вы"), ru("у вас"), ru("У вас есть молоко?") + " Do you have milk? (in a store)"],
    [ru("они"), ru("у них"), ru("У них есть дача.") + " They have a dacha (country house)."],
  ])
  + '<p class="tip"><b>The н- rule:</b> after a preposition, ' + ru("его, её, их") + " add " + ru("н-") + ": " + ru("у него, у неё, у них") + ". Without a preposition, " + ru("его, её, их") + " mean “his, her, their”: " + ru("Это его трактор") + " (That's his tractor). So “у его” is always wrong.</p>"
  + "<p>To answer a question, just repeat " + ru("есть") + ":</p>"
  + exl([("У вас есть хлеб? — Да, есть.", "Do you have bread? — Yes, we do."),
         ("У тебя есть время? — Есть.", "Do you have time? — I do.")])},
 {"h": "Step 3 · The genitive endings: у брата, у жены", "open": False, "html":
  "<p>When the owner is a noun, it takes a genitive ending. In the singular there are only four endings, and the dictionary form tells you which:</p>"
  + t(["Dictionary form", "Genitive", "Examples"], [
    ["masc. consonant", "add " + ru("-а"), ru("брат → у брата") + " · " + ru("друг → у друга") + " · " + ru("сосед → у соседа") + " · " + ru("фермер → у фермера")],
    ["masc. " + ru("-й") + ", " + ru("-ь"), ru("-й / -ь → -я"), ru("Андрей → у Андрея") + " · " + ru("сарай → сарая") + " · " + ru("учитель → у учителя")],
    ["neuter " + ru("-о / -е"), ru("-о → -а, -е → -я"), ru("сено → сена") + " · " + ru("молоко → молока") + " · " + ru("море → моря")],
    ["fem. " + ru("-а"), ru("-а → -ы"), ru("жена → у жены") + " · " + ru("сестра → у сестры") + " · " + ru("мама → у мамы") + " · " + ru("корова → коровы")],
    ["fem. " + ru("-я"), ru("-я → -и"), ru("Таня → у Тани") + " · " + ru("деревня → деревни")],
    ["fem. " + ru("-ь"), ru("-ь → -и"), ru("церковь → церкви") + " · " + ru("соль → соли")],
  ])
  + '<p class="tip"><b>Memory hook:</b> masculine and neuter take ' + ru("-а / -я") + "; feminine takes " + ru("-ы / -и") + ". Feminine " + ru("-ь") + " gives " + ru("-и") + ", the same form you know from " + ru("в церкви") + ".</p>"
  + "<h4>Spelling rule · after г, к, х, ж, ч, ш, щ write и, never ы</h4>"
  + "<p>Like the rule in Lesson 3 (" + ru("учу") + ", not “учю”), this is spelling only; the ending is still the feminine one.</p>"
  + t(["Dictionary form", "Genitive"], [
    [ru("подруга") + " (girl)friend", ru("у подруги")], [ru("собака") + " dog", ru("собаки")], [ru("кошка") + " cat", ru("кошки")],
    [ru("дача") + " country house", ru("дачи")], [ru("батюшка") + " Father (the priest)", ru("у батюшки")],
  ])
  + '<p class="tip"><b>Watch:</b> ' + ru("ц") + " is not on the list, so " + ru("курица") + " keeps " + ru("ы") + ": " + ru("курицы") + ". And " + ru("батюшка, папа, дедушка") + " are masculine (Lesson 1) but decline like feminine " + ru("-а") + " nouns: " + ru("у батюшки, у папы, у дедушки") + ". The <b>ending</b> follows the last letter; the <b>agreement</b> follows the man.</p>"},
 {"h": "Step 4 · нет + genitive: not having", "open": False, "html":
  "<p>To say you <b>don't</b> have something, or that something <b>isn't there</b>, replace " + ru("есть") + " with " + ru("нет") + " and put the thing into the <b>genitive</b>:</p>"
  + t(["есть · have / there is (nominative)", "нет · don't have / there isn't (genitive)"], [
    [ru("У меня есть трактор."), ru("У меня нет трактора.")],
    [ru("У нас есть корова."), ru("У нас нет коровы.")],
    [ru("У соседа есть сено."), ru("У соседа нет сена.")],
    [ru("В магазине есть хлеб."), ru("В магазине нет хлеба.")],
    [ru("Сегодня есть служба."), ru("Сегодня нет службы.")],
  ])
  + "<p><b>Why the genitive?</b> In the " + ru("нет") + " sentence there is <b>no subject at all</b>. " + ru("Нет") + " here means “there is no …”, and Russian puts what's missing into the genitive, the case of “none of”. Diagram " + ru("У меня нет трактора") + ": " + ru("у меня") + " = the owner (object of the preposition, genitive); " + ru("нет") + " = the predicate, “there is no”; " + ru("трактора") + " = what's missing (genitive). Not one word is in the nominative.</p>"
  + '<p class="tip"><b>German does this with a word; Russian does it with a case.</b> Ich habe <i>keinen</i> Traktor = ' + ru("У меня нет трактора") + ". “У меня нет трактор” (nominative) is the classic mistake: after " + ru("нет") + ", always the genitive.</p>"
  + "<p>The same rule covers places and people. Whoever or whatever is absent goes into the genitive:</p>"
  + exl([("В деревне нет интернета.", "There's no internet in the village."),
         ("Зимой в поле нет травы.", "In winter there's no grass in the field."),
         ("Жены нет дома.", "My wife isn't home. (жена → жены)"),
         ("Батюшки сейчас нет.", "Father isn't here right now.")])},
 {"h": "Step 5 · More about у and the genitive", "open": False, "html":
  "<h4>When to leave out есть</h4>"
  + "<p>Use " + ru("есть") + " when the point is <b>whether</b> something exists. When everyone knows it exists and you're <b>describing</b> it, leave " + ru("есть") + " out:</p>"
  + exl([("У меня есть машина.", "I have a car. (new information: it exists)"),
         ("У меня новая машина.", "My car is new. / I have a new car. (describing it)"),
         ("У жены голубые глаза.", "My wife has blue eyes. (of course she has eyes)")])
  + "<h4>у = at someone's place</h4>"
  + exl([("Вчера я был у друга.", "Yesterday I was at my friend's. (bei meinem Freund)"),
         ("В субботу мы обедаем у батюшки.", "On Saturday we're having lunch at Father's.")])
  + "<h4>The genitive for “of”</h4>"
  + "<p>The genitive also means “of” or “'s”. The owner comes <b>after</b> the thing, exactly like German <i>der Traktor des Nachbarn</i>:</p>"
  + exl([("Это трактор соседа.", "That's the neighbor's tractor. (сосед → соседа)"),
         ("Это машина жены.", "That's my wife's car. (жена → жены)"),
         ("Это дом батюшки.", "That's Father's house.")])
  + '<p class="tip"><b>Useful phrases:</b> ' + ru("У меня нет времени") + " (I don't have time; " + ru("время → времени") + " is irregular, learn it as a phrase). " + ru("У вас есть сдача?") + " (Do you have change?)</p>"},
 {"h": "Summary", "open": False, "html":
  '<ul class="sum">'
  + "<li>“I have” = " + ru("у меня есть") + " + <b>nominative</b>. The thing owned is the subject; the owner is the object of " + ru("у") + " (genitive).</li>"
  + "<li>Pronouns: " + ru("у меня, у тебя, у него, у неё, у нас, у вас, у них") + " (н- after a preposition).</li>"
  + "<li>Genitive singular: masculine/neuter " + ru("-а / -я") + "; feminine " + ru("-ы / -и") + ". After " + ru("г, к, х, ж, ч, ш, щ") + " write " + ru("и") + ": " + ru("у подруги, у батюшки") + ".</li>"
  + "<li>“I don't have / there isn't” = " + ru("нет") + " + <b>genitive</b>. No subject: " + ru("У меня нет трактора. Жены нет дома.") + "</li>"
  + "<li>Drop " + ru("есть") + " when describing: " + ru("У меня новая машина") + ". The genitive also means “of”: " + ru("трактор соседа") + ".</li>"
  + "</ul>"},
]

def ga(s, w, ans, d, ex, tr, gl=None):  # Part A: the owner after у (pronoun or noun) in the genitive
    return {"part": "A", "sub": "A · у + the owner (genitive)", "k": "own", "w": w, "s": s, "base": w, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def gb(s, w, ans, d, ex, tr, gl=None):  # Part B: нет + genitive
    return {"part": "B", "sub": "B · нет + genitive", "k": "not", "w": w, "s": s, "base": w, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def gc(k, s, w, ans, d, ex, tr, gl=None):  # Part C: есть + nominative or нет + genitive, from the context
    return {"part": "C", "sub": "C · есть or нет?", "k": k, "w": w, "s": s, "base": w + " · есть or нет?", "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}

EX4 = [
 ga("У ___ есть трактор.", "я", "меня", ["я", "мне", "мной"], "After у the owner is in the genitive: я → меня. The tractor is the subject (nominative). (Steps 1 and 2)", "I have a tractor."),
 ga("У ___ есть собака?", "ты", "тебя", ["ты", "тебе", "тобой"], "у + genitive: ты → тебя. (Step 2)", "Do you have a dog?", ["собака: dog"]),
 ga("У ___ есть машина.", "он", "него", ["его", "он", "нему"], "After a preposition его becomes него: у него. Plain его means “his”. (Step 2)", "He has a car."),
 ga("У ___ есть паспорт?", "она", "неё", ["её", "она", "ней"], "After a preposition её becomes неё: у неё. (Step 2)", "Does she have a passport?"),
 ga("У ___ есть коровы и куры.", "мы", "нас", ["мы", "нам", "нами"], "у + genitive: мы → нас. коровы и куры is the subject, in the nominative. (Steps 1 and 2)", "We have cows and chickens.", ["коровы: cows", "куры: chickens, hens"]),
 ga("У ___ есть время?", "вы", "вас", ["вы", "вам", "вами"], "у + genitive: вы → вас. (Step 2)", "Do you have time?", ["время: time"]),
 ga("У ___ есть дача в Беларуси.", "они", "них", ["их", "они", "ним"], "After a preposition их becomes них: у них. (Step 2)", "They have a dacha in Belarus.", ["дача: country house, dacha"]),
 ga("У ___ есть дача в деревне.", "друг", "друга", ["друг", "другу", "другом"], "Masculine consonant: add -а. друг → у друга. (Step 3)", "My friend has a dacha in the village.", ["дача: country house, dacha", "в деревне: in the village"]),
 ga("У ___ есть новый трактор.", "сосед", "соседа", ["сосед", "соседу", "соседом"], "Masculine consonant: add -а. сосед → у соседа. (Step 3)", "The neighbor has a new tractor.", ["новый: new"]),
 ga("У ___ есть сестра в Минске.", "жена", "жены", ["жена", "жене", "жену"], "Feminine -а → -ы: жена → у жены. (Step 3)", "My wife has a sister in Minsk.", ["сестра: sister"]),
 ga("У ___ есть ключ от храма.", "батюшка", "батюшки", ["батюшка", "батюшкы", "батюшке"], "батюшка declines like a feminine -а noun, and after к you write и, not ы: у батюшки. (Step 3)", "Father has the key to the church.", ["ключ: key", "от храма: to (literally from) the church"]),
 ga("У ___ тоже есть корова.", "сестра", "сестры", ["сестра", "сестре", "сестру"], "Feminine -а → -ы: сестра → у сестры. (Step 3)", "My sister has a cow too.", ["тоже: too, also"]),

 gb("У соседа нет ___, поэтому он берёт наш.", "трактор", "трактора", ["трактор", "трактору", "трактором"], "нет + genitive. Masculine consonant: add -а. трактор → трактора. (Steps 3 and 4)", "The neighbor doesn't have a tractor, so he borrows ours.", ["поэтому: so, that's why", "берёт наш: takes (borrows) ours"]),
 gb("В магазине сегодня нет ___.", "хлеб", "хлеба", ["хлеб", "хлебу", "хлебе"], "There isn't = нет + genitive: хлеб → хлеба. (Steps 3 and 4)", "There's no bread at the store today.", ["в магазине: at the store", "сегодня: today"]),
 gb("В холодильнике нет ___.", "молоко", "молока", ["молоко", "молоку", "молоке"], "нет + genitive. Neuter -о → -а: молоко → молока. (Steps 3 and 4)", "There's no milk in the fridge.", ["в холодильнике: in the fridge"]),
 gb("Извините, у меня нет ___.", "билет", "билета", ["билет", "билету", "билетом"], "нет + genitive: билет → билета. (Steps 3 and 4)", "Sorry, I don't have a ticket.", ["извините: excuse me, sorry", "билет: ticket"]),
 gb("Сегодня нет ___.", "служба", "службы", ["служба", "службу", "службе"], "There isn't = нет + genitive. Feminine -а → -ы: служба → службы. (Steps 3 and 4)", "There's no service today.", ["служба: (church) service"]),
 gb("В деревне нет ___.", "интернет", "интернета", ["интернет", "интернету", "интернете"], "нет + genitive: интернет → интернета. (Steps 3 and 4)", "There's no internet in the village.", ["в деревне: in the village"]),
 gb("У нас нет ___.", "собака", "собаки", ["собака", "собакы", "собаку"], "нет + genitive. Feminine -а normally → -ы, but after к you write и: собаки. (Steps 3 and 4)", "We don't have a dog."),
 gb("Зимой в поле нет ___.", "трава", "травы", ["трава", "траву", "траве"], "нет + genitive. Feminine -а → -ы: трава → травы. (Steps 3 and 4)", "In winter there's no grass in the field.", ["зимой: in winter", "в поле: in the field"]),
 gb("В сарае уже нет ___.", "сено", "сена", ["сено", "сену", "сене"], "нет + genitive. Neuter -о → -а: сено → сена. (Steps 3 and 4)", "There's no more hay in the barn.", ["в сарае: in the barn", "уже нет: no more, not any longer"]),
 gb("В доме нет ___.", "соль", "соли", ["соль", "солью", "солы"], "нет + genitive. Feminine -ь → -и: соль → соли. (Steps 3 and 4)", "There's no salt in the house.", ["в доме: in the house"]),
 gb("В ведре нет ___.", "вода", "воды", ["вода", "воду", "воде"], "нет + genitive. Feminine -а → -ы: вода → воды. (Steps 3 and 4)", "There's no water in the bucket.", ["в ведре: in the bucket"]),
 gb("___ нет дома.", "жена", "Жены", ["Жена", "Жену", "Жене"], "Someone who isn't there goes into the genitive too, and the sentence has no subject: жена → жены. (Step 4)", "My wife isn't home.", ["дома: at home"]),

 gc("not", "Я хожу пешком, потому что у меня ___.", "машина", "нет машины", ["есть машина", "нет машина", "нет машине"], "Walking because … → you don't have one: нет + genitive, машина → машины. (Steps 1 and 4)", "I walk because I don't have a car.", ["хожу пешком: I walk, go on foot", "потому что: because"]),
 gc("have", "Сосед пашет поле, потому что у него ___.", "трактор", "есть трактор", ["нет трактора", "нет трактор", "есть трактору"], "He's plowing, so he has one: есть + nominative. The tractor is the subject. (Step 1)", "The neighbor is plowing the field because he has a tractor.", ["пашет: plows", "поле: field"]),
 gc("have", "Мы не покупаем молоко, потому что у нас ___.", "корова", "есть корова", ["нет коровы", "нет корова", "есть корове"], "You don't buy milk because you have a cow: есть + nominative. (Step 1)", "We don't buy milk because we have a cow.", ["покупаем: (we) buy"]),
 gc("not", "Мой друг не может поехать в Америку, потому что у него ___.", "виза", "нет визы", ["есть виза", "нет виза", "нет визе"], "He can't go → he doesn't have one: нет + genitive, виза → визы. (Steps 1 and 4)", "My friend can't go to America because he doesn't have a visa.", ["не может поехать: can't go", "виза: visa"]),
 gc("not", "Я покупаю хлеб, потому что дома ___.", "хлеб", "нет хлеба", ["есть хлеб", "нет хлеб", "нет хлебу"], "You're buying it because there isn't any: нет + genitive, хлеб → хлеба. (Step 4)", "I'm buying bread because there's none at home.", ["дома: at home"]),
 gc("not", "Коровы едят сено, потому что в поле ___.", "трава", "нет травы", ["есть трава", "нет трава", "нет траве"], "They eat hay because there's no grass: нет + genitive, трава → травы. (Step 4)", "The cows are eating hay because there's no grass in the field.", ["едят: (they) eat", "сено: hay"]),
 gc("not", "Я не могу позвонить, потому что у меня ___.", "телефон", "нет телефона", ["есть телефон", "нет телефон", "нет телефону"], "You can't call → you don't have one: нет + genitive, телефон → телефона. (Step 4)", "I can't call because I don't have a phone.", ["не могу позвонить: I can't call"]),
 gc("not", "Мы едем на рынок, потому что в магазине ___.", "рыба", "нет рыбы", ["есть рыба", "нет рыба", "нет рыбе"], "You're going elsewhere because the store has none: нет + genitive, рыба → рыбы. (Step 4)", "We're going to the market because there's no fish at the store.", ["едем на рынок: we're going to the market"]),
 gc("have", "Можно заплатить картой? — Да, у нас ___.", "терминал", "есть терминал", ["нет терминала", "нет терминал", "есть терминалу"], "Yes, you can pay by card → they have one: есть + nominative. (Step 1)", "Can I pay by card? — Yes, we have a card reader.", ["можно заплатить картой: can (I) pay by card", "терминал: card terminal"]),
 gc("have", "Друг приглашает нас в гости, потому что у него ___ в деревне.", "дом", "есть дом", ["нет дома", "нет дом", "есть дому"], "He's inviting you, so he has a house there: есть + nominative. (Step 1)", "My friend is inviting us to visit because he has a house in the village.", ["приглашает нас в гости: invites us to visit"]),
 gc("not", "Извините, у меня ___.", "сдача", "нет сдачи", ["есть сдача", "нет сдача", "нет сдаче"], "Apologizing → you don't have it: нет + genitive. After ч you write и: сдача → сдачи. (Steps 3 and 4)", "Sorry, I don't have change.", ["извините: excuse me, sorry", "сдача: change (money)"]),
]


# ---------------- Lesson 5 ----------------
SECTIONS5 = [
 {"h": "Step 1 · Making the past tense", "open": True, "html":
  "<p>The past tense is the easiest tense in Russian. Take the infinitive, drop " + ru("-ть") + ", and add " + ru("-л") + ". Then add an ending that matches the <b>subject</b> in <b>gender and number</b>:</p>"
  + t(["Subject · ending", ru("работать") + " work", ru("говорить") + " speak", ru("быть") + " be"], [
    [ru("он") + " · " + ru("-л"), ru(cj("работа", "л")), ru(cj("говори", "л")), ru(cj("бы", "л"))],
    [ru("она") + " · " + ru("-ла"), ru(cj("работа", "ла")), ru(cj("говори", "ла")), ru(cj("бы", "ла"))],
    [ru("оно") + " · " + ru("-ло"), ru(cj("работа", "ло")), ru(cj("говори", "ло")), ru(cj("бы", "ло"))],
    [ru("мы, вы, они") + " · " + ru("-ли"), ru(cj("работа", "ли")), ru(cj("говори", "ли")), ru(cj("бы", "ли"))],
  ])
  + "<p>There is only one past tense. " + ru("Я работал") + " covers I worked, I was working, I used to work and I have worked.</p>"
  + '<p class="tip"><b>Unlike German, the person doesn\'t matter.</b> German changes the ending for every person (ich arbeitete, du arbeitetest, wir arbeiteten). Russian only cares about gender and number. The reason: the ' + ru("-л") + " form was originally a <b>participle</b>, like <i>gearbeitet</i>. Old Russian said the equivalent of “I am worked” (" + ru("есмь работал") + "), like German ich habe gearbeitet. The helper verb dropped away, and the participle kept its adjective-like endings for gender and number.</p>"
  + "<p>The conjugation group from Lesson 3 doesn't matter, and the present-tense stem changes disappear. The past is built on the <b>infinitive</b>:</p>"
  + t(["Infinitive", "Present (Lesson 3)", "Past"], [
    [ru("любить"), ru("я люблю"), ru("он любил") + " (no extra л)"],
    [ru("писать"), ru("я пишу"), ru("он писал")],
    [ru("жить"), ru("я живу"), ru("он жил")],
    [ru("хотеть"), ru("я хочу"), ru("он хотел")],
    [ru("ходить"), ru("я хожу"), ru("он ходил")],
  ])},
 {"h": "Step 2 · Agreeing with the subject", "open": False, "html":
  "<p>To pick the ending, find the <b>subject</b> (the nominative) and ask: is it masculine, feminine, neuter or plural?</p>"
  + t(["Subject", "Ending", "Example"], [
    [ru("я") + " (a man speaking)", ru("-л"), ru("Вчера я работал дома.") + " You say this."],
    [ru("я") + " (a woman speaking)", ru("-ла"), ru("Вчера я работала дома.") + " Your wife says this."],
    [ru("ты"), ru("-л / -ла"), ru("Ты был в храме?") + " (to a man) · " + ru("Ты была в храме?") + " (to a woman)"],
    [ru("он, брат, батюшка"), ru("-л"), ru("Батюшка читал Евангелие.") + " Father read the Gospel."],
    [ru("она, жена, корова"), ru("-ла"), ru("Жена готовила ужин.") + " My wife was cooking dinner."],
    [ru("оно, солнце, сено"), ru("-ло"), ru("Солнце светило весь день.") + " The sun shone all day."],
    [ru("мы, вы, они, дети"), ru("-ли"), ru("Мы с женой были на литургии.") + " My wife and I were at the Liturgy."],
  ])
  + '<p class="tip"><b>Gender from Lesson 1 decides everything.</b> ' + ru("батюшка, папа, дедушка") + " are masculine, so it's " + ru("батюшка читал") + ", never “читала”, even though the noun ends in " + ru("-а") + ".</p>"
  + '<p class="tip"><b>' + ru("вы") + " always takes " + ru("-ли") + "</b>, even when it's polite and you mean one person: " + ru("Батюшка, вы были в Минске?") + " Just as German Sie takes the plural verb. And " + ru("мы с женой") + " is " + ru("мы") + ", so " + ru("-ли") + ".</p>"},
 {"h": "Step 3 · -ся verbs and a few irregular pasts", "open": False, "html":
  "<h4>Verbs with -ся</h4>"
  + "<p>Form the past as usual, then add " + ru("-ся") + " after a consonant and " + ru("-сь") + " after a vowel:</p>"
  + t(["Infinitive", "он", "она", "они"], [
    [ru("учиться") + " study", ru("учи<b>лся</b>"), ru("учила<b>сь</b>"), ru("учили<b>сь</b>")],
    [ru("молиться") + " pray", ru("моли<b>лся</b>"), ru("молила<b>сь</b>"), ru("молили<b>сь</b>")],
  ])
  + "<h4>Irregular pasts to learn now</h4>"
  + "<p>Learn these four now. Verbs whose infinitive ends in " + ru("-ти") + " or " + ru("-чь") + " often have no " + ru("-л") + " in the masculine (" + ru("шёл, мог, пас") + "), and " + ru("есть") + " (eat) simply loses its " + ru("с") + ":</p>"
  + t(["Infinitive", "он", "она", "оно", "они"], [
    [ru("идти") + " go (on foot)", ru("шёл"), ru("шла"), ru("шло"), ru("шли")],
    [ru("есть") + " eat", ru("ел"), ru("ела"), ru("ело"), ru("ели")],
    [ru("мочь") + " can, be able", ru("мог"), ru("могла"), ru("могло"), ru("могли")],
    [ru("пасти") + " graze, herd", ru("пас"), ru("пасла"), ru("пасло"), ru("пасли")],
  ])
  + exl([("Утром я шёл в храм.", "In the morning I was walking to church."),
         ("Раньше мой дед пас коров.", "My grandfather used to graze cows."),
         ("Что ты ела на завтрак?", "What did you eat for breakfast? (to a woman)")])
  + '<p class="tip"><b>You\'ll also see</b> past forms like ' + ru("купил, сделал, сбежала") + ". They're <b>perfective</b> verbs (aspect is Lesson 11), but the past tense is formed exactly the same way: " + ru("Корова сбежала!") + " (The cow got out!)</p>"},
 {"h": "Step 4 · был, была, было, были", "open": False, "html":
  "<p>Russian drops “is / am / are” in the present (" + ru("Я в храме") + "), but in the past you need " + ru("быть") + ", and it agrees with the subject like any other verb:</p>"
  + t(["Present", "Past"], [
    [ru("Я в храме.") + " (a man)", ru("Я был в храме.")],
    [ru("Жена на работе."), ru("Жена была на работе.")],
    [ru("Солнце на небе."), ru("Солнце было на небе.")],
    [ru("Мы дома."), ru("Мы были дома.")],
  ])
  + "<p><b>No subject → neuter.</b> Sentences like “it was cold” have no subject in Russian. With nothing to agree with, the verb takes the neuter " + ru("-о") + ":</p>"
  + exl([("Утром было холодно.", "It was cold in the morning."),
         ("Было интересно.", "It was interesting."),
         ("Было поздно.", "It was late.")])
  + '<p class="tip"><b>Stress:</b> with ' + ru("не") + ", the stress jumps onto " + ru("не") + " in " + ru("не был, не было, не были") + " (say NYE-byl), but not in " + ru("не была") + " (stress on the end). Tap the words to hear them.</p>"},
 {"h": "Step 5 · Having and not having in the past", "open": False, "html":
  "<p>In Lesson 4 the thing you have is the <b>subject</b> (nominative). So in the past, " + ru("был / была / было / были") + " agrees with the <b>thing</b>, not with the owner:</p>"
  + t(["Present", "Past", "Why"], [
    [ru("У меня есть трактор."), ru("У меня был трактор."), ru("трактор") + " is masculine"],
    [ru("У нас есть корова."), ru("У нас была корова."), ru("корова") + " is feminine"],
    [ru("У нас есть сено."), ru("У нас было сено."), ru("сено") + " is neuter"],
    [ru("У нас есть куры."), ru("У нас были куры."), ru("куры") + " is plural"],
  ])
  + "<p>You and your wife say the same thing: " + ru("У меня был трактор") + ". The owner (" + ru("меня") + ") is only the object of " + ru("у") + "; it doesn't control the verb.</p>"
  + "<p><b>Not having:</b> " + ru("нет") + " becomes " + ru("не было") + ", always neuter, because the sentence has no subject:</p>"
  + t(["Present", "Past"], [
    [ru("У меня нет времени."), ru("У меня не было времени.")],
    [ru("В магазине нет хлеба."), ru("В магазине не было хлеба.")],
    [ru("Сегодня нет службы."), ru("Вчера не было службы.")],
  ])
  + '<p class="tip"><b>Classic mistake:</b> “В магазине не был хлеба”, matching хлеб. But ' + ru("хлеба") + " is genitive, not a subject, so nothing agrees with it: always " + ru("не было") + ".</p>"},
 {"h": "Step 6 · Words for talking about the past", "open": False, "html":
  t(["Russian", "English"], [
    [ru("вчера"), "yesterday"], [ru("позавчера"), "the day before yesterday"], [ru("утром · днём · вечером"), "in the morning · in the afternoon · in the evening"],
    [ru("в субботу · в воскресенье"), "on Saturday · on Sunday"], [ru("на прошлой неделе"), "last week"], [ru("в прошлом году"), "last year"],
    [ru("неделю назад"), "a week ago"], [ru("раньше"), "before, used to"], [ru("давно"), "a long time ago, for a long time"],
  ])
  + exl([("Раньше у деда были свиньи.", "Grandpa used to have pigs."),
         ("В прошлом году мы ездили в Беларусь.", "Last year we went to Belarus."),
         ("Позавчера я косил траву.", "The day before yesterday I mowed the grass.")])},
 {"h": "Summary", "open": False, "html":
  '<ul class="sum">'
  + "<li>Past = infinitive minus " + ru("-ть") + " + " + ru("-л / -ла / -ло / -ли") + ". One past tense for worked / was working / used to work.</li>"
  + "<li>The ending agrees with the subject's <b>gender and number</b>, not its person. " + ru("я / ты") + ": the real person's gender. " + ru("вы, мы с женой") + ": " + ru("-ли") + ". " + ru("батюшка читал") + ".</li>"
  + "<li>" + ru("-ся") + " after a consonant, " + ru("-сь") + " after a vowel: " + ru("учился, училась") + ". Irregular: " + ru("шёл / шла, ел, мог, пас") + ".</li>"
  + "<li>No subject → neuter: " + ru("было холодно") + ".</li>"
  + "<li>" + ru("У меня был трактор / была корова / было сено / были куры") + ": the verb agrees with the thing. Not having: " + ru("не было") + " + genitive, always.</li>"
  + "</ul>"},
]

def p1(g, subj, s, base, ans, d, ex, tr, gl=None):  # g: m / f / n / pl, the gender-number of subj
    return {"part": "A", "sub": "A · -л, -ла, -ло, -ли", "g": g, "subj": subj, "s": s, "base": base, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def p2(g, subj, s, ans, d, ex, tr, gl=None):  # быть; subj None = no subject (impersonal / не было)
    return {"part": "B", "sub": "B · был, была, было, были", "g": g, "subj": subj, "s": s, "base": "быть", "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}
def p3(g, subj, s, base, ans, d, ex, tr, gl=None):
    return {"part": "C", "sub": "C · irregular and -ся", "g": g, "subj": subj, "s": s, "base": base, "a": ans, "d": d, "ex": ex, "translation": tr, "glosses": gl or []}

EX5 = [
 p1("m", "Андрей", "«Вчера я ___ дома», — говорит Андрей.", "работать", "работал", ["работала", "работали", "работало"], "Andrey is a man, so я takes the masculine: -л. (Steps 1 and 2)", "“Yesterday I worked at home,” says Andrey.", ["говорит: says"]),
 p1("f", "жена", "Жена ___ борщ.", "готовить", "готовила", ["готовил", "готовили", "готовило"], "The subject жена is feminine: -ла. (Steps 1 and 2)", "My wife was making borscht.", ["борщ: borscht"]),
 p1("m", "батюшка", "Батюшка ___ Евангелие.", "читать", "читал", ["читала", "читали", "читало"], "батюшка ends in -а but is masculine (Lesson 1): -л. (Step 2)", "Father read the Gospel.", ["Евангелие: the Gospel"]),
 p1("pl", "мы", "Вечером мы с женой ___ фильм.", "смотреть", "смотрели", ["смотрел", "смотрела", "смотрело"], "мы с женой = мы, plural: -ли. (Step 2)", "In the evening my wife and I watched a movie.", ["вечером: in the evening", "мы с женой: my wife and I"]),
 p1("f", "Таня", "Таня, что ты ___ в субботу?", "делать", "делала", ["делал", "делали", "делало"], "You're asking Tanya, a woman, so ты takes -ла. (Step 2)", "Tanya, what did you do on Saturday?", ["в субботу: on Saturday"]),
 p1("pl", "вы", "Батюшка, вы ___ с епископом?", "говорить", "говорили", ["говорил", "говорила", "говорило"], "вы always takes -ли, even when it's polite and means one person. (Step 2)", "Father, did you speak with the bishop?", ["с епископом: with the bishop"]),
 p1("m", "фермер", "Утром фермер ___ сено.", "косить", "косил", ["косила", "косили", "косило"], "The subject фермер is masculine: -л. (Steps 1 and 2)", "In the morning the farmer was mowing hay.", ["утром: in the morning", "сено: hay"]),
 p1("f", "жена", "Утром жена ___ кур.", "кормить", "кормила", ["кормил", "кормили", "кормило"], "The subject жена is feminine: -ла. кур is the direct object. (Steps 1 and 2)", "In the morning my wife fed the chickens.", ["кур: the chickens (direct object)"]),
 p1("pl", "друзья", "Вчера друзья из Минска ___ нам.", "звонить", "звонили", ["звонил", "звонила", "звонило"], "The subject друзья (friends) is plural: -ли. (Step 2)", "Yesterday our friends from Minsk called us.", ["друзья: friends", "нам: (to) us, the indirect object"]),
 p1("f", "мама", "Мама долго ___ в Гомеле.", "жить", "жила", ["жил", "жили", "жило"], "The subject мама is feminine: -ла. The past is built on the infinitive жи-ть, not on живу. (Step 1)", "Mom lived in Gomel for a long time.", ["долго: for a long time"]),
 p1("n", "солнце", "Солнце ___ весь день.", "светить", "светило", ["светил", "светила", "светили"], "The subject солнце is neuter (-е): -ло. (Step 2)", "The sun shone all day.", ["весь день: all day"]),
 p1("m", "сосед", "Вчера сосед ___ поле.", "пахать", "пахал", ["пахала", "пахали", "пахало"], "The subject сосед is masculine: -л. The present пашет has a stem change, but the past comes from the infinitive: пахал. (Step 1)", "Yesterday the neighbor plowed the field.", ["поле: field"]),

 p2("pl", "мы", "В воскресенье мы ___ на литургии.", "были", ["был", "была", "было"], "Subject мы, plural: были. (Step 4)", "On Sunday we were at the Liturgy.", ["в воскресенье: on Sunday"]),
 p2("m", "Андрей", "Андрей, где ты ___ вчера?", "был", ["была", "были", "было"], "You're asking Andrey, a man: ты был. (Steps 2 and 4)", "Andrey, where were you yesterday?", ["вчера: yesterday"]),
 p2("f", "жена", "Жена ___ в магазине.", "была", ["был", "были", "было"], "Subject жена, feminine: была. (Step 4)", "My wife was at the store.", ["в магазине: at the store"]),
 p2("f", "погода", "Вчера ___ хорошая погода.", "была", ["был", "было", "были"], "The subject is погода (weather), feminine: была. The subject can come after the verb. (Step 4)", "Yesterday the weather was nice.", ["хорошая погода: nice weather"]),
 p2("n", None, "Утром ___ холодно.", "было", ["был", "была", "были"], "“It was cold” has no subject in Russian, so the verb is neuter: было. (Step 4)", "It was cold in the morning.", ["утром: in the morning", "холодно: cold"]),
 p2("m", "трактор", "Раньше у нас ___ старый трактор.", "был", ["была", "было", "были"], "In у нас … the thing owned is the subject. трактор is masculine: был. (Step 5)", "We used to have an old tractor.", ["раньше: before, used to", "старый: old"]),
 p2("f", "корова", "У бабушки ___ корова.", "была", ["был", "было", "были"], "The subject is корова (feminine), not бабушка (the owner, after у): была. (Step 5)", "Grandma had a cow.", ["у бабушки: grandma had (literally: by grandma)"]),
 p2("n", "сено", "Осенью у нас ___ сено на всю зиму.", "было", ["был", "была", "были"], "The subject сено is neuter: было. (Step 5)", "In the fall we had hay for the whole winter.", ["осенью: in the fall", "на всю зиму: for the whole winter"]),
 p2("pl", "куры", "Раньше у нас ___ куры.", "были", ["был", "была", "было"], "The subject куры (chickens) is plural: были. (Step 5)", "We used to have chickens.", ["раньше: before, used to"]),
 p2("n", None, "У меня не ___ времени.", "было", ["был", "была", "были"], "нет in the past is не было, always neuter: времени is genitive, not a subject. (Step 5)", "I didn't have time.", ["времени: time (genitive)"]),
 p2("n", None, "Вчера в магазине не ___ хлеба.", "было", ["был", "была", "были"], "хлеба is genitive, so nothing agrees with it: не было, never “не был”. (Step 5)", "Yesterday there was no bread at the store.", ["хлеба: bread (genitive)"]),
 p2("n", None, "В субботу не ___ службы.", "было", ["была", "был", "были"], "службы is genitive, not a subject: не было, never “не была”. (Step 5)", "There was no service on Saturday.", ["службы: (church) service (genitive)"]),

 p3("m", "Андрей", "Андрей ___ домой.", "идти", "шёл", ["шла", "шли", "идл"], "идти is irregular: шёл, шла, шли. Андрей is masculine. (Step 3)", "Andrey was walking home.", ["домой: home (direction)"]),
 p3("f", "жена", "Жена ___ в церковь.", "идти", "шла", ["шёл", "шли", "идла"], "идти is irregular: шёл, шла, шли. жена is feminine. (Step 3)", "My wife was walking to church."),
 p3("pl", "мы", "Мы ___ по улице.", "идти", "шли", ["шёл", "шла", "идли"], "идти is irregular: шёл, шла, шли. мы is plural. (Step 3)", "We were walking down the street.", ["по улице: down the street"]),
 p3("f", "Таня", "Таня, что ты ___ на завтрак?", "есть", "ела", ["ел", "ели", "есла"], "есть (eat): ел, ела, ели. You're asking Tanya, so feminine. (Step 3)", "Tanya, what did you eat for breakfast?", ["на завтрак: for breakfast"]),
 p3("pl", "дети", "Дети ___ блины.", "есть", "ели", ["ел", "ела", "если"], "есть (eat): ел, ела, ели. дети (children) is plural. (Step 3)", "The children were eating pancakes.", ["блины: pancakes, blini"]),
 p3("m", "Андрей", "Андрей не ___ прийти в субботу.", "мочь", "мог", ["могла", "могли", "мочл"], "мочь: мог, могла, могли (no -л in the masculine). (Step 3)", "Andrey couldn't come on Saturday.", ["прийти: to come"]),
 p3("f", "жена", "Жена не ___ найти ключи.", "мочь", "могла", ["мог", "могли", "мочла"], "мочь: мог, могла, могли. жена is feminine. (Step 3)", "My wife couldn't find the keys.", ["найти: to find", "ключи: keys"]),
 p3("m", "дед", "Раньше мой дед ___ коров.", "пасти", "пас", ["пасл", "пасла", "пасли"], "пасти: пас, пасла, пасли. The masculine has no -л. (Step 3)", "My grandfather used to graze cows.", ["раньше: before, used to", "коров: cows (direct object)"]),
 p3("pl", "мы", "Летом мы с братом ___ коров на лугу.", "пасти", "пасли", ["пас", "пасла", "пасл"], "пасти: пас, пасла, пасли. мы с братом is plural. (Steps 2 and 3)", "In the summer my brother and I grazed cows in the meadow.", ["летом: in the summer", "на лугу: in the meadow"]),
 p3("m", "друг", "Мой друг ___ в Минске.", "учиться", "учился", ["училась", "учились", "училсь"], "-ся after a consonant: учил + ся = учился. друг is masculine. (Step 3)", "My friend studied in Minsk.", ["мой друг: my friend"]),
 p3("f", "Таня", "Таня ___ в Гомеле.", "учиться", "училась", ["учился", "учились", "училася"], "After a vowel -ся becomes -сь: учила + сь = училась. (Step 3)", "Tanya studied in Gomel."),
 p3("pl", "мы", "Вчера мы долго ___ в храме.", "молиться", "молились", ["молился", "молилась", "молилися"], "Plural: молили + сь (after a vowel) = молились. (Step 3)", "Yesterday we prayed in church for a long time.", ["долго: for a long time"]),
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
 },
 "L3": {
  "id": "L3", "n": 3,
  "title": "The present tense: 1st and 2nd conjugation",
  "goal": "By the end you'll be able to say what you and other people do: Я работаю в IT. Вы говорите по-русски? Мы с женой живём в Джексоне.",
  "minutes": "15–20 min to read, then 33 exercises",
  "sections": SECTIONS3,
  "parts": {"A": "Part A · 1st conjugation (-ешь, -ют)", "B": "Part B · 2nd conjugation (-ишь, -ят)", "C": "Part C · Stem changes, хотеть, and any subject"},
  "practice": {
    "title": "Now use it: write to your tutor",
    "text": "Answer in chat: Что ты делаешь после работы? Write 3 short sentences: one about yourself (я), one about your wife or your friend (3rd person), and one with мы с женой. Use at least one 2nd-conjugation verb (-ишь).",
    "examples": ["После работы я отдыхаю.", "Вечером я смотрю фильм.", "Мой друг живёт в Беларуси.", "Мы с женой ходим в церковь."]
  },
  "exercises": EX3,
 },

 "L4": {
  "id": "L4", "n": 4,
  "title": "The genitive case: у меня есть / у меня нет (having and not having)",
  "goal": "By the end you'll be able to say what you and others have and don't have: У меня есть трактор. У нас нет собаки. В магазине нет хлеба.",
  "minutes": "15–20 min to read, then %d exercises",
  "sections": SECTIONS4,
  "parts": {"A": "Part A · у + the owner (genitive)", "B": "Part B · нет + the genitive", "C": "Part C · есть or нет? Read the context"},
  "practice": {
    "title": "Now use it: write to your tutor",
    "text": "Answer in chat: Что у тебя есть на ферме? Write 4 short sentences: two things you have (у меня есть / у нас есть), one thing you don't have yet (у нас нет + genitive), and one about someone else (у жены, у друга, у соседа).",
    "examples": ["У нас есть коровы и куры.", "У меня есть трактор.", "У нас пока нет козы.", "У друга есть дача в Беларуси."]
  },
  "exercises": EX4,
 },
 "L5": {
  "id": "L5", "n": 5,
  "title": "The past tense: я был, она была",
  "goal": "By the end you'll be able to say what you did and where you were: Вчера я косил сено. Жена была в магазине. У нас была корова.",
  "minutes": "15–20 min to read, then %d exercises",
  "sections": SECTIONS5,
  "parts": {"A": "Part A · -л, -ла, -ло, -ли", "B": "Part B · был, была, было, были (and не было)", "C": "Part C · Irregular pasts and -ся verbs"},
  "practice": {
    "title": "Now use it: write to your tutor",
    "text": "Answer in chat: Что ты делал в субботу? Write 4 sentences about last weekend: one thing you did (-л), one thing your wife did (-ла), one with мы с женой (-ли), and one with был / была / было or не было.",
    "examples": ["В субботу я косил траву.", "Жена готовила ужин.", "В воскресенье мы с женой были на литургии.", "Вечером не было дождя."]
  },
  "exercises": EX5,
 },
}

for _k in ("L4", "L5"): LESSONS[_k]["minutes"] = LESSONS[_k]["minutes"] % len(LESSONS[_k]["exercises"])

import numbers_lesson
NUMBERS = numbers_lesson.build(t, ru, exl)
out = {"version": 1, "course": COURSE, "lessons": LESSONS, "numbers": NUMBERS}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "..", "lessons.json"), "w"), ensure_ascii=False, indent=1)
print("lessons.json:", len(COURSE), "roadmap entries,", sum(len(l["exercises"]) for l in LESSONS.values()), "exercises")
