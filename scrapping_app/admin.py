from django.contrib import admin
from .models import *


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_editable = ['slug']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_editable = ['slug']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'city']
    list_editable = ['city']
    ordering = ['title']

