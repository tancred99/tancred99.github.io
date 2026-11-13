# Adds the "никогда / иногда / всегда / часто / редко" grammar drills (cat "frequency") to exercises.json.
# Idempotent: run from the repo root.  python3 src/frequency_exercises.py
# Two item kinds:
#   gap  - pick the adverb that the context clue demands (typeable too)
#   pick - choose the one correct sentence for an English meaning (double negative / extra не), choice only
import json
A,B="A1-A2","B1-C1"
ADV="никогда · иногда · всегда · часто · редко"
S_CLUE="context clues: which adverb?"
S_NEG="никогда + не: the double negative"
S_BCLUE="ни разу, почти никогда, время от времени"
S_BNEG="multiple negation: никто, ничего, никуда + не"
# gap items: (level, sub, sentence, answer, distractors, translation, explanation, glosses)
G=[
# --- A1-A2: context clues ---
(A,S_CLUE,"Мой друг ___ звонит мне в субботу, но не каждую неделю.","иногда",["всегда","никогда"],
 "My friend sometimes calls me on Saturday, but not every week.",
 "Clue: «но не каждую неделю» (but not every week) = not always, but it happens → иногда. Всегда contradicts the clue; никогда would also need не before the verb.",["звонить: to call"]),
(A,S_CLUE,"Я ___ не курю.","никогда",["всегда","часто","редко"],
 "I never smoke.",
 "The не before the verb (курю) is the clue: Russian uses a double negative, никогда + не + verb = never. «Всегда/часто/редко не курю» makes no sense.",["курить: to smoke"]),
(A,S_CLUE,"Батюшка ___ приходит в церковь рано. Каждое утро в семь часов он уже там.","всегда",["никогда","редко","иногда"],
 "Father always comes to church early. Every morning at seven he is already there.",
 "Clue: «каждое утро» (every morning, no exceptions) → всегда. Редко and иногда contradict «каждое утро»; никогда would need не.",["батюшка: Father (priest)","приходить: to arrive, come"]),
(A,S_CLUE,"Я ___ хожу в церковь в воскресенье, каждую неделю.","всегда",["иногда","редко","никогда"],
 "I always go to church on Sunday, every week.",
 "Clue: «каждую неделю» (every week) → всегда. Ходить (not идти) because it is a regular, repeated action.",["ходить: to go (regularly)"]),
(A,S_CLUE,"Я ___ не был в Москве.","никогда",["всегда","часто","иногда"],
 "I have never been to Moscow.",
 "Не + был (past tense of быть) = haven't been. With the double negative: никогда не был = have never been.",[]),
(A,S_CLUE,"Мы с женой ___ ходим в ресторан: только раз в год, на годовщину.","редко",["всегда","часто","никогда"],
 "My wife and I rarely go to a restaurant: only once a year, on our anniversary.",
 "Clue: «только раз в год» (only once a year) → редко (rarely). Никогда would need не and would contradict «раз в год».",["годовщина: anniversary"]),
(A,S_CLUE,"Жена ___ покупает хлеб в этом магазине: почти каждый день.","часто",["всегда","редко","никогда"],
 "My wife often buys bread in this store: almost every day.",
 "Clue: «почти каждый день» (almost every day) → часто (often). «Почти» rules out всегда (always = every time).",["хлеб: bread"]),
(A,S_CLUE,"Я ___ пью кофе утром. Без кофе я не могу работать!","всегда",["никогда","редко","иногда"],
 "I always drink coffee in the morning. I can't work without coffee!",
 "Clue: «без кофе я не могу работать» (I can't work without coffee) → every morning → всегда.",["без + genitive: without"]),
(A,S_CLUE,"Мой друг живёт в Беларуси, поэтому мы ___ видимся: раз в два-три года.","редко",["часто","всегда","никогда"],
 "My friend lives in Belarus, so we rarely see each other: once every two or three years.",
 "Clue: «раз в два-три года» (once every two or three years) → редко.",["видеться: to see each other","поэтому: so, that's why"]),
(A,S_CLUE,"Я ___ не смотрю телевизор. У нас дома нет телевизора.","никогда",["часто","всегда","иногда"],
 "I never watch TV. We don't have a TV at home.",
 "Clue: there is no TV at home, and не stands before the verb → никогда не смотрю (double negative).",["телевизор: TV set"]),
(A,S_CLUE,"Я ___ гуляю в парке: два-три раза в неделю.","часто",["никогда","редко","всегда"],
 "I often walk in the park: two or three times a week.",
 "Clue: «два-три раза в неделю» (two or three times a week) → часто. Not every day, so not всегда.",["гулять: to stroll, take a walk"]),
(A,S_CLUE,"Я ___ не ем мясо в пятницу: в пятницу пост.","никогда",["всегда","часто","иногда"],
 "I never eat meat on Friday: Friday is a fast day.",
 "Clue: Friday is a fast day, and не stands before the verb → никогда не ем. (Ем is the я-form of the irregular verb есть, to eat.)",["пост: fast (religious)","мясо: meat"]),
(A,S_CLUE,"В магазине я ___ плачу картой. У меня нет наличных.","всегда",["никогда","редко","иногда"],
 "In the store I always pay by card. I don't have any cash.",
 "Clue: «у меня нет наличных» (I have no cash) → card every time → всегда. Картой is instrumental: pay with what?",["платить (плачу): to pay","наличные: cash"]),
(A,S_CLUE,"Мой друг ___ пишет мне письма: может быть, одно письмо в год.","редко",["часто","всегда","никогда"],
 "My friend rarely writes me letters: maybe one letter a year.",
 "Clue: «одно письмо в год» (one letter a year) → редко.",["письмо: letter"]),
(A,S_CLUE,"Ты работаешь в субботу? — ___. Не каждую субботу.","Иногда",["Всегда","Никогда"],
 "Do you work on Saturday? — Sometimes. Not every Saturday.",
 "Clue: «не каждую субботу» (not every Saturday) → it happens, but not always → иногда.",[]),
(A,S_CLUE,"Я ___ слушаю музыку в машине: каждый раз, когда я еду на работу.","всегда",["никогда","редко","иногда"],
 "I always listen to music in the car: every time I drive to work.",
 "Clue: «каждый раз» (every time) → всегда.",["каждый раз: every time"]),
(A,S_CLUE,"Ты ___ звонишь другу в Беларусь? — Да, почти каждый день.","часто",["никогда","редко","всегда"],
 "Do you often call your friend in Belarus? — Yes, almost every day.",
 "Clue: «почти каждый день» (almost every day) → часто. «Почти» rules out всегда. Звонить кому? → dative: другу.",[]),
(A,S_CLUE,"Я ___ покупаю рыбу. Я не очень люблю рыбу, поэтому покупаю её раз в два месяца.","редко",["часто","всегда","никогда"],
 "I rarely buy fish. I don't really like fish, so I buy it once every two months.",
 "Clue: «не очень люблю» and «раз в два месяца» (once every two months) → редко.",["рыба: fish"]),
(A,S_CLUE,"___ я пью чай, а иногда — кофе.","Иногда",["Всегда","Никогда"],
 "Sometimes I drink tea, and sometimes coffee.",
 "The fixed pattern «иногда…, а иногда…» = sometimes…, and sometimes…. Всегда contradicts «а иногда кофе»; никогда would need не.",[]),
# --- B1-C1 ---
(B,S_BCLUE,"Я ___ не был в Беларуси, но очень хочу поехать к другу.","ни разу",["редко","иногда","часто"],
 "I have never once been to Belarus, but I really want to go visit my friend.",
 "Ни разу (not once) works like никогда: it is a negative word, so the verb needs не → ни разу не был. Note the spelling: ни разу, not «не разу».",["ни разу: not once"]),
(B,S_BCLUE,"Мы с женой ___ не ходим в кино — может быть, раз в три года.","почти никогда",["почти всегда","часто","время от времени"],
 "My wife and I almost never go to the movies — maybe once every three years.",
 "Clue: «раз в три года» (once every three years) → почти никогда (almost never). Like никогда, почти никогда needs не before the verb: почти никогда не ходим.",["кино: the movies"]),
(B,S_BCLUE,"Я ___ хожу в этот ресторан: раз в месяц, не чаще — когда есть время.","время от времени",["всегда","почти всегда","никогда"],
 "I go to this restaurant from time to time: once a month, no more often — when I have time.",
 "Clue: «раз в месяц, не чаще» (once a month, no more often) → время от времени (from time to time), a slightly more bookish synonym of иногда.",["не чаще: no more often","время от времени: from time to time"]),
(B,S_BCLUE,"Мой друг ___ не опаздывает: за десять лет он опоздал только два раза.","почти никогда",["никогда","всегда","часто"],
 "My friend almost never runs late: in ten years he has been late only twice.",
 "Clue: «только два раза» (only twice) → not never, but nearly → почти никогда не. Plain никогда would contradict the two times.",["опаздывать: to be late"]),
(B,S_BCLUE,"Я ___ в жизни не пил текилу.","ни разу",["иногда","часто","редко"],
 "I have never once in my life drunk tequila.",
 "«Ни разу в жизни не…» = never once in my life. Ни разу is negative, so не is required before the verb.",["в жизни: in (my) life"]),
(B,S_BCLUE,"Он ___ не ходит в магазин — всё покупает жена.","никогда",["часто","всегда","редко"],
 "He never goes to the store — his wife buys everything.",
 "Clue: «всё покупает жена» (his wife buys everything) → he never goes → никогда не ходит.",[]),
(B,S_BCLUE,"Я ___ хожу в магазин в воскресенье, только если что-то срочно нужно.","редко",["всегда","часто","никогда"],
 "I rarely go to the store on Sunday, only if something is urgently needed.",
 "Clue: «только если что-то срочно нужно» (only if something is urgent) → редко. Никогда would need не.",["срочно: urgently"]),
(B,S_BCLUE,"Я ___ не видел такой красивой церкви!","никогда",["часто","всегда","редко"],
 "I have never seen such a beautiful church!",
 "Никогда не видел = have never seen. Notice the genitive of negation: after не видел the object often goes into the genitive (такой красивой церкви), not the accusative.",["такой: such"]),
(B,S_BCLUE,"Вы ___ бываете в Минске? — Да, почти каждую неделю, по работе.","часто",["никогда","редко","ни разу"],
 "Do you often come to Minsk? — Yes, almost every week, for work.",
 "Clue: «почти каждую неделю» → часто. Бывать = to be somewhere repeatedly, to visit regularly.",["бывать: to be (somewhere) regularly","по работе: for work"]),
(B,S_BCLUE,"Жена ___ не забывает купить молоко, а я забываю почти каждый раз.","никогда",["часто","всегда","редко"],
 "My wife never forgets to buy milk, but I forget almost every time.",
 "The contrast (а я забываю почти каждый раз) shows she never forgets → никогда не забывает.",["забывать: to forget"]),
(B,S_BNEG,"Я никогда ___ не покупаю в этом магазине.","ничего",["что-то","что","нечего"],
 "I never buy anything in this store.",
 "In a negative sentence every 'any-' word becomes a ни-word: никогда + ничего + не. Что-то (something) can't stand under не here; нечего means 'there is nothing to' and is a different construction.",[]),
(B,S_BNEG,"В субботу мне ___ не звонит.","никто",["кто-то","все","ничего"],
 "Nobody calls me on Saturday.",
 "Никто (nobody) is the subject (nominative) and needs не before the verb: никто не звонит. Все would need a plural verb (звонят); ничего is 'nothing', not a person.",[]),
]
# pick items: (level, sub, English meaning, correct sentence, wrong sentences, explanation)
P=[
(A,S_NEG,"I never drink vodka.","Я никогда не пью водку.",["Я никогда пью водку.","Я иногда не пью водку.","Я ни когда не пью водку."],
 "Никогда needs не before the verb (double negative): никогда не пью. «Иногда не пью» means 'sometimes I don't drink'. Никогда is one word."),
(A,S_NEG,"Sometimes I don't work on Saturday.","Я иногда не работаю в субботу.",["Я никогда не работаю в субботу.","Я иногда ни работаю в субботу.","Я никогда работаю в субботу."],
 "Иногда is not a negative word, so it adds no не of its own; here не is there because the meaning is 'don't work': иногда не работаю. The particle is не, never «ни». Никогда не работаю = never work."),
(A,S_NEG,"My wife always cooks borscht on Sunday.","Жена всегда готовит борщ в воскресенье.",["Жена всегда не готовит борщ в воскресенье.","Жена никогда готовит борщ в воскресенье.","Жена никогда не готовит борщ в воскресенье."],
 "Всегда takes no не: всегда готовит. An extra не reverses the meaning; никогда не готовит = never cooks; никогда without не is ungrammatical."),
(A,S_NEG,"My friend never calls me in the morning.","Мой друг никогда не звонит мне утром.",["Мой друг никогда звонит мне утром.","Мой друг не никогда звонит мне утром.","Мой друг всегда не звонит мне утром."],
 "The не goes right before the verb, after никогда: никогда не звонит. «Не никогда» is wrong order; «всегда не звонит» is not how Russian says 'never'."),
(A,S_NEG,"I often don't understand the priest when he speaks fast.","Я часто не понимаю батюшку, когда он говорит быстро.",["Я никогда понимаю батюшку, когда он говорит быстро.","Я часто понимаю батюшку, когда он говорит быстро.","Я никогда не понимаю батюшку, когда он говорит быстро."],
 "Часто + не + verb = often don't: часто не понимаю. Without не it means 'often understand'; никогда не понимаю (never understand) is too strong."),
(A,S_NEG,"We never rest on Monday.","Мы никогда не отдыхаем в понедельник.",["Мы никогда отдыхаем в понедельник.","Мы всегда отдыхаем в понедельник.","Мы иногда не отдыхаем в понедельник."],
 "Never = никогда не + verb: никогда не отдыхаем. Иногда не отдыхаем = sometimes we don't rest."),
(A,S_NEG,"Nobody here speaks English.","Здесь никто не говорит по-английски.",["Здесь никто говорит по-английски.","Здесь не никто говорит по-английски.","Здесь кто-то не говорит по-английски."],
 "Никто (nobody) works like никогда: it is the subject (nominative) and the verb still needs не → никто не говорит. Кто-то не говорит = someone doesn't speak."),
(A,S_NEG,"I don't buy anything in this store.","Я ничего не покупаю в этом магазине.",["Я ничего покупаю в этом магазине.","Я не покупаю что-то в этом магазине.","Я ничто не покупаю в этом магазине."],
 "'Not … anything' = ничего не. Ничего is the direct object here (genitive form after negation); ничто is only used as a subject or after prepositions, and что-то (something) doesn't go with не like this."),
(A,S_NEG,"I rarely smoke.","Я редко курю.",["Я редко не курю.","Я никогда курю.","Я никогда не курю."],
 "Редко already means 'rarely', so no не: редко курю. Никогда не курю = I never smoke (different meaning)."),
(A,S_NEG,"My wife never watches football.","Жена никогда не смотрит футбол.",["Жена никогда смотрит футбол.","Жена часто не смотрит футбол.","Жена всегда смотрит футбол."],
 "Никогда + не + verb: никогда не смотрит. Часто не смотрит = often doesn't watch (but sometimes does)."),
(B,S_BNEG,"I never buy anything here.","Я здесь никогда ничего не покупаю.",["Я здесь никогда что-то не покупаю.","Я здесь никогда ничего покупаю.","Я здесь не никогда ничего покупаю."],
 "Russian stacks negatives: every 'ever/any' word becomes a ни-word, and there is still one не before the verb: никогда ничего не покупаю."),
(B,S_BNEG,"Nobody ever calls me on Saturday.","В субботу мне никто никогда не звонит.",["В субботу мне никто никогда звонит.","В субботу мне кто-то никогда не звонит.","В субботу мне никто всегда не звонит."],
 "Nobody + ever = никто никогда, plus не before the verb. All the 'any/ever' words go negative together."),
(B,S_BNEG,"I have not been to Moscow even once.","Я ни разу не был в Москве.",["Я ни разу был в Москве.","Я не разу не был в Москве.","Я один раз не был в Москве."],
 "Ни разу (not once) is spelled with ни and needs не before the verb: ни разу не был. «Не разу» is a common spelling mistake, even among native speakers."),
(B,S_BNEG,"I almost never cook.","Я почти никогда не готовлю.",["Я почти никогда готовлю.","Я почти не никогда готовлю.","Я иногда готовлю."],
 "Почти никогда (almost never) behaves like никогда: it needs не before the verb → почти никогда не готовлю."),
(B,S_BNEG,"Sometimes I don't understand anything.","Иногда я ничего не понимаю.",["Иногда я ничего понимаю.","Иногда я что-то не понимаю.","Никогда я ничего понимаю."],
 "Иногда is positive, but ничего (nothing/anything) is negative, so it needs не: ничего не понимаю. «Что-то не понимаю» = there's something I don't understand."),
(B,S_BNEG,"My friend never tells anybody anything.","Мой друг никогда никому ничего не рассказывает.",["Мой друг никогда никому ничего рассказывает.","Мой друг никогда кому-то что-то не рассказывает.","Мой друг не никогда никому ничего рассказывает."],
 "Three ни-words, one не: никогда (never) + никому (to nobody, dative = indirect object) + ничего (nothing, direct object) + не рассказывает."),
(B,S_BNEG,"On Sunday I don't go anywhere except church.","В воскресенье я никуда не хожу, кроме церкви.",["В воскресенье я никуда хожу, кроме церкви.","В воскресенье я нигде не хожу, кроме церкви.","В воскресенье я куда-то не хожу, кроме церкви."],
 "Хожу is a verb of motion, so 'anywhere' answers куда? (where to?) → никуда, with не before the verb. Нигде answers где? (location) and does not fit a motion verb here."),
]
P.append((B,S_BNEG,"Never say \"never\".","Никогда не говори «никогда».",["Никогда говори «никогда».","Не никогда говори «никогда».","Всегда не говори «никогда»."],
 "A common saying. The double negative works in commands too: никогда + не + imperative (говори). The не always stands directly before the verb."))
def cap(w,on): return w[0].upper()+w[1:] if on else w
def items():
    out=[]
    for lv,sub,s,a,d,tr,ex,gl in G:
        assert s.count('___')==1 and a not in d and len(set(d))==len(d)>=2, s
        up=s.startswith('___')
        assert a==cap(a,up), s
        out.append(dict(level=lv,cat="frequency",sub=sub,s=s,base=ADV if lv==A else " · ".join(sorted(x.lower() for x in [a]+d)),a=a,alt=[],d=d,ex=ex,translation=tr,glosses=gl))
    for lv,sub,en,a,d,ex in P:
        assert a not in d and len(set(d))==3, a
        out.append(dict(level=lv,cat="frequency",sub=sub,s="___",base='Which sentence means: "'+en+'"',a=a,alt=[],d=d,ex=ex,translation="",glosses=[],choiceOnly=True))
    return out
if __name__=="__main__":
    ex=[e for e in json.load(open('exercises.json')) if e.get('cat')!='frequency']
    nid=max(e['id'] for e in ex)+1
    new=items()
    # A1-A2 first, then B1-C1 (same ordering idea as kakoy)
    new.sort(key=lambda e:e['level'])
    for e in new:
        e=dict(id=nid,**e); ex.append(e); nid+=1
    json.dump(ex,open('exercises.json','w'),ensure_ascii=False,indent=1)
    print(len(new),'frequency exercises;',sum(1 for x in new if x['level']==A),'A1-A2,',sum(1 for x in new if x['level']==B),'B1-C1; total',len(ex))
