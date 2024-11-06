# excel_reader.py
import pandas as pd
import chardet

def get_encoding(path):
    with open(path, 'rb') as file:
        encoding = chardet.detect(file.read(10000))['encoding']
        return encoding if encoding else 'ISO-8859-1'

def get_dict(path, columns=None):
    df = pd.read_excel(path, usecols=columns)
    return df.to_dict(orient="records")