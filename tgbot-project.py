import telebot
import requests
import json
from telebot import types
import config

tgbot = telebot.TeleBot(config.TG_TOKEN)

@tgbot.message_handler(commands=['start', 'return'])
def start(message):
    file_photo_0 = open('./_-2.jpg', 'rb')
    tgbot.send_message(message.chat.id, 'Здравствуйте, вас приветствует телеграмм бот Здоровое питание.\n'
                                        ''
                                        'В этом боте вы найдете все, что касается еды.\n'
                                        'Автор этого бота советует пройтись по всем пунктам этого бота,'
                                        ' чтобы лучше понимать то, как правильно питаться и какая должна'
                                        ' быть норма потребления пищи у человека.\n'
                                        'Если вам интересно ответьте любым сообщением :)')
    tgbot.send_photo(message.chat.id, file_photo_0)
    tgbot.register_next_step_handler(message, start_all)
@tgbot.message_handler(commands=['next'])
def start_all(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Пищевая ценность продукта")
    item2 = types.KeyboardButton("Общая информация")
    item3 = types.KeyboardButton("Расчёт нормы дня")
    markup.add(item2)
    markup.row(item1, item3)
    tgbot.send_message(message.chat.id,  'Выберите один из трех пунктов, '
                                         'который вам наиболее интересен:', reply_markup=markup)
    tgbot.register_next_step_handler(message, answer)

@tgbot.message_handler(content_types=['text'])
def answer(message):
    amount_11 = message.text.strip()
    if amount_11 == "Пищевая ценность продукта":
        tgbot.send_message(message.chat.id, 'Нажмите -> /repeat <-, чтобы перейти к пункту "Пищевая ценность продукта".')
        tgbot.register_next_step_handler(message, start_1)
    elif amount_11 == "Общая информация":
        tgbot.send_message(message.chat.id, 'Нажмите -> /info <-, чтобы перейти к пункту "Общая информация".')
        tgbot.register_next_step_handler(message, information)
    elif amount_11 == "Расчёт нормы дня":
        tgbot.send_message(message.chat.id, 'Нажмите -> /count <-, чтобы перейти к пункту "Расчёт нормы дня".')
        tgbot.register_next_step_handler(message, count_all)
    else:
        tgbot.send_message(message.chat.id, 'Неизвестная команда😵.\n'
                                            'Нажмите -> /next <- и выберите корректное название.')
@tgbot.message_handler(commands=['repeat'])
def start_1(message):
    tgbot.send_message(message.chat.id, 'Напишите название продукта на английском.')
    tgbot.register_next_step_handler(message, foods)
@tgbot.message_handler(content_types=['text'])
def foods(message):
    query = message.text.strip()
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    response = requests.get(api_url + query, headers={'X-Api-Key': 'TMlmjRluaZPtVMZwUlLxNQ==Z4p1aagNU4v35a2T'})
    if response.status_code == 200:
        data = json.loads(response.text)
        data = data['items']
        for i in data:
            tgbot.send_message(message.chat.id, f'В {query} на {str(i['serving_size_g'])} грамм продукта'
                                                f' содержится:\n'
                                            f'{str(i['calories'])} калорий,\n{str(i['protein_g'])} грамм белка,\n'
                                            f'{str(i['fat_total_g'])} грамм жира,\n'
                                            f'{str(i['carbohydrates_total_g'])} грамм углеводов,\n'
                                            f'{str(i['sugar_g'])} грамм сахара.')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Да")
        item2 = types.KeyboardButton("Нет")
        markup.row(item1, item2)
        tgbot.send_message(message.chat.id, 'Не желаете ли снова убедиться в калорийности какого-либо продукта?\n'
                                            'Нажмите "Да" или "Нет".', reply_markup=markup)
        tgbot.register_next_step_handler(message, call_message)
    else:
        tgbot.send_message(message.chat.id, 'Возможно вы ввели название продукта с ошибкой или'
                                            'не на английском языке😵.\n'
                                            'Нажмите -> /repeat <- и заново введите название продукта.')
        tgbot.register_next_step_handler(message, start_1)
@tgbot.message_handler(content_types=['text'])
def call_message(message):
    amount = message.text.strip()
    if amount == 'Да':
        tgbot.send_message(message.chat.id, 'Хорошо☺️.\n'
                                            'Введите -> /repeat <- для ввода продукта.')
        tgbot.register_next_step_handler(message, start_1)
    elif amount == 'Нет':
        tgbot.send_message(message.chat.id, 'Хорошо, я вас понял.\n'
                                            'Нажмите -> /next <-, чтобы вернуться в главное меню.')
        tgbot.register_next_step_handler(message, start_all)

    else:
        tgbot.send_message(message.chat.id, 'Я не понимаю, что вы говорите😵.\nЧтобы узнать калорийность продукта, '
                                            'нажмите -> /repeat <-')

@tgbot.message_handler(commands=['info'])
def information(message):
    file_photo_1 = open('./scale_1200.jpg', 'rb')
    tgbot.send_message(message.chat.id, 'Функции белков, жиров и углеводов в организме.\n'
                                        '\n'
                                        'Белок — основной строительный материал клеток, наше тело состоит из белка'
                                        ' на ? часть: второе место после воды! Из белка образуются стенки клеток,'
                                        ' а значит, и мышцы, ткани, кости и волокна. Отсутствие или недостаток белка'
                                        ' в рационе может привести к последствиям разной степени тяжести: снижению'
                                        ' тонуса мышц, отекам из-за нарушения водно-солевого баланса, ломкости волос,'
                                        ' ногтей, хрупкости костей, замедлению метаболизма.')
    tgbot.send_photo(message.chat.id, file_photo_1)
    file_photo_2 = open('./1682965304m5l6zpgdtj.jpg', 'rb')
    tgbot.send_message(message.chat.id, 'Углеводы выполняют, пожалуй, самую заметную на первый взгляд функцию'
                                        ' — энергетическую. Кроме этого, они участвуют наравне с белками'
                                        ' в «строительстве» клеточных мембран, а также влияют на свертываемость крови.'
                                        ' Еще углеводы — наш основной защитник: так называемые «сложные углеводы»'
                                        ' входят в состав иммунной системы, они защищают нас от проникновения в'
                                        ' организм вирусов и бактерий. В случае с углеводами опасен как недобор их,'
                                        ' так и перебор: недобор ведет к снижению аппетита, вялости, работоспособность'
                                        ' падает, а раздражительность становится привычным состоянием. Перебор'
                                        ' потенциально может привести к сахарному диабету второго типа, ожирению'
                                        ' и атеросклерозу.', )
    tgbot.send_message(message.chat.id, 'Примеры продуктов с простыми углеводами:\n'
                                        '\n'
                                        '- белый хлеб и мучные изделия из белой муки'
                                        ' (торты, пирожные, печенье, булочки);'
                                        '- колбасы;\n'
                                        '- мед;\n'
                                        '- магазинные сладости (напитки, газировка, конфеты);\n'
                                        '- крахмал;\n'
                                        '- быстроотвариваемые макароны из мягких сортов пшеницы;\n'
                                        '- картофель;\n'
                                        '- овощи после термической обработки, с появившимся легкоусваиваемым'
                                        ' крахмалом;\n'
                                        '- обогащенные сахаром консервированные фрукты, легко переходящие в глюкозу;\n'
                                        '- алкоголь, особенно крепкие спиртные напитки и пиво;\n'
                                        '- сахар и изделия с его добавлением, мороженое, варенья, джемы;\n'
                                        '- картофель жареный или фри;\n'
                                        '- фастфуд и почти все блюда в ресторанах быстрого питания, содержащие много'
                                        ' крахмала и сахара.')
    tgbot.send_message(message.chat.id, 'Примеры продуктов со сложными углеводами:\n'
                                        '\n'
                                        '- Овощи и зелень – это, прежде всего, помидоры, лук, кабачки,'
                                        ' сельдерей, капуста, шпинат, латук;\n'
                                        '- Ягоды и фрукты – киви, яблоках, инжире, вишне;\n'
                                        '- Крупы – гречка, пшеница, бурый и белый рисе, овёс;\n'
                                        '- Бобовые и зерновые – макаронные твердых сортов,'
                                        ' ячменные хлопьях, горох, фасоль, чечевица.')
    tgbot.send_photo(message.chat.id, file_photo_2)
    file_photo_3 = open('./h6q07yna6nfc52xr9vksi40l000bz3t3.webp', 'rb')
    tgbot.send_message(message.chat.id, 'Жиры также принимают активное участие в функционировании организма'
                                        ' человека. Они, например, участвуют в дыхании, помогают восстанавливать'
                                        ' мембраны клеток, участвуют в синтезе гормонов. Поэтому безжировые диеты'
                                        ' — это вещь, конечно, интересная, но довольно рисковая.')
    tgbot.send_photo(message.chat.id, file_photo_3)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Да")
    item2 = types.KeyboardButton("Нет")
    markup.row(item1, item2)
    tgbot.send_message(message.chat.id, 'Это была краткая информация о белках, жирах и углеводах😄. Теперь вы'
                                        ' понимаете, какие функции выполняют эти макронутриенты.\n'
                                        'Хотите ли вы узнать о важности баланса в питании?', reply_markup=markup)
    tgbot.register_next_step_handler(message, neeext)

@tgbot.message_handler(content_types=['text'])
def neeext(message):
    amount_111 = message.text.strip()
    if amount_111 == 'Да':
        tgbot.send_message(message.chat.id, 'Хорошо😄.')
        file_photo_4 = open('./volga.jpg', 'rb')
        tgbot.send_message(message.chat.id, 'О важности баланса в питании.\n'
                                            '\n'
                                            'Даже беглый обзор функций БЖУ дает понять, что шутить с ними не получится,'
                                            ' и в пище должен быть баланс: пусть не перманентный, но держать под'
                                            ' контролем уровень белков, жиров и углеводов все-таки следует. Но зачем'
                                            ' вообще что-либо именно подсчитывать и к чему такой серьезный подход, если'
                                            ' человек, скажем, и употребляет в пищу полезные продукты? Конечно,'
                                            ' здорово, если вы едите много свежих овощей и фруктов, не злоупотребляете'
                                            ' кофе и шоколадом, но организм человека — вещь хрупкая. Тибетские врачи,'
                                            ' например, считают, что болезни у человека развиваются при нарушении'
                                            ' баланса «дош», которое случается при несбалансированном питании и вредных'
                                            ' привычках. Тибетская мудрость сегодня подтверждается и традиционной'
                                            ' медициной. Питание должно быть не только условно полезным,'
                                            ' но и сбалансированным.')
        tgbot.send_photo(message.chat.id, file_photo_4)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Да")
        item2 = types.KeyboardButton("Нет")
        markup.row(item1, item2)
        tgbot.send_message(message.chat.id, 'Остался последний пункт, который вам стоит знать - расчёт БЖУ.\n'
                                            'Хотите узнать что это и посмотреть пример?', reply_markup=markup)
        tgbot.register_next_step_handler(message, count_set)
    elif amount_111 == 'Нет':
        tgbot.send_message(message.chat.id, 'Я вас понял, нажмите -> /next <-, чтобы вернуться в главное меню.')
        tgbot.register_next_step_handler(message, start_all)
    else:
        tgbot.send_message(message.chat.id, 'Я не понимаю, что вы говорите😵.\nЧтобы узнать информацию о важности'
                                            ' баланса в питании, '
                                            'нажмите -> /info <- и пройдите все заново.')
        tgbot.register_next_step_handler(message, information)

@tgbot.message_handler(commands=['count'])
def count_set(message):
    amount_1111 = message.text.strip()
    if amount_1111 == 'Да':
        tgbot.send_message(message.chat.id, 'Под аббревиатурой БЖУ заключается понятие о правильном соотношении'
                                            ' в нашей пище белков, жиров и углеводов, а также взаимосвязь данного'
                                            ' соотношения с общей калорийностью. Соотношение БЖУ имеет большое значение'
                                            ' как в стандартных тренировках, так и в вопросе оптимизации массы тела.')
        tgbot.send_message(message.chat.id, 'Пример расчета БЖУ.\n'
                                            '\n'
                                            'Чтобы рассчитать свою потребность в калораже, нужно измерить свой вес.'
                                            'Затем измерить свой рост и определить суточную норму калорий по формуле:\n'
                                            '1. Qж = (рост в см х1,8) — '
                                            '(возраст в годах х 4,7) + (вес тела в кг х 9,6) + 655 , где Qж —'
                                            ' количество суточной нормы калорий для женщин.\n'
                                            '2. Qм = (рост в см х 5) — (возраст в годах х 6,8)'
                                            ' + (вес тела в кг х13,7) + 66 , где Qм -количество суточной'
                                            'нормы калорий для мужчин.\n'   
                                            'По этим формулам можно рассчитать сколько калорий нужно вашему организму'
                                            ' в состоянии покоя. При низкой физической активности полученный результат'
                                            ' надо умножить на 1,1, при средней — на 1,3. А тем, кто занимается '
                                            'спортом или занят тяжелым физическим трудом на 1,5.'
                                            'Например посчитаем норму калорий в день мужчины, которому 35 лет, рост 180'
                                            ' см, вес 80 кг и у него средняя активность:'
                                            ' для этого подставим значения в формулу.\n Qм = 180 * 5 - 35 * 6,8 + 80'
                                            ' * 13,7 + 66 * 1,3. Получаем 2372 калории')
        tgbot.send_message(message.chat.id, 'Финальный шаг на нашем пути — это перевод из калорий в граммы трио БЖУ:'
                                            '\n'
                                            '1 г белка = 4 калории;\n'
                                            '1 г жира = 9 калорий;\n'
                                            '1 г углеводов = 4 калории.\n'
                                            'Теперь узнаем количество каждого из нутриентов: возьмем полученное в'
                                            ' ходе расчетов число калорий и применим формулу,'
                                            ' в которой 0,3 и 0,4 — это показатель соотношения БЖУ в рационе'
                                            ' (наши 30, 30 и 40 % БЖУ), а 4, 9, 4 — калории БЖУ. Итак:\n'
                                            '2372 * 0.3 / 4 = 178 г — белки;\n'
                                            '2372 * 0.3 / 9 = 79 г — жиры;\n'
                                            '2372 * 0.4 / 4 = 237 г — углеводы.\n'
                                            'Оптимальным будет именно такой уровень БЖУ в день для нашего'
                                            ' гипотетического мужчины.')
        tgbot.send_message(message.chat.id, 'Что делать после расчета нормы БЖУ?\n'
                                            '\n'
                                            'Что делать дальше с показателями, которые вы посчитаете? Для начала можно'
                                            ' просто проанализировать свой ежедневный рацион и понять, сбалансированно'
                                            ' вы питаетесь или нет. Показатели содержания БЖУ в продуктах можно взять'
                                            ' в сети Интернет. Важно, конечно, знать (хотя бы примерно), какое'
                                            ' количество того или иного продукта вы съели. Поэтому одна из рекомендаций'
                                            ' тем, кто хочет следить за уровнем БЖУ, — завести кухонные весы.'
                                            ' И здесь для многих будет сюрприз: есть правила взвешивания продуктов.'
                                            ' Например, важно взвешивать продукт не в сыром виде, а уже в готовом,'
                                            ' ведь масса будет отличаться из-за коэффициента уварки или ужарки. Орехи'
                                            ' взвешиваются в очищенном виде, ягоды можно взвешивать с косточкой,'
                                            ' но без веточек. При взвешивании любой еды важно учитывать вес емкости.\n'
                                            'Также немаловажным является учет потребления воды и клетчатки, о которых '
                                            'мы часто забываем. Усредненной нормой считается 28 грамм клетчатки в'
                                            ' сутки. Это норма и для мужчин, и для женщин среднего возраста.'
                                            ' У подсчета необходимого количества воды тоже есть свои хитрости.'
                                            ' Скажем лишь, что минимальное количество в день для любого взрослого'
                                            ' человека — это 1,5 литра воды (сок, чай, кофе, увы, в учет не идут).\n'                                           
                                            'Расчет всех этих показателей может обескуражить своей'
                                            ' кажущейся сложностью, но стоит один раз рассчитать калории'
                                            ' и приноровиться подмечать количество съеденного (не забывая пить воду)'
                                            ', как результат от этого перевесит все неудобства.')
        tgbot.send_message(message.chat.id, 'Основная информация закончилась и теперь ты знаешь, что такое БЖУ,'
                                            ' как его рассчитать;\n'
                                            'Ты узнал о функциях белков, жиров и углеводов, а также, где'
                                            ' они сожержатся.\n'
                                            'Теперь жми -> /next <- и наш третий пункт поможет тебе рассчитать твою'
                                            ' норму БЖУ :)')
        tgbot.register_next_step_handler(message, start_all)
    elif amount_1111 == 'Нет':
        tgbot.send_message(message.chat.id, 'Очень жаль😔.\n'
                                            'Тогда жми -> /next <- и выбирай наш третий пункт, который поможет'
                                            ' рассчитать тебе твою норму БЖУ.')
        tgbot.register_next_step_handler(message, start_all)
    else:
        tgbot.send_message(message.chat.id, 'Я не понимаю, что вы говорите😵.\nЧтобы узнать информацию о важности'
                                            ' баланса в питании, '
                                            'нажмите -> /info <- и пройдите все заново.')
        tgbot.register_next_step_handler(message, information)

@tgbot.message_handler(commands=['count'])
def count_all(message):
    tgbot.send_message(message.chat.id, 'Если вы уже ознакомились с пунктом "Общая информация",'
                                        ' то знаете, что сейчас будет происходить. Вам нужно будет вводить информацию,'
                                        ' которую запрашивает бот. Тем самым вы узнаете свою норму калорий☺️.')
    tgbot.send_message(message.chat.id, 'Введите ваш вес (в кг):')
    tgbot.register_next_step_handler(message, ves_all)

def ves_all(message):
    global ves
    try:
        ves = int(message.text.strip())
    except Exception:
        tgbot.send_message(message.chat.id, 'Неверный формат😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, ves_all)
        return
    if ves > 0:
        tgbot.send_message(message.chat.id, 'Введите ваш рост (в см):')
        tgbot.register_next_step_handler(message, rost_all)
    else:
        tgbot.send_message(message.chat.id, 'Неверный формат😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, ves_all)

def rost_all(message):
    global rost
    try:
        rost = int(message.text.strip())
    except Exception:
        tgbot.send_message(message.chat.id, 'Неверный формат😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, rost_all)
        return
    if rost > 0:
        tgbot.send_message(message.chat.id, 'Введите ваш возраст (в годах):')
        tgbot.register_next_step_handler(message, vosrast_all)
    else:
        tgbot.send_message(message.chat.id, 'Неверный формат😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, rost_all)

def vosrast_all(message):
    global vosrast
    try:
        vosrast = int(message.text.strip())
    except Exception:
        tgbot.send_message(message.chat.id, 'Неверный формат😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, vosrast_all)
        return
    if rost > 0:
        tgbot.send_message(message.chat.id, 'Коэффициент А — это показатель активности человека.\n'                                       
                                            'У него пять вариантов:\n'                                        
                                            '(1) - 1,1 —  низкая физическая активность.\n'                                      
                                            '(2) - 1,3 — средняя физическая активность.\n'                                         
                                            '(3) - 1,5 — высокая физическая активность.')
        tgbot.send_message(message.chat.id, 'Введите коэффициент A (число от 1 до 3):')
        tgbot.register_next_step_handler(message, A_cof)
    else:
        tgbot.send_message(message.chat.id, 'Неверный формат😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, vosrast_all)

def A_cof(message):
    global A
    try:
        A = int(message.text.strip())
    except Exception:
        tgbot.send_message(message.chat.id, 'Неверный формат😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, A_cof)
    if A == 1:
        A = 1.1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Мужской")
        item2 = types.KeyboardButton("Женский")
        markup.row(item1, item2)
        tgbot.send_message(message.chat.id, 'Введите ваш пол:', reply_markup=markup)
        tgbot.register_next_step_handler(message, pol)
    elif A == 2:
        A = 1.3
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Мужской")
        item2 = types.KeyboardButton("Женский")
        markup.row(item1, item2)
        tgbot.send_message(message.chat.id, 'Введите ваш пол:', reply_markup=markup)
        tgbot.register_next_step_handler(message, pol)
    elif A == 3:
        A = 1.5
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Мужской")
        item2 = types.KeyboardButton("Женский")
        markup.row(item1, item2)
        tgbot.send_message(message.chat.id, 'Введите ваш пол:', reply_markup=markup)
        tgbot.register_next_step_handler(message, pol)
    else:
        tgbot.send_message(message.chat.id, 'Неверный формат😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, A_cof)

def pol(message):
    amount_11111 = message.text.strip()
    if amount_11111 == 'Мужской':
        global pol_m
        pol_m = ((rost * 5) - (vosrast * 6.8) + (ves * 13.7) + 66) * A
        global belki
        belki = round((pol_m * 0.3) / 4)
        global lipid
        lipid = round((pol_m * 0.3) / 9)
        global yglevod
        yglevod = round((pol_m * 0.4) / 4)
        tgbot.send_message(message.chat.id, f'Ваша норма калорий в день: {round(pol_m)}.\n'
                                            f'Ваша норма белков в день: {belki} грамм.\n' 
                                            f'Ваша норма жиров в день: {lipid} грамм.\n'
                                            f'Ваша норма углеводов в день: {yglevod} грамм.')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Да")
        item2 = types.KeyboardButton("Нет")
        markup.row(item1, item2)
        tgbot.send_message(message.chat.id, 'Хотите ли вы пройти тест заново?', reply_markup=markup)
        tgbot.register_next_step_handler(message, renext)
    elif amount_11111 == 'Женский':
        global pol_g
        pol_g = ((rost * 1.8) - (vosrast * 4.7) + (ves * 9.6) + 665) * A
        belki = round((pol_g * 0.3) / 4)
        lipid = round((pol_g * 0.3) / 9)
        yglevod = round((pol_g * 0.4) / 4)
        tgbot.send_message(message.chat.id, f'Ваша норма калорий в день: {round(pol_g)}.\n'
                                            f'Ваша норма белков в день: {belki} грамм.\n'
                                            f'Ваша норма жиров в день: {lipid} грамм.\n'
                                            f'Ваша норма углеводов в день: {yglevod} грамм.')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Да")
        item2 = types.KeyboardButton("Нет")
        markup.row(item1, item2)
        tgbot.send_message(message.chat.id, 'Хотите ли вы пройти тест заново?', reply_markup=markup)
        tgbot.register_next_step_handler(message, renext)
    else:
        tgbot.send_message(message.chat.id, 'Неверный ввод😵. Введите значение заново.')
        tgbot.register_next_step_handler(message, pol)

def renext(message):
    amount_1101 = message.text.strip()
    if amount_1101 == 'Да':
        tgbot.send_message(message.chat.id, 'Нажмите -> /count <-, чтобы заново пройти тест.')
        tgbot.register_next_step_handler(message, count_all)
    elif amount_1101 == 'Нет':
        tgbot.send_message(message.chat.id, 'Нажмите -> /next <-, чтобы перейти в главное меню.')
        tgbot.register_next_step_handler(message, start_all)
    else:
        tgbot.send_message(message.chat.id, 'Не понимаю, что вы говорите😵. Введите ответ заново ("Да" или "Нет")')
        tgbot.register_next_step_handler(message, renext)
tgbot.polling(none_stop=True)

# список литературы
# https://www.sport-express.ru/zozh/reviews/bzhu-chto-eto-takoe-kak-pravilno-rasschityvat-normu-pochemu-eto-vazhno-1946582
# https://calorieninjas.com



