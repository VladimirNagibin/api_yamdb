import csv

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from reviews.models import Category, Comments, Genre, Review, Title

DIR_DATA = settings.BASE_DIR / 'static/data'
DATA = (
    ('users.csv',
     get_user_model(),
     ['id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name']),
    ('category.csv', Category, ['id', 'name', 'slug']),
    ('genre.csv', Genre, ['id', 'name', 'slug']),
    ('titles.csv', Title, ['id', 'name', 'year', 'category_id']),
    ('genre_title.csv',
     apps.get_model('reviews', 'title_genre'),
     ['id', 'title_id', 'genre_id']),
    ('review.csv',
     Review,
     ['id', 'title_id', 'text', 'author_id', 'score', 'pub_date']),
    ('comments.csv', Comments, [
        'id', 'review_id', 'text', 'author_id', 'pub_date'
    ])
)


class Command(BaseCommand):

    def load_obj(self, filename, obj, fields):
        try:
            with open(f'{DIR_DATA}/{filename}', encoding='utf-8') as file_data:
                reader = csv.reader(file_data)
                header = next(reader)
                if header == fields:
                    for row in reader:
                        object_value = {
                            key: value for key, value in zip(header, row)
                        }
                        try:
                            obj.objects.update_or_create(**object_value)
                        except IntegrityError:
                            return (f'Файл {filename} не корректные данные: '
                                    f'{object_value} для {obj.__name__}')
                else:
                    return (f'Файл {filename} cтруктура полей не '
                            f'соответствует таблице {obj.__name__}')
        except FileNotFoundError:
            return f'Файл {filename} невозможно открыть'
        except Exception as e:
            return f"Ошибка {e} при работе с файлом {filename}"
        return f'Файл {filename} загружен'

    def handle(self, *args, **kwargs):
        report = ''
        for filename, obj, fields in DATA:
            if kwargs['erase']:
                obj.objects.all().delete()
            report += self.load_obj(filename, obj, fields) + '\n'
        return report

    def add_arguments(self, parser):
        parser.add_argument(
            '-e',
            '--erase',
            action='store_true',
            default=False,
            help='Очистить таблицу перед загрузкой'
        )
