from django.shortcuts import render
import re,os
from . import util
import markdown2



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
    
    #### insert case for "page not found" ####
    return render(request,"encyclopedia/page_not_found.html")    

import re

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


