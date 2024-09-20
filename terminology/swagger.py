from drf_yasg import openapi

from .serializers import HandbookSerializer, HandbookElementSerializer


class SettingsViewSwagger:
    """Параметры отображения полей в swagger"""

    def __init__(self, name):
        self.class_name = name

    def parameters(self):
        """Отображение передаваемых параметров в swagger"""

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
            case 'get_list_handbooks':
                return [date, ]
            case 'get_elements_handbook':
                return [id, version]
            case 'check_element_handbook':
                return [id, code, value, version]

    def responses(self):
        """Обьявление ожидаемой информации от сервера при разных кодах запроса"""

        get_list_handbooks = {200: openapi.Response("Удачная операция", HandbookSerializer,
                                          examples={"application/json": {"refbooks": [
                                              {"id": 1,"code": "1","name": "Специальности медицинских работников"},
                                              {"id": 2,"code": "2","name": "Справочник болезней"},
                                              {"id": 3,"code": "3","name": "Список адресов"}]}}),
                                          400: openapi.Response("Некорректный формат даты", HandbookSerializer,
                                          examples={"application/json":
                                                    {'error': ['Введен некорректный формат даты - корректный формат: YYYY-MM_DD']}}),
                                          404: openapi.Response( "Не найдены справочники", HandbookSerializer,
                                          examples={"application/json": {'not_found': ['Не найдены справочники'],
                                                                         'not_found_2': ['Не найдены справочники с датой начала действия версии'
                                                                                         ' раннее или равной указанной']}})}
        get_elements_handbook = {200: openapi.Response("Удачная операция", HandbookElementSerializer,
                                          examples={"application/json": {"elements": [{"code": "1", "value": "Вирусная инфекция"},
                                                                                      {"code": "2", "value": "Лихорадка"}]}}),
                                          404: openapi.Response("Не найдены элементы", HandbookElementSerializer,
                                          examples={"application/json": {'not_found': ['Не найдены элементы в указанной версии справочника'],
                                                                         'not_found_2': ['Не найдены элементы в текущей версии справочника']}})
                                          }
        check_element_handbook = {200: openapi.Response("Удачная операция", HandbookElementSerializer,
                                          examples={"application/json": {"validation": [{"code": "3", "value": "Хирург"}]}}),
                                          404: openapi.Response( "Не найден элемент", HandbookElementSerializer,
                                          examples={"application/json": {"not_found": ["Не найден элемент"],
                                                                         'not_found_2': ['Не найден элемент в текущей версии справочника']}})
                                          }
        match self.class_name:
            case 'get_list_handbooks':
                return get_list_handbooks
            case 'get_elements_handbook':
                return get_elements_handbook
            case 'check_element_handbook':
                return check_element_handbook

    def operation_description(self):
        """Описание работы сервиса"""

        get_list_handbooks = 'Дата начала действия в формате ГГГГ-ММ-ДД. Если указана дата, \
                              то вовращает справочники, в которых имеются версии с датой начала \
                              действия раннее или равной указанной.'
        get_elements_handbook = 'Получение элементов заданного справочника, если не указана версия, \
                                 то возвращает элементы текущей версии. Текущей является \
                                 та версия, дата начала действия которой позже всех остальных \
                                 версий данного справочника, но не позже текущей даты.'
        check_element_handbook = 'Проверка, что элемент с данным кодом и значением присутствует \
                                  в указанной версии справочника если не указана версия, то должны \
                                  проверяться элементы в текущей версии. Текущей является та версия,\
                                  дата начала действия которой позже всех остальных версий данного \
                                  справочника, но не позже текущей даты.'
        match self.class_name:
            case 'get_list_handbooks':
                return get_list_handbooks
            case 'get_elements_handbook':
                return get_elements_handbook
            case 'check_element_handbook':
                return check_element_handbook

    def tags(self):
        """Теги отображения в swagger"""

        match self.class_name:
            case 'get_list_handbooks':
                return ['Получение списка справочников']
            case 'get_elements_handbook':
                return ['Получение элементов справочника']
            case 'check_element_handbook':
                return ['Проверка на наличие элемента в справочнике']
