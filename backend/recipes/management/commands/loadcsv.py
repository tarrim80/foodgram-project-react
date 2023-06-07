import csv
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Model


class Command(BaseCommand):
    """
    Загрузка данных из файлов с расширением *.csv в таблицы БД через DjangoORM

    Загрузка производится по команде loadcsv с указанием пути к папке с файлами
    и имени приложения в котором расположены модели, например:
    manage.py loadcsv data recipes

    Класс осуществляет построчное чтение записей в файлах и заносит их в
    таблицы БД, если таковых записей не существует, или обновляет записи,
    если таковые уже есть в БД.

    В названиях файлов используется нумерация, по приоритетности загрузки
    с разделителем "_".

    В первую очередь необходимо загружать записи, поля которых имеют связи с
    другими моделями.
    """
    help = 'Загрузка данных из CSV-файлов в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('files_folder', nargs='+', type=str,
                            help='Путь к CSV-файлам')
        parser.add_argument('current_app', nargs='+', type=str,
                            help='Имя приложения с моделями')

    def handle(self, *args, **options):
        files_folder = ''.join(options['files_folder'])
        self.app = ''.join(options['current_app'])

        self.files_folder_path = os.path.join(settings.BASE_DIR.parent,
                                              files_folder)
        files = sorted(os.listdir(self.files_folder_path))
        self.csv_count, self.success_count = 0, 0

        for file in files:
            self.csv_proccess(file)

        if self.csv_count != len(files):
            self.stdout.write(
                self.style.WARNING(
                    f'Некоторые файлы в папке {files_folder} '
                    'не были обработаны.'
                )
            )
        if self.success_count == self.csv_count:
            self.stdout.write(
                self.style.SUCCESS('Все данные успешно загружены!'))
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Все файлы *.csv обработаны,'
                    ' некоторые данные не загружены.'
                )
            )

    def csv_proccess(self, file) -> None:
        """ Чтение данных из файла *.csv и запись (обновление) их в БД """
        model = self.get_model_by_name(file)
        if not model:
            return None
        path = os.path.join(self.files_folder_path, file)
        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [model(**row) for row in reader]
            fields = [f for f in reader.fieldnames if f != 'id']
            try:
                model.objects.bulk_create(
                    data, ignore_conflicts=True)
                model.objects.bulk_update(data, fields)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Данные в модель {model.__name__} успешно загружены'
                    )
                )
                self.success_count += 1
            except Exception as err:
                self.stderr.write(
                    f'С файлом {file} что-то пошло не так: {err}')

    def check_file(self, val) -> bool:
        """ Проверка расширения файла и наличия порядкового номера в имени """
        name, ext = os.path.splitext(val)
        if ext != '.csv':
            self.stdout.write(
                self.style.WARNING(
                    f'Файл {val} имеет расширение отличное от ".csv",'
                    ' поэтому не будет обработан'
                )
            )
            return False
        self.csv_count += 1
        name_list = name.split('_')
        try:
            int(name_list[0])
        except Exception:
            self.stderr.write(
                f'Файл {val} не имеет в имени порядкового номера обработки и'
                ' не может быть обработан'
            )
            return False
        self.model_name = name_list[-1]
        return True

    def get_model_by_name(self, file) -> Model or None:
        """ Определение модели Django по имени файла"""
        if not self.check_file(file):
            return None
        try:
            model = apps.get_model(self.app, self.model_name)
        except Exception:
            self.stderr.write(
                f'Модель с именем {self.model_name} '
                f'в приложении {self.app} не обнаружена'
            )
            return None
        return model
