import numpy as np
import pandas as pd
from openpyxl.utils import get_column_letter


def format_df(df, name='temp.xlsx', sheet_name='Hoja'):
    
    df = df.T.reset_index().T.reset_index(drop=True)
    df = df.fillna('-')

    writer = pd.ExcelWriter(name, engine='xlsxwriter', date_format='dd-mm-yyyy', datetime_format='dd-mm-yyyy')

    df.to_excel(writer, sheet_name=sheet_name, index=True, header=False)
    workbook = writer.book
    
    cuadricula = workbook.add_format({'border': 1, 'font_name': 'Arial Narrow'})
    titulos = workbook.add_format({'bold': 'True', 'text_wrap': 'True', 'font_name': 'Arial Narrow'})
    titulos.set_align('vcenter')
    titulos.set_align('center')
    valores = workbook.add_format({'font_name': 'Arial Narrow'})
    valores.set_align('center')

    for sheet in writer.sheets:

        writer.sheets[sheet].set_row(0, 15, titulos)

        for n in range(len(df.columns)):
            col = get_column_letter(n+2)
            width = col_width(df, n)
            writer.sheets[sheet].set_column(f'{col}:{col}', width, valores)

        writer.sheets[sheet].conditional_format('A1:ZZ9999', {'type': 'no_blanks', 'format': cuadricula})

        writer.sheets[sheet].write('A1', ' ')

    return writer
    

def col_width(df, index):
    try:
        length = df[index].apply(len).max() *1.15
        if length < 8: length = 8
        if length > 40: length = 40
        return length
    except TypeError:
        return 15


