from django.db import models


class Handbook(models.Model):
    """Модель справочника"""
    code = models.CharField(max_length=100, unique=True, verbose_name='Код')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        db_table = 'handbook'
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return f'{self.name}'


class HandbookVersion(models.Model):
    """Модель версии справочника"""
    handbook = models.ForeignKey(to=Handbook, on_delete=models.CASCADE, related_name='versions', 
                                verbose_name='Справочник')
    version = models.CharField(max_length=50, verbose_name='Версия')
    effective_date = models.DateField(verbose_name='Дата начала действия версии справочника')

    class Meta:
        db_table = 'handbookversion'
        unique_together = ('handbook', 'version'), ('handbook', 'effective_date')
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочника'

    def __str__(self):
        return f"{self.handbook.name} - {self.version}"


class HandbookElement(models.Model):
    """Модель Элементов справочников"""
    version = models.ForeignKey(to=HandbookVersion, on_delete=models.CASCADE, related_name='elements',
                                verbose_name='Справочник-версия')
    element_code = models.CharField(max_length=100, verbose_name='Код элемента')
    value = models.CharField(max_length=300, verbose_name='Значение элемента')

    class Meta:
        db_table = 'handbookelement'
        unique_together = ('version', 'element_code')
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'

    def __str__(self):
        return f'{self.value}'
