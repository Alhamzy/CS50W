from django.shortcuts import render
from django import forms
import re,os
from . import util
import markdown2
from django.views.decorators.csrf import csrf_protect


class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label = "Title")
    text_area = forms.CharField(label = "Description")

    entries = util.list_entries()
    def clean_entry_title(self):
        entry_title = self.cleaned_data['entry_title']
        if entry_title in self.entries:
            raise forms.ValidationError("Entry with this title already exists.")
        return entry_title

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_entry(request,entry): # entry page
    markdown_content = util.get_entry(entry)
    if markdown_content:
        # convert MD to HTML
        # convert headings, bold text, lists and links
        markdown_content = markdown_to_html(markdown_content)
        return render(request,"encyclopedia/view_entry.html", {
            'markdown_content': markdown_content
        })
    
    return render(request,"encyclopedia/page_not_found.html")    

def new_entry(request):
    entries = util.list_entries()
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid(): # add new entry to list
            util.save_entry(form.cleaned_data['entry_title'],form.cleaned_data['text_area'])
            markdown_content = util.get_entry(form.cleaned_data['entry_title'])
            if markdown_content:
                markdown_content = markdown_to_html(markdown_content)
                return render(request,"encyclopedia/view_entry.html", {
            'markdown_content': markdown_content
        })
            # return view_entry(request,form.cleaned_data['entry_title'])
        else: # give user a chance to correct form
            return render(request, "encyclopedia/new_entry.html",{
                'form': form
            })
            
    return render(request,"encyclopedia/new_entry.html",{
        'form': NewEntryForm()
    })

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


