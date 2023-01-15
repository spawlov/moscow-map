# Интерактивная карта Москвы

## Учебный проект на онлайн-курсе DevMan

#### Демо-версия доступна по <a target="_blank" href="http://spavlov.pythonanywhere.com/map/">ссылке</a>

### Как установить

Python3 должен быть уже установлен. 
Для установки зависимостей:

```
pip install -r requirements.txt
```

Применить миграции к базе данных:

````
python manage.py migrate
````

Для запуска в корне проекта нужно создать файл .env со следующим содержимым:

```
SECRET_KEY=<Здесь должен быть секретный ключ Django>

ALLOWED_HOSTS=<Хост, на котором будет размещен проект>
```

Создать админа для базы данных:

```
python manage.py createsuperuser
```

Добавить локации и картинки в базу данных через admin панель.<br>
Добавление локаций возможно с помощью команды:

```
python manage.py load_place http://адрес/файла.json
```

Формат файла локации:

```
{
    "title": "Экскурсионный проект «Крыши24.рф»",
    "imgs": [
        "https://kudago.com/media/images/place/d0/f6/d0f665a80d1d8d110826ba797569df02.jpg",
        "https://kudago.com/media/images/place/66/23/6623e6c8e93727c9b0bb198972d9e9fa.jpg",
        "https://kudago.com/media/images/place/64/82/64827b20010de8430bfc4fb14e786c19.jpg",
    ],
    "description_short": "Хотите увидеть Москву с высоты птичьего полёта?",
    "description_long": "<p>Проект «Крыши24.рф» проводит экскурсии ...</p>",
    "coordinates": {
        "lat": 55.753676,
        "lng": 37.64
    }
}
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
