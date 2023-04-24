from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django import forms
from . import util
import markdown as md
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


class EntryForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)


def edit(request, title):
    if request.method == 'POST':
        content = request.POST['content'].encode()
        util.save_entry(title, content)
        return entry(request, title)
    else:
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'content': util.get_entry(title)
        })


def error(request, content):
    return render(request, 'encyclopedia/error.html', {
        'error': md.markdown(content)
    })


def entry(request, title):
    content = f"## 404 \n Sorry! the {title} page was not found."
    if util.get_entry(title) == None:
        return error(request, content)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/entry_page.html", {
            "title": title,
            "content": md.markdown(content)
        })


def search(request):
    userInput = request.GET.get('q')
    possible_result = []

    if userInput == '':
        return HttpResponseRedirect('/')
    if userInput.capitalize() in util.list_entries():
        return HttpResponseRedirect('wiki/' + userInput.capitalize())

    for entry in util.list_entries():
        if userInput.lower() in entry.lower():
            possible_result.append(entry)

    if len(possible_result) != 0:
        return render(request, "encyclopedia/index.html", {
            "entries": possible_result
        })
    else:
        return index(request)


def newEntry(request):
    if request.method == 'POST':
        title = request.POST.get('title').capitalize()
        content = request.POST.get('content')

        if title in util.list_entries():
            content = f"## 409 \n Sorry! the {title} page already exists."
            return error(request, content)

        util.save_entry(title, content)
        return HttpResponseRedirect('/')

    else:
        return render(request, 'encyclopedia/new_entry.html', {
            'form': EntryForm()
        })


def randomEntry(request):
    position = random.randint(0, len(util.list_entries()) - 1)
    title = util.list_entries()[position]
    return HttpResponseRedirect('wiki/' + title)
