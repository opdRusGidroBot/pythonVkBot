# -*- coding: utf-8 -*-
import os
import datetime
import vk_api  # импортируем библиотеки
import vk
import random
import numpy
from vk_api.keyboard import VkKeyboard, VkKeyboardColor  # импортируем нужные модули
from vk_api.utils import get_random_id

vk_session = vk_api.VkApi(
    token='6181ac09755b06b499b0aed67cb6ff0b3cbbb7d8cc598a0f5c311b31fa5e252eff8dfb48c3170b8a1c34f')  # авторизируемся
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType  # импортируем нужные модули

longpoll = VkBotLongPoll(vk_session, 203652377)
vk = vk_session.get_api()
from vk_api.longpoll import VkLongPoll, VkEventType  # импортируем модуль Long pool для личных сообщений

Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()


class student():
    """Модель студента"""

    def __init__(self, nid, position, size):
        self.id = nid
        self.position = position
        self.free_quest = numpy.zeros(size, dtype=int)
        self.score = 0
        self.already = 0
        self.game = 0


def count_lines(filename):
    return sum(1 for line in open(filename, 'r'))


def get_maxsize(filename):
    a = open(filename, 'r')
    line = a.readline()
    line = line.strip()
    a.close()
    return int(line)


def check(list, nid, size):
    current = 0
    for i in list:
        if i.id == nid:
            current = i
    if current:
        return current
    else:
        list.append(student(nid, "lobby", size))
        return list[-1]


def get_quest(filename, cur, quest, vars):
    a = open(filename, 'r')
    number = random.randint(1, size) - 1
    if (cur.free_quest[number] == 1):
        flag = 0
        while cur.free_quest[number]:
            number += 1
            number %= size
            flag += 1
            if (flag == size):
                cur.free_quest.fill(0)
    cur.free_quest[number] = 1
    number += 1
    for i in range(number * 2):
        line = a.readline()
    quest = line.split('"')
    vars = a.readline()
    a.close()
    vars = vars.strip()
    vars = vars.split(';')
    cur.already += 1
    return quest, vars


def print_start(Nmessage):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Старт', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    Lsvk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=Nmessage,
    )


def print_variants(quest, vars):
    keyboard = VkKeyboard(one_time=True)
    if (len(vars) > 1):
        for letter in vars:
            keyboard.add_button(str(letter), color=VkKeyboardColor.NEGATIVE)
    else:
        keyboard.add_button("Я не знаю(", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Закончить викторину", color=VkKeyboardColor.SECONDARY)
    Lsvk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=str(quest[1]),
    )


def exit(where, Nmessage, cur, lock):
    if Nmessage:
        Lsvk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=Nmessage
        )
    cur.position = where
    return lock + 1


def check_answers(event, quest, cur):
    if len(event.text) == len(quest[3]) and event.text in quest[3]:
        cur.score += 1
        Lsvk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Ваш ответ верный!',
        )
    else:
        Lsvk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Ваш ответ не верный(',
        )


def out_result(cur):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Еще раз", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Выход", color=VkKeyboardColor.SECONDARY)
    output = 'Викторина окончена и вы набрали ' + str(cur.score) + ' очков'
    Lsvk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=output
    )
    cur.score = 0
    cur.already = 0
    cur.game = 0


def out_lobby(msg):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Расписание', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()

    keyboard.add_button('Обратная связь', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()

    keyboard.add_button('Информация', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()

    keyboard.add_button('Викторина', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()

    keyboard.add_button('Новости', color=VkKeyboardColor.NEGATIVE)

    Lsvk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=msg,
    )


def out_info(keyboard):
    keyboard.add_button('Общая информация', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Информация о ВУЗах-партнерах', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Олимпиады', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)

def  feedback(event):
    if not os.path.isdir("Feedback"):  # проверяем есть ли папка, если нет, то создаем
        os.mkdir("Feedback")
    vars_end = ['Назад']
    #vars_further = ['Вернуться в Главное меню']
    vars_personal_data = ['Оставить личные данные']
    keyboard = VkKeyboard(one_time=True)
    # keyboard.add_button('Вернуться в Главное меню', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
    Lsvk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Здесь вы можете оставить отзыв о наших заведениях либо задать вопрос(что то такое) для обратной связи с вами свяжутся'
    )
    for event in Lslongpoll.listen():  # слушаем longpool на предмет новых сообщений. event — переменная в которой будет храниться само сообщение и некоторые данные о нем.
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.text not in vars_end:
                if event.from_user:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Вернуться в Главное меню', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_button('Оставить личные данные', color=VkKeyboardColor.PRIMARY)
                    Lsvk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message='Ваше сообщение было сохранено. Вы можете оставить свои обратные данные для связи с вами или для статистики'
                    )
                    # здесь тоже должно быть добавление в файл
                    string_name_file = 'Feedback/' + str(event.user_id) + '.txt'
                    output_file = open(string_name_file, "a+")
                    now = datetime.datetime.now()
                    output_file.write(now.strftime("%d-%m-%Y %H:%M")+'\n')
                    output_file.write(event.text+'\n')
                    output_file.close()

                for event in Lslongpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                        if event.text in vars_personal_data:
                            Lsvk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                #keyboard=keyboard.get_keyboard(),
                                message='Введите ваши личные данные'
                            )
                            for event in Lslongpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                                    Lsvk.messages.send(
                                        user_id=event.user_id,
                                        random_id=get_random_id(),
                                        keyboard=keyboard.get_keyboard(),
                                        message='Введенные данные успешно сохранены'
                                    )  # надо добавить добавление в файл
                                    output_file = open(string_name_file, "a+")
                                    output_file.write('Personal data: ' + event.text + '\n')
                                    output_file.close()
                                    break

                        break
                output_file = open(string_name_file, "a+")
                output_file.write('\r\n')
                output_file.close()
            break


def get_position(msg):
    if msg == "Викторина":
        return "quiz"

    elif msg == "Расписание":
        return "schedule"

    elif msg == "Информация":
        return "info"

    elif msg == "Обратная связь":
        return "feedback"

    elif msg == "Новости":
        return "news"


filename = 'questionsForQuiz.txt'

ListOfStudents = []
quest = []
vars = []

size = int((count_lines(filename) - 1) / 2)
maxsize = get_maxsize(filename)
lock = 0

for event in Lslongpoll.listen():  # слушаем longpool на предмет новых сообщений. event — переменная в которой будет храниться само сообщение и некоторые данные о нем.
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
        cur = check(ListOfStudents, event.user_id, size)
        lock = 1
        while lock:
            if cur.position == "lobby":
                lock -= 1
                greetings = ['Привет', 'Ку', 'Хай', 'Хеллоу']
                listOfOptions = ['Викторина', 'Расписание', 'Обратная связь', 'Информация', 'Новости']
                if event.text in greetings:
                    out_lobby('Привет, выбери снизу интересующую кнопку!)')
                elif event.text in listOfOptions:
                    cur.position = get_position(event.text)
                    lock += 1
                else:
                    out_lobby('Выбери снизу интересующую кнопку!')
            elif cur.position == "info":
                lock -= 1
                university = ['Информация о ВУЗах-партнерах']
                olimpyc = ['Олимпиады']
                exitWordsForInfo = ['Назад']
                genral_info = ['Общая информация']
                keyboard = VkKeyboard(one_time=True)
                out_info(keyboard)
                if event.text in university:
                    Lsvk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message='Благодаря Энергоклассам ПАО "РусГидро" у тебя есть шанс поступить в наши ВУЗы-партнеры, среди которых: Санкт-Петербургский политехнический университети им.Петра Великого в Институт...',
                    )
                elif event.text in olimpyc:
                    Lsvk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message='У нас ты сможешь принять участие в олимпиадах от ПАО "РусГидро", такие как: Отраслевая олимпиада школьников «Энергия образования» и другие Всероссийские олимпиады! При успешном участии...',
                    )
                elif event.text in genral_info:
                    Lsvk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message='РусГидро приглашает школьников девяти регионов России в Энергоклассы и на факультативные занятия по теории решения изобретательских задач (ТРИЗ). В рамках образовательного проекта Энергоклассов учащиеся 9-11 классов...',
                    )
                elif event.text in exitWordsForInfo:
                    lock = exit('lobby', '', cur, lock)
                else:
                    Lsvk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message='Выбери снизу интересующую кнопку!',
                    )


            elif cur.position == "schedule":
                lock -= 1
                # тело расписания
                # if event.text in exitWordsForSchedule:
                #    lock = exit('lobby','',cur, lock) Выход из Расписания закачивать этой функцией


            elif cur.position == "feedback":
                lock -= 1
                # тело обратной связи
                feedback(event)
                #if event.text in exitWordsForFeedback:
                event.text = " "
                lock = exit('lobby','',cur, lock) #Выход из Обратной связи закачивать этой функцией
               # print("lock= ", lock)

            elif cur.position == "news":
                lock -= 1
                # тело обратной связи
                # if event.text in exitWordsForNews:
                #   lock = exit('lobby','',cur, lock) Выход из Новостей закачивать этой функцией


            elif cur.position == "quiz":
                lock -= 1
                greetingWordsForQuiz = ['Викторина']
                startWordsForQuiz = ['Старт', 'Еще раз']
                exitWordsForQuiz = ['Закончить викторину', 'Выход', 'Назад']

                if event.text in greetingWordsForQuiz:
                    print_start('Для начала викторины жми \"Старт\"')

                elif event.text in startWordsForQuiz:
                    cur.game = 1
                    quest, vars = get_quest(filename, cur, quest, vars)
                    print_variants(quest, vars)

                elif event.text in exitWordsForQuiz:  # Выход
                    cur.game = 0
                    cur.already = 0
                    cur.score = 0
                    lock = exit('lobby', 'Удачи!', cur, lock)
                elif cur.game == 1:
                    if cur.already < maxsize:
                        check_answers(event, quest, cur)
                        quest, vars = get_quest(filename, cur, quest, vars)
                        print_variants(quest, vars)

                    else:
                        check_answers(event, quest, cur)
                        out_result(cur)

                else:
                    print_start('Попробуй ввести что-то другое')


