from django.core.management.base import BaseCommand
from live_game_blog.logic import weather_daily
from conference.logic import rpis, year


class Command(BaseCommand):
    help = "set weather data for games 2 to 500 days out"

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        weather_daily.get_and_set_weather_data_daily()
        rpis.store_b1g_rpi_data_in_database(year.get_this_year())
