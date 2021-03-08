from django import forms
from django.contrib import admin
from .models import Manga, Author, Category, Chapter
from django_ace import AceWidget


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'
        widgets = {
            'content': AceWidget(
                mode='html', theme='twilight', wordwrap=True,
                width='100%', height='300px'
            )
        }

# Register your models here.


class MangaAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    search_fields = ('title',)
    list_filter = ('status', )
    readonly_fields = ('last_update',)

    class Meta:
        model = Manga


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        model = Author


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ('name',)

    class Meta:
        model = Category


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    raw_id_fields = ('manga',)
    search_fields = ('title',)
    form = ChapterForm

    class Meta:
        model = Chapter


admin.site.register(Manga, MangaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Chapter, ChapterAdmin)
