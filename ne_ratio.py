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

directory = 'h:/Data/TOMION/2017/03'
filenames = filter(lambda s: s.startswith('ne_ratio'), FileList.get(directory))

data = list()
for name in filenames:
    filename = path.join(directory, name)
    wopen = gzip.open if filename.endswith('.gz') else open

    with wopen(filename) as file:
        tmp = [[float(v) for v in s.strip().split()] for s in file.readlines()]
    if tmp:
        data.extend(tmp)

lat = -44.7
lon = 273.4
dlat = 5
dlon = 4

filtered = filter(lambda d: abs(d[2]-lat)<=dlat and abs(d[10]-lon)<=dlon and abs(d[3]-1130)<50, data)

with open('out.txt', 'wt') as file:
    format_title = '{:19s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>16s}{:>16s}\n'
    field_names = ['DateTime', 'UT', 'Lat', 'Lon', 'RealLat', 'RealLon', 'h0', 'ne', 'sne']
    title = format_title.format(*field_names)
    file.write(title)
    for d in filtered:
        date = from_jd(d[0], fmt='mjd').replace(microsecond=0)
        format = '{:19s}{:8.2f}{:8.2f}{:8.2f}{:8.2f}{:8.2f}{:8.0f}{:16.6e}{:16.6e}\n'
        m = 1.e+14/1.05
        h = date.hour + date.minute/60.0 + date.second/3600.0
        s = format.format(date.isoformat(), h, lat, lon, d[2], d[10], d[3], d[4]*m, d[5]*m)
        file.write(s)
