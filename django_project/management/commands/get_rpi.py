from django.core.management.base import BaseCommand
from conference.logic import rpis
from conference.logic import year


class Command(BaseCommand):
    help = "add rpi values for 2025"

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        rpis.store_b1g_rpi_data_in_database(year.get_spring_year())
