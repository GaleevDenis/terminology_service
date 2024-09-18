from datetime import date, datetime

from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q, Max
from drf_yasg.utils import swagger_auto_schema

from .serializers import HandbookSerializer, HandbookElementSerializer
from .models import Handbook, HandbookElement
# Импорт настроек для каждого представления декоратора @swagger_auto_schema
from .swagger import SettingsViewSwagger


# Создание обьектов для персонализированных настроек декоратора @swaggerautoscheme
get_list_handbooks_swagger_views = SettingsViewSwagger('get_list_handbooks')
get_elements_handbook_swagger_views = SettingsViewSwagger('get_elements_handbook')
check_element_handbook_swaagger_views =SettingsViewSwagger('check_element_handbook')


class GetListHandbooksAPIView(generics.ListAPIView):
    """Получение списка справочников (+ актуальных на указанную дату)"""

    # Для отображение полей и описания работы API в swagger
    @swagger_auto_schema(manual_parameters=get_list_handbooks_swagger_views.parameters(),
                         responses=get_list_handbooks_swagger_views.responses(),
                         tags=get_list_handbooks_swagger_views.tags(),
                         operation_description=get_list_handbooks_swagger_views.operation_description())
    def get(self, request):
        # Проверяем было ли в GET запросе значение date
        if (get_date := request.GET.get('date', '')) != '':
            # Преобразовываем дату в формат date, если дата некорректная выводим сообщение об ошибке
            try:
                converted_date = datetime.strptime(get_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({'error':
                                 ['Введен некорректный формат даты - корректный формат: YYYY-MM_DD']},
                                 status=400)

            # фильтруем справочники по дате начала действия версии раньше или равной указанной
            # в converted_date по значениям атрибутов связанной модели version_model
            filtered_handbooks = Handbook.objects.prefetch_related('version_model').filter(
                version_model__effective_date__lte=converted_date)
            # проверяем filtered_handboks на пустоту, если значений нет выводим сообщение что справочники не найдены
            if len(filtered_handbooks) != 0:
                # находим список уникальных справочников - с неповторяющимися значениями handbook.id
                unique_handbooks = []
                for handbook in filtered_handbooks:
                    if handbook.id not in [h.id for h in unique_handbooks]:
                        unique_handbooks.append(handbook)
                return Response({'refbooks': HandbookSerializer(unique_handbooks, many=True).data})
            else:
                return Response({'not_found_2':
                                 ['Не найдены справочники с датой начала действия версии раннее или равной указанной']},
                                 status=404)

        else:
            # Получаем список всех справочников
            list_all_handboks = Handbook.objects.all()
            # Проверяем список всех справочников на пустоту
            if len(list_all_handboks) != 0:
                return Response({'refbooks': HandbookSerializer(list_all_handboks, many=True).data})
            else:
                return Response({'not_found': ['Не найдены справочники']}, status=404)


class GetElementsHandbookAPIView(generics.ListAPIView):
    """Получение элементов заданного справочника"""

    @swagger_auto_schema(manual_parameters=get_elements_handbook_swagger_views.parameters(),
                         responses=get_elements_handbook_swagger_views.responses(),
                         tags=get_elements_handbook_swagger_views.tags(),
                         operation_description=get_elements_handbook_swagger_views.operation_description())
    def get(self, request, id):
        # Проверяем было ли передано значение version
        if (get_version := request.GET.get('version', '')) != '':
            # Фильтруем элементы справочника по значению get_version и полученому параметру id,
            # по атрибутам полученым из связаной модели HandbookVersion
            filtered_elements_handbook = HandbookElement.objects.prefetch_related('version_id').filter(
                Q(version_id__version=get_version) & Q(version_id__handbook_id=id))
            if len(filtered_elements_handbook) != 0:
                return Response({'elements': HandbookElementSerializer(filtered_elements_handbook, many=True).data})
            else:
                return Response({'not_found': ['Не найдены элементы указанной версии справочника']}, status=404)

        else:
            # Получаем элементы справочника, с атрибутами из связанной модели с HandbookVersion
            get_elements_handbook = HandbookElement.objects.prefetch_related('version_id')
            # Фильтруем список элементов справочника по атрибуту handbook_id из связанной модели HandbookVersion
            # равному id справочника и оставляем версии с датой создания раньше или равной текущей дате
            filtered_elements_handbook = get_elements_handbook.filter(
                Q(version_id__effective_date__lte=date.today())
                & Q(version_id__handbook_id=id))
            # Находим самую позднюю дату создания версии в списке элементов
            max_date_value = filtered_elements_handbook.aggregate(max_date=Max('version_id__effective_date'))['max_date']
            # Фильтруем список элементов справочника по max_date и находим актуальную версию справочника
            # с самой поздней датой создания версии до текущей даты включительно
            filtered_with_date_elements_handbook = \
                filtered_elements_handbook.filter(version_id__effective_date=max_date_value)

            # Проверяем список элементов на пустоту
            if len(filtered_with_date_elements_handbook) != 0:
                return Response({'elements': HandbookElementSerializer(filtered_with_date_elements_handbook,
                                                                       many=True).data})
            else:
                return Response({'not_found_2': ['Не найдены элементы текущей версии справочника']}, status=404)


class CheckElementHandbookAPIView(generics.ListAPIView):
    """Проверка на то, что элемент с данным кодом и значением присутствует в указанной версии справочника"""

    @swagger_auto_schema(manual_parameters=check_element_handbook_swaagger_views.parameters(),
                         responses=check_element_handbook_swaagger_views.responses(),
                         tags=check_element_handbook_swaagger_views.tags(),
                         operation_description=check_element_handbook_swaagger_views.operation_description())
    def get(self, request, id):
        # Проверяем были ли переданы значения 'code' и 'value' в параметрах GET запроса
        get_code_element = request.GET.get('code', '')
        get_value_element = request.GET.get('value', '')

        # Фильтруем список элементов справочника, по атрибутам из связанной модели HandbookVersion
        # равным значениям get_code_element & get_value_element & id
        filtered_elements_handbook = HandbookElement.objects.prefetch_related(
            'version_id').filter(Q(code=get_code_element) & Q(value=get_value_element) & Q(version_id__handbook_id=id))
        # Проверяем было ли передано значение 'version' в параметрах GET запроса
        if (get_version := request.GET.get('version', '')) != '':
            # По атрибутам из связанной модели HandbookVersion ищем значения версии равные переданому
            # параметру 'version' в отфильтрованом списке
            filtered_again_elements_handbook = \
                filtered_elements_handbook.filter(version_id__version=get_version)
        # Иначе ищем все значения в текущей версии справочника - дата начала действия которой
        # позже всех остальных версий данного справочника, но не позже текущей даты.
        else:
            # Находим все значения созданные раньше или равные текущей дате
            filtered_with_today_elements_handbook = \
                filtered_elements_handbook.filter(version_id__effective_date__lte=date.today())
            # Получаем самую позднюю дату по атрибуту "effective_date" из связаной модели HandbookVersion
            max_date_value = filtered_with_today_elements_handbook.aggregate(
                max_date=Max('version_id__effective_date'))['max_date']
            # Фильтруем список элементов справочника по max_date и находим актуальную версию справочника
            # с самой поздней датой создания версии до текущей даты включительно
            filtered_again_elements_handbook = \
                filtered_with_today_elements_handbook.filter(version_id__effective_date=max_date_value)
            
        # Проверяем список элементов справочника на пустоту и возвращаем элемент справочника
        if len(filtered_again_elements_handbook) !=0:
            return Response({'validation': HandbookElementSerializer(filtered_again_elements_handbook, many=True).data})
        else:
            return Response({'not_found': ['Не найден элемент']}, status=404)
        