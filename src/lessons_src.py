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
  {"n": 9, "id": "L9", "title": "Plurals and the genitive plural", "topic": "пять коров, много друзей; для, кроме, напротив"},
  {"id": "LK", "title": "The relative pronoun который", "topic": "дом, который я купил; друг, которого я видел"},
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
  ])
  + "<p>To say where you are from, ask " + ru("Откуда вы?") + " and answer with " + ru("Я из") + " + the <b>genitive</b> (" + ru("родительный падеж") + "): " + ru("Я из Минска") + ", " + ru("Я из Бреста") + ", " + ru("Я из Беларуси") + ", " + ru("Я из Техаса") + ", " + ru("Я из Арканзаса") + ". Foreign names in " + ru("-о") + " often stay put: " + ru("Я из Колорадо") + ", " + ru("Я еду в Колорадо") + ".</p>"},
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
  + '<p class="tip"><b>The sure test is the ' + ru("ты") + " form.</b> " + ru("-ешь") + " means 1st conjugation, " + ru("-ишь") + " means 2nd. That's why good dictionaries list every verb with its " + ru("я") + " and " + ru("ты") + " forms: " + ru("читать (-аю, -аешь)") + ", " + ru("говорить (-ю, -ишь)") + ". Learn new verbs in threes: " + ru("говорить · говорю · говоришь") + ". From those you can build the whole verb.</p>"
  + '<p class="tip"><b>' + ru("уметь") + " vs " + ru("мочь") + ".</b> " + ru("уметь") + " is “know how”: " + ru("Я не умею танцевать") + " (I don’t know how to dance). " + ru("мочь") + " is “be able / can / may”: " + ru("Я не могу вам помочь") + " (I can’t help you — maybe there is no time, or you’re not allowed). Both take an infinitive. Don’t swap them.</p>"},
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


# ---------------- Review 1 ----------------

SECTIONS_R1 = [
 {"h": "Step 1 · Gender and где? (the prepositional)", "open": True, "html":
  "<p>Every noun is masculine, feminine or neuter, and the last letter of the dictionary form almost always tells you. That gender then picks the prepositional ending when you say <b>where</b> something is (" + ru("где?") + ").</p>"
  + t(["Ends in", "Gender", "Prepositional (где?)"], [
    ["a consonant or " + ru("-й"), "masculine", ru("-е") + ": " + ru("в офисе") + ", " + ru("в храме") + ", " + ru("в Бресте") + ", " + ru("на сервере")],
    [ru("-а / -я"), "feminine", ru("-а → -е, -я → -е") + ": " + ru("на кухне") + ", " + ru("на ферме") + ", " + ru("в гостинице")],
    [ru("-о / -е"), "neuter", ru("-е") + " (often no change): " + ru("на пастбище") + ", " + ru("в поле") + ", " + ru("в письме")],
    [ru("-ь"), "masc. or fem.", "masculine " + ru("-е") + " (" + ru("в Гомеле") + "), feminine " + ru("-и") + " (" + ru("в церкви") + ", " + ru("на площади") + ")"],
    [ru("-ий / -ия / -ие"), "various", ru("-ии") + ": " + ru("в санатории") + ", " + ru("в России") + ", " + ru("в здании") + ", " + ru("на литургии")],
  ])
  + "<p>" + ru("в") + " or " + ru("на") + " is the same pair you already learned: " + ru("в") + " for indoors and countries (" + ru("в офисе, в храме, в Беларуси") + "), " + ru("на") + " for surfaces, events and a short list of places (" + ru("на кухне, на ферме, на концерте, на рынке, на работе") + ").</p>"
  + '<p class="tip"><b>German:</b> ' + ru("где?") + " is <i>wo?</i> The prepositional is the case after “in / at / on” for location: in dem Büro = " + ru("в офисе") + ", auf der Küche isn’t German, but auf dem Konzert ≈ " + ru("на концерте") + ". Men ending in " + ru("-а") + " (" + ru("батюшка, папа, дедушка") + ") stay masculine for agreement, even though they decline like feminine nouns.</p>"},
 {"h": "Step 2 · Accusative of things and куда?", "open": False, "html":
  "<p>The <b>accusative</b> (" + ru("винительный падеж") + ") marks the <b>direct object</b> — the thing you buy, write, see or listen to. For <i>things</i> (Lesson 2) the ending is simple:</p>"
  + t(["Dictionary form", "Accusative", "Examples"], [
    [ru("-а / -я") + " (mostly fem.)", ru("-у / -ю"), ru("программа → программу") + " · " + ru("песня → песню") + " · " + ru("икона → икону") + " · " + ru("ферма → на ферму")],
    ["everything else", "no change", ru("файл → файл") + " · " + ru("код → код") + " · " + ru("корм → корм") + " · " + ru("письмо → письмо") + " · " + ru("Брест → в Брест")],
  ])
  + "<p>" + ru("куда?") + " (“where to?”) uses the same " + ru("в") + " or " + ru("на") + " as " + ru("где?") + ", but the noun goes into the <b>accusative</b>. Compare:</p>"
  + exl([("Я в офисе.", "I'm in the office. (где? prepositional)"),
         ("Я еду в офис.", "I'm going to the office. (куда? accusative)"),
         ("Жена на кухне.", "My wife is in the kitchen. (где?)"),
         ("Я иду на кухню.", "I'm going to the kitchen. (куда?)"),
         ("Мы на концерте.", "We're at the concert. (где?)"),
         ("Мы идём на концерт.", "We're going to the concert. (куда?)"),
         ("Коровы на пастбище.", "The cows are in the pasture. (где? — neuter, same form)"),
         ("Я еду на ферму.", "I'm going to the farm. (куда?)")])
  + '<p class="tip"><b>German:</b> ' + ru("где?") + " = <i>wo?</i>, " + ru("куда?") + " = <i>wohin?</i> ich bin im Büro / ich fahre ins Büro. And “home” is still irregular: " + ru("дома") + " (где?) vs " + ru("домой") + " (куда?). Lesson 6 will add people and animals, where the accusative sometimes looks different.</p>"},
 {"h": "Step 3 · The present tense", "open": False, "html":
  "<p>A Russian verb has two conjugation classes. The " + ru("ты") + " form tells you which: " + ru("-ешь / -ёшь") + " is 1st conjugation (е-verbs), " + ru("-ишь") + " is 2nd (и-verbs).</p>"
  + t(["", "я", "ты", "он / она", "мы", "вы", "они"], [
    ["1st: " + ru("работать, писать, слушать"), ru("работаю") + "<br>" + ru("пишу") + "<br>" + ru("слушаю"), ru("работаешь") + "<br>" + ru("пишешь") + "<br>" + ru("слушаешь"), ru("работает") + "<br>" + ru("пишет") + "<br>" + ru("слушает"), ru("работаем") + "<br>" + ru("пишем") + "<br>" + ru("слушаем"), ru("работаете") + "<br>" + ru("пишете") + "<br>" + ru("слушаете"), ru("работают") + "<br>" + ru("пишут") + "<br>" + ru("слушают")],
    ["2nd: " + ru("звонить, готовить, говорить"), ru("звоню") + "<br>" + ru("готовлю") + "<br>" + ru("говорю"), ru("звонишь") + "<br>" + ru("готовишь") + "<br>" + ru("говоришь"), ru("звонит") + "<br>" + ru("готовит") + "<br>" + ru("говорит"), ru("звоним") + "<br>" + ru("готовим") + "<br>" + ru("говорим"), ru("звоните") + "<br>" + ru("готовите") + "<br>" + ru("говорите"), ru("звонят") + "<br>" + ru("готовят") + "<br>" + ru("говорят")],
  ])
  + "<p>A few 1st-conjugation verbs change the stem: " + ru("писать → пишу, пишешь") + "; " + ru("жить → живу") + ". Some 2nd-conjugation verbs drop a consonant in the " + ru("я") + " form only: " + ru("видеть → вижу, видишь") + "; " + ru("любить → люблю, любишь") + "; " + ru("готовить → готовлю, готовишь") + ". " + ru("хотеть") + " is mixed: " + ru("хочу, хочешь, хочет") + " but " + ru("хотим, хотите, хотят") + ".</p>"
  + '<p class="tip"><b>German:</b> this is just like choosing a weak vs. a strong verb, except Russian marks the choice on every person, not only on <i>er/sie/es</i>. Once you know the ' + ru("ты") + " form, the rest of the set is regular.</p>"},
 {"h": "Step 4 · Genitive: у меня есть / нет", "open": False, "html":
  "<p>Russian says “by me there is …” for “I have.” The <b>owner</b> after " + ru("у") + " is in the <b>genitive</b>; the <b>thing owned</b> is the <b>subject</b> (nominative). To say you don’t have something, use " + ru("нет") + " + genitive, and drop the subject:</p>"
  + exl([("У меня есть компьютер.", "I have a computer. (компьютер = subject, nominative)"),
         ("У жены есть подруга в Бресте.", "My wife has a friend in Brest."),
         ("У нас пока нет индюка.", "We don't have a turkey yet. (нет + genitive)"),
         ("У коллеги нет машины.", "My colleague doesn't have a car."),
         ("В этом альбоме нет песни.", "That song isn't on this album.")])
  + t(["Nominative", "After у / after нет (genitive)"], [
    [ru("я, ты, он, она, мы, вы, они"), ru("меня, тебя, него, неё, нас, вас, них")],
    ["masc. / neut. consonant or " + ru("-о"), ru("-а") + ": " + ru("компьютер → компьютера") + ", " + ru("индюк → индюка") + ", " + ru("ключ → ключа")],
    ["masc. " + ru("-й / -ь") + ", neut. " + ru("-е"), ru("-я") + ": " + ru("пароль → пароля") + ", " + ru("учитель → учителя")],
    ["fem. " + ru("-а / -я / -ь"), ru("-ы / -и") + ": " + ru("жена → жены") + ", " + ru("песня → песни") + ", " + ru("коза → козы") + ". After " + ru("г, к, х, ж, ч, ш, щ") + " write " + ru("и") + ": " + ru("у подруги")],
  ])
  + '<p class="tip"><b>Remember:</b> after a preposition, ' + ru("его / её / их") + " add " + ru("н-") + ": " + ru("у него, у неё, у них") + ". And " + ru("время") + " is irregular: " + ru("нет времени") + ". German " + ru("у") + " ≈ <i>bei</i>: bei mir ist ein Computer.</p>"},
 {"h": "Summary", "open": False, "html":
  '<ul class="sum">'
  + "<li>Gender comes from the last letter. " + ru("где?") + " = " + ru("в / на") + " + <b>prepositional</b> (" + ru("в офисе, на кухне, на пастбище, в церкви") + ").</li>"
  + "<li>" + ru("куда?") + " = the same " + ru("в / на") + " + <b>accusative</b> of a thing (" + ru("в офис, на кухню, на ферму") + "). Direct objects: " + ru("-а / -я → -у / -ю") + ", otherwise no change (" + ru("пишу программу, открываю файл") + ").</li>"
  + "<li>Present tense: 1st conjugation " + ru("-ешь / -ет / -ют") + ", 2nd " + ru("-ишь / -ит / -ят") + ". Watch stem changes: " + ru("пишу, живу, вижу, люблю, готовлю") + ".</li>"
  + "<li>“I have” = " + ru("у меня есть") + " + nominative. “I don’t have” = " + ru("нет") + " + genitive. The owner after " + ru("у") + " is genitive: " + ru("у меня, у жены, у него") + ".</li>"
  + "</ul>"},
]

def r1(part, sub, k, s, base, ans, d, ex, tr, gl=None, **extra):
    item = {"part": part, "sub": sub, "k": k, "s": s, "base": base, "a": ans, "d": d,
            "ex": ex, "translation": tr, "glosses": gl or []}
    item.update(extra)
    return item

R1A, R1B, R1C, R1D = "A", "B", "C", "D"
R1SA = "A · Lesson 1: gender and где?"
R1SB = "B · Lesson 2: accusative and куда?"
R1SC = "C · Lesson 3: present tense"
R1SD = "D · Lesson 4: у меня есть / нет"

EX_R1_A = [
 r1(R1A, R1SA, "gender", "компьютер — ___", "computer", "masculine", ["feminine", "neuter", "plural"],
    "It ends in a consonant (р), so it's masculine: он. (Step 1)", "", choiceOnly=True),
 r1(R1A, R1SA, "where", "Жена сейчас на ___.", "кухня", "кухне", ["кухню", "кухня", "кухни"],
    "где? takes the prepositional: -я → -е. кухня → на кухне. (Step 1)", "My wife is in the kitchen now."),
 r1(R1A, R1SA, "gender", "письмо — ___", "letter", "neuter", ["masculine", "feminine", "plural"],
    "It ends in -о, so it's neuter: оно. (Step 1)", "", choiceOnly=True),
 r1(R1A, R1SA, "where", "Друг живёт в ___.", "Брест", "Бресте", ["Брест", "Бреста", "Бресту"],
    "где? in a city: a consonant adds -е. Брест → в Бресте. (Step 1)", "My friend lives in Brest.", ["живёт: lives"]),
 r1(R1A, R1SA, "where", "Коровы сейчас на ___.", "пастбище", "пастбище", ["пастбища", "пастбищу", "пастбищи"],
    "Neuter -е often stays -е in the prepositional: на пастбище. Same word, new job in the sentence. (Step 1)", "The cows are in the pasture now."),
 r1(R1A, R1SA, "gender", "песня — ___", "song", "feminine", ["masculine", "neuter", "plural"],
    "It ends in -я, so it's feminine: она. (Step 1)", "", choiceOnly=True),
 r1(R1A, R1SA, "where", "Бык сейчас в ___.", "коровник", "коровнике", ["коровник", "коровника", "коровнику"],
    "где? a masculine consonant adds -е. коровник → в коровнике. (Step 1)", "The bull is in the cow barn now.", ["коровник: cow barn"]),
 r1(R1A, R1SA, "where", "Сегодня я в ___.", "офис", "офисе", ["офис", "офиса", "офису"],
    "где? at the office: в + prepositional, офис → офисе. (Step 1)", "I'm in the office today.", ["офис: office"]),
 r1(R1A, R1SA, "gender", "лошадь — ___", "horse", "feminine", ["masculine", "neuter", "plural"],
    "лошадь ends in -ь after д, so it is feminine, like площадь. (Step 1)", "", choiceOnly=True),
 r1(R1A, R1SA, "ven", "Мы уже ___.", "концерт · в or на?", "на концерте", ["в концерте", "на концерт", "в концерт"],
    "Events take на. We're already there (где?), so prepositional: на концерте, not на концерт. (Steps 1 and 2)", "We're already at the concert."),
]

EX_R1_B = [
 r1(R1B, R1SB, "acc", "Я пишу ___.", "программа", "программу", ["программа", "программы", "программе"],
    "программа is the direct object. Feminine -а → -у in the accusative: программу. (Step 2)", "I'm writing a program.", ["пишу: I'm writing"]),
 r1(R1B, R1SB, "whereto", "Вечером я иду ___.", "кухня · куда?", "на кухню", ["на кухне", "в кухню", "в кухне"],
    "куда? going there: the same на as на кухне, but accusative кухню. (Step 2)", "In the evening I go to the kitchen."),
 r1(R1B, R1SB, "acc", "Я открываю ___.", "файл", "файл", ["файла", "файлу", "файле"],
    "файл is masculine and a thing, so the accusative is unchanged. (Step 2)", "I'm opening a file.", ["открываю: I open"]),
 r1(R1B, R1SB, "whereto", "Летом я еду ___.", "Брест · куда?", "в Брест", ["в Бресте", "на Брест", "в Бреста"],
    "куда? to a city: в + accusative. Masculine place names don't change: в Брест. Compare в Бресте (где?). (Step 2)", "In the summer I'm going to Brest."),
 r1(R1B, R1SB, "whereto", "После работы я еду ___.", "ферма · куда?", "на ферму", ["на ферме", "в ферму", "в ферме"],
    "ферма takes на (like работа, почта). куда? → accusative: на ферму. (Step 2)", "After work I drive to the farm."),
 r1(R1B, R1SB, "acc", "Вечером мы слушаем ___.", "песня", "песню", ["песня", "песни", "песне"],
    "песня is the direct object. Feminine -я → -ю: песню. (Step 2)", "In the evening we listen to a song."),
 r1(R1B, R1SB, "whereto", "Я иду ___.", "коровник · куда?", "в коровник", ["в коровнике", "на коровник", "в коровника"],
    "куда? into the barn: в + accusative. коровник is a masculine thing, so no ending change. (Step 2)", "I'm going into the cow barn.", ["коровник: cow barn"]),
 r1(R1B, R1SB, "whereto", "Утром я еду ___.", "офис · куда?", "в офис", ["в офисе", "на офис", "в офиса"],
    "куда? to the office: в + accusative, unchanged. Compare сегодня я в офисе (где?). (Step 2)", "In the morning I drive to the office."),
 r1(R1B, R1SB, "acc", "Я покупаю ___ для коров.", "корм", "корм", ["корма", "корму", "корме"],
    "корм is a masculine thing (feed), so the accusative doesn't change. (Step 2)", "I'm buying feed for the cows.", ["корм: feed (for animals)"]),
 r1(R1B, R1SB, "whereto", "Завтра мы идём ___.", "концерт · куда?", "на концерт", ["на концерте", "в концерт", "в концерте"],
    "куда? to an event: на + accusative. на концерт, not на концерте (that's где?). (Step 2)", "Tomorrow we're going to a concert."),
]

EX_R1_C = [
 r1(R1C, R1SC, "verb", "Дома я ___ код.", "писать", "пишу", ["писаю", "пишую", "пишаю"],
    "писать is 1st conjugation and changes its stem: я пишу, ты пишешь. (Step 3)", "At home I write code.", ["код: code"], p="1s"),
 r1(R1C, R1SC, "verb", "Что ты ___ после литургии?", "делать", "делаешь", ["делаешьь", "делишь", "делают"],
    "делать is 1st conjugation: ты делаешь. (Step 3)", "What do you do after the Liturgy?", ["литургия: the Liturgy"], p="2s"),
 r1(R1C, R1SC, "verb", "Коллега ___ в Минске.", "работать", "работает", ["работаит", "работаешь", "работают"],
    "A noun subject is 3rd person singular. работать is 1st conjugation: он работает. (Step 3)", "My colleague works in Minsk.", ["коллега: colleague"], p="3s"),
 r1(R1C, R1SC, "verb", "Они ___ в Витебске.", "жить", "живут", ["жиют", "жилают", "живёт"],
    "жить is 1st conjugation with a stem change: они живут. (Step 3)", "They live in Vitebsk.", p="3p"),
 r1(R1C, R1SC, "verb", "По утрам я ___ на ферме.", "работать", "работаю", ["работам", "работаешь", "работа"],
    "я takes the -ю / -у form: я работаю. (Step 3)", "In the mornings I work on the farm.", p="1s"),
 r1(R1C, R1SC, "verb", "Ты ___ Молчат Дома?", "слушать", "слушаешь", ["слушаишь", "слушаешьь", "слушаете"],
    "слушать is 1st conjugation: ты слушаешь. The band name Молчат Дома doesn't decline. (Step 3)", "Do you listen to Molchat Doma?", ["Молчат Дома: a Belarusian band"], p="2s"),
 r1(R1C, R1SC, "verb", "Вы ___ в храм пешком?", "идти", "идёте", ["идётеь", "ходите", "идёшь"],
    "идти is the one-direction “going on foot”: вы идёте. (ходить is the habitual verb: мы ходим в церковь.) (Step 3)", "Are you walking to church?", ["пешком: on foot"], p="2p"),
 r1(R1C, R1SC, "verb", "Коллеги ___ новый сайт.", "делать", "делают", ["делаютт", "делаютъ", "делаютa"],
    "Коллеги is plural, so 3rd person plural: они делают. делать is 1st conjugation (-ют). (Step 3)", "The colleagues are making a new site.", ["сайт: website"], p="3p"),
 r1(R1C, R1SC, "verb", "Жена ___ обед.", "готовить", "готовит", ["готовет", "готовитc", "готовлю"],
    "готовить is 2nd conjugation (ты готовишь). она готовит. The я form drops л: я готовлю. (Step 3)", "My wife is making lunch.", ["обед: lunch, dinner (the midday/main meal)"], p="3s"),
 r1(R1C, R1SC, "verb", "Друг ___ мне каждый вечер.", "звонить", "звонит", ["звонет", "звонитc", "звоню"],
    "звонить is 2nd conjugation: он звонит. (мне is dative “to me” — that's Lesson 7, but you can already use the form.) (Step 3)", "My friend calls me every evening.", p="3s"),
]

# Fix C8 distractors - "делаютт" etc. are ugly. Use real wrong person forms:
# I need to fix this in a moment after thinking about L3 style distractors.

EX_R1_D = [
 r1(R1D, R1SD, "own", "У ___ есть новый компьютер.", "я", "меня", ["я", "мне", "мной"],
    "After у the owner is in the genitive: я → меня. компьютер is the subject (nominative). (Step 4)", "I have a new computer.", w="я"),
 r1(R1D, R1SD, "own", "У ___ есть подруга в Бресте.", "жена", "жены", ["жену", "жене", "жена"],
    "жена is feminine -а → genitive жены. (Step 4)", "My wife has a friend in Brest.", ["подруга: (girl)friend"], w="жена"),
 r1(R1D, R1SD, "not", "У коллеги нет ___.", "машина", "машины", ["машина", "машину", "машине"],
    "нет + genitive: машина → машины. (Step 4)", "My colleague doesn't have a car.", ["коллега: colleague"], w="машина"),
 r1(R1D, R1SD, "have", "Друг уже заказал место, потому что у него ___ на концерт.", "билет · есть or нет?", "есть билет", ["нет билета", "нет билет", "есть билету"],
    "He already booked a seat, so he has a ticket: есть + nominative. (Step 4)", "My friend already reserved a seat, because he has a ticket to the concert.", ["заказал место: reserved a seat"], w="билет"),
 r1(R1D, R1SD, "not", "У нас пока нет ___.", "индюк", "индюка", ["индюк", "индюку", "индюке"],
    "нет + genitive. индюк is masculine: add -а → индюка. (Step 4)", "We don't have a turkey yet.", ["индюк: turkey (the male bird)", "пока: yet, for now"], w="индюк"),
 r1(R1D, R1SD, "not", "В этом альбоме нет ___.", "песня", "песни", ["песня", "песню", "песне"],
    "нет + genitive. песня is feminine -я → песни. (Step 4)", "This album doesn't have that song.", ["альбом: album"], w="песня"),
 r1(R1D, R1SD, "not", "У меня нет ___ от номера.", "ключ", "ключа", ["ключ", "ключу", "ключе"],
    "нет + genitive. ключ is masculine: ключа. (Step 4)", "I don't have the key to the room.", ["номер: hotel room"], w="ключ"),
 r1(R1D, R1SD, "notc", "Я не могу открыть почту, потому что у меня ___.", "пароль", "нет пароля", ["есть пароль", "нет пароль", "нет паролю"],
    "You can't open the mail, so you don't have it: нет + genitive. пароль (masc. -ь) → пароля. (Step 4)", "I can't open my mail because I don't have the password.", ["пароль: password", "почта: mail (here: email)"], w="пароль"),
 r1(R1D, R1SD, "not", "У соседа нет ___.", "коза", "козы", ["коза", "козу", "козе"],
    "нет + genitive. коза is feminine -а → козы. (Step 4)", "The neighbor doesn't have a goat.", w="коза"),
 r1(R1D, R1SD, "notc", "Мы остаёмся дома, потому что у жены ___.", "время", "нет времени", ["есть время", "нет время", "нет времениу"],
    "You're staying home because she has no time: нет + genitive. время is irregular: времени. (Step 4)", "We're staying home because my wife doesn't have time.", ["остаёмся: we're staying"], w="время"),
]

# interleave A,B,C,D
EX_R1 = []
for i in range(10):
    EX_R1.extend([EX_R1_A[i], EX_R1_B[i], EX_R1_C[i], EX_R1_D[i]])

# Fix present-tense distractors to match Lesson 3 style (other persons + plausible misspellings).
EX_R1_C[0]["d"] = ["писаю", "пишет", "пишут"]
EX_R1_C[1]["d"] = ["делаю", "делает", "делаишь"]
EX_R1_C[2]["d"] = ["работаю", "работают", "работаит"]
EX_R1_C[3]["d"] = ["живит", "живёт", "живу"]
EX_R1_C[4]["d"] = ["работаешь", "работает", "работают"]
EX_R1_C[5]["d"] = ["слушаю", "слушает", "слушишь"]
EX_R1_C[6]["d"] = ["идёшь", "идём", "идут"]
EX_R1_C[7]["d"] = ["делаем", "делает", "делаим"]
EX_R1_C[8]["d"] = ["готовлит", "готовлю", "готовет"]
EX_R1_C[9]["d"] = ["звоню", "звонят", "звонет"]


# ---------------- Lesson 6 ----------------

SECTIONS6 = [
 {"h": "Step 1 · People and animals are “animate”", "open": True, "html":
  "<p>In Lesson 2 the <b>direct object</b> (the thing you see, know, love, feed or look for) took the <b>accusative</b> (" + ru("винительный падеж") + "). For things, that was easy: " + ru("-а / -я → -у / -ю") + ", and everything else stayed the same. When the direct object is a <b>person or an animal</b>, Russian adds one more rule.</p>"
  + "<p>Grammarians call these nouns <b>animate</b> (" + ru("одушевлённые") + "). The question word changes too:</p>"
  + t(["Question", "Asks about", "Example"], [
    [ru("что?"), "a thing (inanimate)", ru("Что ты видишь? — Храм. Код. Письмо.")],
    [ru("кого?"), "a person or animal (animate)", ru("Кого ты видишь? — Брата. Быка. Жену.")],
  ])
  + '<p class="tip"><b>German helps, with a catch:</b> German marks <i>every</i> masculine noun in the accusative: ich sehe <i>den Bruder</i>, ich sehe <i>den Tisch</i>. Russian only does the special marking when the noun is a person or animal: ' + ru("я вижу брата") + ", but " + ru("я вижу стол") + ". So the Russian “" + ru("den") + "” is reserved for <i>whom?</i>, not <i>what?</i> The pronoun is the same idea: ich sehe <i>ihn</i> = " + ru("я вижу его") + ".</p>"},
 {"h": "Step 2 · Masculine animate: accusative = genitive", "open": False, "html":
  "<p>If a masculine noun ends in a <b>consonant, " + ru("-й") + " or " + ru("-ь") + "</b> and names a person or animal, the accusative singular copies the <b>genitive</b> you already know from Lesson 4:</p>"
  + t(["Nominative (subject)", "Accusative = genitive", "In a sentence"], [
    [ru("брат") + " brother", ru("брата"), ru("Я вижу брата.")],
    [ru("друг") + " friend", ru("друга"), ru("Я встречаю друга в аэропорту.")],
    [ru("учитель") + " teacher", ru("учителя"), ru("Я знаю учителя.")],
    [ru("отец") + " father", ru("отца"), ru("Дети любят отца.")],
    [ru("Андрей"), ru("Андрея"), ru("Я знаю Андрея из Гомеля.")],
    [ru("священник") + " priest", ru("священника"), ru("Мы слушаем священника.")],
    [ru("врач") + " doctor", ru("врача"), ru("Я ищу врача.")],
    [ru("бык") + " bull", ru("быка"), ru("На лугу мы видим быка.")],
    [ru("олень") + " deer", ru("оленя"), ru("Утром у леса я вижу оленя.")],
    [ru("петух") + " rooster", ru("петуха"), ru("Жена кормит петуха.")],
    [ru("заяц") + " hare", ru("зайца"), ru("Ты видишь зайца в поле?")],
  ])
  + "<p>Inanimate masculines still follow Lesson 2 — <b>no change</b>:</p>"
  + exl([("Из окна я вижу храм.", "I see the church from the window. (a building, not a person)"),
         ("Я проверяю код.", "I'm checking the code."),
         ("Я покупаю корм.", "I'm buying feed.")])
  + '<p class="tip"><b>Memory hook:</b> for these masculines, “whom I see” looks like “of whom”: ' + ru("вижу брата") + " / " + ru("у брата") + ". Same ending, different job. " + ru("брату") + " would be the dative (Lesson 7): to the brother.</p>"},
 {"h": "Step 3 · Feminine, and men ending in -а", "open": False, "html":
  "<p>Feminine nouns in " + ru("-а / -я") + " do <b>not</b> copy the genitive. They take the same " + ru("-у / -ю") + " you already know from Lesson 2, whether the noun is a person, an animal, or a thing:</p>"
  + t(["Nominative", "Accusative", "Not the genitive"], [
    [ru("жена") + " wife", ru("жену"), ru("жены") + " is genitive: " + ru("у жены")],
    [ru("сестра") + " sister", ru("сестру"), ru("сестры")],
    [ru("мама") + " mom", ru("маму"), ru("мамы")],
    [ru("девушка") + " young woman", ru("девушку"), ru("девушки")],
    [ru("корова") + " cow", ru("корову"), ru("коровы")],
    [ru("курица") + " hen", ru("курицу"), ru("курицы")],
    [ru("собака") + " dog", ru("собаку"), ru("собаки")],
    [ru("песня") + " song (a thing)", ru("песню"), "same ending, because of " + ru("-я") + ", not because it's animate"],
  ])
  + "<p>And the masculine names in " + ru("-а / -я") + " from Lesson 1 — " + ru("папа, дедушка, батюшка, мужчина, коллега") + " — follow the <b>last letter</b>, not “masculine = genitive”:</p>"
  + exl([("На службе я вижу батюшку.", "At the service I see Father. (not “батюшки” — that's genitive: у батюшки)"),
         ("Дети любят дедушку.", "The children love Grandpa."),
         ("Я встречаю коллегу в офисе.", "I meet my colleague at the office.")])
  + '<p class="tip"><b>Don\'t overgeneralize.</b> “Animate accusative = genitive” is a <b>masculine-consonant</b> rule, plus all animates in the plural (Step 5). It is not a rule for ' + ru("жена") + " or " + ru("батюшка") + ".</p>"},
 {"h": "Step 4 · Feminine -ь: no change in the singular", "open": False, "html":
  "<p>A handful of feminine animate nouns end in " + ru("-ь") + ". In the <b>singular</b> their accusative is the same as the nominative — even though they are people or animals:</p>"
  + t(["Nominative = accusative", "Genitive (for comparison)", "Example"], [
    [ru("лошадь") + " horse", ru("лошади"), ru("В поле я вижу лошадь.")],
    [ru("дочь") + " daughter", ru("дочери"), ru("Я люблю дочь.")],
    [ru("мать") + " mother", ru("матери"), ru("Дети любят мать.")],
    [ru("мышь") + " mouse", ru("мыши"), ru("Кошка видит мышь.")],
  ])
  + "<p>In the <b>plural</b> they behave like other animates: accusative = genitive: " + ru("вижу лошадей, дочерей, матерей, мышей") + ".</p>"
  + '<p class="tip">You already know this pattern from things in ' + ru("-ь") + ": " + ru("я вижу церковь, я вижу площадь") + ". The new fact is that " + ru("лошадь") + " and " + ru("дочь") + " work the same way in the singular, even though you would ask " + ru("кого?") + ", not " + ru("что?") + ".</p>"},
 {"h": "Step 5 · Animate plurals: accusative = genitive", "open": False, "html":
  "<p>In the plural the animate rule is broader: <b>all</b> animate nouns (masculine, feminine, and the " + ru("-а") + " men) take accusative = genitive. Inanimate plurals keep accusative = nominative.</p>"
  + t(["Nominative plural", "Accusative plural", "Animate?"], [
    [ru("братья") + " brothers", ru("братьев"), "yes: " + ru("Я знаю братьев.")],
    [ru("друзья") + " friends", ru("друзей"), "yes"],
    [ru("девушки") + " young women", ru("девушек"), "yes: " + ru("Я вижу девушек.")],
    [ru("коровы") + " cows", ru("коров"), "yes: " + ru("Мы пасём коров.")],
    [ru("олени") + " deer", ru("оленей"), "yes: " + ru("Зимой мы видим оленей.")],
    [ru("батюшки") + " priests (Fathers)", ru("батюшек"), "yes"],
    [ru("храмы") + " churches", ru("храмы"), "no: same as nominative"],
    [ru("письма") + " letters", ru("письма"), "no"],
    [ru("файлы") + " files", ru("файлы"), "no"],
    [ru("песни") + " songs", ru("песни"), "no"],
  ])
  + '<p class="tip"><b>A useful pair:</b> ' + ru("я вижу коровы") + " is always wrong. " + ru("коровы") + " is nominative plural (the cows are the subject: " + ru("коровы на пастбище") + "). As a direct object you need " + ru("коров") + ". You'll meet that genitive-plural form again after numbers: " + ru("пять коров") + " (Numbers section).</p>"},
 {"h": "Step 6 · The pronouns: меня, тебя, его, её, нас, вас, их", "open": False, "html":
  "<p>The personal pronouns have their own accusative forms. They are the same as the genitive forms you learned after " + ru("у") + " in Lesson 4, <b>except</b> that without a preposition there is no " + ru("н-") + ":</p>"
  + t(["Nominative", "Accusative (direct object)", "After a preposition (for comparison)", "German"], [
    [ru("я"), ru("меня"), ru("у меня") + " · " + ru("для меня"), "mich"],
    [ru("ты"), ru("тебя"), ru("у тебя"), "dich"],
    [ru("он / оно"), ru("его"), ru("у него") + ", " + ru("для него"), "ihn / es"],
    [ru("она"), ru("её"), ru("у неё") + ", " + ru("для неё"), "sie (her)"],
    [ru("мы"), ru("нас"), ru("у нас"), "uns"],
    [ru("вы"), ru("вас"), ru("у вас"), "euch / Sie"],
    [ru("они"), ru("их"), ru("у них") + ", " + ru("для них"), "sie (them)"],
  ])
  + exl([("Ты видишь меня?", "Do you see me?"),
         ("Да, я знаю тебя.", "Yes, I know you."),
         ("Жена ищет его.", "My wife is looking for him. (его, not него — no preposition)"),
         ("Мы очень любим её.", "We love her very much."),
         ("Батюшка знает нас.", "Father knows us."),
         ("Смотри, я вижу их на пастбище.", "Look, I see them in the pasture.")])
  + '<p class="tip"><b>German:</b> Wen siehst du? — Ich sehe <i>ihn</i> / <i>sie</i> / <i>uns</i>. Russian: ' + ru("Кого ты видишь? — Я вижу его / её / нас") + ". The " + ru("н-") + " only appears after a preposition, the same rule as " + ru("у него") + " in Lesson 4.</p>"},
 {"h": "Summary", "open": False, "html":
  '<ul class="sum">'
  + "<li>The accusative still marks the <b>direct object</b>. Ask " + ru("что?") + " for things, " + ru("кого?") + " for people and animals.</li>"
  + "<li>Masculine animate (consonant / " + ru("-й") + " / " + ru("-ь") + "): accusative = genitive. " + ru("вижу брата, быка, учителя, оленя") + ". Inanimate: no change (" + ru("вижу храм, проверяю код") + ").</li>"
  + "<li>Feminine " + ru("-а / -я") + " and men in " + ru("-а") + ": always " + ru("-у / -ю") + ". " + ru("вижу жену, корову, батюшку") + " — not the genitive.</li>"
  + "<li>Feminine " + ru("-ь") + " in the singular: no change. " + ru("вижу лошадь, люблю дочь") + ".</li>"
  + "<li>All animate plurals: accusative = genitive. " + ru("вижу братьев, коров, девушек") + ". Inanimate plurals stay nominative: " + ru("вижу храмы, письма") + ".</li>"
  + "<li>Pronouns: " + ru("меня, тебя, его, её, нас, вас, их") + ". No " + ru("н-") + " without a preposition.</li>"
  + "</ul>"},
]

def l6(part, sub, k, s, w, ans, d, ex, tr, gl=None, **extra):
    item = {"part": part, "sub": sub, "k": k, "w": w, "s": s, "base": w, "a": ans, "d": d,
            "ex": ex, "translation": tr, "glosses": gl or []}
    item.update(extra)
    return item

EX6 = [
 # Part A · masculine animate singular (and inanimate contrast)
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "В аэропорту я встречаю ___.", "друг", "друга", ["друг", "другу", "другом"],
    "друг is masculine and a person, so accusative = genitive: друга. (Steps 1 and 2)",
    "At the airport I meet my friend.", ["встречаю: I meet"]),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "Я хорошо знаю ___.", "учитель", "учителя", ["учитель", "учителю", "учителем"],
    "учитель is masculine animate ending in -ь: accusative = genitive, учителя. (Step 2)",
    "I know the teacher well."),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "На лугу мы видим ___.", "бык", "быка", ["бык", "быку", "быке"],
    "бык is a masculine animal: accusative = genitive, быка. (Step 2)",
    "We see the bull in the meadow.", ["луг: meadow"]),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "Утром у леса я вижу ___.", "олень", "оленя", ["олень", "оленю", "олене"],
    "олень is masculine animate ending in -ь: олень → оленя. (Step 2)",
    "In the morning I see a deer by the woods."),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "Жена кормит ___.", "петух", "петуха", ["петух", "петуху", "петухе"],
    "петух is a masculine animal: accusative = genitive, петуха. (Step 2)",
    "My wife is feeding the rooster.", ["петух: rooster", "кормит: is feeding"]),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "Ты видишь ___ в поле?", "заяц", "зайца", ["заяц", "зайцу", "зайце"],
    "заяц is masculine animate, and the я drops: заяц → зайца. (Step 2)",
    "Do you see a hare in the field?", ["заяц: hare, wild rabbit"]),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "Я ищу ___.", "врач", "врача", ["врач", "врачу", "враче"],
    "врач is masculine animate: врача. Don't use врачу — that's the dative (to the doctor). (Step 2)",
    "I'm looking for the doctor.", ["ищу: I'm looking for"]),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "Дети любят ___.", "отец", "отца", ["отец", "отцу", "отцом"],
    "отец is masculine animate; the е drops: отец → отца. (Step 2)",
    "The children love their father."),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "Я знаю ___ из Гомеля.", "Андрей", "Андрея", ["Андрей", "Андрею", "Андреем"],
    "Андрей ends in -й, masculine animate: Андрея. Same ending as у Андрея in Lesson 4, different job. (Step 2)",
    "I know Andrey from Gomel."),
 l6("A", "A · masculine animate (and a few things)", "anim_m",
    "Мы слушаем ___.", "священник", "священника", ["священник", "священнику", "священнике"],
    "священник is masculine animate: священника. (Step 2)",
    "We're listening to the priest.", ["священник: priest"]),
 l6("A", "A · masculine animate (and a few things)", "inan_m",
    "Из окна я вижу ___.", "храм", "храм", ["храма", "храму", "храме"],
    "храм is a building, not a person, so the accusative stays храм. (Steps 1 and 2)",
    "I see the church from the window."),
 l6("A", "A · masculine animate (and a few things)", "inan_m",
    "Я проверяю ___.", "код", "код", ["кода", "коду", "коде"],
    "код is an inanimate thing: accusative = nominative, код. (Step 2)",
    "I'm checking the code.", ["проверяю: I check, I'm checking"]),

 # Part B · feminine, -а masculines, feminine -ь
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "fem",
    "Вечером я встречаю ___.", "жена", "жену", ["жена", "жены", "жене"],
    "жена is feminine -а → -у: жену. жены is the genitive (у жены), not the accusative. (Step 3)",
    "In the evening I meet my wife."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "fem",
    "Я очень люблю ___.", "сестра", "сестру", ["сестра", "сестры", "сестре"],
    "сестра is feminine -а → -у: сестру, not genitive сестры. (Step 3)",
    "I love my sister very much."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "fem",
    "Утром мы кормим ___.", "корова", "корову", ["корова", "коровы", "корове"],
    "корова is feminine, so -а → -у: корову. Don't use коровы (nominative/genitive) here. (Step 3)",
    "In the morning we feed the cow."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "masc_a",
    "На службе я вижу ___.", "батюшка", "батюшку", ["батюшка", "батюшки", "батюшке"],
    "батюшка is masculine, but it ends in -а, so accusative батюшку — like a feminine -а noun, not genitive батюшки. (Step 3)",
    "At the service I see Father."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "masc_a",
    "Дети любят ___.", "дедушка", "дедушку", ["дедушка", "дедушки", "дедушке"],
    "дедушка ends in -а: accusative дедушку. (Step 3)",
    "The children love Grandpa."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "fem",
    "Я знаю ___ в Минске.", "девушка", "девушку", ["девушка", "девушки", "девушке"],
    "девушка is feminine -а → -у: девушку. After ш write у, not ю. (Step 3)",
    "I know a young woman in Minsk.", ["девушка: young woman, girl"]),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "fem",
    "Жена кормит ___.", "курица", "курицу", ["курица", "курицы", "курице"],
    "курица is feminine -а → -у: курицу. (Step 3)",
    "My wife is feeding the hen."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "fem",
    "Во дворе я вижу ___.", "собака", "собаку", ["собака", "собаки", "собаке"],
    "собака is feminine -а → -у: собаку. After к write у. (Step 3)",
    "I see a dog in the yard.", ["двор: yard, courtyard"]),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "soft_f",
    "В поле я вижу ___.", "лошадь", "лошадь", ["лошади", "лошадю", "лошадя"],
    "лошадь is feminine -ь: in the singular the accusative stays лошадь, even though it's an animal. (Step 4)",
    "I see a horse in the field."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "soft_f",
    "Я люблю ___.", "дочь", "дочь", ["дочери", "дочю", "дочу"],
    "дочь is feminine -ь: accusative singular = nominative, дочь. дочери is genitive/dative. (Step 4)",
    "I love my daughter."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "fem",
    "Батюшка знает ___.", "мама", "маму", ["мама", "мамы", "маме"],
    "мама is feminine -а → -у: маму. (Step 3)",
    "Father knows my mom."),
 l6("B", "B · feminine, men in -а, and лошадь / дочь", "fem",
    "Мы слушаем ___.", "песня", "песню", ["песня", "песни", "песне"],
    "песня is a thing, but it still takes -я → -ю because of the ending, not because it's animate: песню. (Step 3)",
    "We're listening to a song."),

 # Part C · plurals and pronouns
 l6("C", "C · plurals and pronouns", "anim_pl",
    "Я хорошо знаю ___.", "брат", "братьев", ["братья", "братьям", "братов"],
    "Animate plural: accusative = genitive. братья → братьев. (Step 5)",
    "I know the brothers well.", ["братья: brothers"], base="брат · plural"),
 l6("C", "C · plurals and pronouns", "anim_pl",
    "Утром мы пасём ___.", "корова", "коров", ["коровы", "коровам", "корову"],
    "Animate plural: коровы → коров. коровы would make the cows the subject. (Step 5)",
    "In the morning we graze the cows.", ["пасём: we graze, we herd"], base="корова · plural"),
 l6("C", "C · plurals and pronouns", "anim_pl",
    "На улице я вижу ___.", "девушка", "девушек", ["девушки", "девушкам", "девушку"],
    "Animate plural: девушки → девушек. (Step 5)",
    "I see some young women on the street.", ["девушка: young woman, girl"], base="девушка · plural"),
 l6("C", "C · plurals and pronouns", "anim_pl",
    "Зимой у леса мы видим ___.", "олень", "оленей", ["олени", "оленям", "оленя"],
    "Animate plural: олени → оленей. (Step 5)",
    "In the winter we see deer by the woods.", base="олень · plural"),
 l6("C", "C · plurals and pronouns", "inan_pl",
    "В городе я вижу ___.", "храм", "храмы", ["храмов", "храмам", "храма"],
    "храмы is inanimate plural: accusative = nominative, храмы. (Step 5)",
    "I see churches in the city.", base="храм · plural"),
 l6("C", "C · plurals and pronouns", "inan_pl",
    "Я отправляю ___ другу.", "письмо", "письма", ["писем", "письмам", "письмо"],
    "письма is inanimate plural: accusative = nominative, письма. (The friend is dative другу — Lesson 7.) (Step 5)",
    "I'm sending letters to my friend.", ["отправляю: I send"], base="письмо · plural"),
 l6("C", "C · plurals and pronouns", "pron",
    "Скажи, ты видишь ___?", "я", "меня", ["я", "мне", "мной"],
    "я as a direct object is меня. (Step 6)",
    "Tell me, do you see me?", ["скажи: tell me"]),
 l6("C", "C · plurals and pronouns", "pron",
    "Да, я знаю ___.", "ты", "тебя", ["ты", "тебе", "тобой"],
    "ты as a direct object is тебя. (Step 6)",
    "Yes, I know you."),
 l6("C", "C · plurals and pronouns", "pron",
    "Жена ищет ___.", "он", "его", ["он", "ему", "него"],
    "он as a direct object is его. Not него — there's no preposition here. (Step 6)",
    "My wife is looking for him.", ["ищет: is looking for"]),
 l6("C", "C · plurals and pronouns", "pron",
    "Мы очень любим ___.", "она", "её", ["она", "ей", "неё"],
    "она as a direct object is её. Not неё, because there's no preposition. (Step 6)",
    "We love her very much."),
 l6("C", "C · plurals and pronouns", "pron",
    "Смотри, я вижу ___ на пастбище.", "они", "их", ["они", "им", "них"],
    "они as a direct object is их. Not них — no preposition. (Step 6)",
    "Look, I see them in the pasture.", ["смотри: look"]),
]


# ---------------- Lesson 7 ----------------

SECTIONS7 = [
 {"h": "Step 1 · The dative is the indirect object", "open": True, "html":
  "<p>The <b>dative</b> (" + ru("дательный падеж") + ") marks the <b>indirect object</b>: <b>to whom</b> or <b>for whom</b> something is given, said, sent or done. The question is " + ru("кому?") + ".</p>"
  + "<p>A sentence you already almost had — and one worth getting right — is:</p>"
  + exl([("Я дал воду коровам.", "I gave water to the cows.")])
  + "<p>Diagram it and every word has a clear job:</p>"
  + t(["Word", "Job in the sentence", "Case"], [
    [ru("я"), "<b>subject</b> — who did it", "nominative"],
    [ru("дал"), "verb (past tense, masculine: Lesson 5)", "—"],
    [ru("воду"), "<b>direct object</b> — what was given", "accusative (Lesson 2)"],
    [ru("коровам"), "<b>indirect object</b> — who received it", "dative"],
  ])
  + '<p class="tip"><b>A real mistake to watch:</b> ' + ru("Я дал воду коров") + " uses " + ru("коров") + ", which is the accusative/genitive plural (the cows as a direct object: " + ru("вижу коров") + "). Here the cows are receiving the water, so they need the dative plural: " + ru("коровам") + ".</p>"
  + '<p class="tip"><b>German:</b> this is <i>der Dativ</i>, the same job as <i>dem / der / den</i> and <i>mir, dir, ihm</i>. ich gebe dem Bruder das Buch = ' + ru("я даю брату книгу") + ". ich gab den Kühen Wasser = " + ru("я дал воду коровам") + ".</p>"},
 {"h": "Step 2 · The singular endings", "open": False, "html":
  "<p>In the singular there are only a few endings, and the dictionary form tells you which:</p>"
  + t(["Dictionary form", "Dative singular", "Examples"], [
    ["masc. consonant / neut. " + ru("-о"), ru("-у"), ru("друг → другу") + " · " + ru("бык → быку") + " · " + ru("врач → врачу") + " · " + ru("окно → окну")],
    ["masc. " + ru("-й / -ь") + ", neut. " + ru("-е"), ru("-ю"), ru("Андрей → Андрею") + " · " + ru("учитель → учителю") + " · " + ru("олень → оленю") + " · " + ru("поле → полю")],
    ["fem. " + ru("-а"), ru("-е"), ru("жена → жене") + " · " + ru("сестра → сестре") + " · " + ru("корова → корове")],
    ["fem. " + ru("-я") + " / " + ru("-ь"), ru("-и"), ru("песня → песне") + " is " + ru("-я → -е") + "; but " + ru("-ия → -ии") + " (" + ru("Мария → Марии") + "), and " + ru("-ь → -и") + ": " + ru("лошадь → лошади") + ", " + ru("дочь → дочери") + ", " + ru("церковь → церкви")],
    ["masc. " + ru("-а / -я"), ru("-е") + " (like feminine)", ru("батюшка → батюшке") + " · " + ru("папа → папе") + " · " + ru("дедушка → дедушке") + " · " + ru("коллега → коллеге")],
  ])
  + "<p>After " + ru("г, к, х, ж, ч, ш, щ") + " the vowel is still the dative one, with the usual spelling: " + ru("подруга → подруге") + ", " + ru("девушка → девушке") + ".</p>"
  + '<p class="tip">Same idea as Lesson 6: the <b>ending</b> follows the last letter, the <b>agreement</b> follows the person. ' + ru("батюшке") + " looks like " + ru("жене") + ", but " + ru("батюшка дал") + " stays masculine.</p>"},
 {"h": "Step 3 · The plural, and two irregulars", "open": False, "html":
  "<p>The dative plural is regular for almost every noun: " + ru("-ам") + " after a hard stem, " + ru("-ям") + " after a soft one.</p>"
  + t(["Nominative plural", "Dative plural", "Example"], [
    [ru("коровы"), ru("коровам"), ru("Я дал воду коровам.")],
    [ru("куры / курицы"), ru("курицам"), ru("Я даю зерно курицам.")],
    [ru("друзья"), ru("друзьям"), ru("Я пишу письма друзьям.")],
    [ru("братья"), ru("братьям"), ru("Я звоню братьям.")],
    [ru("жены"), ru("жёнам"), ru("Батюшка говорит жёнам и мужьям.")],
    [ru("коллеги"), ru("коллегам"), ru("Я отправил файл коллегам.")],
  ])
  + "<p>Two very common words are irregular. Learn them as a pair:</p>"
  + t(["Nominative", "Dative"], [
    [ru("дети") + " children (sg. " + ru("ребёнок") + ")", ru("детям")],
    [ru("люди") + " people (sg. " + ru("человек") + ")", ru("людям")],
  ])
  + exl([("Мама читает книгу детям.", "Mom is reading a book to the children."),
         ("Батюшка говорит людям.", "Father is speaking to the people.")])
  + '<p class="tip">If you remember only two plural datives this week, make them ' + ru("коровам") + " and " + ru("детям") + " / " + ru("людям") + ".</p>"
  + "<p>One more preposition takes the dative: " + ru("благодаря") + " (thanks to). " + ru("Благодаря родителям дети учатся в школе.") + " It is <b>not</b> the genitive (that would be " + ru("для родителей") + ", which you know from Lesson 9).</p>"},
 {"h": "Step 4 · The pronouns: мне, тебе, ему, ей, нам, вам, им", "open": False, "html":
  "<p>The dative pronouns are new forms — they are <b>not</b> the same as the accusative/genitive " + ru("меня, тебя, его") + ".</p>"
  + t(["Nominative", "Dative (to / for whom)", "Accusative (for contrast)", "German"], [
    [ru("я"), ru("мне"), ru("меня"), "mir"],
    [ru("ты"), ru("тебе"), ru("тебя"), "dir"],
    [ru("он / оно"), ru("ему"), ru("его"), "ihm"],
    [ru("она"), ru("ей"), ru("её"), "ihr"],
    [ru("мы"), ru("нам"), ru("нас"), "uns"],
    [ru("вы"), ru("вам"), ru("вас"), "euch / Ihnen"],
    [ru("они"), ru("им"), ru("их"), "ihnen"],
  ])
  + exl([("Друг звонит мне каждый вечер.", "My friend calls me every evening."),
         ("Я пишу тебе письмо.", "I'm writing you a letter."),
         ("Жена даёт ему ключ.", "My wife gives him the key.")])
  + "<p>After a preposition, " + ru("ему / ей / им") + " add " + ru("н-") + ", the same rule as Lesson 4:</p>"
  + exl([("Я иду к нему.", "I'm going to him. (к + dative)"),
         ("Мы идём к ней.", "We're going to her."),
         ("Я иду к ним.", "I'm going to them.")])
  + '<p class="tip"><b>Don\'t mix the cases:</b> ' + ru("вижу его") + " (direct object, accusative) vs " + ru("звоню ему") + " (to him, dative) vs " + ru("иду к нему") + " (to him, preposition + dative with " + ru("н-") + ").</p>"},
 {"h": "Step 5 · мне нравится, нужно / надо, мне холодно", "open": False, "html":
  "<p>A group of very common expressions puts the person in the <b>dative</b> and makes the thing the <b>subject</b>.</p>"
  + "<h4>" + ru("нравиться") + " — to be pleasing (to like)</h4>"
  + "<p>" + ru("мне нравится") + " is built like German <i>das gefällt mir</i>: “it is pleasing to me.” The thing you like is the subject, so the verb agrees with <b>that thing</b>, not with “me”:</p>"
  + exl([("Мне нравится эта песня.", "I like this song. (песня is singular → нравится)"),
         ("Мне нравятся коровы.", "I like the cows. (коровы is plural → нравятся)"),
         ("Тебе нравится Молчат Дома?", "Do you like Molchat Doma?"),
         ("Ей нравится Беларусь.", "She likes Belarus."),
         ("Жене нравится этот альбом.", "My wife likes this album."),
         ("Детям нравятся блины.", "The children like pancakes.")])
  + "<h4>" + ru("нужно / надо") + " — need to / have to, and " + ru("мне холодно") + "</h4>"
  + exl([("Мне нужно ехать в Минск.", "I need to go to Minsk."),
         ("Нам надо позвонить домой.", "We need to call home."),
         ("Что вам нужно?", "What do you need?"),
         ("Зимой нам холодно на улице.", "In winter we're cold outside. (literally: it is cold to us)"),
         ("Сегодня мне можно не работать.", "I don't have to work today. (можно + dative: it's allowed to me)")])
  + '<p class="tip"><b>German:</b> es gefällt mir, es ist mir kalt, mir ist schlecht, ich muss nach Minsk — Russian uses the dative for all of these except “I must,” which is still ' + ru("мне нужно / мне надо") + " + infinitive, not a verb that conjugates with " + ru("я") + ".</p>"},
 {"h": "Step 6 · к + dative, and по + dative", "open": False, "html":
  "<p>" + ru("к") + " + dative means <b>to a person</b> (or toward someone). Use " + ru("в / на") + " + accusative for a <b>place</b>, the way you did in Lesson 2:</p>"
  + t(["To a person (к + dative)", "To a place (в / на + accusative)"], [
    [ru("Я иду к батюшке."), ru("Я иду в храм.")],
    [ru("Мы едем к другу в Гомель."), ru("Мы едем в Гомель.")],
    [ru("Завтра я иду к врачу."), ru("Завтра я иду в больницу.")],
    [ru("Я иду к ней."), ru("Я иду к ней домой.")],
  ])
  + "<p>The same " + ru("к") + " works in the <b>plural</b> when you visit more than one person: " + ru("Мы ездили к друзьям в Минск") + ", " + ru("он ходит к врачам") + ".</p>"
  + "<p>" + ru("по") + " + dative covers several useful meanings: by means of, along, and “every / on (Saturdays)”:</p>"
  + exl([("Мы часто говорим по телефону.", "We often talk on the phone. (by telephone)"),
         ("По субботам я работаю на ферме.", "On Saturdays I work on the farm. (every Saturday)"),
         ("По воскресеньям мы идём в храм.", "On Sundays we go to church."),
         ("По дороге мы видим оленя.", "Along the road we see a deer.")])
  + '<p class="tip"><b>German:</b> ' + ru("к врачу") + " ≈ zu dem Arzt / zum Arzt. " + ru("по субботам") + " is close to <i>samstags</i> (regularly on Saturdays), not just <i>am Samstag</i> (this Saturday). " + ru("по телефону") + " is per Telefon / am Telefon.</p>"},
 {"h": "Step 7 · Age: мне сорок лет", "open": False, "html":
  "<p>To say how old someone is, Russian uses the <b>dative</b> + the number + the word for “year.” Literally: “to me are forty years.”</p>"
  + exl([("Мне сорок лет.", "I'm forty years old."),
         ("Другу тридцать два года.", "My friend is thirty-two."),
         ("Детям пять лет.", "The children are five."),
         ("Сыну один год.", "My son is one year old."),
         ("Ей двадцать два года.", "She is twenty-two.")])
  + "<p>The word for “year” follows the number rule from the <b>Numbers</b> section:</p>"
  + t(["The number ends in", "Form", "Examples"], [
    ["1 (but not 11)", ru("год"), ru("один год") + ", " + ru("двадцать один год")],
    ["2, 3 or 4 (but not 12–14)", ru("года"), ru("два года") + ", " + ru("тридцать два года") + ", " + ru("четыре года")],
    ["5–20, or 5–0 at the end (0, 5, 6, 7, 8, 9)", ru("лет"), ru("пять лет") + ", " + ru("сорок лет") + ", " + ru("одиннадцать лет") + ", " + ru("двенадцать лет")],
  ])
  + '<p class="tip"><b>German:</b> ich bin vierzig Jahre alt puts “I” in the nominative. Russian never says “я сорок лет.” It is always ' + ru("мне сорок лет") + ". If you want practice with the numbers themselves, use the Numbers tab, then come back and say your age and your family's ages in the dative.</p>"},
 {"h": "Summary", "open": False, "html":
  '<ul class="sum">'
  + "<li>The dative marks the <b>indirect object</b> (" + ru("кому?") + "): " + ru("Я дал воду коровам") + ", not " + ru("коров") + ".</li>"
  + "<li>Singular: masc./neut. " + ru("-у / -ю") + " (" + ru("другу, учителю, быку") + "); fem. " + ru("-е / -и") + " (" + ru("жене, лошади") + "); men in " + ru("-а") + " take " + ru("-е") + " (" + ru("батюшке, коллеге") + ").</li>"
  + "<li>Plural: " + ru("-ам / -ям") + ". Irregular: " + ru("детям, людям") + ".</li>"
  + "<li>Pronouns: " + ru("мне, тебе, ему, ей, нам, вам, им") + ". After a preposition: " + ru("к нему, к ней, к ним") + ".</li>"
  + "<li>" + ru("мне нравится / нравятся") + " (the thing is the subject); " + ru("нужно / надо") + "; " + ru("мне холодно") + ".</li>"
  + "<li>" + ru("к") + " + dative = to a person (also in the plural: " + ru("к друзьям, к врачам") + "); " + ru("по") + " + dative = by / along / every (Saturday). " + ru("благодаря") + " + dative = thanks to (" + ru("благодаря родителям") + "). Age: " + ru("мне сорок лет") + " (1 " + ru("год") + ", 2–4 " + ru("года") + ", 5+ " + ru("лет") + ").</li>"
  + "</ul>"},
]

def l7(part, sub, k, s, w, ans, d, ex, tr, gl=None, **extra):
    item = {"part": part, "sub": sub, "k": k, "w": w, "s": s, "base": extra.pop("base", w), "a": ans, "d": d,
            "ex": ex, "translation": tr, "glosses": gl or []}
    item.update(extra)
    return item

EX7 = [
 # Part A · noun endings, including the cow error
 l7("A", "A · the indirect object (noun endings)", "dat_pl",
    "Я дал воду ___.", "корова", "коровам", ["коров", "коровы", "корове"],
    "The cows are receiving the water (indirect object), so dative plural: коровам. коров is accusative/genitive plural (вижу коров). (Steps 1 and 3)",
    "I gave water to the cows.", base="корова · plural"),
 l7("A", "A · the indirect object (noun endings)", "dat_sg",
    "Я пишу письмо ___.", "друг", "другу", ["друга", "друг", "другом"],
    "The friend is the indirect object: masculine consonant adds -у, другу. друга would be genitive/accusative. (Step 2)",
    "I'm writing a letter to my friend."),
 l7("A", "A · the indirect object (noun endings)", "dat_sg",
    "Жена звонит ___.", "сестра", "сестре", ["сестру", "сестры", "сестра"],
    "звонить takes the dative (to whom you call). сестра → сестре. (Step 2)",
    "My wife is calling her sister."),
 l7("A", "A · the indirect object (noun endings)", "dat_sg",
    "Мы помогаем ___.", "батюшка", "батюшке", ["батюшку", "батюшки", "батюшка"],
    "помогать takes the dative. батюшка ends in -а, so батюшке (like жене). (Step 2)",
    "We help Father.", ["помогаем: we help"]),
 l7("A", "A · the indirect object (noun endings)", "dat_sg",
    "Я даю сено ___.", "бык", "быку", ["быка", "бык", "быке"],
    "The bull is receiving the hay: dative быку. быка is genitive/accusative (вижу быка). (Step 2)",
    "I give hay to the bull."),
 l7("A", "A · the indirect object (noun endings)", "dat_pl",
    "Мама читает книгу ___.", "дети", "детям", ["детей", "дети", "ребёнку"],
    "дети has an irregular dative: детям. детей would be genitive/accusative plural. (Step 3)",
    "Mom is reading a book to the children.", base="дети"),
 l7("A", "A · the indirect object (noun endings)", "dat_sg",
    "Я отправил файл ___.", "коллега", "коллеге", ["коллегу", "коллеги", "коллега"],
    "коллега ends in -а (a person): dative коллеге. (Step 2)",
    "I sent a file to my colleague.", ["отправил: I sent (perf.)", "коллега: colleague"]),
 l7("A", "A · the indirect object (noun endings)", "dat_sg",
    "Я дарю икону ___.", "жена", "жене", ["жену", "жены", "жена"],
    "The wife is receiving the icon: dative жене. жену is the accusative (вижу жену). (Step 2)",
    "I'm giving my wife an icon as a gift.", ["дарю: I give as a gift", "икона: icon"]),
 l7("A", "A · the indirect object (noun endings)", "dat_sg",
    "Я звоню ___.", "врач", "врачу", ["врача", "врач", "враче"],
    "звонить + dative: врач → врачу. врача is the accusative (ищу врача). (Step 2)",
    "I'm calling the doctor."),
 l7("A", "A · the indirect object (noun endings)", "dat_pl",
    "Батюшка говорит ___.", "люди", "людям", ["людей", "люди", "человеку"],
    "люди has an irregular dative: людям. (Step 3)",
    "Father is speaking to the people.", base="люди"),
 l7("A", "A · the indirect object (noun endings)", "dat_sg",
    "Я купил корм ___.", "лошадь", "лошади", ["лошадь", "лошадью", "лошадя"],
    "лошадь is feminine -ь: dative лошади (the same form as the genitive). (Step 2)",
    "I bought feed for the horse."),
 l7("A", "A · the indirect object (noun endings)", "dat_pl",
    "Я даю зерно ___.", "курица", "курицам", ["курам", "куриц", "курицы"],
    "Dative plural of курица is курицам (not “курам”). (Step 3)",
    "I give grain to the hens.", ["зерно: grain"], base="курица · plural"),

 # Part B · pronouns, нравится, нужно, холодно
 l7("B", "B · pronouns, нравится, нужно, холодно", "pron",
    "___ нравится эта песня.", "я", "Мне", ["Меня", "Я", "Мной"],
    "The person who likes something is in the dative: я → мне. Capital Мне because it's the start of the sentence. (Steps 4 and 5)",
    "I like this song."),
 l7("B", "B · pronouns, нравится, нужно, холодно", "pron",
    "___ нравится Молчат Дома?", "ты", "Тебе", ["Тебя", "Ты", "Тобой"],
    "ты → тебе in the dative. The band name doesn't decline. (Steps 4 and 5)",
    "Do you like Molchat Doma?", ["Молчат Дома: a Belarusian band"]),
 l7("B", "B · pronouns, нравится, нужно, холодно", "nslike",
    "Мне ___ коровы.", "нравиться", "нравятся", ["нравится", "нравлюсь", "нравитесь"],
    "коровы is plural, so the verb is plural: нравятся. The cows are the subject; мне is dative. (Step 5)",
    "I like the cows.", g="pl"),
 l7("B", "B · pronouns, нравится, нужно, холодно", "pron",
    "___ нужно ехать в Минск.", "он", "Ему", ["Его", "Он", "Нему"],
    "он → ему in the dative. Нему would need a preposition (к нему). (Steps 4 and 5)",
    "He needs to go to Minsk."),
 l7("B", "B · pronouns, нравится, нужно, холодно", "pron",
    "На улице ___ холодно.", "мы", "нам", ["нас", "мы", "нами"],
    "мне / нам холодно: the person who feels cold is in the dative. (Step 5)",
    "We're cold outside."),
 l7("B", "B · pronouns, нравится, нужно, холодно", "pron",
    "___ нравится Беларусь.", "она", "Ей", ["Её", "Она", "Ней"],
    "она → ей in the dative. (Steps 4 and 5)",
    "She likes Belarus."),
 l7("B", "B · pronouns, нравится, нужно, холодно", "pron",
    "Что ___ нужно в магазине?", "вы", "вам", ["вас", "вы", "вами"],
    "вы → вам in the dative. (Steps 4 and 5)",
    "What do you need at the store?"),
 l7("B", "B · pronouns, нравится, нужно, холодно", "pron",
    "___ надо позвонить домой.", "мы", "Нам", ["Нас", "Мы", "Нами"],
    "надо / нужно + dative + infinitive: нам надо позвонить. (Steps 4 and 5)",
    "We need to call home.", ["надо: it is necessary, we need to"]),
 l7("B", "B · pronouns, нравится, нужно, холодно", "pron",
    "___ нравится наша ферма.", "они", "Им", ["Их", "Они", "Ним"],
    "они → им in the dative. (Steps 4 and 5)",
    "They like our farm."),
 l7("B", "B · pronouns, нравится, нужно, холодно", "nslike",
    "Жене ___ этот альбом.", "нравиться", "нравится", ["нравятся", "нравлюсь", "нравишься"],
    "альбом is singular, so нравится. Жене is already in the dative. (Step 5)",
    "My wife likes this album."),
 l7("B", "B · pronouns, нравится, нужно, холодно", "nslike",
    "Детям ___ блины.", "нравиться", "нравятся", ["нравится", "нравлюсь", "нравитесь"],
    "блины is plural, so нравятся. Детям is the irregular dative of дети. (Steps 3 and 5)",
    "The children like pancakes.", ["блины: pancakes"], g="pl"),
 l7("B", "B · pronouns, нравится, нужно, холодно", "nslike",
    "Коллеге ___ новый проект.", "нравиться", "нравится", ["нравятся", "нравлюсь", "нравишься"],
    "проект is singular → нравится. коллеге is dative (a person in -а). (Steps 2 and 5)",
    "My colleague likes the new project.", ["коллега: colleague", "проект: project"]),

 # Part C · к, по, age
 l7("C", "C · к, по, and age", "k",
    "После службы я иду к ___.", "батюшка", "батюшке", ["батюшку", "батюшки", "батюшка"],
    "к takes the dative: к батюшке. Not в батюшку and not к батюшку. (Steps 2 and 6)",
    "After the service I go to Father."),
 l7("C", "C · к, по, and age", "k",
    "Летом мы едем к ___ в Гомель.", "друг", "другу", ["друга", "друг", "другом"],
    "к + dative: к другу (to our friend). в Гомель is the place, in the accusative. (Step 6)",
    "In the summer we go to our friend in Gomel."),
 l7("C", "C · к, по, and age", "k",
    "Завтра я иду к ___.", "врач", "врачу", ["врача", "врач", "враче"],
    "к + dative: к врачу (to the doctor). (Step 6)",
    "Tomorrow I'm going to the doctor."),
 l7("C", "C · к, по, and age", "po",
    "Мы часто говорим по ___.", "телефон", "телефону", ["телефон", "телефона", "телефоне"],
    "по + dative: по телефону (by phone). (Step 6)",
    "We often talk on the phone."),
 l7("C", "C · к, по, and age", "po",
    "По ___ я работаю на ферме.", "суббота", "субботам", ["субботе", "субботу", "суббота"],
    "по + dative plural means “every / on Saturdays”: по субботам. (Step 6)",
    "On Saturdays I work on the farm.", base="суббота · plural"),
 l7("C", "C · к, по, and age", "po",
    "По ___ мы идём в храм.", "воскресенье", "воскресеньям", ["воскресенью", "воскресенье", "воскресении"],
    "по + dative plural: по воскресеньям (every Sunday). (Step 6)",
    "On Sundays we go to church.", base="воскресенье · plural"),
 l7("C", "C · к, по, and age", "age_pron",
    "___ сорок лет.", "я", "Мне", ["Я", "Меня", "Мной"],
    "Age uses the dative: мне сорок лет, never “я сорок лет.” сорок takes лет (5+ / 0 at the end). (Step 7)",
    "I'm forty years old."),
 l7("C", "C · к, по, and age", "age_unit",
    "Другу тридцать два ___.", "год", "года", ["лет", "год", "годы"],
    "32 ends in 2 (and is not 12), so года. 1 год, 2–4 года, 5+ лет. (Step 7 and the Numbers section)",
    "My friend is thirty-two.", n=32),
 l7("C", "C · к, по, and age", "age_unit",
    "Детям пять ___.", "год", "лет", ["года", "год", "годы"],
    "5 and up take лет (the genitive plural). (Step 7 and the Numbers section)",
    "The children are five.", n=5),
 l7("C", "C · к, по, and age", "age_unit",
    "Сыну один ___.", "год", "год", ["года", "лет", "годы"],
    "1 (but not 11) takes nominative год. (Step 7 and the Numbers section)",
    "My son is one year old.", n=1),
 l7("C", "C · к, по, and age", "k_pron",
    "Вечером я иду к ___.", "она", "ней", ["ей", "её", "неё"],
    "After the preposition к, ей adds н-: к ней. (Steps 4 and 6)",
    "In the evening I'm going to her place."),
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
 "R1": {
  "id": "R1", "review": True,
  "title": "Review 1",
  "goal": "Mixed practice on Lessons 1–4: gender and где?, accusative of things and куда?, the present tense, and у меня есть / нет. By the end you'll use all four in short sentences about an ordinary day.",
  "minutes": "10–15 min to read the recap, then %d exercises",
  "sections": SECTIONS_R1,
  "parts": {
    "A": "Lesson 1 · Gender and где?",
    "B": "Lesson 2 · Accusative and куда?",
    "C": "Lesson 3 · Present tense",
    "D": "Lesson 4 · у меня есть / нет",
  },
  "practice": {
    "title": "Now use it: write to your tutor",
    "text": "Answer in chat: Расскажи про обычный день. Write 4 short sentences: one with где? (where you or someone is — the prepositional), one with куда? or a direct object (the accusative of a thing), one in the present tense about what you, your wife or a friend does, and one with у меня есть or у меня нет.",
    "examples": ["Сейчас я в офисе.", "После работы я еду на ферму.", "Жена готовит обед.", "У нас пока нет козы."]
  },
  "exercises": EX_R1,
 },
 "L6": {
  "id": "L6", "n": 6,
  "title": "Accusative of people and animals: я вижу брата",
  "goal": "By the end you'll mark people and animals as direct objects: Я вижу брата. Я вижу корову. Я вижу батюшку. Мы пасём коров. Ты видишь меня?",
  "minutes": "15–20 min to read, then %d exercises",
  "sections": SECTIONS6,
  "parts": {"A": "Part A · masculine animate (and a few things)", "B": "Part B · feminine, men in -а, and лошадь / дочь", "C": "Part C · plurals and pronouns"},
  "practice": {
    "title": "Now use it: write to your tutor",
    "text": "Answer in chat: Кого ты видишь за обычный день? Write 4 sentences with a direct object: one masculine person or animal (вижу брата, быка, оленя), one feminine noun or a man in -а (жену, корову, батюшку), one animate plural (коров, друзей, девушек), and one with a pronoun (меня, его, её, их).",
    "examples": ["Утром на лугу я вижу оленя.", "На службе я вижу батюшку.", "Мы пасём коров.", "Жена ищет меня."]
  },
  "exercises": EX6,
 },
 "L7": {
  "id": "L7", "n": 7,
  "title": "The dative: кому? мне нравится",
  "goal": "By the end you'll mark the indirect object and use the main dative patterns: Я дал воду коровам. Мне нравится эта песня. Я иду к батюшке. По субботам я на ферме. Мне сорок лет.",
  "minutes": "15–20 min to read, then %d exercises",
  "sections": SECTIONS7,
  "parts": {"A": "Part A · the indirect object (noun endings)", "B": "Part B · pronouns, нравится, нужно, холодно", "C": "Part C · к, по, and age"},
  "practice": {
    "title": "Now use it: write to your tutor",
    "text": "Answer in chat: Кому ты звонишь и что тебе нравится? Write 4 sentences: one with an indirect object (дал / пишу / звоню + dative), one with нравится or нравятся, one with к or по + dative, and one with someone's age (мне / другу / сыну … лет).",
    "examples": ["Я дал воду коровам.", "Мне нравится эта песня.", "По воскресеньям мы идём к батюшке.", "Другу тридцать два года."]
  },
  "exercises": EX7,
 },
}

for _k in ("L4", "L5", "R1", "L6", "L7"): LESSONS[_k]["minutes"] = LESSONS[_k]["minutes"] % len(LESSONS[_k]["exercises"])

import lesson8
LESSONS["L8"] = lesson8.build(t, ru, exl)

import lesson9
LESSONS["L9"] = lesson9.build(t, ru, exl)

import lesson_kotoryy
LESSONS["LK"] = lesson_kotoryy.build(t, ru, exl)

import numbers_lesson
NUMBERS = numbers_lesson.build(t, ru, exl)
out = {"version": 1, "course": COURSE, "lessons": LESSONS, "numbers": NUMBERS}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "..", "lessons.json"), "w"), ensure_ascii=False, indent=1)
print("lessons.json:", len(COURSE), "roadmap entries,", sum(len(l["exercises"]) for l in LESSONS.values()), "exercises")
