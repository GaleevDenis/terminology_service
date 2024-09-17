from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import HandbookSerializer, HandbookElementSerializer


class GetParamSwagger:
    """Класс инициализации параметров отображения в swagger"""

    def manual_parameters(*parameters):
        """Обьявление полей которые будут отображаться в swagger"""

        id = openapi.Parameter('id', openapi.IN_PATH, description="Идентификатор справочника",
                                  type=openapi.TYPE_STRING, required=True)
        code = openapi.Parameter('code', openapi.IN_QUERY, description="Код элемента справочника",
                                 type=openapi.TYPE_STRING, required=True)
        value = openapi.Parameter('value', openapi.IN_QUERY, description="Значение элемента справочника",
                                  type=openapi.TYPE_STRING, required=True)
        version = openapi.Parameter('version', openapi.IN_QUERY, description="Версия справочника",
                                    type=openapi.TYPE_STRING, required=False)
        date = openapi.Parameter('date', openapi.IN_QUERY, description="Дата начала действия версии",
                                    type=openapi.TYPE_STRING, format='date', required=False)
        
        all_value = []
        for i in parameters:
            if i == 'version':
                all_value.append(version)
            if i == 'code':
                all_value.append(code)
            if i == 'value':
                all_value.append(value)
            if i == 'id':
                all_value.append(id)
            if i == 'date':
                all_value.append(date)
        return all_value

    def responses_handbook_list():
        """Обьявление ожидаемой информации от сервера при разных вариантах запроса"""

        responses = {200: openapi.Response( "Удачная операция", HandbookSerializer,
                                          examples={"application/json": {"refbooks": [
                                              {"id": 1,"code": "1","name": "Специальности медицинских работников"},
                                              {"id": 2,"code": "2","name": "Справочник болезней"},
                                              {"id": 3,"code": "3","name": "Список адресов"}]}}),
                                          400: openapi.Response( "Некорректный формат даты", HandbookSerializer,
                                          examples={"application/json": {'error': ['Введен некорректный формат даты - корректный формат: YYYY-MM_DD']}},),
                                          404: openapi.Response( "Не найдены справочники", HandbookSerializer,
                                          examples={"application/json": {'not_found': ['Не найдены справочники'],
                                                                         'not_found_2': ['Не найдены справочники с датой начала действия версии' \
                                                                                         ' раннее или равной указанной']}},),}
        return responses
    
    def responses_get_element():
        responses = {200: openapi.Response( "Удачная операция", HandbookElementSerializer,
                                          examples={"application/json": { "elements": [{"code": "1", "value": "Вирусная инфекция"},
                                                                                       {"code": "2", "value": "Лихорадка"}]}}),
                                          404: openapi.Response( "Не найдены элементы", HandbookElementSerializer,
                                          examples={"application/json": {'not_found': ['Не найдены элементы указанной версии справочника'],
                                                                         'not_found_2': ['Не найдены элементы текущей версии справочника']}},)
                                          }
        return responses
    
    def responses_check_element():
        responses = {200: openapi.Response( "Удачная операция", HandbookElementSerializer,
                                          examples={"application/json": { "validation": [{"code": "3", "value": "Хирург"}]}}),
                                          404: openapi.Response( "Не найден элемент", HandbookElementSerializer,
                                          examples={"application/json": {"validation3": ["Не найден элемент"]}},)
                                          }
        return responses

    def operation_description(teg):
        """Описание работы приложения"""
        handbook_list = 'Дата начала действия в формате ГГГГ-ММ-ДД.'\
                        ' если указана дата, то вовращает справочники, в которых имеются версии'\
                        ' с датой начала действия раннее или равной указанной.' 
        get_element =   'Получение элементов заданного справочника'\
                        ' если не указана версия, то должны возвращаться элементы текущей версии.'\
                        ' текущей является та версия, дата начала действия которой позже всех остальных'\
                        ' версий данного справочника, но не позже текущей даты.'
        check_element = 'Проверка на то, что элемент с данным кодом и значением присутствует в указанной версии справочника'\
                        ' если не указана версия, то должны проверяться элементы в текущей версии.'\
                        ' текущей является та версия, дата начала действия которой позже всех остальных'\
                        ' версий данного справочника, но не позже текущей даты.'
        match teg:
            case '1':
                return handbook_list
            case '2':
                return get_element
            case '3':
                return check_element
            
