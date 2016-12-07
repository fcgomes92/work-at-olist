from django.core.management.base import BaseCommand

from categories.util.actions import AbsolutePathAction
from categories.models import Channel, Category

import csv


class Command(BaseCommand):
    help = 'Import command in "full update" operation mode, ie it overwrites all categories of a channel with the categories in CSV.'

    def add_arguments(self, parser):
        parser.add_argument('channel', type=str, help='the channel name to be created or overwritten')
        parser.add_argument('csv_file', type=str, help='the absolute or relative path to the csv file',
                            action=AbsolutePathAction)
        parser.add_argument('-c', '--column', type=str,
                            help='the column name for categories inside the csv file. DEFAULT: categories',
                            default='categories')
        parser.add_argument('-d', '--delimiter', type=str,
                            help='csv column delimiter. DEFAULT: ,',
                            default=',')
        parser.add_argument('-q', '--quote-char', type=str,
                            help='csv text quote char',
                            default='"')

    def handle(self, *args, **options):
        csv_file = options.get('csv_file')
        channel_name = options.get('channel')
        column_name = options.get('column')
        # delimiter = options.get('delimiter')
        # quote_char = options.get('quote-char')

        # create the channel to hold all categories
        channel, created = Channel.objects.get_or_create(name=channel_name)
        if not created:
            channel.categories.all().delete()
        channel.save()

        generated_categories = {}
        created_categories = 0
        updated_categories = 0

        with open(csv_file) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                categories = row.get(column_name).split('/')
                if len(categories) > 1:
                    generated_categories['>'.join(categories).strip()], created = \
                        Category.objects.get_or_create(**dict(channel=channel,
                                                              parent=generated_categories[
                                                                  '>'.join(categories[:-1]).strip()],
                                                              name=categories[-1].strip()))

                else:
                    generated_categories[categories[0].strip()], created = \
                        Category.objects.get_or_create(**dict(channel=channel, parent=None, name=categories[0].strip()))
                if created:
                    created_categories += 1
                else:
                    updated_categories += 1

            file.close()
        print('Created categories: ', created_categories)
        print('Updated categories: ', updated_categories)
