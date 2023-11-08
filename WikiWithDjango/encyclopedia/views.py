from django.shortcuts import render,redirect
from django.urls import reverse
from django import forms
import re,os
from . import util
import markdown2
from django.views.decorators.csrf import csrf_protect
import random


class NewEntryForm(forms.Form):
    entry_title = forms.CharField()
    text_area = forms.CharField()

    entries = util.list_entries()
    def assert_unique_title(self):
        entry_title = self.cleaned_data['entry_title']
        if entry_title in self.entries:
            raise forms.ValidationError("Entry with this title already exists.")
        return entry_title

class EditEntryDescription(forms.Form):
    text_area = forms.CharField()



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_entry(request,entry_title): # entry page
    markdown_content = util.get_entry(entry_title)
    if markdown_content: # convert MD to HTML
        markdown_content = markdown_to_html(markdown_content)
        return render(request,"encyclopedia/view_entry.html", {
            'entry_title': entry_title,
            'markdown_content': markdown_content
        })
    return render(request,"encyclopedia/page_not_found.html")    

def new_entry(request):
    entries = util.list_entries()
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        print("request is post")
        if form.is_valid(): # add new entry to list
            util.save_entry(form.cleaned_data['entry_title'],form.cleaned_data['text_area'])
            # redirect user to new entry
            return redirect("encyclopedia:view_entry",entry_title=form.cleaned_data['entry_title'])
        else: # give user a chance to correct form
            return render(request, "encyclopedia/new_entry.html",{
                'form': form
            })
    return render(request,"encyclopedia/new_entry.html",{
        'form': NewEntryForm()
    })

def edit_entry(request,entry_title):
    entry = util.get_entry(entry_title)
    markdown_content = markdown_to_html(entry)
    if request.method == 'POST':
        form = EditEntryDescription(request.POST)
        if form.is_valid(): # add new entry to entries
            print(form.cleaned_data['text_area'])
            util.save_entry(entry_title,html_to_markdown(form.cleaned_data['text_area']))
            # redirect user to updated entry
            return redirect("encyclopedia:view_entry",entry_title)
        else: # give user a chance to correct form
            return render(request, "encyclopedia/edit_entry.html",{
                'form': form
            })
    else:
        form = EditEntryDescription(initial={'text_area': markdown_content})

    return render(request,"encyclopedia/edit_entry.html",{
        'form': form,
        'entry_title': entry_title,
        'markdown_content': markdown_content
    })

def page_not_found(request):
    return render(request,"encyclopedia/page_not_found.html")

def random_entry(request):
    entries = util.list_entries()
    rand  = random.randint(0,len(entries)-1)
    entry_title = entries[rand]
    return redirect('encyclopedia:view_entry',entry_title)


    
    

def markdown_to_html(markdown_text):
    # Convert headers (up to level 6)
    markdown_text = re.sub(r'###### (.*?)\n', r'<h6>\1</h6>', markdown_text)
    markdown_text = re.sub(r'##### (.*?)\n', r'<h5>\1</h5>', markdown_text)
    markdown_text = re.sub(r'#### (.*?)\n', r'<h4>\1</h4>', markdown_text)
    markdown_text = re.sub(r'### (.*?)\n', r'<h3>\1</h3>', markdown_text)
    markdown_text = re.sub(r'## (.*?)\n', r'<h2>\1</h2>', markdown_text)
    markdown_text = re.sub(r'# (.*?)\n', r'<h1>\1</h1>', markdown_text)

    # Convert bold text
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown_text)

    # Convert italic text
    markdown_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', markdown_text)

    # Convert unordered lists
    markdown_text = re.sub(r'^- (.+)', r'<ul>\n<li>\1</li>', markdown_text, flags=re.M)
    markdown_text += '</ul>'

    # Convert line breaks
    markdown_text = re.sub(r'\n', '<br>', markdown_text)

    # Convert links
    markdown_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown_text)

    return markdown_text

def html_to_markdown(html_text):
    # Convert headers (up to level 6)
    html_text = re.sub(r'<h6>(.*?)</h6>', r'###### \1\n', html_text)
    html_text = re.sub(r'<h5>(.*?)</h5>', r'##### \1\n', html_text)
    html_text = re.sub(r'<h4>(.*?)</h4>', r'#### \1\n', html_text)
    html_text = re.sub(r'<h3>(.*?)</h3>', r'### \1\n', html_text)
    html_text = re.sub(r'<h2>(.*?)</h2>', r'## \1\n', html_text)
    html_text = re.sub(r'<h1>(.*?)</h1>', r'# \1\n', html_text)

    # Convert bold text
    html_text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html_text)

    # Convert italic text
    html_text = re.sub(r'<em>(.*?)</em>', r'*\1*', html_text)

    # Convert unordered lists
    html_text = re.sub(r'<ul>\s*<li>(.*?)</li>\s*</ul>', r'\n- \1', html_text)

    # Convert line breaks
    html_text = re.sub(r'<br>', r'\n', html_text)

    # Convert links
    html_text = re.sub(r'<a href="(.*?)">(.*?)</a>', r'[\2](\1)', html_text)

    return html_text

