# Adds the "At home" grammar drills (cat "home") to exercises.json. Idempotent: run from the repo root.
import json
A,B="A1-A2","B1-C1"
G={"в/на+prep":"где? в / на + prepositional","в/на+acc":"куда? в / на + accusative","в или на":"в или на?","дома":"дома / домой",
   "lie":"стоять / лежать / висеть","put":"поставить / положить / повесить","asp":"aspect at home"}
X=[
(A,"в/на+prep","Мама сейчас на ___.","кухня","кухне",[],["кухню","кухня","кухней"],"Кухня takes на, not в: на кухне (in the kitchen). Где? → prepositional, -а/-я → -е.","Mom is in the kitchen now.",["сейчас: now"]),
(A,"в/на+prep","Ключи лежат на ___.","стол","столе",[],["стол","стола","столу"],"Где? → на + prepositional: на столе.","The keys are on the table.",["ключи: keys","лежать: to lie"]),
(A,"в/на+prep","Пальто висит в ___.","шкаф","шкафу",[],["шкафе","шкаф","шкафа"],"Шкаф has a special location ending -у after в/на: в шкафу (but о шкафе, 'about the wardrobe').","The coat is hanging in the wardrobe.",["пальто: coat","висеть: to hang"]),
(A,"в/на+prep","Кошка спит на ___.","пол","полу",[],["поле","пол","пола"],"Пол takes the special location ending -у: на полу. (В поле means 'in a field'!)","The cat is sleeping on the floor.",["кошка: cat","спать: to sleep"]),
(A,"в/на+prep","Стул стоит в ___.","угол","углу",[],["угле","угол","угла"],"Угол loses its о (угл-) and takes the special location ending -у: в углу.","The chair is standing in the corner.",["стоять: to stand"]),
(A,"в/на+prep","Мы сидим в ___.","гостиная","гостиной",[],["гостиную","гостиная","гостиные"],"Гостиная (like ванная, прихожая) declines like an adjective: в гостиной.","We're sitting in the living room.",["сидеть: to sit"]),
(A,"в/на+acc","Положи ключи на ___.","стол","стол",[],["столе","стола","столом"],"Положить (to put) answers куда? → на + accusative. Masculine things don't change: на стол.","Put the keys on the table.",["положить: to put (lying)"]),
(A,"в/на+acc","Поставь молоко в ___.","холодильник","холодильник",[],["холодильнике","холодильника","холодильнику"],"Куда? → в + accusative: в холодильник. Compare где? → в холодильнике.","Put the milk in the fridge.",["поставить: to put (standing)"]),
(A,"в/на+acc","Повесь пальто на ___.","вешалка","вешалку",[],["вешалке","вешалка","вешалки"],"Куда? → на + accusative, -а → -у: на вешалку. Compare где? → на вешалке.","Hang your coat on the coat rack.",["повесить: to hang (up)","вешалка: coat rack"]),
(A,"в/на+acc","Иди на ___, там чай.","кухня","кухню",[],["кухне","кухня","кухни"],"Куда? → на + accusative, -я → -ю: на кухню.","Go to the kitchen, there's tea there.",["иди: go!"]),
(A,"в/на+acc","Сними куртку и повесь её в ___.","шкаф","шкаф",[],["шкафу","шкафе","шкафа"],"Куда? → в + accusative: в шкаф. The -у form (в шкафу) is only for где?","Take off your jacket and hang it in the wardrobe.",["снять: to take off","куртка: jacket"]),
(A,"в/на+acc","Поставь обувь у ___.","дверь","двери",[],["дверь","дверью","дверей"],"У (by, next to) takes the genitive: у двери. It works for both где? and куда?","Put your shoes by the door.",["обувь: shoes"]),
(A,"в или на","Чашки стоят ___ полке.","в / на / у","на",[],["в","у","под"],"A shelf is a surface, so на: на полке.","The cups are on the shelf.",["чашка: cup","полка: shelf"]),
(A,"в или на","Курица ___ духовке.","в / на / у","в",[],["на","у","с"],"An oven is a box you put things inside, so в: в духовке.","The chicken is in the oven.",["курица: chicken","духовка: oven"]),
(A,"в или на","Мы пьём чай ___ кухне.","в / на / у","на",[],["в","у","к"],"Кухня is the exception among rooms: на кухне. Other rooms take в: в комнате, в спальне, в ванной.","We drink tea in the kitchen.",["пить: to drink"]),
(A,"в или на","Дети играют ___ комнате.","в / на / у","в",[],["на","у","к"],"Rooms take в: в комнате, в спальне, в гостиной (but на кухне).","The kids are playing in the room.",["дети: children","играть: to play"]),
(A,"в или на","Он пьёт кофе ___ балконе.","в / на / у","на",[],["в","у","к"],"A balcony is an open platform, so на: на балконе.","He drinks coffee on the balcony.",[]),
(A,"в или на","Картина висит ___ стене.","в / на / у","на",[],["в","у","о"],"Things hang on the surface of a wall: на стене.","The picture is hanging on the wall.",["картина: picture, painting"]),
(A,"в или на","Ключи висят ___ двери.","в / на / у","у",[],["в","к","с"],"У + genitive means 'by, next to': у двери (by the door), у окна (by the window).","The keys hang by the door.",["ключи: keys"]),
(A,"дома","Я сейчас ___.","дом","дома",[],["домой","дом","доме"],"Дома = at home (где?). Домой = (to) home (куда?).","I'm at home now.",[]),
(A,"дома","Уже поздно, пора ___.","дом","домой",[],["дома","дом","доме"],"Пора домой (time to go home) is about direction, so домой.","It's late, time to go home.",["пора: it's time"]),
(B,"lie","Тарелки ___ на столе.","стоять / лежать / висеть","стоят",[],["лежат","висят","ставят"],"Russian says plates, cups and glasses стоят (stand) on the table, even though plates are flat.","The plates are on the table.",["тарелка: plate"]),
(B,"lie","Вилки и ножи ___ на столе.","стоять / лежать / висеть","лежат",[],["стоят","висят","кладут"],"Forks and knives lie flat: лежат.","The forks and knives are on the table.",["вилка: fork","нож: knife"]),
(B,"lie","Пальто ___ на вешалке.","стоять / лежать / висеть","висит",[],["стоит","лежит","вешает"],"Clothes on a hook or rack висят (hang).","The coat is hanging on the coat rack.",[]),
(B,"lie","Ботинки ___ у двери.","стоять / лежать / висеть","стоят",[],["лежат","висят","ставят"],"Shoes standing on the floor стоят.","The boots are by the door.",["ботинки: boots, shoes"]),
(B,"lie","Телефон ___ на диване.","стоять / лежать / висеть","лежит",[],["стоит","висит","кладёт"],"A phone lying flat лежит.","The phone is on the sofa.",["диван: sofa"]),
(B,"lie","Холодильник ___ на кухне.","стоять / лежать / висеть","стоит",[],["лежит","висит","ставит"],"Furniture and appliances стоят: холодильник стоит, шкаф стоит, диван стоит.","The fridge is in the kitchen.",[]),
(B,"put","___ пальто на вешалку.","повесить / поставить / положить","Повесь",[],["Поставь","Положи","Висит"],"Where something will hang → повесить (impf. вешать).","Hang your coat on the coat rack.",[]),
(B,"put","___ вилки на стол.","повесить / поставить / положить","Положи",[],["Поставь","Повесь","Лежат"],"Things that will lie flat → положить (impf. класть).","Put the forks on the table.",[]),
(B,"put","___ стакан на полку.","повесить / поставить / положить","Поставь",[],["Положи","Повесь","Стоит"],"Things that will stand upright → поставить (impf. ставить).","Put the glass on the shelf.",["стакан: glass"]),
(B,"asp","Каждый вечер я ___ ключи на крючок.","вешать / повесить","вешаю",[],["повешу","повесил","вишу"],"Repeated action (каждый вечер) → imperfective вешать: я вешаю.","Every evening I hang my keys on the hook.",["крючок: hook"]),
(B,"asp","Куда ты ___ мои очки? Не могу их найти.","класть / положить","положил",["положила"],["клал","кладёшь","лежал"],"One completed action whose result matters now (I can't find them) → perfective положить.","Where did you put my glasses? I can't find them.",["очки: glasses"]),
(B,"asp","Где можно ___ руки?","мыть / помыть","помыть",["вымыть"],["мыть","моет","помою"],"A single concrete action after можно → perfective: помыть (or вымыть).","Where can I wash my hands?",["рука: hand"]),
(B,"asp","Можно ___ обувь?","снимать / снять","снять",[],["снимать","сниму","снял"],"Asking permission for one action → perfective снять.","May I take off my shoes?",["обувь: shoes"]),
(B,"asp","Проходите, ___!","садиться / сесть","садитесь",[],["сидите","садиться","сидеть"],"A warm invitation to sit down uses the imperfective imperative: садитесь. Сидите means 'stay seated'.","Come in, have a seat!",["проходите: come in"]),
]
ex=[e for e in json.load(open('exercises.json')) if e.get('cat')!='home']
nid=max(e['id'] for e in ex)+1
for lv,sub,s,base,a,alt,d,expl,tr,gl in X:
    assert s.count('___')==1 and a not in d and len(set(d))==3, s
    ex.append(dict(id=nid,level=lv,cat="home",sub=G[sub],s=s,base=base,a=a,alt=alt,d=d,ex=expl,translation=tr,glosses=gl)); nid+=1
json.dump(ex,open('exercises.json','w'),ensure_ascii=False,indent=1)
print(len(X),'home exercises;',sum(1 for x in X if x[0]==A),'A1-A2,',sum(1 for x in X if x[0]==B),'B1-C1; total',len(ex))
