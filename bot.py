# -*- coding: utf-8 -*-
import vk_api #импортируем библиотеки
import vk
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
keyboard.add_button('Информация', color=VkKeyboardColor.NEGATIVE)
for event in Lslongpoll.listen():#слушаем longpool на предмет новых сообщений. event — переменная в которой будет храниться само сообщение и некоторые данные о нем.
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        vars1 = ['Привет', 'Ку', 'Хай', 'Хеллоу']
        if event.text in vars1:
            if event.from_user:#Проверяем откуда направлен наш event
                Lsvk.messages.send(
                                   user_id = event.user_id,
                                   random_id = get_random_id(),
                                   keyboard = keyboard.get_keyboard(),
                                   message = 'Привет, выбери снизу интересующую кнопку!)',
                                   )
        vars2 = ['Информация']
        if event.text in vars2:
            if event.from_user:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Общая информация', color=VkKeyboardColor.NEGATIVE)
                keyboard.add_line()
                keyboard.add_button('Информация о ВУЗах-партнерах', color=VkKeyboardColor.POSITIVE)
                keyboard.add_line()
                keyboard.add_button('Олимпиады', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
                Lsvk.messages.send(
                                   user_id = event.user_id,
                                   random_id = get_random_id(),
                                   keyboard = keyboard.get_keyboard(),
                                   message = 'Видимо ты наш новый друг? Рады тебя приветствовать! Что конкретно тебя интересно?'
                                   )
        vars3 = ['Начать']
        if event.text in vars3:
            if event.from_user:#Проверяем откуда направлен наш event
                Lsvk.messages.send(
                                   user_id = event.user_id,
                                   random_id = get_random_id(),
                                   keyboard = keyboard.get_keyboard(),
                                   message = 'Добро пожаловать в группу Энергоклассов ПАО "РусГидро"! Выбери снизу интересующую кнопку!',
                                   )
        vars4 = ['Общая информация']
        if event.text in vars4:
            if event.from_user:#Проверяем откуда направлен наш event
                Lsvk.messages.send(
                                   user_id = event.user_id,
                                   random_id = get_random_id(),
                                   keyboard = keyboard.get_keyboard(),
                                   message = 'РусГидро приглашает школьников девяти регионов России в Энергоклассы и на факультативные занятия по теории решения изобретательских задач (ТРИЗ). В рамках образовательного проекта Энергоклассов учащиеся 9-11 классов изучают профильные предметы гидроэнергетической тематики, знакомятся с компанией и проходят углубленную довузовскую подготовку по физике и математике. Занятия по ТРИЗ ориентированы на школьников 7-8 классов. Все обучение является бесплатным, начало занятий – в октябре.',
                                   )
        vars5 = ['Информация о ВУЗах-партнерах']
        if event.text in vars5:
            if event.from_user:#Проверяем откуда направлен наш event
                Lsvk.messages.send(
                                   user_id = event.user_id,
                                   random_id = get_random_id(),
                                   keyboard = keyboard.get_keyboard(),
                                   message = 'Благодаря Энергоклассам ПАО "РусГидро" у тебя есть шанс поступить в наши ВУЗы-партнеры, среди которых: Санкт-Петербургский политехнический университети им.Петра Великого в Институт Энергетики,Национальный исследовательский университет ИТМО, Московский политехнический университет, Российский государственный аграрный университет МСХА имени К.А. Тимирязева, Московский авиационный институт, Институт гидроэнергетики и возобновляемых источников энергии, АмГУ- кафедра энергетики! Довольно впечатляющий список...',
                                   )
        vars6 = ['Олимпиады']
        if event.text in vars6:
            if event.from_user:#Проверяем откуда направлен наш event
                Lsvk.messages.send(
                                   user_id = event.user_id,
                                   random_id = get_random_id(),
                                   keyboard = keyboard.get_keyboard(),
                                   message = 'У нас ты сможешь принять участие в олимпиадах от ПАО "РусГидро", такие как: Отраслевая олимпиада школьников «Энергия образования» и другие Всероссийские олимпиады! При успешном участии у тебя есть возможность получить дополнительные балы к ЕГЭ при поступлении в наши ВУЗы-партрнеры!',
                                   )
        vars7 = ['Назад']
        if event.text in vars7:
            if event.from_user:#Проверяем откуда направлен наш event
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Информация', color=VkKeyboardColor.NEGATIVE)
                Lsvk.messages.send(
                                   user_id = event.user_id,
                                   random_id = get_random_id(),
                                   keyboard = keyboard.get_keyboard(),
                                   message = 'Добро пожаловать в группу Энергоклассов ПАО "РусГидро"! Выбери снизу интересующую кнопку!',
                                   )
        if event.text not in vars2 and event.text not in vars1 and event.text not in vars3 and event.text not in vars4 and event.text not in vars5 and event.text not in vars6 and event.text not in vars7 :
            if event.from_user:
                Lsvk.messages.send(
                                   user_id = event.user_id,
                                   random_id = get_random_id(),
                                   keyboard = keyboard.get_keyboard(),
                                   message = 'Лучше выбери снизу интересующую кнопку)))'
                                   )
