### Дипломный проект на Python (с открытым искходным кодом)
---
# Сервис-помощник
(планирование и управление ресурсами (делами, проектами, договорами)

```
Программа формирует персональное расписание на основе проектов и договоров.
Интерфейс сервиса: Web-сайт, Телеграм-бот, приложение для телефона (в  разработке :) 
```
---
### 1. Установка и запуск
1.1 Установите Python 3.11.9 (https://www.python.org/)
1.2 Установите систему контроля версий git 2.38.0 (https://git-scm.com/)
1.3 Установите IDE: VS code или PyCharm (https://code.visualstudio.com | https://www.jetbrains.com)
1.4 Создайте директорию проекта (например "New_project")
1.5 Внутри директории создайте git репозиторий командой:
```
> git init
```
1.6 Скачайте проект с GitHub выполнив две команды:
```
> git remote add origin https://github.com/el710/p-Diploma
> git pull --set-upstream origin main
```
*[Note: на GitHub ocновная ветка называется 'main']*

1.7 С помощью BotFather в Телеграм создайте нового бота и получите ключ: токен
1.8 В IDE откройте созданную директорию и в папке *telegram* создайте файл *id_bot.py*
1.9 В файле создайте переменную *tel_token* и присвойте ей значение токена:
```
"id_bot.py"
            tel_token = "xxxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
1.10 Установите необходимые пакеты командой:
```
> pip install -r requirements.txt
```
1.11 Запустите файл *main.py* командой
```
> python main.py
```
или средствами IDE...

Вывод в терминале при запуске:
![старт программы](screen5.png)


### 2. Алгоритмы

2.1 Основной поток (main.py)

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
        ## case if no message from telegram
        ## free proccess time
        time.sleep(3)
```


---
Copyright (c) 2024 Kim Oleg <theel710@gmail.com>