from django.contrib import admin
from django.db.models import Max
from django.db.models.functions import Cast
from django.db.models import FloatField

from .models import Handbook, HandbookElement, HandbookVersion
# Register your models here.

class HandbookVersionInline(admin.TabularInline):
    model = HandbookVersion
    extra = 0  # Показать пустое поле для добавления новой версии
    ordering = ('-version', '-effective_date') # Сортировка при редактировании в административной панели

@admin.register(Handbook)
class HandbookAdmin(admin.ModelAdmin):
    inlines = [HandbookVersionInline] # какие модели нужно отображать при редактировании
    list_display = ('id', 'code', 'name', 'get_handbook_version') # какие поля отображаются
    list_display_links = ('name', ) # кликабельные категории
    list_filter = ('name', 'code') # фильтрация по значениям полей
    search_fields = ('code', 'name') # поля по которым происходит поиск
    fields = ('name', 'code', 'description') # поля при редактировании записи
    ordering = ('code', ) # Сортировка в административной панели
    list_per_page = 10 # кол-во строк на одной странице

    @admin.display(description='Версия')
    def get_handbook_version(self, obj):
        if obj.versions.all().aggregate(max_value=Max(Cast('version', output_field=FloatField())))['max_value'] is not None:
            return str(obj.versions.all().aggregate(max_value=Max(Cast('version', output_field=FloatField())))['max_value'])
        else:
            return 'Актуальной версии не существует'
        
        # сделать поиск по элементам с датой самой свежей до текущей это будет текущая дата, потом по этой дате найти версию саму актуальную


class HandbookElementInline(admin.TabularInline):
    model = HandbookElement
    extra = 0  # Показать пустое поле для добавления новой версии
    ordering = ('element_code', 'value')

@admin.register(HandbookVersion)
class HandbookVersionAdmin(admin.ModelAdmin):
    inlines = [HandbookElementInline] # какие модели нужно отображать при редактировании
    list_display = ('get_handbook_code', 'get_handbook_name', 'version', 'effective_date') # какие поля отображаются
    list_display_links = ('get_handbook_name', ) # кликабельные категории
    list_filter = ('version', 'effective_date') # фильтрация по значениям полей
    search_fields = ('get_handbook_code', 'get_handbook_name', 'version', 'effective_date') # поля по которым происходит поиск
    fields = ('handbook', 'version', 'effective_date') # поля при редактировании записи
    ordering = ('-version', '-effective_date') # Сортировка в административной панели
    list_per_page = 10 # кол-во строк на одной странице

    @admin.display(description='Код')
    def get_handbook_code(self, obj):
        return str(obj.handbook.code)
    
    @admin.display(description='Наименование')
    def get_handbook_name(self, obj):
        return str(obj.handbook.name)


    class Meta:
        model = HandbookVersion
    

@admin.register(HandbookElement)
class HandbookElementAdmin(admin.ModelAdmin):
    list_display = ('element_code', 'value','version') # какие поля отображаются
    list_display_links = ('value', ) # кликабельные категории
    list_filter = ('version', 'element_code', 'value') # фильтрация по значениям полей
    search_fields = ('version', 'element_code', 'value') # поля по которым происходит поиск
    fields = ('version', 'element_code', 'value') # поля при редактировании записи
    ordering = ('element_code', 'value') # Сортировка в административной панели
    list_per_page = 10 # кол-во строк на одной странице

    class Meta:
        model = HandbookElement