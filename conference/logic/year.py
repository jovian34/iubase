import datetime


def get_spring_year():
    spring_year = datetime.date.today().year
    if datetime.date.today().month > 8:
        return spring_year + 1
    return spring_year