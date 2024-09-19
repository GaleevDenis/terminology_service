from datetime import date

from django.contrib import admin
from django.db.models import Max

from .models import Handbook, HandbookElement, HandbookVersion


class HandbookVersionInline(admin.TabularInline):
    """Встраиваемая модель которая будет использоваться при редактировании справочника"""

    model = HandbookVersion
    extra = 0  # Показать пустое поле для добавления новой версии
    ordering = ('-version', '-effective_date') # Сортировка при редактировании в административной панели


@admin.register(Handbook)
class HandbookAdmin(admin.ModelAdmin):
    """Отображение, сортировка и фильтрация справочников в административной панели"""    

    inlines = [HandbookVersionInline] # какие модели нужно отображать при редактировании
    list_display = ('id', 'code', 'name', 'get_handbook_version', 'get_handbook_effective_date') # какие поля отображаются
    list_display_links = ('name', ) # кликабельные категории
    list_filter = ('name', 'code') # фильтрация по значениям полей
    search_fields = ('code', 'name') # поля по которым происходит поиск
    fields = ('name', 'code', 'description') # поля при редактировании записи
    ordering = ('id', ) # Сортировка в административной панели
    list_per_page = 10 # кол-во строк на одной странице

    @admin.display(description='Текущая версия')
    def get_handbook_version(self, obj):
        """Поиск самой поздней версии справочника до текущей даты включительно"""

        current_version = obj.version_model.filter(effective_date__lte=date.today()).aggregate(max_date=Max('effective_date'))['max_date']
        if current_version is not None:
            return str(obj.version_model.filter(effective_date=current_version)[0].version)
        else:
            return 'Актуальной версии нет'

    @admin.display(description='Дата начала действия версии')
    def get_handbook_effective_date(self, obj):
        """Поиск самой поздней даты начала действия версии справочника до текущей даты включительно"""

        if obj.version_model.filter(effective_date__lte=date.today()).aggregate(max_date=Max('effective_date'))['max_date'] is not None:
            return str(obj.version_model.filter(effective_date__lte=date.today()).aggregate(max_date=Max('effective_date'))['max_date'])
        else:
            return 'Даты начала действия версии нет'


class HandbookElementInline(admin.TabularInline):
    """Встраиваемая модель которая будет использоваться при редактировании версий справочников"""

    model = HandbookElement
    extra = 0
    ordering = ('code', 'value')


@admin.register(HandbookVersion)
class HandbookVersionAdmin(admin.ModelAdmin):
    """Отображение, сортировка и фильтрация версий справочников в административной панели"""

    inlines = [HandbookElementInline]
    list_display = ('get_handbook_code', 'get_handbook_name', 'version', 'effective_date')
    list_display_links = ('get_handbook_name', )
    list_filter = ('version', 'effective_date')
    search_fields = ('get_handbook_code', 'get_handbook_name', 'version', 'effective_date')
    fields = ('handbook_id', 'version', 'effective_date')
    ordering = ('-version', '-effective_date')
    list_per_page = 10

    @admin.display(description='Код справочника')
    def get_handbook_code(self, obj):
        """Отображение кода справочника"""

        return str(obj.handbook_id.code)

    @admin.display(description='Наименование справочника')
    def get_handbook_name(self, obj):
        """Отображение наименования справочника"""

        return str(obj.handbook_id.name)

    class Meta:
        model = HandbookVersion


@admin.register(HandbookElement)
class HandbookElementAdmin(admin.ModelAdmin):
    """Отображение, сортировка и фильтрация элементов справочников в административной панели"""

    list_display = ('code', 'value','version_id', )
    list_display_links = ('value', )
    list_filter = ('version_id', 'code', 'value', )
    search_fields = ('version_id', 'code', 'value', )
    fields = ('version_id', 'code', 'value', )
    ordering = ('code', 'value', )
    list_per_page = 10

    class Meta:
        model = HandbookElement
