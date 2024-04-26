import random

from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
import markdown
from wiki import settings
from . import util
import os
from django.contrib import messages
from django.http import HttpResponseNotFound


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def read_markdown_file(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'entries/', filename + '.md')
    if os.path.exists(file_path):
        with open(file_path, 'r') as markdown_file:
            markdown_content = markdown_file.read()
            html_content = markdown.markdown(markdown_content)
        return render(request, 'encyclopedia/temp.html', {'html_content': html_content, 'filename': filename})
    else:
        return HttpResponse("File Not Found", status=404)



def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            encyclopedia_folder = os.path.join(settings.BASE_DIR, 'entries')
            files = os.listdir(encyclopedia_folder)
            results = []
            for file_name in files:
                with open(os.path.join(encyclopedia_folder, file_name), 'r', encoding='utf-8') as file:
                    content = file.read()
                    if query.lower() in content.lower():
                        title = os.path.splitext(os.path.basename(file_name))[0]
                        url = f'/wiki/{title}/'
                        results.append({'title': title, 'url': url})
            return render(request, 'encyclopedia/search_result.html', {'results': results, 'query': query})
        else:
            return redirect('index')
    else:
        pass
def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if os.path.exists(f'entries/{title}.md'):
            messages.error(request, 'An article with this title already exists.')
        else:
            with open(os.path.join(settings.BASE_DIR, 'entries', f'{title}.md'), 'w') as f:
                f.write(content)
            return read_markdown_file(request, title)
    return render(request, 'encyclopedia/create_page.html')
def edit_page(request, title):
    try:
        with open(f'entries/{title}.md', 'r') as f:
            content = f.read()
        return render(request, 'encyclopedia/edit_page.html', {'title': title, 'content': content})
    except FileNotFoundError:
        return HttpResponseNotFound('Page not found')

def save_page(request, title):
    if request.method == 'POST':
        content = request.POST.get('content')
        with open(os.path.join(settings.BASE_DIR, 'entries', f'{title}.md'), 'w') as f:
            f.write(content)
        return read_markdown_file(request, title)
def random_page_choice(request):
    pages = util.list_entries()
    random_page = random.choice(pages)
    return read_markdown_file(request, random_page)
