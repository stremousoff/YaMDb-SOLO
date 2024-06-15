### О проекте YaMDb:

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Стэк:
```
Python
Sqlite3
Django
Django Restframe Work(DRW)
Djoser
```
### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/stremousoff/yamd_api
```
```
cd yamd_api
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
### Спецификация ReDoc:
```
http://127.0.0.1:8000/redoc/
```
### Примеры запросов:
1- GET - Get item list - HTTP Response Code: 200
```
http://127.0.0.1:8000/api/v1/titles/

    HTTP/1.1 200
    Content-Type: application/json
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": 0,
          "name": "string",
          "year": 0,
          "rating": 0,
          "description": "string",
          "genre": [
            {
              "name": "string",
              "slug": "^-$"
            }
          ],
          "category": {
            "name": "string",
            "slug": "^-$"
          }
        }
      ]
    }
```
2- GET - Get item list - HTTP Response Code: **200**
```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/

    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
```
3- POST - Create a new item - HTTP Response Code: **201**
```
http://127.0.0.1:8000/api/v1/titles/
    HTTP/1.1  201
    Content-Type: application/json
    {
      "name": "string",
      "year": 0,
      "description": "string",
      "genre": [
        "string"
      ],
      "category": "string"
    }
```
Автор проекта  [Stremousoff](https://github.com/stremousoff/)