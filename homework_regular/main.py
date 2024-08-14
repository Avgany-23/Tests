import csv
import re

def read_file(path: str) -> list[str]:
    """Функция считывает файл. Возвращает список строк файла
    path - путь до файла, который нужно считать"""

    with open(path, encoding='utf-8') as f:
        reader = f.readlines()
    return reader


def edin_name(reader: list[str]) -> list[list]:
    """Функция для извлечения имён из списка
    Принимает список, возвращает список с другими списками имён"""
    result_name = []
    for i in reader:
        res = []
        for q in i.strip().split(',')[:3]:
            if q:
                res.extend(q.split())
        if len(res) == 2:
            res.append('None')
        result_name.append(res)
    return result_name


def edin_number_phone(data: list) -> list[list]:
    """Функция для нахождения номера телефона из строки и
    приведение номера телефона к виду +7(XXX)XXX-XX-XX
    Принимает список строк, возвращает список номеров в нужном формате"""

    res_numbers = []
    for i in data:
        pattern = r'\+?(7|8)\s?\(?(\d{3})\)?[ -]?(\d{3})(?:[-]?)(\d{2})(?:[-]?)(\d{2})'
        reg = re.search(pattern, i.strip())

        if reg:
            res_number = re.sub(pattern, r'+7(\2)\3-\4-\5', reg.group())
            extra_num = re.findall(r'доб. \d{4}', i.strip())
            if extra_num:
                res_number += ' ' + extra_num[0]
            res_numbers.append(res_number)
        else:
            res_numbers.append('number missing')

    return res_numbers


def search_email(reader: list[str]) -> list[str]:
    """Функция для поиска email адреса из строки.
    Принимает список, возвращает список с email адресами"""
    res_email = []
    for i in reader:
        email = re.findall(r'[\w\d\.]+@[\w\d]+.ru', i.strip())
        if email:
            res_email.append(email[0])
        else:
            res_email.append('email missing')
    return res_email


def write_file(path: str, names: list, phones: list, email: list, mode: str='w') -> None:
    """Функция для записи файла. Возвращает None
    path - путь к файлу для записи, str
    names - список имён, которые будут записан в файл
    phones - список номеров телефонов, которые будут записан в файл
    mode: 'w' - перезапись, 'a' - запись в конце файла. По умолчанию 'w'"""

    with open(path, mode, encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['lastname', 'firstname', 'surname', 'phone', 'email'])
        for i in zip(names, phones, email):
            writer.writerow([*i[0], i[1], i[2]])

# path = 'phonebook_raw.csv'  # Файл из условия
# reader = read_file(path)
# res_name = edin_name(reader)
# print(res_name)

# if __name__ == '__main__':
#     path = 'phonebook_raw.csv'  # Файл из условия
#     path_res = 'phones_result.csv'             # Файл для записи результата
#     reader = read_file(path)                        # Считывания файла
#
#     res_name = edin_name(reader)                    # Получение готовых имён (без регулярок)
#     res_number = edin_number_phone(reader)          # Получение готовых номеров
#     res_email = search_email(reader)                # Получением email адресов
#
#     write_file(path_res, res_name[1:], res_number[1:], res_email[1:], mode='w')    # Запись в новый файл
