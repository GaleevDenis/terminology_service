from datetime import datetime

from django.test import TestCase

from terminology.models import Handbook, HandbookElement, HandbookVersion

# Create your tests here.

class TestTerminology(TestCase):

    def setUp(self):
        """"Создание обьектов в БД"""
        self.handbook_1 = Handbook.objects.create(
            code="ms1", name="Справочник-болезней", description='Простудные')
        self.handbook_2 = Handbook.objects.create(
            code="ms2", name="Справочник-насекомых", description='Летающие')
        self.handbook_version_1 = HandbookVersion.objects.create(
            handbook_id=self.handbook_1, version=1.0, effective_date=(
                datetime.strptime("2020-12-18", "%Y-%m-%d").date()))
        self.handbook_version_2 = HandbookVersion.objects.create(
            handbook_id=self.handbook_2, version=1.1, effective_date=(
                datetime.strptime("2023-12-18", "%Y-%m-%d").date()))
        self.handbook_element_1 = HandbookElement.objects.create(
            version_id=self.handbook_version_1, code="1", value='ОРВИ')
        self.handbook_element_2 = HandbookElement.objects.create(
            version_id=self.handbook_version_1, code="2", value='ОРЗ')
        self.handbook_element_3 = HandbookElement.objects.create(
            version_id=self.handbook_version_2, code="ms1", value='Пчела')

    def test_get_handbooks_views_objects(self):
        """Тест отображения списка справочников"""
        response = self.client.get('/refbooks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len((response.data)['refbooks']), 2)
        self.assertEqual((response.data)['refbooks'][0],
                         {'id': 1, 'code': 'ms1', 'name': 'Справочник-болезней'})
        self.assertEqual((response.data)['refbooks'][1],
                         {'id': 2, 'code': 'ms2', 'name': 'Справочник-насекомых'})

    def test_get_handbooks_error_date(self):
        """Тест ошибки некорректный формат даты"""
        response = self.client.get('/refbooks/?date=1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual((response.data)['error'][0],
                         "Введен некорректный формат даты - корректный формат: YYYY-MM_DD")

    def test_get_handbooks_not_found_2_objects(self):
        """Тест не найдены справочники с указанной датой"""
        response = self.client.get('/refbooks/?date=2019-12-18')
        self.assertEqual(response.status_code, 404)
        self.assertEqual((response.data)['not_found_2'][0],
                         "Не найдены справочники с датой начала действия версии раннее или равной указанной")

    def test_get_elements_id_objects(self):
        """Тест получение элементов указанного по id справочника в текущей версии"""
        response = self.client.get('/refbooks/2/elements/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len((response.data)['elements']), 1)
        self.assertEqual((response.data)['elements'][0],
                         {'code': 'ms1', 'value': 'Пчела'})

    def test_get_elements_id_version_objects(self):
        """Тест получение элементов указанного по id справочника и версии"""
        response = self.client.get('/refbooks/1/elements/?version=1.0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len((response.data)['elements']), 2)
        self.assertEqual((response.data)['elements'][0],
                         {'code': '1', 'value': 'ОРВИ'})

    def test_get_elements_not_found_objects(self):
        """Тест элементы не найдены по id справочника и версии"""
        response = self.client.get('/refbooks/1/elements/?version=1.1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len((response.data)['not_found']), 1)
        self.assertEqual((response.data)['not_found'][0],
                         "Не найдены элементы в указанной версии справочника")

    def test_check_element_objects(self):
        """Проверка на наличие элемента в текущей версии справочника"""
        response = self.client.get('/refbooks/1/check_element/?code=2&value=ОРЗ')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len((response.data)['validation']), 1)
        self.assertEqual((response.data)['validation'][0],
                         {'code': '2', 'value': 'ОРЗ'})

    def test_check_element_version_objects(self):
        """Проверка на наличие элемента в указанной версии справочника"""
        response = self.client.get('/refbooks/2/check_element/?code=ms1&value=Пчела&version=1.1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len((response.data)['validation']), 1)
        self.assertEqual((response.data)['validation'][0],
                         {'code': 'ms1', 'value': 'Пчела'})

    def test_check_element_not_found_objects(self):
        """Не найден элемент справочника """
        response = self.client.get('/refbooks/1/check_element/?code=ms1&value=Пчела&version=1.0')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len((response.data)['not_found']), 1)
        self.assertEqual((response.data)['not_found'][0],
                         "Не найден элемент")

    def test_check_element_not_found_2_objects(self):
        """Не найден элемент в текущей версии справочника"""
        response = self.client.get('/refbooks/1/check_element/?code=ms1&value=Пчела')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len((response.data)['not_found_2']), 1)
        self.assertEqual((response.data)['not_found_2'][0],
                         "Не найден элемент в текущей версии справочника")
