from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from accounts.models import CustomUser
from live_game_blog.forms import BlogEntryForm
from live_game_blog.models import Game, BlogEntry


@login_required
def view(request, game_pk):
    if request.method == "POST":
        form = BlogEntryForm(request.POST)
        if form.is_valid():
            add_blog = save_blog_entry(request, game_pk, form)
            if form.cleaned_data["is_x_embed"]:
                assign_iubase_as_author(add_blog)
        return redirect(reverse("edit_live_game_blog", args=[game_pk]))
    else:
        form = BlogEntryForm()
        context = {"form": form, "game_pk": game_pk}
        return render(
            request, "live_game_blog/partials/add_blog_entry_only.html", context
        )


def save_blog_entry(request, game_pk, form):
    add_blog = BlogEntry(
        game=Game.objects.get(pk=game_pk),
        author=request.user,
        blog_entry=form.cleaned_data["blog_entry"],
        is_raw_html=form.cleaned_data["is_raw_html"],
        include_scoreboard=False,
    )
    add_blog.save()
    return add_blog


def assign_iubase_as_author(add_blog):
    iubase17 = CustomUser.objects.filter(username="iubase17").last()
    add_blog.author = iubase17
    add_blog.save()
