# Lesson LK: the relative pronoun который (declension, animate acc, prepositions stay,
# verb government, нужна / коллега / о ком vs о чём). Imported by lessons_src.py.
# Forms checked with pymorphy3 (src/verify_lessons.py, check_lk).
# Placed after L9 in the roadmap without renumbering L10–L12.

def build(t, ru, exl):
    def rv(inner, hint="Say each word out loud first. Then check the stress:"):
        return ('<div class="rv nostress"><div class="rvbar"><span class="rvh">%s</span>'
                '<button type="button" class="sbtn" data-rv="1" aria-pressed="false">Show stress ´</button></div>%s</div>') % (hint, inner)

    S = []
    S.append({"h": "Step 1 · который joins two sentences", "open": True, "html":
      "<p>The <b>relative pronoun</b> (" + ru("относительное местоимение") + ") " + ru("который") + " means <b>who / which / that</b>. It takes two short sentences and makes them one.</p>"
      + exl([("Это человек. Человек работает в магазине.", "This is a person. The person works in a store."),
             ("Это человек, который работает в магазине.", "This is a person who works in a store."),
             ("Это девушка. Девушка живёт в Москве.", "This is a girl. The girl lives in Moscow."),
             ("Это девушка, которая живёт в Москве.", "This is a girl who lives in Moscow.")])
      + "<p>A common slip is to drop the preposition: not “работает магазине,” but " + ru("работает в магазине") + ". The relative clause still needs " + ru("в") + ", " + ru("на") + ", " + ru("с") + ", " + ru("о") + " — whatever the original sentence had.</p>"
      + '<p class="tip"><b>' + ru("какой") + " vs " + ru("который") + ".</b> " + ru("какой") + " is an interrogative / descriptive adjective: “what kind? / which one?” (" + ru("Какой у вас телефон?") + ", " + ru("Какие животные вам нравятся?") + "). You already drill it in the Grammar tab. " + ru("который") + " is a <b>relative pronoun</b>: it points back to a noun you just named and opens a new clause about that noun.</p>"})

    S.append({"h": "Step 2 · The endings, and where the case comes from", "open": False, "html":
      "<p><b>Gender and number</b> come from the <b>head noun</b> (the word " + ru("который") + " points back to): " + ru("человек → который") + ", " + ru("девушка → которая") + ", " + ru("письмо → которое") + ", " + ru("друзья → которые") + ".</p>"
      + "<p><b>Case</b> comes from the <b>job " + ru("который") + " does inside the relative clause</b>, not from the case of the head noun in the main clause.</p>"
      + rv(t(["Case (падеж)", "Masc.", "Neut.", "Fem.", "Plural"], [
        ["nominative " + ru("(именительный)"), ru("который"), ru("которое"), ru("которая"), ru("которые")],
        ["genitive " + ru("(родительный)"), ru("которого"), ru("которого"), ru("которой"), ru("которых")],
        ["dative " + ru("(дательный)"), ru("которому"), ru("которому"), ru("которой"), ru("которым")],
        ["accusative " + ru("(винительный)"), ru("который") + " (anim. " + ru("которого") + ")", ru("которое"), ru("которую"), ru("которые") + " (anim. " + ru("которых") + ")"],
        ["instrumental " + ru("(творительный)"), ru("которым"), ru("которым"), ru("которой"), ru("которыми")],
        ["prepositional " + ru("(предложный)"), ru("о котором"), ru("о котором"), ru("о которой"), ru("о которых")],
      ]))
      + exl([("Дом, который я купил.", "The house that I bought. (дом is inanimate masculine → accusative = nominative: который)"),
             ("Друг, которого я видел.", "The friend whom I saw. (друг is animate masculine → accusative = genitive: которого)")])
      + '<p class="tip"><b>German:</b> the relative pronoun takes the case of its job in the relative clause: <i>das Haus, das ich gekauft habe</i> vs <i>der Freund, den ich gesehen habe</i> (accusative <i>den</i>, because he is the person I saw). Russian does the same: ' + ru("дом, который я купил") + " vs " + ru("друг, которого я видел") + ". Gender and number come from the head noun; the case comes from the clause. <i>der / den / dem / dessen</i> is the closest hook for " + ru("который / которого / которому / которого") + " (genitive).</p>"})

    S.append({"h": "Step 3 · Animate vs inanimate accusative", "open": False, "html":
      "<p>In the accusative, " + ru("который") + " follows the same animate rule you know from Lesson 6.</p>"
      + t(["Head noun", "Accusative of " + ru("который"), "Example"], [
        ["masc. inanimate (" + ru("дом, роман, храм") + ")", ru("который") + " (= nom.)", ru("Дом, который я купил.")],
        ["masc. animate (" + ru("друг, врач, сын") + ")", ru("которого") + " (= gen.)", ru("Друг, которого я видел.")],
        ["neuter (" + ru("письмо, сено, лекарство") + ")", ru("которое") + " (always)", ru("Письмо, которое я прочитал.")],
        ["feminine, any (" + ru("книга, корова, девушка") + ")", ru("которую"), ru("Книга, которую я читаю.") + " · " + ru("Девушка, которую я знаю.")],
        ["plural inanimate (" + ru("дома, письма, книги") + ")", ru("которые") + " (= nom.)", ru("Дома, которые мы купили.")],
        ["plural animate (" + ru("друзей, коров, детей") + ")", ru("которых") + " (= gen.)", ru("Друзья, которых я встретил.")],
      ])
      + "<p>Feminine singular is always " + ru("которую") + " in the accusative, whether the noun is a person or a thing. The animate split only shows up in the masculine singular and in the plural.</p>"})

    S.append({"h": "Step 4 · The preposition stays with который", "open": False, "html":
      "<p>If the original sentence had a preposition, keep it, and put " + ru("который") + " in the case that preposition takes. Dropping the preposition is the same slip as “работает магазине.”</p>"
      + t(["Original", "Joined with " + ru("который")], [
        [ru("В этом городе живёт 10 миллионов человек."), ru("город, в котором живёт 10 миллионов человек")],
        [ru("Об этом романе все говорят."), ru("роман, о котором все говорят")],
        [ru("С Анной я не встречался много лет."), ru("Анна, с которой я не встречался много лет")],
        [ru("Этому другу я обещал написать письмо."), ru("друг, которому я обещал написать письмо")],
        [ru("Этого врача я хорошо знаю."), ru("врач, которого я хорошо знаю")],
      ])
      + exl([("Москва — это большой и красивый город, в котором живёт 10 миллионов человек.", "Moscow is a large and beautiful city, in which 10 million people live."),
             ("Я прочитала роман, о котором все говорят.", "I read a novel that everyone is talking about."),
             ("Мне звонила Анна, с которой я не встречался много лет.", "Anna called me, whom I hadn't seen in many years."),
             ("У моего сына есть собака, с которой он любит гулять.", "My son has a dog that he likes to walk with.")])
      + "<p>" + ru("которой") + " alone is ambiguous (feminine genitive, dative, instrumental and prepositional all look the same). Write " + ru("с которой") + ", " + ru("о которой") + ", " + ru("к которой") + " so the preposition is visible.</p>"})

    S.append({"h": "Step 5 · The verb in the clause picks the case", "open": False, "html":
      "<p>Look at the verb (and its preposition) <b>inside</b> the relative clause. That government decides the case, the same way it would without " + ru("который") + ".</p>"
      + t(["Pattern", "Case", "Example"], [
        [ru("рассказать / дать / помочь") + " + person", "dative " + ru("(дательный)"), ru("человек, которому я рассказал эту историю")],
        [ru("играть / работать / встречаться с"), "instrumental with " + ru("с"), ru("коллега, с которым я люблю играть в теннис")],
        [ru("мечтать о"), "prepositional with " + ru("о"), ru("поездка, о которой я мечтал всю жизнь")],
        [ru("привыкнуть к"), "dative with " + ru("к"), ru("лекарство, к которому я привык")],
        [ru("нужна / нужен / нужно / нужны"), "nominative " + ru("(именительный)"), ru("книга, которая мне нужна")],
        [ru("гордиться"), "instrumental, no " + ru("с"), ru("дети, которыми мы гордимся")],
      ])
      + exl([("Человек, которому я рассказал эту историю, обещал мне помочь.", "The person I told this story to promised to help me. (рассказать кому?)"),
             ("Это поездка, о которой я мечтал всю жизнь.", "This is a trip I had dreamed of all my life. (мечтать о + prepositional)"),
             ("Это лекарство, к которому я привык.", "This is the medicine I have gotten used to. (привыкнуть к + dative)")])
      + "<p>" + ru("нужна") + " is the one English speakers miss: in " + ru("книга мне нужна") + ", " + ru("книга") + " is the <b>subject</b> (nominative). So: " + ru("книга, которая мне нужна") + " — not “которую.”</p>"})

    S.append({"h": "Step 6 · Traps and exceptions", "open": False, "html":
      "<p>A short list to check before you lock in an ending.</p>"
      + rv(t(["Trap", "Right form", "Why"], [
        [ru("книга, ___ мне нужна"), ru("которая"), ru("книга") + " is the subject of " + ru("нужна") + ". Not accusative " + ru("которую") + "."],
        [ru("привыкнуть к") + " + noun", ru("к которому") + " / " + ru("к которой"), "The preposition " + ru("к") + " stays, and it takes the dative. Not bare " + ru("которое") + "."],
        [ru("мечтать о") + " + noun", ru("о котором") + " / " + ru("о которой"), ru("о") + " stays; prepositional case."],
        [ru("коллега"), ru("с которым") + " or " + ru("с которой"), ru("коллега") + " is <b>common gender</b> (" + ru("общий род") + "): agreement follows the person’s sex. A man: " + ru("мой коллега, с которым…") + "; a woman: " + ru("моя коллега, с которой…") + ". If the sex is not named, masculine is the textbook default."],
        [ru("о ком") + " vs " + ru("о чём"), ru("о ком") + " (people), " + ru("о чём") + " (things)", ru("О ком вы мечтаете? О жене.") + " " + ru("О чём вы любите говорить? О машинах.") + " The noun itself still takes " + ru("о которой") + " / " + ru("о котором") + " in a relative clause."],
        ["Dropped preposition", ru("в котором") + ", " + ru("с которой") + ", " + ru("к которому"), "Keep " + ru("в") + ", " + ru("с") + ", " + ru("к") + ", " + ru("о") + ". Feminine " + ru("которой") + " alone is not enough."],
        [ru("в какую церковь"), ru("церковь") + " (acc. = nom.)", "Soft-sign feminines you know from Lesson 2: " + ru("в церковь, в Беларусь") + ". The relative form still changes: " + ru("церковь, в которую мы идём") + "."],
      ]))
      + exl([("Ольга дала мне книгу, которая мне нужна.", "Olga gave me a book that I need."),
             ("У меня есть коллега, с которым я люблю играть в теннис.", "I have a colleague I like to play tennis with. (If she is a woman: с которой.)"),
             ("О ком вы мечтаете? О жене. О чём вы любите говорить? О машинах.", "About whom are you dreaming? About my wife. What do you like to talk about? About cars.")])})

    S.append({"h": "Step 7 · Join the sentences (worked examples)", "open": False, "html":
      "<p>These are the joins from this week’s homework, written out in full. The blank in the exercises is just the " + ru("который") + " form — sometimes with its preposition.</p>"
      + t(["#", "Two sentences", "One sentence"], [
        ["1", ru("Москва — это большой и красивый город. В этом городе живёт 10 миллионов человек."), ru("Москва — это большой и красивый город, в котором живёт 10 миллионов человек.")],
        ["2", ru("Я прочитала роман. Об этом романе все говорят."), ru("Я прочитала роман, о котором все говорят.")],
        ["3", ru("Мне звонила Анна. С Анной я не встречался много лет."), ru("Мне звонила Анна, с которой я не встречался много лет.")],
        ["4", ru("Мне звонил друг. Этому другу я обещал написать письмо."), ru("Мне звонил друг, которому я обещал написать письмо.")],
        ["5", ru("Она пошла к врачу. Этого врача я хорошо знаю."), ru("Она пошла к врачу, которого я хорошо знаю.")],
      ])
      + "<p>And the five gap sentences, already filled:</p>"
      + exl([("Человек, которому я рассказал эту историю, обещал мне помочь.", "The person I told this story to promised to help me."),
             ("У меня есть коллега, с которым я люблю играть в теннис.", "I have a colleague I like to play tennis with."),
             ("Это поездка, о которой я мечтал всю жизнь.", "This is a trip I had dreamed of all my life."),
             ("Это лекарство, к которому я привык.", "This is the medicine I have gotten used to."),
             ("Ольга дала мне книгу, которая мне нужна.", "Olga gave me a book that I need.")])})

    S.append({"h": "Summary", "open": False, "html":
      '<ul class="sum">'
      + "<li>" + ru("который") + " is a <b>relative pronoun</b> (" + ru("относительное местоимение") + "): who / which / that. " + ru("какой") + " is a different word (“what kind / which”).</li>"
      + "<li>Gender and number come from the <b>head noun</b>. Case comes from the <b>relative clause</b> (the same rule as German <i>der / den / dem</i>).</li>"
      + "<li>Accusative: inanimate masc. and inanimate plural = nominative (" + ru("который, которые") + "); animate masc. and animate plural = genitive (" + ru("которого, которых") + "); feminine is always " + ru("которую") + "; neuter is " + ru("которое") + ".</li>"
      + "<li>Prepositions stay: " + ru("в котором, о котором, с которой, к которому") + " — not bare " + ru("которой") + ".</li>"
      + "<li>Watch the verb: " + ru("рассказать") + " + dative; " + ru("играть с") + " + instrumental; " + ru("мечтать о") + " + prepositional; " + ru("привыкнуть к") + " + dative; " + ru("нужна") + " takes a nominative subject (" + ru("книга, которая мне нужна") + ").</li>"
      + "<li>" + ru("коллега") + " is common gender: " + ru("с которым") + " or " + ru("с которой") + ", following the person’s sex. " + ru("О ком") + " is for people, " + ru("о чём") + " for things.</li>"
      + "</ul>"})

    def it(part, sub, k, s, w, ans, d, ex, tr, gl=None, **extra):
        item = {"part": part, "sub": sub, "k": k, "w": w, "s": s, "base": extra.pop("base", w), "a": ans, "d": d,
                "ex": ex, "translation": tr, "glosses": gl or []}
        item.update(extra)
        return item

    PA = "A · agreement and the basic cases"
    PB = "B · prepositions stay; joining sentences"
    PC = "C · verb government, and the traps"
    EX = [
     # Part A · 12
     it("A", PA, "rel", "Это человек, ___ работает в магазине.", "который", "который",
        ["которая", "которого", "которое"],
        "Head noun человек is masculine singular; in the clause который is the subject (nominative). Don’t drop в: работает в магазине. (Steps 1 and 2)",
        "This is a person who works in a store."),
     it("A", PA, "rel", "Это девушка, ___ живёт в Москве.", "который", "которая",
        ["который", "которую", "которое"],
        "Head noun девушка is feminine singular; which/who is the subject of живёт → nominative которая. (Steps 1 and 2)",
        "This is a girl who lives in Moscow."),
     it("A", PA, "rel", "Письмо, ___ пришло из Беларуси, лежит на столе.", "который", "которое",
        ["который", "которая", "которого"],
        "Письмо is neuter, and которое is the subject of пришло → nominative neuter которое. (Step 2)",
        "The letter that arrived from Belarus is lying on the table.",
        ["пришло: arrived"]),
     it("A", PA, "rel", "Дом, ___ я купил, стоит в деревне.", "который", "который",
        ["которого", "которому", "которое"],
        "Дом is masculine inanimate. In the clause it is the object of купил → accusative, which equals nominative: который. (Steps 2 and 3)",
        "The house that I bought stands in the village."),
     it("A", PA, "rel", "Друг, ___ я видел вчера, живёт в Минске.", "который", "которого",
        ["который", "которому", "которым"],
        "Друг is masculine animate. Object of видел → accusative = genitive: которого. Compare дом, который я купил. (Step 3)",
        "The friend I saw yesterday lives in Minsk."),
     it("A", PA, "rel", "Это друзья, ___ работают на ферме.", "который", "которые",
        ["которых", "которым", "который"],
        "Друзья is plural; they are the subject of работают → nominative plural которые. (Step 2)",
        "These are friends who work on the farm."),
     it("A", PA, "rel", "Машина, ___ отец купил, стоит у дома.", "который", "которую",
        ["которая", "которой", "которое"],
        "Машина is feminine; object of купил → accusative которую. Feminine accusative is always которую, person or thing. (Step 3)",
        "The car Father bought is standing by the house."),
     it("A", PA, "rel", "Это сено, ___ мы сушили вчера.", "который", "которое",
        ["который", "которого", "которую"],
        "Сено is neuter; object of сушили → accusative neuter, which equals nominative: которое. (Step 3)",
        "This is the hay we dried yesterday.",
        ["сушили: dried (past plural)", "сено: hay"]),
     it("A", PA, "rel", "Я люблю собак, ___ мы кормим на ферме.", "который", "которых",
        ["которые", "которым", "которого"],
        "Собак is animate plural (object of люблю, and of кормим). Accusative animate plural = genitive: которых. (Step 3)",
        "I love the dogs that we feed on the farm."),
     it("A", PA, "rel", "Батюшка, ___ служит в нашей церкви, знает всех.", "который", "который",
        ["которого", "которому", "которая"],
        "Батюшка is masculine; который is the subject of служит → nominative. (Steps 1 and 2)",
        "The priest who serves in our church knows everyone."),
     it("A", PA, "rel", "Программист, ___ пишет код, работает из Бреста.", "который", "который",
        ["которое", "которого", "которая"],
        "Программист is masculine; который is the subject of пишет → nominative. (Step 2)",
        "The programmer who writes the code works from Brest.",
        ["код: code"]),
     it("A", PA, "rel", "Дети, ___ играют во дворе, живут рядом с фермой.", "который", "которые",
        ["которых", "которыми", "который"],
        "Дети is plural; которые is the subject of играют → nominative plural. (Step 2)",
        "The children who are playing in the yard live next to the farm.",
        ["двор: yard"]),

     # Part B · 10, including the tutor's 5 join items
     it("B", PB, "rel_prep", "Москва — это большой и красивый город, ___ живёт десять миллионов человек.", "который", "в котором",
        ["котором", "в который", "о котором"],
        "Original: В этом городе живёт… Где? в + prepositional. The preposition stays: в котором. Bare котором is the dropped-preposition trap. (Steps 4 and 7)",
        "Moscow is a large and beautiful city in which ten million people live."),
     it("B", PB, "rel_prep", "Я прочитала роман, ___ все говорят.", "который", "о котором",
        ["котором", "о которой", "в котором"],
        "Original: Об этом романе все говорят. говорить о + prepositional. Keep о: о котором. (Steps 4, 5 and 7)",
        "I read a novel that everyone is talking about.",
        ["роман: novel"]),
     it("B", PB, "rel_prep", "Мне звонила Анна, ___ я не встречался много лет.", "который", "с которой",
        ["которой", "с которым", "которую"],
        "Original: С Анной я не встречался… встречаться с + instrumental. Анна is feminine → с которой, not bare которой. (Steps 4 and 7)",
        "Anna called me, whom I hadn't seen in many years.",
        ["встречаться: to meet, see each other"]),
     it("B", PB, "rel_prep", "Мне звонил друг, ___ я обещал написать письмо.", "который", "которому",
        ["которого", "которым", "который"],
        "Original: Этому другу я обещал написать письмо. обещать / написать письмо кому? → dative которому. No preposition here. (Steps 5 and 7)",
        "A friend called me, to whom I had promised to write a letter."),
     it("B", PB, "rel_prep", "Она пошла к врачу, ___ я хорошо знаю.", "который", "которого",
        ["которому", "который", "которым"],
        "Original: Этого врача я хорошо знаю. знать + accusative; врач is animate masculine → которого. The к in пошла к врачу belongs to the main clause, not to который. (Steps 3, 4 and 7)",
        "She went to a doctor whom I know well."),
     it("B", PB, "rel_prep", "У моего сына есть собака, ___ он любит гулять.", "который", "с которой",
        ["которой", "с которым", "которую"],
        "гулять с + instrumental. Собака is feminine → с которой. The preposition stays. (Step 4)",
        "My son has a dog that he likes to walk with."),
     it("B", PB, "rel_prep", "Я ездил в храм, ___ служит наш батюшка.", "который", "в котором",
        ["в который", "котором", "в которой"],
        "Где? The priest serves in the church: в + prepositional. Храм is masculine → в котором. В который would be куда? (Step 4)",
        "I went to the church in which our priest serves."),
     it("B", PB, "rel_prep", "Церковь, ___ мы идём, стоит напротив почты.", "который", "в которую",
        ["в которой", "в который", "которую"],
        "Куда? мы идём в церковь: в + accusative. Церковь is feminine → в которую. (The noun itself is a soft-sign feminine, acc. = nom., but который still takes которую.) (Steps 3 and 4)",
        "The church we are going to stands across from the post office."),
     it("B", PB, "rel_prep", "Сервер, ___ мы работаем, стоит в офисе.", "который", "на котором",
        ["на который", "в котором", "котором"],
        "работать на + prepositional (на сервере). Сервер is masculine → на котором. (Step 4)",
        "The server we work on is in the office.",
        ["сервер: server"]),
     it("B", PB, "rel_prep", "Родители, ___ я живу, держат коров.", "который", "с которыми",
        ["которыми", "с которым", "которых"],
        "жить с + instrumental, plural → с которыми. Bare которыми would drop the preposition. (Step 4)",
        "My parents, who I live with, keep cows."),

     # Part C · 10, including the tutor's 5 gap items
     it("C", PC, "rel_trap", "Человек, ___ я рассказал эту историю, обещал мне помочь.", "который", "которому",
        ["которого", "которым", "который"],
        "рассказать кому? → dative которому. (Steps 5 and 7)",
        "The person I told this story to promised to help me."),
     it("C", PC, "rel_trap", "У меня есть коллега, ___ я люблю играть в теннис.", "который", "с которым",
        ["которому", "которой", "которым"],
        "играть с + instrumental. коллега is common gender (общий род): с которым if the colleague is a man (the textbook default when sex is not named), с которой if a woman. Not dative которому. (Steps 5, 6 and 7)",
        "I have a colleague I like to play tennis with.",
        ["теннис: tennis"],
        alt=["с которой"]),
     it("C", PC, "rel_trap", "Это поездка, ___ я мечтал всю жизнь.", "который", "о которой",
        ["которой", "к которой", "о котором"],
        "мечтать о + prepositional. Поездка is feminine → о которой, not bare которой and not к которой. (Steps 5, 6 and 7)",
        "This is a trip I had dreamed of all my life.",
        ["мечтать: to dream of"]),
     it("C", PC, "rel_trap", "Это лекарство, ___ я привык.", "который", "к которому",
        ["которое", "к которой", "которому"],
        "привыкнуть к + dative. Лекарство is neuter → к которому, not bare которое. (Steps 5, 6 and 7)",
        "This is the medicine I have gotten used to.",
        ["привыкнуть: to get used to", "лекарство: medicine"]),
     it("C", PC, "rel_trap", "Ольга дала мне книгу, ___ мне нужна.", "который", "которая",
        ["которую", "которой", "которое"],
        "книга мне нужна: книга is the subject of нужна, so nominative которая — not accusative которую. English “a book which I need” is the trap. (Steps 5, 6 and 7)",
        "Olga gave me a book that I need."),
     it("C", PC, "rel_trap", "О ___ вы мечтаете? О жене.", "о ком", "ком",
        ["чём", "которой", "ком-то"],
        "For a person the question is о ком, not о чём. The answer О жене is prepositional, but the question-word is ком. (Step 6)",
        "About whom are you dreaming? About my wife."),
     it("C", PC, "rel_trap", "О ___ вы любите говорить с друзьями? О машинах.", "о чём", "чём",
        ["ком", "чём-то", "которых"],
        "For things the question is о чём, not о ком. (Step 6)",
        "What do you like to talk about with friends? About cars."),
     it("C", PC, "rel_trap", "Коллега Анна, ___ я работаю, живёт в Гомеле.", "который", "с которой",
        ["с которым", "которой", "с которому"],
        "работать с + instrumental. Анна is a woman, so even though коллега is common gender, agreement follows her sex: с которой, not с которым. (Step 6)",
        "My colleague Anna, who I work with, lives in Gomel."),
     it("C", PC, "rel_trap", "Это люди, ___ я горжусь.", "который", "которыми",
        ["которых", "с которыми", "которым"],
        "гордиться + instrumental, no с: которыми. С которыми would be “with whom.” (Step 5)",
        "These are people I am proud of.",
        ["гордиться: to be proud of"]),
     it("C", PC, "rel_trap", "Фермер, ___ мы помогаем, держит кур.", "который", "которому",
        ["которого", "которым", "который"],
        "помогать кому? → dative которому. Not accusative которого. (Step 5)",
        "The farmer we are helping keeps hens.",
        ["помогать: to help", "держит кур: keeps hens"]),
    ]
    assert len(EX) == 32, len(EX)
    return {
      "id": "LK",
      "title": "The relative pronoun который",
      "goal": "By the end you'll join two sentences with который, take gender and number from the head noun and case from the relative clause, and keep the preposition: Это человек, который работает в магазине. Друг, которого я видел. Книга, которая мне нужна.",
      "minutes": "20–25 min to read, then %d exercises" % len(EX),
      "sections": S,
      "parts": {"A": PA, "B": PB, "C": PC},
      "practice": {
        "title": "Now use it: write to your tutor",
        "text": "Answer in chat: Who or what did you see, need, or dream of this week? Write 4 sentences with который: one nominative (X, который/которая works…), one animate accusative (друг, которого…), one with a preposition that stays (в котором / о которой / с которым), and one trap (нужна → которая, привыкнуть к, мечтать о, or коллега).",
        "examples": ["Это человек, который работает в магазине.", "Я видел друга, которого знаю из Минска.", "Я прочитал роман, о котором все говорят.", "Ольга дала мне книгу, которая мне нужна."]
      },
      "exercises": EX,
    }
