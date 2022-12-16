import pandas as pd
from datetime import datetime


def format_date(str):
    """
    Создаёт объект типа datetime, содержащий год, месяц и день из строки
    :param str: (str) входная строка с датой
    :return: (datetime) отформатированная дата
    """
    str = str[:10]
    year, month, day = map(int, str.split('-'))
    return datetime(year, month, day)


def get_csv_data(filename):
    """
    Получает данные из csv файла с помощью pandas
    :param filename: (str) имя файла или ссылка на него
    :return: currensies (list): список валют указанных в более чем 5000 вакансиях
                start_date(datetime): дата самой ранней вакансии в выгрузке
                end_date(datetime): дата самой свежей вакансии в выгрузке
    """
    df = pd.read_csv(filename)
    print("File read succesfully")
    salary_count = df['salary_currency'].value_counts()
    currensies = salary_count[salary_count > 5000].index.to_list()
    start_date = format_date(df['published_at'].min())
    end_date = format_date(df['published_at'].max())

    return currensies, start_date, end_date


def main():
    filename = 'vacancies_dif_currencies.csv'
    currensies, start_date, end_date = get_csv_data(filename)
    print(currensies)
    print(start_date, end_date)


if __name__ == "__main__":
    main()