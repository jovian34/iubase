from django.core.management.base import BaseCommand, CommandError
from live_game_blog.logic import weather_daily


class Command(BaseCommand):
    help = "set weather data for games 2 to 500 days out"

    def add_arguments(self, parser):
        return super().add_arguments(parser)
    
    def handle(self, *args, **options):
        weather_daily.get_and_set_weather_data_daily()