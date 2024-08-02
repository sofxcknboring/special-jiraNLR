import datetime
import calendar

months_russian_name = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}


class DateDetails:
    """
    Attr:
        date(datetime.datetime): datetime object
        year(int): Целочисленное значение года.
        month(int): Целочисленное значение месяца.
        day(int): Целочисленное значение дня.
        days_in_month(int): Количество дней в текущем месяце.
        month_ru(str): Название текущего месяца на русском языке.
        str_date(str): >>> '2024-01-01'
    """
    def __init__(self, year, month, day):
        self.date = datetime.datetime(year=year, month=month, day=day)
        self.year = year
        self.month = month
        self.day = day
        self.days_in_month = calendar.monthrange(year, month)[1]
        self.month_ru = months_russian_name[month]

    @property
    def str_date(self) -> str:
        return self.date.strftime('%Y-%m-%d')


def get_next_day(year, month, day, days_in_month):
    """
    Получить следующий день.
    """
    if day == days_in_month:
        next_day = 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
    else:
        next_day = day + 1
        next_month = month
        next_year = year
    return next_year, next_month, next_day


def get_date_from_input():
    """
    Запрос даты у пользователя.
    :return:
        Экземпляр DateDetails
    """
    print('Введите дату с которой необходимо начать.')
    year = int(input('Введите год(2024):'))
    month = int(input('Введите месяц(1-12):'))
    day = int(input('Введите день(1-31):'))
    return DateDetails(year, month, day)
