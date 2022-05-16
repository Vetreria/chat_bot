# Боты для поддержки

Программа состоит из трёх частей. Позволяет распознавать речь пользователя и подбирает оптимальные ответы от поддержки.
Содержит два бота для telegram и VK, а так же скрипт обучения ботов из вопросов и ответов.


## Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

## Запустить


Для работы программы нужно создать файл окружения .env
В него необходимо ввести данные для авторизации в соцсетях и сервисе dialogflow.
Соответсвующую группу в ВК и бот в Telegram нужно создать отдельно.

Дополнительно нужно будет создать проекты:

https://cloud.google.com/dialogflow/docs/quick/setup
https://dialogflow.cloud.google.com/#/login
https://cloud.google.com/dialogflow/docs/quick/build-agent

А так же можно руками создать в проекте intent  с вопросами и ответами.


```
TG_TOKEN='ТОКЕН_ТЕЛЕГРАММ_БОТА'
GOOGLE_APPLICATION_CREDENTIALS='ПУТЬ_ДО_JSON_ФАЙЛА_АВТОРИЗАЦИИ '
GOOGLE_CLOUD_PROJECT_ID="ID_ПРОЕКТА_GOOGLE_CLOUD"
LEARNING_INTENTS="путь_до_файла_с_обучением_бота.json"
VK_GROUP_API="API_TOKEN_VK_GROUP"
```

Для запуска бота telegram нужно запустить main.py

```
python main.py
```

Для запуска бота для группы в VK нужно запустить файл vk.py

```
python vk.py
```

Для обучения бота новым темам нужно запустить lerning.py

```
python lerning.py
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](dvmn.org)