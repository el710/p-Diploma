### Дипломный проект на Python (с открытым исходным кодом)
---
# Сервис-помощник
(планирование и управление ресурсами (делами, проектами, договорами)

```
Программа формирует персональное расписание на основе проектов и договоров.
Интерфейс сервиса: Web-сайт, Телеграм-бот, приложение для телефона (в  разработке :) 
```

[1. Установка и запуск](#1-установка-и-запуск)
[2. Алгоритмы](#2-алгоритмы)
[ - Создание события](#создание-события)

---
### 1. Установка и запуск
- Установите Python 3.11.9 (https://www.python.org/)
- Установите систему контроля версий git 2.38.0 (https://git-scm.com/)
- Установите IDE: VS code или PyCharm (https://code.visualstudio.com | https://www.jetbrains.com)
- Создайте директорию проекта (например "New_project")
- Внутри директории создайте git репозиторий командой:
```
> git init
```
- Скачайте проект с GitHub выполнив две команды:
```
> git remote add origin https://github.com/el710/p-Diploma
> git pull --set-upstream origin main
```
*[Note: на GitHub ocновная ветка называется 'main']*

- С помощью BotFather в Телеграм создайте нового бота и получите ключ: токен
- В IDE откройте созданную директорию и в папке *telegram* создайте файл *id_bot.py*
- В файле создайте переменную *tel_token* и присвойте ей значение токена:
```
"id_bot.py"
            tel_token = "xxxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
- Установите необходимые пакеты командой:
```
> pip install -r requirements.txt
```
- Запустите файл *main.py* командой
```
> python main.py
```
или средствами IDE...

Вывод в терминале при запуске:
![старт программы](screen5.png)


### 2. Алгоритмы

>Основной поток (Файл: main.py)

В основном потоке запускаются потоки телеграм бота и web api:
```
    ...
    # start thread with telegram bot
    telegram_link = run_thread_agent(telebot_start)

    # start thread with webapi
    webapi_link = run_thread_agent(webapi_start)
    ...
```
в результате функции *run_thread_agent()* мы получем словарь с идентификаторами
очередей под ключами "in" / "out" для обмена данными с функцией потока

Далее запускается основной цикл диспетчера - *while True:*

Чтение сообщений производится с ожиданием в 1 секунду (*timeout=1*) и с обработкой исключительной ситуации - отсутствия сообщений. В случае отсутсвия сообщений поток останавливается, для освобождения процессорного времени.
```
    try:
        event_query = telegram_link["out"].get(timeout=1)
        ...
        обработка
        ...
    except Empty:
        ## in case no message from telegram
        ## free proccess time
        time.sleep(3)
```
>
Распаковка сообщения производится путем преобразования в объект класса  *TMessage()*, где данные передаются в параметры объекта класса
```
 mess = TMessage(event_query)
```
*ПЛАН: создать класс протокола обмена с упаковкой и распаковкой данных...*

В зависимости от типа сообщения производиться обработка данных, формирование ответа *user_schedule* и отправка ответа в телеграм бот:
```
match mess.get_message_type():
    case "create_event":
    ...
    
    case "read_event":
    ...
    
    case "udpate_event":
    ...
    
    case "delete_event":
    ...           
    
    case _:
        ## wrong message - set None user
        mess.set_user()

## send user schedule as answer
user_schedule = get_user_events(mess.get_user())

telegram_link["in"].put(user_schedule)
```
>
## Создание события
По идентификатору пользователя в сообщений проводиться поиск пользователя в базе:
```
tmp_user = read_base_user(mess.get_user())
```
Если пользователь существует то по данным из сообщения добавляется новое событие в базу:
```
new_event = CreateEvent(... )
 
 create_base_event(new_event)
```
>

## Чтение события - вход пользователя
При запросе данных, также определяется пользователь.
Если такого пользователя нет в базе, то создается новый пользователь:
```
tmp_user = CreateUser(username = mess.username,
                      firstname = mess.firstname,
                      lastname = mess.lastname,
                      email = 'user@mail',
                      language = mess.language,
                      is_human = mess.is_human,
                      telegram_id = mess.telegram_id
                     )

create_base_user(tmp_user)
```
>
## Редактирование события
При изменении события создается экземпляр события с новыми данными,
производится замена данных в базе:
```
new_event = CreateEvent(task = mess.task,
                        date = mess.date,
                        time = mess.time,
                        owner_id = mess.get_user(),
                        dealer = mess.dealer)

update_base_event(mess.event_id, new_event)
```
>
## Удаление события
При удалении, событие удаляется из базы:
```
delete_base_event(mess.event_id)
```

---
Copyright (c) 2024 Kim Oleg <theel710@gmail.com>