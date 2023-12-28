# cafe_azu_bot_3


### О проекте

Данный проект предназначен для автоматизации процесса резервации столов в AZU кафе



### Запуск
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SGERx/cafe_azu_bot.git
```

```
cd cafe_azu_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Запуск
```
# Из дирректории cafe_azu_bot/app/

python3 main.py
```
 Создание миграций и применение
```
alembic revision --autogenerate -m 'YOUR MESSAGE'

alembic upgrade head
```


### Технологии
Проект написан на Python/AIOGRAM/SQLALCHEMY, а все используемые технологии удобно расположены в файле requirements.txt

### Автор
Дмитрий С - Teamleader
Сергей Герасимов
Кирилл П
Максим Т
Андрей Б
