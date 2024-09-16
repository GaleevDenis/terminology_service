from typing import Any
from urllib import request
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Q, Max
from .serializers import HandbookSerializer, HandbookElementSerializer
from .models import Handbook, HandbookElement, HandbookVersion
from datetime import date, datetime


class GetHandbookListAPIView(generics.ListAPIView):
    """Получение списка справочников (+ актуальных на указанную дату)"""

    def get(self, request): 
        # Проверяем было ли в GET запросе значение date
        if (get_date := request.GET.get('date', '')) != '':
            # Преобразовываем дату в формат date и если дата некорректная выводим сообщение об ошибке
            try:
                converted_date = datetime.strptime(get_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({'error': 'Введен некорректный формат даты - корректный формат: YYYY-MM_DD'}, status=400)
            # фильтруем справочники по дате начала действия версии раньше или равной указанной в converted_date в связанной модели version_model
            queryset = Handbook.objects.prefetch_related('version_model').filter(
                version_model__effective_date__lte=converted_date)
            # проверяем queryset на пустоту, если значений нет выводим сообщение что справочники не найдены
            if len(queryset) != 0:
                # находим список уникальных справочников - с неповторяющимися значениями handbook.id
                unique_handbooks = []
                for handbook in queryset:
                    if handbook.id not in [h.id for h in unique_handbooks]:
                        unique_handbooks.append(handbook)
                return Response({'refbooks': HandbookSerializer(unique_handbooks, many=True).data})
            else:
                return Response({'refbooks': ['Не найдены справочники с датой начала действия версии раннее или равной указанной']}, status=404)
        else:
            queryset = Handbook.objects.all()
            if len(queryset) != 0:
                return Response({'refbooks': HandbookSerializer(queryset, many=True).data})
            else:
                return Response({'refbooks': ['Не найдены справочники']}, status=404)
            

class GetHandbookElementAPIViev(generics.ListAPIView):
    """Получение элементов заданного справочника"""

    def get(self, request, id):
        # Проверяем было ли передано значение version
        if (get_version := request.GET.get('version', '')) != '':
            # Фильтруем элементы по значению get_version и полученому параметру id, предварительно загрузив связанные обьекты с version_id
            queryset = HandbookElement.objects.prefetch_related('version_id').filter(
                Q(version_id__version=get_version) & Q(version_id__handbook_id=id))
            if len(queryset) != 0:
                return Response({'elements': HandbookElementSerializer(queryset, many=True).data})
            else:
                return Response({'elements': ['Не найдены элементы указанной версии справочника']}, status=404)
        else:
            # Получаем элементы справочника, предварительно загрузив связанные обьекты с version_id
            queryset = HandbookElement.objects.prefetch_related('version_id')
            # Фильтруем список элементов по указаному id справочника и оставляем версии с датой создания раньше или равной текущей дате
            queryset = queryset.filter(Q(version_id__effective_date__lte=date.today()) & Q(version_id__handbook_id=id))
            # Находим самую позднюю дату создания версии в списке элементов
            max_date = queryset.aggregate(max_date=Max('version_id__effective_date'))['max_date']
            # Фильтруем список элементов по max_date и находим актуальную версию справочника
            # с самой поздней датой создания версии до текущей даты включительно
            queryset = queryset.filter(version_id__effective_date=max_date)
            if len(queryset) != 0:
                return Response({'elements': HandbookElementSerializer(queryset, many=True).data})
            else:
                return Response({'elements': ['Не найдены элементы текущей версии справочника']}, status=404)


class CheckHandbookElementAPIViev(generics.ListAPIView):
    """Проверка на то, что элемент с данным кодом и значением присутствует в указанной версии справочника"""

    def get(self, request, id):
        get_code_element = request.GET.get('code', '')
        get_value_element = request.GET.get('value', '')
        # Фильтруем список элементов справочника, предварительно загрузив связанные обьекты с version_id
        # по значениям равным get_code_element & get_value_element & id
        queryset = HandbookElement.objects.prefetch_related('version_id').filter(
            Q(code=get_code_element) & Q(value=get_value_element) & Q(version_id__handbook_id=id))
        if (get_version := request.GET.get('version', '')) != '':
            # Если было передано значение version
            queryset = queryset.filter(version_id__version=get_version)
        else:
            queryset = queryset.filter(version_id__effective_date__lte=date.today())
            max_date = queryset.aggregate(max_date=Max('version_id__effective_date'))['max_date']
            queryset = queryset.filter(version_id__effective_date=max_date)
        if len(queryset) !=0:
            return Response({'validation': HandbookElementSerializer(queryset, many=True).data})
        else:
            return Response({'validation': ['Не найден элемент']}, status=404)
