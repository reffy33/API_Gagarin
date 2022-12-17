import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from urllib.request import urlopen
import xml.etree.ElementTree as ET


def format_csv_date(str):
    """
    Создаёт объект типа datetime, из строки формата %Y-%m-%dT%H:%M:%S%z
    :param str: (str) входная строка с датой
    :return: (datetime) отформатированная дата
    """
    str = str[:10]
    year, month, day = map(int, str.split('-'))
    return datetime(year, month, day)


def get_xml_date(str):
    """
    Создаёт объект типа datetime, из строки формата %d.%m.%Y
    :param str: (str) входная строка с датой
    :return: (datetime) отформатированная дата
    """
    day, month, year = map(int, str.split('.'))
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
    start_date = format_csv_date(df['published_at'].min())
    end_date = format_csv_date(df['published_at'].max())

    return currensies, start_date, end_date


def get_currency_history(start_date, end_date, currency_code):
    """
    Создаёт словарь с выгрузкой истории курса валюты с помощью API Центробанка
    :param start_date: (datetime) дата начала выгрузки
    :param end_date: (datetime) дата конца выгрузки
    :param currency_code: (str) ISO код валюты
    :return: (dict) словарь формата {(str)'год-месяц' : (float)курс валюты в этом месяце}
    """
    url = f'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date.__format__("%d/%m/%Y")}&date_req2={end_date.__format__("%d/%m/%Y")}&VAL_NM_RQ={currency_code}&d=1'
    var_url = urlopen(url)
    tree = ET.parse(var_url)
    root = tree.getroot()

    current_date = start_date.replace(day=1)
    nominal = float(root[0][0].text)
    digits = len(root[0][1].text)

    result = {}
    for item in root:
        xlm_date = get_xml_date(item.attrib['Date'])
        if xlm_date.month == current_date.month:
            value = float(item[1].text.replace(',', '.'))

            result[xlm_date.__format__('%Y-%m')] = round(value / nominal, digits)
            current_date = current_date + relativedelta(months=1)

    return result



def main():
    currensies_codes = {'USD': 'R01235', 'EUR': 'R01239', 'KZT': 'R01335', 'UAH': 'R01720', 'BYR': 'R01090'}
    filename = 'vacancies_dif_currencies.csv'
    currensies, start_date, end_date = get_csv_data(filename)
    print(get_currency_history(start_date, end_date, 'R01090'))



if __name__ == "__main__":
    main()