from django.core.management.base import BaseCommand, CommandError
from live_game_blog.logic import weather


class Command(BaseCommand):
    help = "set weather data for games 8 to 500 days out"

    def add_arguments(self, parser):
        return super().add_arguments(parser)
    
    def handle(self, *args, **options):
        weather.get_weather_for_games_over_one_week_from_now()