import string
import unidecode
from leven import levenshtein
import numpy as np
from sklearn.cluster import dbscan


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





