# e_utils

Miscellaneous utilities I sometimes use.

## Installing
```python
pip install git+https://github.com/ebravofm/e_utils.git
```

## Filename()
Takes any string and returns a new string that is valid for naming files. 
 + Removes accents and tildes.
 + Removes invalid characters.
 + Replaces spaces (' ') with underscores ('_')
 + Keeps first 255 characters only.
 
```python
>>> s = "La vie d'Adèle (2003).mp4"
>>> filename(s)

'La_vie_dAdele_(2003).mp4'
```
## Clean_df()
Takes a pandas dataframe or series and homogenizes each row by doing the following vector actions:
 + Applies lower case
 + Strips leading and trailing spaces
 + Removes accents and tildes

## Homog_lev()
Takes a pandas dataframe or series and homogenizes each row matching similar strings and naming them the same. The module uses levenshtein distance to compare the strings to each other, by default, strings that are one single-character edit away are taken as the same. The module takes de levenshtein distance matrix, creates clusters and renames all the elements within the cluster the same. This module uses scikitlearn's DBSCAN.

```python
>>> from e_utils.utils import clean_df
>>> from e_utils.utils import homog_lev

>>> series
0        Bad Bunny
1         bad buny
2      bag bunny
3            Ozuna
4     De La Ghetto
5      de la geto
6     Daddy Yankee
7      dade yankee
8        Nicky Jam
9        nicky jam
10        J Balvin
11        jbalvin
12          Maluma
13          maluma
14        Anuel AA

>>> series2 = clean_df(series)
>>> series2 = homog_lev(series2, eps=3)
>>> pd.concat([series, series2.str.title()], axis=1, keys=['*Original*', '*Fixed*'])

      *Original*       *Fixed*
0      Bad Bunny     Bad Bunny
1       bad buny     Bad Bunny
2    bag bunny       Bad Bunny
3          Ozuna         Ozuna
4   De La Ghetto  De La Ghetto
5    de la geto   De La Ghetto
6   Daddy Yankee  Daddy Yankee
7    dade yankee  Daddy Yankee
8      Nicky Jam     Nicky Jam
9      nicky jam     Nicky Jam
10      J Balvin      J Balvin
11      jbalvin       J Balvin
12        Maluma        Maluma
13        maluma        Maluma
14      Anuel AA      Anuel Aa
```
