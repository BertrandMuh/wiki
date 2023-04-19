from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
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
    userInput = request.GET.get('q').capitalize()
    possible_result = []

    if userInput == '':
        return HttpResponseRedirect('/')
    elif userInput in util.list_entries():
        return HttpResponseRedirect('wiki/' + userInput)

    for entry in util.list_entries():
        if userInput.lower() in entry.lower():
            possible_result.append(entry)

    if len(possible_result) != 0:
        return render(request, "encyclopedia/index.html", {
            "entries": possible_result
        })


def newPage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect('/')

    else:
        return render(request, 'encyclopedia/new_page.html', {
            'form': util.NewPageForm()
        })
