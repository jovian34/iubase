import requests
from bs4 import BeautifulSoup
from django.db.models import Q

from conference import models as conf_models
from live_game_blog import models as lgb_models


def store_b1g_rpi_data_in_database(spring_year):
    rpis = make_b1G_rpi_dict(spring_year)
    for team_name, rpi_rank in rpis.items():
        print(f"{team_name}: {rpi_rank}")
        team = lgb_models.Team.objects.get(team_name=team_name)
        try:
            team_rpi = conf_models.TeamRpi.objects.get(
                Q(team=team) & Q(spring_year=spring_year)
            )
        except conf_models.TeamRpi.DoesNotExist:
            add_team_rpi = conf_models.TeamRpi(
                team=team,
                rpi_rank=rpi_rank,
                spring_year=spring_year,
            )
            add_team_rpi.save()
            continue  
        team_rpi.rpi_rank = rpi_rank
        team_rpi.save()


def make_b1G_rpi_dict(spring_year):
    table = parse_table(spring_year)
    big_ten_rpi = {}
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if not cells:
            continue
        team_name = cells[1].get_text(strip=True)
        rpi_text = cells[7].get_text(strip=True)
        if rpi_text.isdigit():
                big_ten_rpi[team_name] = int(rpi_text)
    return big_ten_rpi


def parse_table(spring_year):
    soup = request_table_into_parser(spring_year)
    table = soup.find(
        "table",
        class_="normal-grid alternating-rows stats-table"
    )
    if table is None:
        raise RuntimeError("Stats table not found")
    return table


def request_table_into_parser(spring_year):
    nolan_url = f"https://www.warrennolan.com/baseball/{spring_year}/conference/Big-Ten"
    HEADERS = {"User-Agent": "Mozilla/5.0_apps.iubase.com"}
    resp = requests.get(nolan_url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")