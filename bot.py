import vk_api #импортируем библиотеки
import vk
import random
import numpy
from vk_api.keyboard import VkKeyboard, VkKeyboardColor#импортируем нужные модули
from vk_api.utils import get_random_id
vk_session = vk_api.VkApi(token='6181ac09755b06b499b0aed67cb6ff0b3cbbb7d8cc598a0f5c311b31fa5e252eff8dfb48c3170b8a1c34f')#авторизируемся
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType#импортируем нужные модули
longpoll = VkBotLongPoll(vk_session,203652377)
vk = vk_session.get_api()
from vk_api.longpoll import VkLongPoll, VkEventType#импортируем модуль Long pool для личных сообщений
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Викторина', color=VkKeyboardColor.NEGATIVE)


class student():

    """Модель студента"""

    def __init__(self,nid,position,size):
        self.id=nid
        self.position=position
        self.free_quest = numpy.zeros(size,dtype=int)
        self.score = 0
        self.already = 0


def count_lines(filename):
    return sum(1 for line in open(filename, 'r'))


def get_maxsize(filename):
    a = open(filename,'r')
    line = a.readline()
    line = line.strip()
    a.close()
    return int(line)


def check(list,nid,size):
    current = 0
    for i in list:
        if i.id == nid:
            current = i
    if current:
        return current
    else:
        list.append(student(nid,"lobby",size))
        return list[-1]


def get_quest(filename,cur,quest,vars):
    a = open(filename,'r')
    number = random.randint(1,size)-1
    if(cur.free_quest[number]==1):
        flag=0
        while cur.free_quest[number]:
            number+=1
            number%=size
            flag+=1
            if(flag==size):
                cur.free_quest.fill(0)
    cur.free_quest[number]=1
    cur.already+=1
    number+=1
    for i in range(number*2):
        line = a.readline()
    quest = line.split('"')
    vars = a.readline()
    a.close()
    vars = vars.strip()
    vars = vars.split(';')
    return quest,vars


def print_start(Nmessage):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Start', color=VkKeyboardColor.NEGATIVE)
    Lsvk.messages.send(
                       user_id = event.user_id,
                       random_id = get_random_id(),
                       keyboard = keyboard.get_keyboard(),
                       message = Nmessage,
                       )


def print_variants(quest,vars):
    keyboard = VkKeyboard(one_time=True)
    if(len(vars)>1):
        for letter in vars:
            keyboard.add_button(str(letter), color=VkKeyboardColor.NEGATIVE)
    else :
        keyboard.add_button("Я не знаю(", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Закончить викторину", color=VkKeyboardColor.NEGATIVE)
    Lsvk.messages.send(
                       user_id = event.user_id,
                       random_id = get_random_id(),
                       keyboard = keyboard.get_keyboard(),
                       message = str(quest[1]),
                       )


def exit(where,Nmessage,cur,lock):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Start', color=VkKeyboardColor.NEGATIVE)
    Lsvk.messages.send(
                       user_id = event.user_id,
                       random_id = get_random_id(),
                       keyboard = keyboard.get_keyboard(),
                       message = Nmessage
                       )
    cur.position = where
    return lock+1

def check_answers(event,quest,cur):
    if len(event.text) == len(quest[3]) and event.text in quest[3]:
        cur.score+=1
        Lsvk.messages.send(
                           user_id = event.user_id,
                           random_id = get_random_id(),
                           keyboard = keyboard.get_keyboard(),
                           message = 'Ваш ответ верный!'
                           )
    else:
        Lsvk.messages.send(
                           user_id = event.user_id,
                           random_id = get_random_id(),
                           keyboard = keyboard.get_keyboard(),
                           message = 'Ваш ответ не верный('
                           )
def out_result(cur):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Еще раз", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button("Выход", color=VkKeyboardColor.NEGATIVE)
    output = 'Викторина окончена и вы набрали '+str(cur.score)+' очков'
    Lsvk.messages.send(
                   user_id = event.user_id,
                   random_id = get_random_id(),
                   keyboard = keyboard.get_keyboard(),
                   message = output
                   )
    cur.score=0
    cur.already=0


filename = 'quests.txt'

ListOfStudents=[]
quest=[]
vars=[]

size = int((count_lines(filename)-1) / 2)
maxsize = get_maxsize(filename)
lock = 0


for event in Lslongpoll.listen():#слушаем longpool на предмет новых сообщений. event — переменная в которой будет храниться само сообщение и некоторые данные о нем.
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
        cur = check(ListOfStudents,event.user_id,size)
        lock = 1
        while lock:
            if cur.position == "lobby":
                lock -= 1
                vars1 = ['Привет', 'Ку', 'Хай', 'Хеллоу']
                if event.text in vars1:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Викторина', color=VkKeyboardColor.NEGATIVE)
                    Lsvk.messages.send(
                                       user_id = event.user_id,
                                       random_id = get_random_id(),
                                       keyboard = keyboard.get_keyboard(),
                                       message = 'Привет, выбери снизу интересующую кнопку!)',
                                       )
                elif event.text == "Викторина":
                    cur.position = "victorina"
                    lock += 1
                else:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Викторина', color=VkKeyboardColor.NEGATIVE)
                    Lsvk.messages.send(
                                       user_id = event.user_id,
                                       random_id = get_random_id(),
                                       keyboard = keyboard.get_keyboard(),
                                       message = 'You are in lobby',
                                       )
            if cur.position == "victorina":
                lock -= 1
                hello = ['Викторина']
                start = ['Start','Еще раз']
                end = ['Закончить викторину','Выход']

                if event.text in hello:
                    print_start('Для начала викторины жми \"Start\"')

                elif event.text in start:
                    quest,vars = get_quest(filename,cur,quest,vars)
                    print_variants(quest,vars)

                elif event.text in end: #Выход
                    lock = exit('lobby','Удачи!',cur, lock)

                elif cur.already<maxsize:
                    check_answers(event,quest,cur)
                    quest,vars = get_quest(filename,cur,quest,vars)
                    print_variants(quest,vars)

                else:
                    check_answers(event,quest,cur)
                    out_result(cur)