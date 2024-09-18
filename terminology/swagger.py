from drf_yasg import openapi

from .serializers import HandbookSerializer, HandbookElementSerializer


class SettingsViewSwagger:
    """Параметры отображения полей в swagger"""
    
    def __init__(self, name):
        self.class_name = name

    def parameters(self):
        """Обьявление полей и их отображение в swagger"""

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
        match self.class_name:
            case 'handbook_list':
                return [date, ]
            case 'get_element':
                return [id, version]
            case 'check_element':
                return [id, code, value, version]

    def responses(self):
        """Обьявление ожидаемой информации от сервера при разных вариантах запроса"""

        handbook_list = {200: openapi.Response( "Удачная операция", HandbookSerializer,
                                          examples={"application/json": {"refbooks": [
                                              {"id": 1,"code": "1","name": "Специальности медицинских работников"},
                                              {"id": 2,"code": "2","name": "Справочник болезней"},
                                              {"id": 3,"code": "3","name": "Список адресов"}]}}),
                                          400: openapi.Response( "Некорректный формат даты", HandbookSerializer,
                                          examples={"application/json":
                                                    {'error': ['Введен некорректный формат даты - корректный формат: YYYY-MM_DD']}},),
                                          404: openapi.Response( "Не найдены справочники", HandbookSerializer,
                                          examples={"application/json": {'not_found': ['Не найдены справочники'],
                                                                         'not_found_2': ['Не найдены справочники с датой начала действия версии' \
                                                                                         ' раннее или равной указанной']}},),}
        get_element = {200: openapi.Response( "Удачная операция", HandbookElementSerializer,
                                          examples={"application/json": {"elements": [{"code": "1", "value": "Вирусная инфекция"},
                                                                                      {"code": "2", "value": "Лихорадка"}]}}),
                                          404: openapi.Response( "Не найдены элементы", HandbookElementSerializer,
                                          examples={"application/json": {'not_found': ['Не найдены элементы указанной версии справочника'],
                                                                         'not_found_2': ['Не найдены элементы текущей версии справочника']}},)
                                          }
        check_element = {200: openapi.Response( "Удачная операция", HandbookElementSerializer,
                                          examples={"application/json": {"validation": [{"code": "3", "value": "Хирург"}]}}),
                                          404: openapi.Response( "Не найден элемент", HandbookElementSerializer,
                                          examples={"application/json": {"not_found": ["Не найден элемент"]}},)
                                          }
        match self.class_name:
            case 'handbook_list':
                return handbook_list
            case 'get_element':
                return get_element
            case 'check_element':
                return check_element

    def operation_description(self):
        """Описание работы сервиса"""

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
        match self.class_name:
            case 'handbook_list':
                return handbook_list
            case 'get_element':
                return get_element
            case 'check_element':
                return check_element
            
    def tags(self):
        """Теги отображение в swagger"""

        match self.class_name:
            case 'handbook_list':
                return ['Получение списка справочников']
            case 'get_element':
                return ['Получение элементов справочника']
            case 'check_element':
                return ['Проверка на наличие элемента']

# Создание обьектов для персонализированных настроек декоратора @swaggerautoscheme
handbook_list = SettingsViewSwagger('handbook_list')
get_element= SettingsViewSwagger('get_element')
check_element =SettingsViewSwagger('check_element')
