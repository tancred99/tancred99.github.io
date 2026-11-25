# Lesson 8: the instrumental case (singular and plural), с / рядом с / между / перед,
# чем for tools, работать учителем, pronouns (со мной), and the irregulars children / people / daughters.
# Imported by lessons_src.py. Forms checked with pymorphy3 (src/verify_lessons.py, check_l8).

def build(t, ru, exl):
    def rv(inner, hint="Say each word out loud first. Then check the stress:"):
        return ('<div class="rv nostress"><div class="rvbar"><span class="rvh">%s</span>'
                '<button type="button" class="sbtn" data-rv="1" aria-pressed="false">Show stress ´</button></div>%s</div>') % (hint, inner)
    def ar(a, b): return ru(a) + " → " + ru(b)

    S = []
    S.append({"h": "Step 1 · The instrumental is “with” and “by means of”", "open": True, "html":
      "<p>The <b>instrumental</b> (" + ru("творительный падеж") + ") answers two everyday questions: " + ru("с кем?") + " — <b>with whom?</b> — and " + ru("чем?") + " — <b>with what? / by means of what?</b> A sentence you already almost had is:</p>"
      + exl([("Я пью чай с молоком.", "I drink tea with milk."),
             ("Я живу с женой.", "I live with my wife."),
             ("Жена режет хлеб ножом.", "My wife cuts the bread with a knife.")])
      + "<p>" + ru("с молоком") + " and " + ru("с женой") + " take " + ru("с") + " plus the instrumental. " + ru("ножом") + " has no preposition: the case itself means “by means of a knife.”</p>"
      + '<p class="tip"><b>German:</b> the closest match is <i>mit</i> + Dativ. <i>ich trinke Tee mit Milch</i> = ' + ru("я пью чай с молоком") + ". <i>mit wem?</i> = " + ru("с кем?") + "; <i>mit dem Bruder / mit der Frau / mit den Kindern</i> = " + ru("с братом, с женой, с детьми") + ". Russian has no article, so the <b>ending</b> does the work of dem / der / den.</p>"})

    S.append({"h": "Step 2 · The singular endings", "open": False, "html":
      "<p>In the singular the dictionary form tells you the ending, the same way it did for the dative in Lesson 7.</p>"
      + rv(t(["Dictionary form", "Instrumental singular", "Examples"], [
        ["masc. consonant / neut. " + ru("-о"), ru("-ом / -ём"), ar("друг", "другом") + " · " + ar("стол", "столом") + " · " + ar("нож", "ножом") + " · " + ar("молоко", "молоком") + " · " + ar("отец", "отцом")],
        ["masc. " + ru("-й / -ь") + ", neut. " + ru("-е"), ru("-ем / -ём"), ar("Андрей", "Андреем") + " · " + ar("учитель", "учителем") + " · " + ar("карандаш", "карандашом") + " · " + ar("поле", "полем")],
        ["fem. " + ru("-а"), ru("-ой / -ёй"), ar("жена", "женой") + " · " + ar("сестра", "сестрой") + " · " + ar("ручка", "ручкой") + " · " + ar("собака", "собакой")],
        ["fem. " + ru("-я / -ь"), ru("-ей / -ёй") + " or " + ru("-ью"), ar("семья", "семьёй") + " · " + ar("деревня", "деревней") + " · " + ru("дочь → дочерью") + " · " + ru("мать → матерью") + " · " + ru("церковь → церковью")],
        ["masc. " + ru("-а / -я") + " (like feminine)", ru("-ой / -ей"), ar("батюшка", "батюшкой") + " · " + ar("папа", "папой") + " · " + ar("коллега", "коллегой")],
      ]))
      + "<p>After ж, ч, ш, щ, ц you still use the instrumental ending, with the usual spelling: " + ru("карандаш → карандашом") + ", " + ru("ручка → ручкой") + ". Soft " + ru("-ь") + " feminines (" + ru("дочь, мать, церковь, лошадь") + ") take " + ru("-ью") + ", not " + ru("-ой") + ".</p>"
      + '<p class="tip"><b>German:</b> <i>mit dem Freund, mit der Frau, mit dem Messer</i>. The Russian endings ' + ru("-ом, -ой, -ью") + " are doing the same job as dem / der.</p>"})

    S.append({"h": "Step 3 · The plural: -ами / -ями", "open": False, "html":
      "<p>The instrumental plural (" + ru("творительный падеж, множественное число") + ") is regular for almost every noun: " + ru("-ами") + " after a hard stem, " + ru("-ями") + " after a soft one (including the " + ru("-ья") + " plurals you already know).</p>"
      + rv(t(["Nominative plural", "Instrumental plural", "Example"], [
        [ru("коровы"), ru("коровами"), ru("Мы гордимся нашими коровами.")],
        [ru("ножи / вилки / ложки"), ru("ножами, вилками, ложками"), ru("Мы едим ножами и вилками.")],
        [ru("ручки / карандаши"), ru("ручками, карандашами"), ru("Мы пишем ручками и карандашами.")],
        [ru("друзья"), ru("друзьями"), ru("Я путешествую с друзьями.")],
        [ru("братья"), ru("братьями"), ru("Мы ездили в Минск с братьями.")],
        [ru("сёстры"), ru("сёстрами"), ru("Она живёт с сёстрами.")],
        [ru("коллеги"), ru("коллегами"), ru("Я работаю с коллегами.")],
        [ru("родители"), ru("родителями"), ru("Я живу рядом с родителями.")],
      ]))
      + '<p class="tip"><b>German:</b> <i>mit den Freunden, mit den Brüdern, mit den Messern</i> — always <i>den</i> in the plural. Russian shows the plural on the noun: ' + ru("с друзьями, с братьями, ножами") + ".</p>"})

    S.append({"h": "Step 4 · Exceptions to watch", "open": False, "html":
      "<p>A short list Russians notice instantly. If the form you built from Step 3 looks regular, stop and check this box. The hidden " + ru("-ер-") + " in " + ru("дочь / мать") + " comes back, just as it did in Lesson 9; the instrumental plural ending on " + ru("дети, люди, дочь") + " is " + ru("-ьми") + ", not " + ru("-ями") + ".</p>"
      + rv(t(["Dictionary / plural", "Instrumental", "The trap"], [
        [ru("дети") + " (sg. " + ru("ребёнок") + ")", ru("детьми"), "not “детйами” or “ребенками”"],
        [ru("люди") + " (sg. " + ru("человек") + ")", ru("людьми"), "not “людями” or “человеками”"],
        [ru("дочь → дочери"), ru("дочерьми"), ru("-ьми") + ", not “дочерями”. Singular is " + ru("дочерью") + "."],
        [ru("мать → матери"), ru("матерями"), "the hidden " + ru("-ер-") + " comes back: " + ru("матерями") + " (regular " + ru("-ами") + " on that stem)"],
        [ru("друг → друзья"), ru("друзьями"), "the " + ru("-ья") + " stem, not “другами”"],
        [ru("брат → братья"), ru("братьями"), "same pattern: not “братами”"],
        [ru("семья"), ru("семьёй"), ru("ё") + " in the singular: " + ru("с семьёй") + ", not “семьей” without " + ru("ё")],
        [ru("со") + " + a cluster", ru("со студентами") + ", " + ru("со мной") + ", " + ru("со своей женой"), ru("с") + " becomes " + ru("со") + " before " + ru("с, з, ш, ж") + " + another consonant, and before " + ru("мной") + ". Never “с студентами” or “с мной”."],
        [ru("ножницы, лыжи, палочки") + " (plural only, or used as a pair)", ru("ножницами, лыжами, палочками"), "You already know farm " + ru("вилы → вилами") + " and " + ru("ворота → воротами") + ". Same idea: " + ru("ножницы") + " has no everyday singular."],
      ]))
      + exl([("Я еду на ферму со своими детьми.", "I'm going to the farm with my children."),
             ("Батюшка говорит с людьми.", "Father is speaking with the people."),
             ("Мы очень гордимся нашими дочерьми.", "We are very proud of our daughters."),
             ("Я работаю со студентами.", "I work with students."),
             ("Чем мы стрижём волосы? Ножницами.", "What do we cut hair with? With scissors.")])
      + '<p class="tip"><b>German:</b> <i>mit den Kindern, mit den Leuten, mit den Töchtern</i> are regular. Russian ' + ru("детьми, людьми, дочерьми") + " are the ones to memorise. <i>mit mir</i> is " + ru("со мной") + " (that " + ru("со") + " is required).</p>"})

    S.append({"h": "Step 5 · The pronouns: мной, тобой, им, ей, нами, вами, ими", "open": False, "html":
      "<p>The instrumental pronouns are new forms. After a preposition, " + ru("им / ей / ими") + " add " + ru("н-") + ", the same rule as Lessons 4 and 7: " + ru("с ним, с ней, с ними") + ". And " + ru("я") + " is special: it is " + ru("со мной") + ", never “с мной”.</p>"
      + rv(t(["Nominative", "Instrumental (with / by)", "After " + ru("с / со"), "German"], [
        [ru("я"), ru("мной"), ru("со мной"), "mit mir"],
        [ru("ты"), ru("тобой"), ru("с тобой"), "mit dir"],
        [ru("он / оно"), ru("им"), ru("с ним"), "mit ihm"],
        [ru("она"), ru("ей"), ru("с ней"), "mit ihr"],
        [ru("мы"), ru("нами"), ru("с нами"), "mit uns"],
        [ru("вы"), ru("вами"), ru("с вами"), "mit euch / Ihnen"],
        [ru("они"), ru("ими"), ru("с ними"), "mit ihnen"],
      ]))
      + exl([("Посиди со мной минутку.", "Sit with me for a minute."),
             ("Я рядом с тобой, не бойся.", "I'm right next to you, don't be afraid."),
             ("После службы мы говорили с ним.", "After the service we talked with him."),
             ("Вы поедете с нами на ферму?", "Will you go to the farm with us?")])
      + '<p class="tip"><b>Don\'t mix the cases:</b> ' + ru("вижу его") + " (accusative) vs " + ru("звоню ему") + " (dative) vs " + ru("говорю с ним") + " (instrumental, with " + ru("н-") + ").</p>"})

    S.append({"h": "Step 6 · с, рядом с, между, перед", "open": False, "html":
      "<p>Four prepositions take the <b>instrumental</b>. You already met " + ru("перед") + " in Lesson 9 (in front of — not " + ru("напротив") + ", which is genitive).</p>"
      + rv(t(["Preposition", "Meaning · German", "Example"], [
        [ru("с / со"), "with · mit", ru("чай с молоком") + " · " + ru("с друзьями") + " · " + ru("со студентами")],
        [ru("рядом с / со"), "next to, beside · neben", ru("Я живу рядом с родителями.") + " · " + ru("рядом с тобой")],
        [ru("между"), "between · zwischen", ru("Между фермой и лесом течёт ручей.") + " · " + ru("между странами")],
        [ru("перед"), "in front of · vor", ru("Машина стоит перед домом.") + " · " + ru("перед церковью")],
      ]))
      + "<p>A useful trap: " + ru("с / со") + " plus the <b>genitive</b> means <b>from</b> (off, down from), not “with”: " + ru("с работы") + " = from work, " + ru("со стола") + " = off the table. If you mean “together with,” you need the instrumental: " + ru("с женой") + ", " + ru("с молоком") + ".</p>"
      + exl([("Я живу рядом с родителями, в соседнем доме.", "I live next to my parents, in the neighbouring house."),
             ("Между фермой и лесом течёт ручей.", "A stream runs between the farm and the forest."),
             ("Жена молится перед иконой.", "My wife prays in front of the icon.")])
      + '<p class="tip"><b>German:</b> mit, neben, zwischen, vor all take the dative in German (vor dem Haus, zwischen dem Hof und dem Wald). In Russian these four take the instrumental: ' + ru("перед домом, между фермой и лесом") + ".</p>"})

    S.append({"h": "Step 7 · чем for tools, and работать учителем", "open": False, "html":
      "<p>" + ru("чем?") + " asks “with what? / using what?” The tool goes in the instrumental, usually <b>without</b> " + ru("с") + ":</p>"
      + exl([("Чем мы обычно едим? Ножами и вилками, ложками.", "What do we usually eat with? With knives and forks, with spoons."),
             ("Чем мы пишем? Ручками. Чем мы рисуем? Ручками и карандашами.", "What do we write with? With pens. What do we draw with? With pens and pencils."),
             ("Чем мы стрижём волосы? Ножницами.", "What do we cut hair with? With scissors."),
             ("В китайском ресторане мы едим палочками.", "In a Chinese restaurant we eat with chopsticks.")])
      + "<p>A second pattern uses the instrumental <b>without</b> " + ru("с") + " for a job or role: " + ru("работать / быть") + " + instrumental = “work as / be a …”:</p>"
      + exl([("Мой брат работает учителем.", "My brother works as a teacher."),
             ("Она работает программистом в Джексоне.", "She works as a programmer in Jackson."),
             ("Его отец был священником.", "His father was a priest.")])
      + '<p class="tip"><b>German:</b> tools take <i>mit</i> — <i>mit einem Messer, mit den Scheren</i>. A job does <b>not</b>: <i>er arbeitet als Lehrer</i>, never “mit Lehrer.” Russian matches that split: ' + ru("ножом") + " or " + ru("ножницами") + " for the tool, " + ru("учителем") + " for the job, no " + ru("с") + " in either of those two patterns.</p>"})

    S.append({"h": "Summary", "open": False, "html":
      '<ul class="sum">'
      + "<li>The instrumental (" + ru("творительный падеж") + ") answers " + ru("с кем?") + " (with whom?) and " + ru("чем?") + " (with what? / by means of what?).</li>"
      + "<li>Singular: masc./neut. " + ru("-ом / -ем") + " (" + ru("другом, учителем, ножом, молоком") + "); fem. " + ru("-ой / -ёй") + " or " + ru("-ью") + " (" + ru("женой, семьёй, дочерью") + "); men in " + ru("-а") + " take " + ru("-ой") + " (" + ru("батюшкой, коллегой") + ").</li>"
      + "<li>Plural: " + ru("-ами / -ями") + " (" + ru("коровами, друзьями, братьями, ножами") + ").</li>"
      + "<li>Exceptions: " + ru("детьми, людьми, дочерьми, матерями, друзьями, братьями") + "; " + ru("семьёй") + "; " + ru("со") + " before a cluster and before " + ru("мной") + "; plural-only " + ru("ножницы, лыжи, палочки") + " (and farm " + ru("вилы, ворота") + ").</li>"
      + "<li>Pronouns: " + ru("мной, тобой, им, ей, нами, вами, ими") + ". After a preposition: " + ru("со мной, с тобой, с ним, с ней, с ними") + ".</li>"
      + "<li>Prepositions: " + ru("с / со") + " (with), " + ru("рядом с") + " (next to), " + ru("между") + " (between), " + ru("перед") + " (in front of) — all + instrumental. " + ru("с") + " + genitive is “from,” not “with.”</li>"
      + "<li>Tools: " + ru("чем?") + " → " + ru("ножом, ручками, ножницами") + " (no " + ru("с") + "). Jobs: " + ru("работает учителем, программистом") + " (no " + ru("с") + ").</li>"
      + "</ul>"})

    def it(part, sub, k, s, w, ans, d, ex, tr, gl=None, **extra):
        item = {"part": part, "sub": sub, "k": k, "w": w, "s": s, "base": extra.pop("base", w), "a": ans, "d": d,
                "ex": ex, "translation": tr, "glosses": gl or []}
        item.update(extra)
        return item
    PA, PB, PC = "A · singular endings", "B · the plural, and exceptions", "C · pronouns, prepositions, tools and jobs"
    EX = [
     # Part A · singular
     it("A", PA, "ins_sg", "Я пью чай с ___.", "молоко", "молоком", ["молоко", "молока", "молоку"],
        "С (with) takes the instrumental. Neut. -о → -ом: молоко → молоком. (Steps 1 and 2)",
        "I drink tea with milk."),
     it("A", PA, "ins_sg", "Я живу с ___.", "жена", "женой", ["жена", "жене", "жену"],
        "С + instrumental. Feminine -а → -ой: жена → женой. (Step 2)",
        "I live with my wife."),
     it("A", PA, "ins_sg", "Утром я гуляю с ___.", "собака", "собакой", ["собака", "собаке", "собаку"],
        "С + instrumental. Feminine -а → -ой: собака → собакой. (Step 2)",
        "In the morning I walk with the dog.", ["гулять: to walk, go for a stroll"]),
     it("A", PA, "ins_sg", "Я хожу в кино с ___.", "друг", "другом", ["друг", "другу", "друга"],
        "С + instrumental. Masculine consonant → -ом: друг → другом. (Step 2)",
        "I go to the cinema with a friend."),
     it("A", PA, "ins_sg", "Жена режет хлеб ___.", "нож", "ножом", ["нож", "ножа", "ножу"],
        "Чем? (with what?) The tool is instrumental, with no с: нож → ножом. (Steps 2 and 7)",
        "My wife cuts the bread with a knife.", ["резать: to cut"]),
     it("A", PA, "ins_sg", "Мы едим суп ___.", "ложка", "ложкой", ["ложка", "ложку", "ложке"],
        "Чем? Instrumental, no с. Feminine -а → -ой: ложка → ложкой. (Steps 2 and 7)",
        "We eat soup with a spoon."),
     it("A", PA, "ins_sg", "На рынок она пошла с ___.", "сестра", "сестрой", ["сестра", "сестре", "сестру"],
        "С + instrumental. Feminine -а → -ой: сестра → сестрой. (Step 2)",
        "She went to the market with her sister."),
     it("A", PA, "ins_sg", "После службы мы говорили с ___.", "батюшка", "батюшкой", ["батюшка", "батюшке", "батюшку"],
        "Men in -а take the feminine-looking ending: батюшка → батюшкой. (Step 2)",
        "After the service we talked with Father."),
     it("A", PA, "ins_sg", "Мой брат работает ___.", "учитель", "учителем", ["учитель", "учителя", "учителю"],
        "Работать + instrumental (no с) means “work as”: учитель → учителем. (Step 7)",
        "My brother works as a teacher."),
     it("A", PA, "ins_sg", "Я горжусь своей ___.", "семья", "семьёй", ["семья", "семье", "семью"],
        "Гордиться takes the instrumental. Семья is feminine -я → семьёй (with ё). (Steps 2 and 4)",
        "I'm proud of my family.", ["гордиться: to be proud of"]),
     it("A", PA, "ins_sg", "Мама гуляет с ___.", "дочь", "дочерью", ["дочь", "дочери", "дочерей"],
        "Feminine -ь: дочь → дочерью (the -ью ending), not “дочой”. (Steps 2 and 4)",
        "Mom is out for a walk with her daughter."),
     it("A", PA, "ins_sg", "Машина стоит перед ___.", "дом", "домом", ["дом", "дома", "дому"],
        "Перед (in front of) takes the instrumental: дом → домом. Напротив would take the genitive (дома). (Step 6)",
        "The car is parked in front of the house."),
     it("A", PA, "ins_sg", "Между ___ и лесом течёт ручей.", "ферма", "фермой", ["ферму", "фермы", "ферме"],
        "Между (between) takes the instrumental: ферма → фермой. (Step 6)",
        "A stream runs between the farm and the forest.", ["ручей: stream"]),
     it("A", PA, "ins_sg", "Я пишу ___.", "ручка", "ручкой", ["ручка", "ручку", "ручке"],
        "Чем? Instrumental, no с. Ручка → ручкой. (Steps 2 and 7)",
        "I write with a pen.", ["ручка: pen"]),
     # Part B · plural and exceptions
     it("B", PB, "ins_pl", "Я путешествую с ___.", "друг", "друзьями", ["другом", "друзей", "друзья"],
        "С + instrumental plural. Друг → друзья → друзьями, not “другами”. (Steps 3 and 4)",
        "I travel with friends.", ["путешествовать: to travel"]),
     it("B", PB, "ins_pl", "Мы ездили в Минск с ___.", "брат", "братьями", ["братом", "братьев", "братья"],
        "Брат → братья → братьями, not “братами”. (Steps 3 and 4)",
        "We went to Minsk with (our) brothers."),
     it("B", PB, "ins_pl", "Она живёт с ___.", "сестра", "сёстрами", ["сестрой", "сестёр", "сёстры"],
        "Сестра → сёстры → сёстрами (ё in the plural). (Step 3)",
        "She lives with (her) sisters."),
     it("B", PB, "ins_pl", "Мы гордимся нашими ___.", "корова", "коровами", ["коровой", "коров", "коровы"],
        "Regular plural: коровы → коровами. Гордиться takes the instrumental. (Step 3)",
        "We are proud of our cows."),
     it("B", PB, "ins_pl", "Чем мы обычно едим? ___ и вилками.", "нож", "Ножами", ["Ножом", "Ножи", "Ножей"],
        "Чем? Instrumental plural, no с: ножи → ножами. (Steps 3 and 7)",
        "What do we usually eat with? With knives and forks."),
     it("B", PB, "ins_pl", "Мы пишем ___.", "ручка", "ручками", ["ручкой", "ручки", "ручек"],
        "Чем? Instrumental plural: ручки → ручками. (Steps 3 and 7)",
        "We write with pens."),
     it("B", PB, "ins_pl", "Я еду на ферму со своими ___.", "ребёнок", "детьми", ["ребёнком", "детей", "дети"],
        "Exception: ребёнок → дети → детьми, not “детйами”. Со before своими (с + consonant cluster). (Step 4)",
        "I'm going to the farm with my children."),
     it("B", PB, "ins_pl", "Батюшка говорит с ___.", "человек", "людьми", ["человеком", "людей", "люди"],
        "Exception: человек → люди → людьми, not “людями” or “человеками”. (Step 4)",
        "Father is speaking with the people."),
     it("B", PB, "ins_pl", "Мы очень гордимся нашими ___.", "дочь", "дочерьми", ["дочерью", "дочерей", "дочери"],
        "Exception: дочь → дочери → дочерьми (-ьми, not “дочерями”). (Step 4)",
        "We are very proud of our daughters."),
     it("B", PB, "ins_pl", "Я работаю со ___.", "студент", "студентами", ["студентом", "студентов", "студенты"],
        "Со (not с) before ст-: со студентами. Regular plural -ами. (Steps 3 and 4)",
        "I work with students."),
     it("B", PB, "ins_pl", "Чем мы стрижём волосы? ___.", "ножницы", "Ножницами", ["Ножницы", "Ножниц", "Ножницам"],
        "Ножницы is plural only: instrumental ножницами. Чем? — no с. (Steps 4 and 7)",
        "What do we cut hair with? With scissors.", ["стричь: to cut (hair)"]),
     it("B", PB, "ins_pl", "В китайском ресторане мы едим ___.", "палочка", "палочками", ["палочкой", "палочки", "палочек"],
        "Палочки (chopsticks) are used in the plural: палочками. (Steps 4 and 7)",
        "In a Chinese restaurant we eat with chopsticks.", ["палочки: chopsticks"]),
     it("B", PB, "ins_pl", "Зимой мы пользуемся ___.", "лыжи", "лыжами", ["лыжи", "лыж", "лыжам"],
        "Лыжи is used as a pair (plural): пользоваться + instrumental → лыжами. (Steps 4 and 7)",
        "In winter we use skis.", ["пользоваться: to use (+ instrumental)","лыжи: skis"]),
     it("B", PB, "ins_pl", "Мы рисуем ручками и ___.", "карандаш", "карандашами", ["карандашом", "карандаши", "карандашей"],
        "Чем? Instrumental plural: карандаши → карандашами. (Steps 3 and 7)",
        "We draw with pens and pencils.", ["карандаш: pencil","рисовать: to draw"]),
     # Part C · pronouns, prepositions, jobs
     it("C", PC, "pron", "Посиди со ___ минутку.", "я", "мной", ["мне", "меня", "нам"],
        "Я → мной, and с becomes со before мной: со мной, never “с мной”. (Steps 4 and 5)",
        "Sit with me for a minute."),
     it("C", PC, "pron", "Я рядом с ___, не бойся.", "ты", "тобой", ["тебе", "тебя", "вами"],
        "Рядом с takes the instrumental. Ты → тобой. (Steps 5 and 6)",
        "I'm right next to you, don't be afraid."),
     it("C", PC, "pron", "После службы мы говорили с ___.", "он", "ним", ["им", "его", "ему"],
        "After a preposition, им adds н-: с ним. Им would be right without a preposition. (Step 5)",
        "After the service we talked with him."),
     it("C", PC, "pron", "Я иду в храм с ___.", "она", "ней", ["ей", "её", "ею"],
        "After с, ей adds н-: с ней. (Step 5)",
        "I'm going to church with her."),
     it("C", PC, "pron", "Вы поедете с ___ на ферму?", "мы", "нами", ["нас", "нам", "мной"],
        "Мы → нами. С нами = with us. (Step 5)",
        "Will you go to the farm with us?"),
     it("C", PC, "ins_pl", "Дети играют рядом с ___.", "родители", "родителями", ["родителей", "родителям", "родители"],
        "Рядом с (next to) takes the instrumental: родители → родителями. (Steps 3 and 6)",
        "The children are playing next to (their) parents.", ["родители: parents"]),
     it("C", PC, "ins_pl", "Между этими ___ находится река.", "страна", "странами", ["стране", "страны", "стран"],
        "Между takes the instrumental plural: страны → странами. (Steps 3 and 6)",
        "The river is between these countries.", ["страна: country"]),
     it("C", PC, "ins_sg", "Перед ___ всегда много людей.", "церковь", "церковью", ["церковь", "церкви", "церквей"],
        "Перед takes the instrumental. Церковь (fem. -ь) → церковью. (Steps 2 and 6)",
        "There are always a lot of people in front of the church."),
     it("C", PC, "ins_sg", "Она работает ___ в Джексоне.", "программист", "программистом", ["программиста", "программисту", "программисты"],
        "Работать + instrumental (no с): программист → программистом, “as a programmer.” (Step 7)",
        "She works as a programmer in Jackson."),
     it("C", PC, "prep", "Я живу ___ родителями, в соседнем доме.", "с / рядом с / между / перед", "рядом с", ["с", "между", "перед"],
        "Next to, in the neighbouring house: рядом с + instrumental (родителями). С родителями would be “with my parents” (in the same house). (Step 6)",
        "I live next to my parents, in the neighbouring house."),
    ]
    assert len(EX) == 38, len(EX)
    return {
      "id": "L8", "n": 8,
      "title": "The instrumental: с кем? чай с молоком",
      "goal": "By the end you'll say who you're with and what you use: Я живу с женой. Мы едим ножами и вилками. Я еду со своими детьми. Мой брат работает учителем.",
      "minutes": "20–25 min to read, then %d exercises" % len(EX),
      "sections": S,
      "parts": {"A": PA, "B": PB, "C": PC},
      "practice": {
        "title": "Now use it: write to your tutor",
        "text": "Answer in chat: С кем вы живёте и работаете? Чем вы обычно пишете и едите? Write 4 sentences: one with с + a person (singular or plural), one with a tool (чем?), one with an exception (детьми, людьми, дочерьми, со студентами or со мной), and one with рядом с, между or перед — or with работать + a job.",
        "examples": ["Я живу с женой и дочкой.", "Мы едим суп ложкой.", "Я работаю со студентами.", "Мой брат работает учителем."]
      },
      "exercises": EX,
    }
