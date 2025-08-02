
import openpyxl

import csv

def read_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    headers = [cell.value for cell in sheet[1]]
    rows = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        rows.append(dict(zip(headers, row)))
    return rows

def read_csv(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    except UnicodeDecodeError:
        with open(file_path, newline='', encoding='latin1') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
