## Тестовое задание Workmate-Django-DRF
### Описание проекта

Этот проект представляет собой онлайн выставку котят, где пользователи могут регистрироваться, добавлять своих котят, оценивать их и оставлять комментарии. Основная цель проекта - создать интерактивную платформу для любителей, где они могут делиться информацией, участвовать в выставках и оценивать котят других пользователей.

Основные возможности:

1. Регистрация пользователей:
- Пользователи могут зарегистрироваться, указав свою электронную почту, имя и другие данные. Доступны две роли: “participant” (Участник) и “visitor” (Посетитель).
2. Управление породами:
- Пользователи с ролью “participant” могут добавлять, редактировать и удалять породы.
3. Управление созданием:
- Пользователи могут добавлять информацию о своих котятах, включая цвет, имя, возраст и описание. Котята привязываются к породам и владельцам.
4. Оценка:
- Пользователи могут оставлять оценки и комментарии. Оценки могут быть в диапазоне от 1 до 5.
5. Фильтрация и поиск:
- Возможность фильтрации котят по породе.
6. Статистика:
- Возможность получения статистики оценок для каждого котенка.

### __Технологии и библиотеки__
* [Python 3.10.12](https://www.python.org/doc/)
* [Django 5.1.1](https://docs.djangoproject.com/en/4.2/)
* [Django REST Framework  3.15.2](https://www.django-rest-framework.org/)
* [djangorestframework-simplejwt 5.3.1](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [PostgreSQL 14](https://www.postgresql.org/docs/14/index.html)
* [pytest-xdist 3.6.1](https://pytest-xdist.readthedocs.io/en/stable/)
* [pytest-django 4.9.0](https://pytest-django.readthedocs.io/en/latest/index.html)
* [pytest-factoryboy 2.7.0](https://pytest-factoryboy.readthedocs.io/en/stable/)
* [Docker-Compose](https://docs.docker.com/compose/release-notes/)

## Установка на локальном компьютере
### 1. Клонируйте репозиторий:
```
git clone https://github.com/minkeviiich/Online_exhibition-Workmate--Django-DRF.git
```
### 2. Сборка Docker-образа: (Команды автоматизированы с помощью Makefile)

- Соберите Docker-образ

```
make build
```

### 3. Запуск Docker Compose:

```
make up
```
### 4. Запуск Тестов: (Внимание: команда make test запускает тесты с использованием pytest-xdist, распределяя их выполнение на 4 процессора/ядра. Значение можно изменить в Makefile)

```
make test
```
### 5. Остановка и удаление контейнеров:

```
make down
```

### __OpenAPI документация__
* Swagger: http://0.0.0.0:8000/swagger/
