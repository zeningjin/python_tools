import time

import openpyxl
wb = openpyxl.load_workbook('tests.xlsx')
# ws = wb.worksheets[1] # index
ws = wb.get_sheet_by_name('111')  # sheet
# sheet
ws.append([1, 2, 3, 4, 5, 6])

a = [1, 2, 3]
ws.append(a)

b = [9, 7, 5, 4]
ws.cell(row=5, column=5).value = '12344'
wb.save('tests.xlsx')
