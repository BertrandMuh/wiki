from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from . import util

import markdown as md


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    content = f"## 404 \n Sorry! the {title} page was not found." if util.get_entry(
        title) == None else util.get_entry(title)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "entry": md.markdown(content)
    })


def search(request):
    page = request.GET.get('q')
    # if page != "":
    if page in util.list_entries():
        return HttpResponseRedirect('wiki/' + page)
    else:
        possible_result = []
        for entry in util.list_entries():
            if page in entry:
                possible_result.append(entry)
        return HttpResponse(page)
    # for entry in util.list_entries():
    #     if page == entry:
    #         return HttpResponse(util.list_entries())
