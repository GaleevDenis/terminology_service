from typing import Any
from urllib import request
from django.shortcuts import render
from rest_framework import generics
from .serializers import HandbookVersionSerializer, HandbookSerializer
from .models import Handbook, HandbookElement, HandbookVersion
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from datetime import date, datetime
from django.db.models import Q
# Create your views here.
#class TerminologyAPIView(generics.ListAPIView): # через сериализер
#    queryset = HandbookVersion.objects.select_related('handbook').all()
#    serializer_class = HandbookSerializer


class HandbookListAPIView(generics.ListAPIView):

    def get(self, request): 
        # Проверяем было ли в GET запросе значение date
        if (get_date := request.GET.get('date', '')) != '':
            # Преобразовываем дату в формат date и если дата некорректная выводим сообщение об ошибке
            try:
                converted_date = datetime.strptime(get_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({'error': 'Введен некорректный формат даты - корректный формат: YYYY-MM_DD'})
            # фильтруем справочники по дате начала действия версии раньше или равной указанной в converted_date в связанной модели versions
            queryset = Handbook.objects.prefetch_related('versions').filter(versions__effective_date__lte=converted_date)
            # проверяем queryset имеет ли значения, если значений нет выводим сообщение что справочники не найдены
            if len(queryset) != 0:
                # находим список уникальных справочников - с неповторяющимися значениями handbook.id
                unique_handbooks = []
                for handbook in queryset:
                    if handbook.id not in [h.id for h in unique_handbooks]:
                        unique_handbooks.append(handbook)
                return Response({'refbooks': HandbookSerializer(unique_handbooks, many=True).data})
            else:
                return Response({'refbooks': ['Не найдены справочники с датой начала действия версии раннее или равной указанной']})
        else:
            queryset = Handbook.objects.all()
            if len(queryset) != 0:
                return Response({'refbooks': HandbookSerializer(queryset, many=True).data})
            else:
                return Response({'refbooks': ['Не найдены справочники']})
            

class HandbookElementAPIViev(generics.ListAPIView):

    def get(self, request, id):
        if (version := request.GET.get('version', '')) != '':
            return Response({'refbooks': [str(id), version]})
        else:
            return Response({'refbooks': [str(id), version]})


    #Response({year, month, day})

           
#        return render(request {'year': number})

#    def get(self, request):
#        queryset = HandbookVersion.objects.select_related('handbook').all()
#    serializer_class = HandbookSerializer
#        return Response({'elements': HandbookSerializer(queryset, many=True).data})

