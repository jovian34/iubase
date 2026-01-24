from django.core.management.base import BaseCommand
from live_game_blog.logic import weather_hourly


class Command(BaseCommand):
    help = "set weather data for games under 48 hours out"

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        weather_hourly.get_and_set_weather_data_hourly()
