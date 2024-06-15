import csv
import os

import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

with open('../../static/data/category.csv', encoding='utf-8') as file:
    from reviews.models import Category
    reader = csv.reader(file)
    colum_names = next(reader)
    for row in reader:
        row_data = dict(zip(colum_names, row))
        genre = Category.objects.create(**row_data)
        genre.save()

with open('../../static/data/genre.csv', encoding='utf-8') as file:
    from reviews.models import Genre
    reader = csv.reader(file)
    colum_names = next(reader)
    for row in reader:
        row_data = dict(zip(colum_names, row))
        genre = Genre.objects.create(**row_data)
        genre.save()

with open('../../static/data/users.csv', encoding='utf-8') as file:
    user = get_user_model()
    reader = csv.reader(file)
    colum_names = next(reader)
    for row in reader:
        row_data = dict(zip(colum_names, row))
        genre = user.objects.create(**row_data)
        genre.save()

with open('../../static/data/titles.csv', encoding='utf-8') as file:
    from reviews.models import Category, Title
    reader = csv.reader(file)
    colum_names = next(reader)
    for row in reader:
        row_data = dict(zip(colum_names, row))
        category = Category.objects.get(id=row_data.pop('category'))
        genre = Title.objects.create(category=category, **row_data)
        genre.save()

with open('../../static/data/review.csv', encoding='utf-8') as file:
    from reviews.models import Review
    reader = csv.reader(file)
    colum_names = next(reader)
    for row in reader:
        row_data = dict(zip(colum_names, row))
        author = get_user_model().objects.get(id=row_data.pop('author'))
        genre = Review.objects.create(author=author, **row_data)
        genre.save()

with open('../../static/data/comments.csv', encoding='utf-8') as file:
    from reviews.models import Comment
    reader = csv.reader(file)
    colum_names = next(reader)
    for row in reader:
        row_data = dict(zip(colum_names, row))
        author = get_user_model().objects.get(id=row_data.pop('author'))
        genre = Comment.objects.create(author=author, **row_data)
        genre.save()

with open('../../static/data/genre_title.csv', encoding='utf-8') as file:
    from reviews.models import Genre, Title
    reader = csv.reader(file)
    column_names = next(reader)
    for row in reader:
        row_data = dict(zip(column_names, row))
        genre = Genre.objects.get(id=row_data.get('genre_id'))
        title = Title.objects.get(id=row_data.get('title_id'))
        title.genre.add(genre)
        title.save()
