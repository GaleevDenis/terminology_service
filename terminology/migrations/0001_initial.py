# Generated by Django 4.2.15 on 2024-09-19 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Handbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
                'db_table': 'handbook',
            },
        ),
        migrations.CreateModel(
            name='HandbookVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50, verbose_name='Версия')),
                ('effective_date', models.DateField(verbose_name='Дата начала версии')),
                ('handbook_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='version_model', to='terminology.handbook', verbose_name='Справочник')),
            ],
            options={
                'verbose_name': 'Версия справочника',
                'verbose_name_plural': 'Версии справочника',
                'db_table': 'handbookversion',
                'unique_together': {('handbook_id', 'version'), ('handbook_id', 'effective_date')},
            },
        ),
        migrations.CreateModel(
            name='HandbookElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, verbose_name='Код элемента')),
                ('value', models.CharField(max_length=300, verbose_name='Значение элемента')),
                ('version_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_model', to='terminology.handbookversion', verbose_name='Справочник-версия')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочников',
                'db_table': 'handbookelement',
                'unique_together': {('version_id', 'code')},
            },
        ),
    ]
