from django import shortcuts, urls


def index(request):
    return shortcuts.redirect(urls.reverse("index"))
