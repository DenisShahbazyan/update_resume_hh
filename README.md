# Автоподнятие резюме HH.RU

## Описание:
Автоподнятие резюме на сайте HH.RU. Заходит каждые тридцать минут на сайт и проверяет, можно ли поднять Ваше резюме, если можно - поднимает, если нет, ждет еще тридцать минут. Действия выводятся в консоль, а так же логгируются.
Скрипт поднимает ВСЕ резюме, которые есть в списке!
При работе скрипта, в корневой папке проекта создаются две папки:
1. `cookie` - с Вашими куками, для авторизации.
2. `logs` - с Вашими логами.
<img src="/data/img/Screenshot.png" alt="sch" style="max-width: 100%;">

## Развертывание:
- Склонируйте проект на Ваш компьютер 
```sh 
git clone https://github.com/DenisShahbazyan/update_resume_hh.git
``` 
- Перейдите в папку с проектом 
```sh 
cd update_resume_hh
``` 
- Создайте и активируйте виртуальное окружение 
```sh 
python -m venv venv 
source venv/Scripts/activate 
``` 
- Обновите менеджер пакетов (pip) 
```sh 
pip install --upgrade pip 
``` 
- Установите необходимые зависимости 
```sh 
pip install -r requirements.txt
``` 

В папке `src` создайте файл `.env` - в нем будут храниться переменные окружения для проекта. Пример его содержимого ниже:
```sh
LOGIN=79991112255
PASSWORD=my_password
```
- Готово! Можно запускать

### Запуск exe:
- Из корня проекта выполняем команду
```sh
pyinstaller --name update_resume_hh src/main.py
```
- Появятся две папки:
1. build - в ней служебная информация (эта папка нам не нужна)
2. dist - в ней как раз будет наш проект в папке `update_resume_hh`
- Эту папку можно скопировать, куда удобно, и в ней запускать файл `update_resume_hh.exe` (так же для него можно создать ярлык).
- В папке `update_resume_hh` создать `.env` файл, с вашими данными для авторизации.
```sh
LOGIN=79991112255
PASSWORD=my_password
```

## Системные требования:
- [Python](https://www.python.org/) 3.10.4

## Планы по доработке:
>Если появятся баги, будем исправлять 😆

## Используемые технологии:
- [python-dotenv](https://pypi.org/project/python-dotenv/) 0.20.0
- [tqdm](https://pypi.org/project/tqdm/) 4.64.0
- [selenium](https://pypi.org/project/selenium/) 4.3.0
- [webdriver-manager](https://pypi.org/project/webdriver-manager/) 3.8.2

## Авторы:
- [Denis Shahbazyan](https://github.com/DenisShahbazyan)

## Лицензия:
- MIT
