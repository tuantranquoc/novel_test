from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import requests
from bs4 import BeautifulSoup
from .models import Author, Manga, Category, Chapter
from django.template import loader
import re
from django.template.defaultfilters import slugify
# Create your views here.


def craw(href):
    # ...
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')

    description_scrap = soup.find_all(class_="desc-text")
    author = soup.find("a", itemprop="author")
    categories = soup.find_all("a", itemprop="genre")
    source = soup.find("span", class_="source")
    status = soup.find("span", class_="text-primary")
    status_01 = soup.find("span", class_="text-success")
    chapters = soup.find_all("ul", class_="list-chapter")
    title = soup.find("h3", class_="title")

    description = description_scrap[0]

    if not Author.objects.filter(name=author.text):
        Author.objects.create(name=author.text)
    if not status:
        status = status_01
    if status.text == "Đang ra":
        status = 1
    else:
        status = 2
    if title:
        if not Manga.objects.filter(title=title.text):
            Manga.objects.create(
                title=title.text, description=description.text, status=status, slug=slugify(title.text))
    for c in categories:
        if c.text:
            if not Category.objects.filter(name=c.text):
                Category.objects.create(name=c.text)
            manga = Manga.objects.filter(title=title.text).first()
            category = Category.objects.filter(name=c.text).first()
            manga.category.add(category)

    for page in chapters:
        chapter = page.find_all("a")
        manga = Manga.objects.filter(title=title.text).first()
        if manga:
            for c in chapter:
                chapter_number = int(re.search(r'\d+', c.text).group())
                check_chapter_list = Chapter.objects.filter(manga=manga)
                chapter_ = Chapter.objects.filter(
                    title=c.text, chapter=chapter_number, manga=manga).first()
                if not chapter_:
                    chapter_ = Chapter.objects.create(
                        title=c.text, chapter=chapter_number, manga=manga)
                    craw_chapter_content(c.get('href'), manga, chapter_)


def craw_chapter_content(href, manga, chapter):
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find("div", id="chapter-c")
    if content:
        chapter.content = content.text
        chapter.save()


def main_function(request):
    page = requests.get(
        "https://truyenfull.vn")
    soup = BeautifulSoup(page.content, 'html.parser')
    mangas = soup.find_all("h3", itemprop="name")

    for m in mangas:
        children = m.findChildren("a", recursive=False)

        for c in children:
            href = c.get('href')
            craw(href)
        # href = children[1].get('href')

    return HttpResponse('<h1>Craw success</h1>')


def index(request):
    novel_list = Manga.objects.all().order_by('-created')[:10]
    template = loader.get_template('polls/index.html')
    context = {
        'novel_list': novel_list,
    }
    return HttpResponse(template.render(context, request))


def novel(request, novel_name):
    manga_title = request.GET['manga_title']
    chapter_list = Chapter.objects.filter(manga__title=manga_title)
    template = loader.get_template('polls/novel.html')
    context = {
        'chapter_list': chapter_list,
        'manga_title': manga_title
    }
    return HttpResponse(template.render(context, request))


def chapter_detail(request, chapter_title):
    title = request.GET['title']
    manga_title = request.GET['manga_title']
    chapter = Chapter.objects.filter(
        manga__title=manga_title, title=title).first()
    template = loader.get_template('polls/chapter.html')
    context = {
        'chapter': chapter,
    }
    return HttpResponse(template.render(context, request))
