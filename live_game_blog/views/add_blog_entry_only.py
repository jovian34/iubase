from django import http, shortcuts, urls
from django.contrib.auth import decorators as auth
from django.contrib.auth import models as auth_models
from accounts import models as acc_models
from live_game_blog import forms as lgb_forms
from live_game_blog import models as lgb_models


def view(request, game_pk):
    if not request.user.has_perm("live_game_blog.add_blogentry"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        return process_form_validate_and_save_new_blog(request, game_pk)
    else:
        return render_clean_add_blog_entry_form(request, game_pk)


def process_form_validate_and_save_new_blog(request, game_pk):
    form = lgb_forms.BlogEntryForm(request.POST)
    if form.is_valid():
        add_blog = save_blog_entry(request, game_pk, form)
        if form.cleaned_data["is_x_embed"]:
            assign_iubase_as_author(add_blog)
    return shortcuts.redirect(urls.reverse("live_game_blog", args=[game_pk]))


def save_blog_entry(request, game_pk, form):
    add_blog = lgb_models.BlogEntry(
        game=lgb_models.Game.objects.get(pk=game_pk),
        author=request.user,
        blog_entry=form.cleaned_data["blog_entry"],
        is_raw_html=form.cleaned_data["is_raw_html"],
        is_photo_only=form.cleaned_data["is_photo_only"],
        include_scoreboard=False,
    )
    add_blog.save()
    return add_blog


def assign_iubase_as_author(add_blog):
    iubase17 = acc_models.CustomUser.objects.filter(username="iubase17").last()
    add_blog.author = iubase17
    add_blog.save()


def render_clean_add_blog_entry_form(request, game_pk):
    context = {"form": lgb_forms.BlogEntryForm(), "game_pk": game_pk}
    template_path = "live_game_blog/partials/add_blog_entry_only.html"
    return shortcuts.render(request, template_path, context)
