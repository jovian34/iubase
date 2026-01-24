from django.core.management.base import BaseCommand
from live_game_blog import models as lgb_models


class Command(BaseCommand):
    help = "report a database output to prove this works"

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        iu = lgb_models.Team.objects.get(team_name="Indiana")
        self.stdout.write(f"Indiana is the {iu.mascot}")
