from django.core.management.base import BaseCommand
from conference import rpis


class Command(BaseCommand):
    help = "add rpi values for 2025"

    def add_arguments(self, parser):
        return super().add_arguments(parser)
    
    def handle(self, *args, **options):
        rpis.store_b1g_rpi_data_in_database(2025)