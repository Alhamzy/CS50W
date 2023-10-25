from django.shortcuts import render

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_entry(request,entry_name): # entry page
    entry = util.get_entry(entry_name)
    if entry:
        # convert MD to HTML
        pass
    pass
