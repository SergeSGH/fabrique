# message distribution
### Описание:
проект предоставляет api-интерфейс для организации рассылки сообщений 


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/SergeSGH/fabrique.git
```
```
cd fabrique/distrib
```

В папке проекта создать файл .env в котором определить ключевые переменные:
```
DB_ENGINE: вид БД
DB_NAME: имя БД
POSTGRES_USER: логин пользователя БД
POSTGRES_PASSWORD: пароль пользователя БД
DB_HOST: приложение БД 
DB_PORT: порт БД
SECRET_KEY: секретный ключ
TOKEN1: секретный токен для доступа к API отправки сообщений
TOKEN2: секретный токен (ч2)
TOKEN3: секретный токен (ч3)
```
Запустить сервер БД PostgreSQL
Выполнить миграции и создать суперпользователя 
```
python manage.py migrate
python manage.py createsuperuser

```
Запустить сервер:
```
python manage.py runserver
```

### Документация проекта в формате OpenAPI:

```
http://127.0.0.1:8000/docs/
```