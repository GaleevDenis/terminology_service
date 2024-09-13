from django.db import models

# Create your models here.

class Handbook(models.Model):
    """"Класс представляющий Cправочник"""

    code = models.CharField(max_length=100, unique=True, verbose_name='Код')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return f'{self.name}'

class HandbookVersion(models.Model):
    """"Класс представлящий Версии справочника"""

    handbook = models.ForeignKey(to=Handbook, on_delete=models.CASCADE, related_name='versions', verbose_name='Справочник')
    version = models.CharField(max_length=50, verbose_name='Версия')
    effective_date = models.DateField(verbose_name='Дата начала действия версии')

    class Meta:
        unique_together = ('handbook', 'version')
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочника'

    def __str__(self):
        return f"{self.handbook.name} - {self.version}"

class HandbookElement(models.Model):
    """"Класс представлящий Элементы справочника"""

    version = models.ForeignKey(to=HandbookVersion, on_delete=models.CASCADE, related_name='elements', verbose_name='Идентификатор Версии справочника')
    element_code = models.CharField(max_length=100, verbose_name='Код элемента')
    value = models.CharField(max_length=300, verbose_name='Значение элемента')

    class Meta:
        unique_together = ('version', 'element_code')
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'

    def __str__(self):
        return f'{self.value}'
