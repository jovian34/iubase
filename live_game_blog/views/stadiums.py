from django import shortcuts

def view(request):
    template_path = "live_game_blog/stadiums.html"
    context = {

    }
    return shortcuts.render(request, template_path, context)