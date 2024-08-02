import pandas as pd
import json
from src.utils import read_txt_to_list, get_invalid_users, get_xlsx_sheet_name, get_dir_path, get_dir_path_test
from src.date_details import get_date_from_input, get_next_day


# Перед сборкой в exe
# Change dir_path = get_dir_path_test()  ->  dir_path = get_dir_path()
date_in = get_date_from_input()
dir_path = get_dir_path()


def get_users_schedule() -> dict:
    """
    :return:{
        user(str): {
            day(int): status(str),
            ...,
        }
        ...,
    }

    """
    group_file_txt = f'{dir_path}\\group_list.txt'
    valid_users_file_txt = f'{dir_path}\\valid_users.txt'
    schedule_file_xlsx = f'{dir_path}\\schedule.xlsx'
    print(f'group list: {group_file_txt}\nvalid users: {valid_users_file_txt}\nschedule: {schedule_file_xlsx}')

    group_list = read_txt_to_list(group_file_txt)
    valid_users_list = read_txt_to_list(valid_users_file_txt)

    if get_invalid_users(group_list, valid_users_list):
        return {'Invalid data': {'Файл group_list.txt': get_invalid_users(group_list, valid_users_list)}}
    if not get_xlsx_sheet_name(date_in.month_ru, schedule_file_xlsx):
        return {'Invalid data': {'Лист не найден': date_in.month_ru}}

    # Парсит excel файл в словарь
    df_schedule = pd.read_excel(
        schedule_file_xlsx,
        sheet_name=date_in.month_ru,
        engine='openpyxl'
    )
    df_schedule = df_schedule[df_schedule['Сотрудник'].isin(group_list)]
    column_needed = ['Сотрудник'] + [day for day in range(date_in.day, date_in.days_in_month + 1)]
    final_df_schedule = df_schedule[column_needed]
    if final_df_schedule.isnull().values.any():
        return {'Invalid data': {'Пустые ячейки в DataFrame проверьте .xlsx': schedule_file_xlsx}}

    schedule_users_dict = {}
    for index, row in final_df_schedule.iterrows():
        user = row.iloc[0]
        day_status_list = row.iloc[1:].tolist()
        schedule = {}
        start_date = date_in.day
        for day in day_status_list:
            schedule[start_date] = day
            start_date += 1
        schedule_users_dict[user] = schedule
    for user in group_list:
        if user not in schedule_users_dict:
            return {'Invalid data': {'В xlsx не найден': user}}
    return schedule_users_dict


def get_non_working_period(schedule_users_dict: dict) -> list:
    """
    :param schedule_users_dict:
    :return: list [
        non_working_period(str),
        ...,
    ]
    """
    non_working_period = []
    current_non_working_start = None

    for day in range(date_in.day, date_in.days_in_month + 1):
        current_day_str = f'{date_in.year}-{date_in.month:02d}-{day:02d}'
        next_year, next_month, next_day = get_next_day(
            date_in.year,
            date_in.month,
            day,
            date_in.days_in_month,
        )
        next_day_str = f'{next_year}-{next_month:02d}-{next_day:02d}'
        out_days = ['выходной', 'отпуск', 'больничный', None]
        work_type = schedule_users_dict.get(day)
        if work_type not in out_days:
            hours = work_type.split('-')
            if int(hours[0][:2]) > int(hours[1][:2]):
                if day == 1:
                    non_working_period.append(f'{current_day_str} 08:00 \u2192 {current_day_str} {hours[0]}')
                elif current_non_working_start:
                    non_working_period.append(f'{current_non_working_start} \u2192 {current_day_str} {hours[0]}')
                    current_non_working_start = None
                current_non_working_start = f'{next_day_str} {hours[1]}'
            else:
                if current_non_working_start:
                    non_working_period.append(f'{current_non_working_start} \u2192 {current_day_str} {hours[0]}')
                    current_non_working_start = None
                current_non_working_start = f'{current_day_str} {hours[1]}'
        else:
            if not current_non_working_start:
                current_non_working_start = f'{current_day_str} 08:00'
            if day == date_in.days_in_month:
                non_working_period.append(f'{current_non_working_start} \u2192 {next_day_str} 08:00')
    return non_working_period


def get_non_working_periods_dict() -> dict:
    """
    :return: dict {
        user(str) : [
            non_working_period(str),
            non_working_period(str),
            ...,
            ]
    }
    """
    excel_data = get_users_schedule()
    if 'Invalid data' in excel_data.keys():
        return excel_data
    non_working_periods_dict = {}
    for user, schedule in excel_data.items():
        non_working_periods_dict[user] = get_non_working_period(schedule)

    with open(f'{dir_path}\\non_working_periods_result.json', 'w', encoding='utf-8') as json_file:
        json.dump(non_working_periods_dict, json_file, ensure_ascii=False, indent=4)
    return non_working_periods_dict


# print(get_non_working_period(get_users_schedule()))
# print(get_non_working_periods_dict())
