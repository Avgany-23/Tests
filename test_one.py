from homework_regular.main import *
import unittest
import os


def choose_plural(amount: int, declensions: tuple[str]) -> str:
    """Функция для склонения слов. Принимает число и 3 варианта его склонения,
    Например, 91 ('день', 'дня', 'дней')
    Принимает amount - количество (int), declensions - список склонений (кортеж строк)
    Возвращает строку, содержащую в себе число и правильное склонение"""

    selector = {
        amount % 10 == 1: 0,
        amount % 10 in [2, 3, 4]: 1,
        amount % 10 in [0, 5, 6, 7, 8, 9]: 2,
        amount % 100 in range(11, 21): 2
    }
    return f'{amount} {declensions[selector[True]]}'


class TestChoose_plural(unittest.TestCase):
    def test_work_function(self):
        """Проверка на правильность склонения слов"""
        declensions = ('яблоко', 'яблока', 'яблок')

        for i, (count, res) in enumerate(zip([1, 2, 5, 100, 603],
                                             [
                                                 '1 яблоко',
                                                 '2 яблока',
                                                 '5 яблок',
                                                 '100 яблок',
                                                 '603 яблока',
                                             ])):
            with self.subTest(i):
                result = choose_plural(count, declensions)
                self.assertRegex(result, r'\d{1,3} яблок[оа]?')
                self.assertEqual(result, res)

    def test_type_params(self):
        self.assertRaises(TypeError, choose_plural, '1', ('яблоко', 'яблока', 'яблок'))

    @unittest.expectedFailure
    def test_none(self):
        self.assertIsNone(choose_plural(1, ('яблоко', 'яблока', 'яблок')))


class TestRegularSearchCSV(unittest.TestCase):
    path = 'homework_regular/phonebook_raw.csv'
    reader = read_file(path)        # Получение данных из файла
    res_name = edin_name(reader)    # Получение списков имён

    def test_len_readlines(self):
        """Проверка значений из файла по пути path"""
        self.assertEqual(len(self.res_name), 10)

    def test_check_name(self):
        """Проверка значений из файла по пути path"""
        for i, list_name in enumerate(
            [
                ['Усольцев', 'Олег', 'Валентинович'],
                ['Мартиняхин', 'Виталий', 'Геннадьевич'],
                ['Наркаев', 'Вячеслав', 'Рифхатович'],
            ],
            1
        ):
            with self.subTest(i):
                self.assertListEqual(self.res_name[i], list_name)

    def test_check_count_available_numbers(self):
        """Проверка значений из файла по пути path"""
        count = 0
        for phone in edin_number_phone(self.reader):
            if phone != 'number missing':
                count += 1
        self.assertEqual(count, 7)

    def test_check_format_phone(self):
        """Проверяет, правильно ли функция достает номер телефона"""

        for i, (result, phone) in enumerate(
            [
                ('+7(495)913-04-78', 'FF+7(495)913-04-78AAA'),
                ('number missing', '9999-9999-9999-999'),
                ('+7(111)111-11-11', 'Звони по +8(111)111-11-11 ввв'),
                ('number missing', '+5(111)111-11-11 phone'),
            ]
        ):
            with self.subTest(i):
                self.assertListEqual(edin_number_phone([phone]), [result])

    @unittest.skipUnless(os.path.exists('homework_regular/phones_result.csv'), 'Файл не нашелся')
    def test_check_write_correct_file(self):
        """Проверка на то, правильно ли произошла запись в файл. В конце файл удаляется"""
        path_res = 'phones_result_test.csv'                                                 # Файл для записи результата
        res_number = edin_number_phone(self.reader)                                         # Получение готовых номеров
        res_email = search_email(self.reader)                                               # Получением email адресов
        write_file(path_res, self.res_name[1:], res_number[1:], res_email[1:], mode='w')    # Запись в новый файл

        with open('homework_regular/phones_result.csv', encoding='utf-8') as f:
            reader1 = f.readlines()  # Получение данных с файла, где данные записанные правильно

        with open(path_res, encoding='utf-8') as f:
            reader2 = f.readlines()  # Получение только что записанных данных

        for i, (line1, line2) in enumerate(zip(reader1, reader2)):
            with self.subTest(i):
                self.assertEqual(line1, line2)

        os.remove(path_res)

