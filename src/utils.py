import sys
import os
from openpyxl.reader.excel import load_workbook


def get_dir_path() -> str:
    """
    Возвращает строку из которой был запущен .exe файл

    :return:
        str: Полный путь к директории, содержащей .exe файл.
    :example:
    'C:\\dir\\path'
    """

    exe_path = sys.executable
    exe_dir = os.path.dirname(exe_path)
    return exe_dir


def get_dir_path_test() -> str:
    """
    :return:
        str: Полный путь к директории, содержащей файлы .txt .xlsx для теста перед сборкой.
    """
    return 'C:\\NLR'


def read_txt_to_list(txt_file_path) -> list:
    """
    Принимает путь к .txt файлу.
    Возвращает список пользователей.
    :param:
        str: 'C:\\txt_file\\path\\group_list.txt'
    :return:
        list: Список пользователей.
    """
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        group_list = file.readlines()
        group_list = [line.strip() for line in group_list if line.strip()]
        return group_list


def get_invalid_users(group_list: list, valid_users_list: list) -> list:
    """
    :param: list сформированный из group_list.txt файла
    :return: list с невалидными пользователями.
    """
    not_valid_users = []
    for user in group_list:
        if user not in valid_users_list:
            not_valid_users.append(user)
    return not_valid_users


def get_xlsx_sheet_name(excel_sheet_name: str, schedule_filepath: str) -> bool:
    """
    :param: имя .xlsx листа и путь к .xlsx файлу.
    :return: boolean(if sheet_name)
    """
    work_book = load_workbook(schedule_filepath, read_only=True)
    if excel_sheet_name in work_book:
        return True
    return False

