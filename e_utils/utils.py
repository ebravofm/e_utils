import string
import unidecode
from leven import levenshtein
import numpy as np
from sklearn.cluster import dbscan
import pandas as pd
from openpyxl.utils import get_column_letter


def filename(s):
    s = unidecode.unidecode(s)

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_')
    filename = filename[:255]
    return filename


def clean_df(obj, encoding=True, lower_case=True, strip_spaces=True):

    def clean(obj, encoding=encoding, lower_case=lower_case, strip_spaces=strip_spaces):
        if lower_case:
            obj = obj.str.lower()
        if strip_spaces:
            obj = obj.str.strip()
        if encoding:
            obj = obj.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        return obj

    if isinstance(obj, pd.DataFrame):
        for col in obj.columns:
            obj['{}'.format(col)] = clean(obj['{}'.format(col)])
    else:
        obj = clean(obj)

    return obj


def homog_lev(obj, eps=1, min_samples=2):

    def homog_lev_series(obj, eps=eps, min_samples=min_samples):
        name = obj.name

        original = obj.copy()
        obj = obj.drop_duplicates()
        data = obj.tolist()

        def lev_metric(x, y):
            i, j = int(x[0]), int(y[0])
            return levenshtein(data[i], data[j])

        X = np.arange(len(data)).reshape(-1, 1)
        labels = dbscan(X, metric=lev_metric, eps=eps, min_samples=min_samples)[1]

        x = pd.DataFrame({'A': obj.reset_index(drop=True), 'B': pd.Series(labels)})
        y = x.drop_duplicates('B')
        y = y[~(y.B==-1)]
        y.columns = ['C', 'B']
        x = x.merge(y, on='B', how='left')
        x['C'] = np.where(x.C.isnull(), x.A, x.C)

        results = pd.DataFrame({'A': original})
        results = results.merge(x[['A', 'C']], on='A', how='left')
        out = results.C.rename(name)
        
        return out

    if isinstance(obj, pd.DataFrame):
        for col in obj.columns:
            obj['{}'.format(col)] = homog_lev_series(obj['{}'.format(col)])
    else:
        obj = homog_lev_series(obj)

    return obj


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


