import requests


class CGM:

    def __init__(self, proxies={}, headers={}):
        self.proxies = proxies
        self.headers = headers
        self.url = 'https://omniweb.gsfc.nasa.gov/cgi/vitmo/vitmo_model.cgi'

    def geom(self, lat, long, year):

        data = {
            'model': 'cgm',
            'format': '0',  # list
            'year': str(year),
            'geo_flag': '1',  # Geocentric
            'latitude': str(lat),
            'longitude': str(long),
            'height': '0',  # height
            'profile': '1',  # height profile
            'start': '0.',
            'stop': '1.',
            'step': '2.',
            'vars': ['04', '05']  # [CGM  Latitude, deg; CGM Longitude, deg.]
        }

        r = requests.post(self.url,
                          data=data,
                          proxies=self.proxies,
                          headers=self.headers)

        ss = r.text[r.text.index('<pre>') + 5: r.text.index('</pre>')]
        ss = ss.strip().split('\n')[5].strip().split(' ')
        return (float(ss[0]), float(ss[-1]))


if __name__ == '__main__':

    proxies = {  # if needed
              'https': 'http://172.17.10.2:3128'
            }

    headers = {
                'Connection': 'close',
            }

    c = CGM()
    for year in range(2010, 2019):
        print(year, c.geom(49.6754912, 36.2922004, year))
