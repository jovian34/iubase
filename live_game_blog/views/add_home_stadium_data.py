from django import shortcuts, http, urls

from live_game_blog import models as lgb_models
from live_game_blog import forms


def view(request, team_pk):
    if not request.user.has_perm("live_game_blog.add_stadium"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        form = forms.AddHomeStadiumDataForm(request.POST)
        if form.is_valid():
            add_stadium = lgb_models.Stadium(
                address = form.cleaned_data["address"],
                city = form.cleaned_data["city"],
                state = form.cleaned_data["state"],
                country = form.cleaned_data["country"],
                timezone = form.cleaned_data["timezone"],
                lat = form.cleaned_data["lat"],
                long = form.cleaned_data["long"],
            )
            add_stadium.save()
            this_stadium = lgb_models.Stadium.objects.get(
                address=form.cleaned_data["address"],
                city = form.cleaned_data["city"],
                state = form.cleaned_data["state"],
            )
            add_stadium_config = lgb_models.StadiumConfig(
                stadium = this_stadium,
                stadium_name = form.cleaned_data["stadium_name"],
                config_date = form.cleaned_data["config_date"],
                surface_inf = form.cleaned_data["surface_inf"],
                surface_out = form.cleaned_data["surface_out"],
                surface_mound = form.cleaned_data["surface_mound"],
                photo = form.cleaned_data["photo"],
                orientation = form.cleaned_data["orientation"],
                left = form.cleaned_data["left"],
                center = form.cleaned_data["center"],
                right = form.cleaned_data["right"],
                capacity = form.cleaned_data["capacity"],
                lights = form.cleaned_data["lights"],
                home_dugout = form.cleaned_data["home_dugout"],
            )
            add_stadium_config.save()
            this_stadium_config = lgb_models.StadiumConfig.get(
                stadium_name = form.cleaned_data["stadium_name"],
            )
            add_home_stadium = lgb_models.HomeStadium(
                team = lgb_models.Team.objects.get(pk=team_pk),
                stadium_config = this_stadium_config,
                designate_date = form.cleaned_data["designate_date"],
            )
            add_home_stadium.save()
            return shortcuts.redirect(urls.reverse("stadiums"))
        else:
            print("FORM NOT VALID!!!!!!!")
    else:
        team = lgb_models.Team.objects.get(pk=team_pk)
        template_path = "live_game_blog/add_home_stadium_data.html"
        context = {
            "team": team,
            "page_title": f"Add Home Stadium Data for {team.team_name}",
            "form": forms.AddHomeStadiumDataForm,
        }
        return shortcuts.render(request, template_path, context)