# Adds the "какой / какая / какое / какие" grammar drills (cat "kakoy") to exercises.json.
# Idempotent: run from the repo root.  python3 src/kakoy_exercises.py
import json
A,B="A1-A2","B1-C1"
# The full table (correct forms)
F={"m":{"N":"какой","A":"какой","AA":"какого","G":"какого","D":"какому","I":"каким","P":"каком"},
   "n":{"N":"какое","A":"какое","G":"какого","D":"какому","I":"каким","P":"каком"},
   "f":{"N":"какая","A":"какую","AA":"какую","G":"какой","D":"какой","I":"какой","P":"какой"},
   "p":{"N":"какие","A":"какие","AA":"каких","G":"каких","D":"каким","I":"какими","P":"каких"}}
SUB={"N":"nominative: какой / какая / какое / какие","A":"accusative (things): какой / какую / какое / какие",
     "AA":"accusative (people, animals): какого / какую / каких","P":"prepositional (в / на / о): каком / какой / каких",
     "G":"genitive (из / у / для / без): какого / какой / каких","D":"dative (к / по): какому / какой / каким",
     "I":"instrumental (с / чем?): каким / какой / какими"}
LV={"N":A,"A":A,"P":A,"AA":B,"G":B,"D":B,"I":B}
GN={"m":"masculine","n":"neuter","f":"feminine","p":"plural"}
# (gender, case, sentence, head noun as written, translation, explanation, glosses)
X=[
# --- tutor's sentences (verbatim) ---
("m","N","___ сегодня день?","день","What day is it today?","День is masculine and the subject (nominative) → какой.",[]),
("f","N","___ у тебя машина?","машина","What kind of car do you have?","Машина is feminine; у тебя (есть) машина — машина is the subject, nominative → какая.",[]),
("f","P","В ___ стране ты живёшь?","стране","Which country do you live in?","Где? в + prepositional. Страна is feminine → в какой стране.",[]),
("f","A","___ ручку ты купил?","ручку","Which pen did you buy?","Ручка is feminine, the object of купил → accusative какую.",["ручка: pen"]),
("f","G","Для ___ подруги этот подарок?","подруги","Which friend is this present for?","Для always takes the genitive. Подруга is feminine → для какой подруги.",["подарок: present, gift"]),
("f","A","___ машину ты любишь?","машину","Which car do you like?","Машина is feminine, the object of любишь → accusative какую.",[]),
("m","N","___ фрукт тебе нравится?","фрукт","Which fruit do you like?","With нравится the thing you like is the subject (nominative). Фрукт is masculine → какой.",["фрукт: fruit"]),
("n","N","___ мясо тебе нравится?","мясо","What meat do you like?","With нравится the thing you like is nominative. Мясо is neuter → какое.",["мясо: meat"]),
("f","N","___ страна тебе нравится?","страна","Which country do you like?","With нравится the thing you like is nominative. Страна is feminine → какая.",[]),
("f","A","___ собаку ты любишь?","собаку","Which dog do you love?","Собака is feminine, object of любишь → какую. (Feminine accusative is -ую for animals too.)",["собака: dog"]),
# --- nominative ---
("m","N","___ твой любимый ресторан?","ресторан","What's your favorite restaurant?","Ресторан is masculine, the subject → какой.",["любимый: favorite"]),
("m","N","___ город тебе больше нравится — Минск или Джексон?","город","Which city do you like more, Minsk or Jackson?","With нравится the thing you like is nominative. Город is masculine → какой.",[]),
("n","N","___ сегодня число?","число","What's the date today?","Число is neuter, the subject → какое. A set phrase: Какое сегодня число?",["число: date (day of month)"]),
("n","N","___ у вас фирменное блюдо?","блюдо","What's your signature dish?","Блюдо is neuter, the subject → какое.",["фирменное блюдо: signature dish"]),
("f","N","___ сегодня погода?","погода","What's the weather like today?","Погода is feminine, the subject → какая.",["погода: weather"]),
("f","N","___ музыка тебе нравится?","музыка","What music do you like?","With нравится the thing you like is nominative. Музыка is feminine → какая.",[]),
("p","N","___ у тебя планы на выходные?","планы","What are your plans for the weekend?","Планы is plural, the subject → какие.",["выходные: weekend"]),
("p","N","___ фрукты тебе нравятся?","фрукты","Which fruits do you like?","Plural subject → нравятся (not нравится) and какие.",[]),
("p","N","___ брюки тебе нравятся — синие или чёрные?","брюки","Which trousers do you like, the blue or the black?","Брюки exists only in the plural → какие, and the verb is нравятся.",["брюки: trousers","синий: blue"]),
("p","N","___ деньги у тебя есть — доллары или рубли?","деньги","What money do you have, dollars or rubles?","Деньги is always plural. У тебя есть деньги → subject, nominative какие.",["деньги: money"]),
# --- accusative, things ---
("m","A","___ хлеб ты купил?","хлеб","What bread did you buy?","Хлеб is masculine and not alive: accusative looks like nominative → какой.",["хлеб: bread"]),
("m","A","___ кофе вы будете?","кофе","What coffee will you have?","Кофе is masculine (an exception!). Object of будете, not alive → какой. (In casual speech you may hear какое кофе, but какой is the standard.)",[]),
("m","A","___ язык ты учишь?","язык","Which language are you learning?","Язык is masculine, not alive → accusative = nominative: какой.",["учить: to study"]),
("n","A","___ вино вы посоветуете?","вино","Which wine would you recommend?","Вино is neuter. Neuter accusative = nominative → какое.",["посоветовать: to recommend"]),
("n","A","___ молоко ты обычно покупаешь?","молоко","What milk do you usually buy?","Молоко is neuter, object of покупаешь → какое.",[]),
("f","A","___ музыку ты слушаешь?","музыку","What music do you listen to?","Музыка is feminine, object of слушаешь → какую.",[]),
("f","A","___ книгу ты сейчас читаешь?","книгу","What book are you reading now?","Книга is feminine, object of читаешь → какую.",[]),
("p","A","___ языки ты знаешь?","языки","Which languages do you know?","Plural, not alive: accusative = nominative → какие.",[]),
("p","A","___ продукты ты купил в магазине?","продукты","What groceries did you buy at the store?","Plural things: accusative = nominative → какие.",["продукты: groceries"]),
("p","A","___ брюки ты наденешь в церковь?","брюки","Which trousers will you wear to church?","Брюки is plural-only and not alive → accusative какие.",["надеть: to put on"]),
# --- prepositional ---
("m","P","В ___ городе ты живёшь?","городе","Which city do you live in?","Где? в + prepositional. Город is masculine → в каком городе.",[]),
("m","P","На ___ этаже твой офис?","этаже","What floor is your office on?","Где? на + prepositional. Этаж is masculine → на каком этаже.",["этаж: floor, storey"]),
("n","P","В ___ кафе мы встречаемся?","кафе","Which café are we meeting at?","Кафе is neuter (it never changes) → в каком кафе.",["встречаться: to meet"]),
("f","P","В ___ церкви ты был в воскресенье?","церкви","Which church were you at on Sunday?","Где? в + prepositional. Церковь is feminine → в какой церкви.",["воскресенье: Sunday"]),
("f","P","На ___ улице твой дом?","улице","What street is your house on?","Улица takes на. Prepositional feminine → на какой улице.",[]),
("f","P","На ___ кассе можно платить картой?","кассе","At which register can I pay by card?","Касса takes на. Prepositional feminine → на какой кассе.",["платить картой: pay by card"]),
("m","P","О ___ фильме ты говоришь?","фильме","Which film are you talking about?","О (about) takes the prepositional. Фильм is masculine → о каком фильме.",[]),
("p","P","В ___ странах ты был?","странах","Which countries have you been to?","Где? в + prepositional plural → в каких странах.",[]),
("p","P","На ___ языках ты говоришь?","языках","Which languages do you speak?","Говорить на языке: на + prepositional. Plural → на каких языках.",[]),
("p","P","В ___ брюках ты пойдёшь в церковь?","брюках","Which trousers will you wear to church?","В брюках = wearing trousers: в + prepositional plural → в каких брюках.",[]),
# --- animate accusative ---
("m","AA","___ врача ты посоветуешь?","врача","Which doctor would you recommend?","Врач is masculine and a person: accusative = genitive → какого.",["врач: doctor"]),
("m","AA","___ брата ты ждёшь — старшего или младшего?","брата","Which brother are you waiting for, the older or the younger?","Брат is a masculine person: accusative = genitive → какого.",["старший / младший: older / younger"]),
("m","AA","___ кота ты хочешь взять?","кота","Which cat do you want to take?","Кот is a masculine animal: accusative = genitive → какого.",["кот: cat (male)"]),
("p","AA","___ друзей ты пригласил на ужин?","друзей","Which friends did you invite to dinner?","Друзья are people: plural accusative = genitive → каких.",["пригласить: to invite","ужин: dinner"]),
("p","AA","___ животных ты любишь?","животных","Which animals do you like?","Животные are alive: plural accusative = genitive → каких.",["животное: animal"]),
# --- genitive ---
("m","G","Из ___ города ты приехал?","города","Which city did you come from?","Из takes the genitive. Город is masculine → из какого города.",["приехать: to arrive"]),
("m","G","У ___ врача ты был?","врача","Which doctor did you go to?","У (at someone's) takes the genitive → у какого врача.",[]),
("n","G","Из ___ мяса этот суп?","мяса","What meat is this soup made from?","Из takes the genitive. Мясо is neuter → из какого мяса.",[]),
("n","G","До ___ числа нужно заплатить?","числа","By what date do I need to pay?","До takes the genitive. Число is neuter → до какого числа.",["заплатить: to pay"]),
("f","G","Из ___ страны твой друг?","страны","Which country is your friend from?","Из takes the genitive. Страна is feminine → из какой страны.",[]),
("f","G","У ___ кассы очередь меньше?","кассы","Which register has the shorter line?","У (by, next to) takes the genitive. Касса is feminine → у какой кассы.",["очередь: line, queue"]),
("p","G","___ продуктов у нас нет?","продуктов","Which groceries are we out of?","Нет takes the genitive. Plural → каких продуктов.",[]),
("p","G","___ документов не хватает?","документов","Which documents are missing?","Не хватает takes the genitive. Plural → каких документов.",["не хватает: is/are missing"]),
("p","G","Для ___ документов нужна печать?","документов","Which documents need a stamp?","Для takes the genitive. Plural → для каких документов.",["печать: stamp, seal"]),
# --- dative ---
("m","D","К ___ врачу ты идёшь?","врачу","Which doctor are you going to?","К (to a person) takes the dative. Врач is masculine → к какому врачу.",[]),
("m","D","По ___ адресу мы едем?","адресу","What address are we going to?","По takes the dative. Адрес is masculine → по какому адресу.",["адрес: address"]),
("n","D","К ___ блюду подходит это вино?","блюду","Which dish does this wine go with?","Подходить к + dative. Блюдо is neuter → к какому блюду.",["подходить: to suit, go with"]),
("f","D","По ___ дороге лучше ехать в Минск?","дороге","Which road is it better to take to Minsk?","По takes the dative. Дорога is feminine → по какой дороге.",["дорога: road"]),
("f","D","___ подруге ты пишешь?","подруге","Which friend are you writing to?","Писать кому? → dative. Подруга is feminine → какой подруге.",[]),
("p","D","По ___ дням работает магазин?","дням","On which days is the store open?","По + dative plural (on which days) → по каким дням.",[]),
("p","D","По ___ праздникам ты ходишь в церковь?","праздникам","On which holidays do you go to church?","По + dative plural → по каким праздникам.",["праздник: holiday, feast"]),
# --- instrumental ---
("m","I","С ___ другом ты ездил в Минск?","другом","Which friend did you go to Minsk with?","С (with) takes the instrumental. Друг is masculine → с каким другом.",[]),
("m","I","___ транспортом ты ездишь на работу?","транспортом","How do you get to work? (what transport)","Ездить чем? → instrumental. Транспорт is masculine → каким транспортом.",["транспорт: transport"]),
("n","I","С ___ мясом эти пирожки?","мясом","What meat are these pies filled with?","С (with) takes the instrumental. Мясо is neuter → с каким мясом.",["пирожки: little pies"]),
("f","I","___ картой вы будете платить?","картой","Which card will you pay with?","Платить чем? → instrumental. Карта is feminine → какой картой.",["карта: card"]),
("f","I","Над ___ задачей ты сейчас работаешь?","задачей","Which task are you working on now?","Работать над + instrumental. Задача is feminine → над какой задачей.",["задача: task"]),
("p","I","С ___ программами ты работаешь?","программами","Which programs do you work with?","С (with) takes the instrumental. Plural → с какими программами.",["программа: program, software"]),
("p","I","С ___ друзьями ты был в ресторане?","друзьями","Which friends were you at the restaurant with?","С (with) takes the instrumental. Plural → с какими друзьями.",[]),
("n","A","___ окно можно открыть?","окно","Which window can I open?","Окно is neuter. Neuter accusative = nominative → какое.",["открыть: to open"]),
("n","P","В ___ здании твой офис?","здании","Which building is your office in?","Где? в + prepositional. Здание is neuter → в каком здании.",["здание: building"]),
("n","P","На ___ месте мы встречаемся?","месте","Where (at what spot) are we meeting?","На + prepositional. Место is neuter → на каком месте.",["место: place, spot"]),
("n","D","По ___ расписанию ходит автобус?","расписанию","What schedule does the bus run on?","По takes the dative. Расписание is neuter → по какому расписанию.",["расписание: schedule"]),
("m","D","___ другу ты звонил?","другу","Which friend did you call?","Звонить кому? → dative. Друг is masculine → какому другу.",["звонить: to call"]),
("n","I","Перед ___ зданием мы встречаемся?","зданием","Which building are we meeting in front of?","Перед takes the instrumental. Здание is neuter → перед каким зданием.",["перед: in front of"]),
]
ORDER=["m","f","n","p"]; CASES=["N","A","G","D","I","P"]
def distractors(g,c,a):
    cc="A" if c=="AA" else c
    same_case=[F[x].get(c,F[x][cc]) for x in ORDER if x!=g]
    same_gen=[F[g][k] for k in CASES if k!=cc]
    out=[]
    for pair in zip(same_case+[None]*6,same_gen):
        for o in pair:
            if o and o!=a and o not in out: out.append(o)
    return out[:3]
def cap(w,on): return w[0].upper()+w[1:] if on else w
if __name__=="__main__":
    ex=[e for e in json.load(open('exercises.json')) if e.get('cat')!='kakoy']
    nid=max(e['id'] for e in ex)+1
    for g,c,s,noun,tr,expl,gl in X:
        a=F[g][c]; d=distractors(g,c,a); up=s.startswith('___')
        assert s.count('___')==1 and len(set(d))==3 and a not in d, s
        ex.append(dict(id=nid,level=LV[c],cat="kakoy",sub=SUB[c],s=s,base="какой",a=cap(a,up),alt=[],
                       d=[cap(x,up) for x in d],ex=expl,translation=tr,glosses=gl)); nid+=1
    json.dump(ex,open('exercises.json','w'),ensure_ascii=False,indent=1)
    print(len(X),'kakoy exercises;',sum(1 for x in X if LV[x[1]]==A),'A1-A2,',sum(1 for x in X if LV[x[1]]==B),'B1-C1; total',len(ex))
