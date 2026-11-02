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
 }
}

out = {"version": 1, "course": COURSE, "lessons": LESSONS}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "..", "lessons.json"), "w"), ensure_ascii=False, indent=1)
print("lessons.json:", len(COURSE), "roadmap entries,", sum(len(l["exercises"]) for l in LESSONS.values()), "exercises")
