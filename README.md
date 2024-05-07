# QUIZZZ

## Запуск
Для запуска проекта необходимо установить зависимости из файла requirements.txt
```bash
py -m venv venv
venv\Scripts\activate.bat
pip install requirements.txt
```
Затем нужно выполнить миграции
```bash
py manage.py migrate
```
Далее создать пользователя для входа в панель администратора (/admin)
```bash
py manage.py createsuperuser
```
И, наконец, запустить проект!
```bash
py manage.py runserver
```