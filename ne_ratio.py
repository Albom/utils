import gzip
from os import path
from julian import from_jd
from filelist import FileList


"""
#_field field   meaning                                         example[*]
1       djm1    Modified Julian date / days                     55914.48958333
2       ra      Right Ascension / deg                           214.481000
3       dec     Declination / deg                               21.232300
4       h0      Ionospheric shell mean height / km              1130
5       ne      Estimated electron density mean / m_del_LI / km 1.63293129e-03
6       sne     Estim. electron density Std.Dev./ m_del_LI / km 1.3463e-04
7       ne/net  ne to ne_total (adding vertical voxels) ratio   3.56394610e-01
8       net     ne_total (adding vertical voxels)               0.00458181
9       lt      local time / hours                              8.501561
10      lon     longitude / deg                                 311.273414
11      smlon   Solar-Magnetic longitude / deg                  134.496119
12      smlat   Solar-Magnetic latitude / deg                   31.415062
"""

directory = './ne_ratio'
filenames = filter(lambda s: s.startswith(''), FileList.get(directory))

data = list()
for name in filenames:
    filename = path.join(directory, name)
    wopen = gzip.open if filename.endswith('.gz') else open

    with wopen(filename) as file:
        tmp = [[float(v) for v in s.strip().split()] for s in file.readlines()]
    if tmp:
        data.extend(tmp)

lat = 37.8
lon = 288.5
dlat = 5
dlon = 4

filtered = filter(lambda d: abs(d[2]-lat)<=dlat and abs(d[10]-lon)<=dlon, data)

with open('out.txt', 'wt') as file:
    for d in filtered:
        date = from_jd(d[0], fmt='mjd').replace(microsecond=0).isoformat()
        format = '{:s}{:8.2f}{:8.2f}{:8.2f}{:8.2f}\n'
        s = format.format(date, lat, lon, d[2], d[10])
        file.write(s)
