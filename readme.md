# Гриша Бот
Бот для бесед, написанный на **Python 3.10**

Исходники некоторых функций бота:

- [Казино](/src/blueprints/casino.py)
- [Кастомные ники](/src/blueprints/custom_name.py)
- [Обзывалки](/src/blueprints/insults.py)
- [Рп команды](/src/blueprints/rp.py)
- [Выбор человека дня](/src/blueprints/person_of_day.py)
- [Казино и миниэкономика](/src/blueprints/balance.py)

---
## Гайд по установке
1. Установить зависимости (`pip3.10 install -U -r requirements.txt`)
1. Скопировать файл `.env.example` в `.env` и заполнить
1. `aerich upgrade`
1. Запуск командой `python3.10 -m src`
---
## Гайд по обновлению
1. `git pull`
1. `pip3.10 install -U -r requirements.txt`
1. `aerich upgrade`
1. Проверить `.env.example` на наличие новых переменных
---
## Contributing
Пул реквесты приветствуются.

---
## Лицензия
Этот проект имеет [MIT](/LICENSE) лицензию.
