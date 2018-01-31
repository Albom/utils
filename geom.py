import requests

def geom(lat, long, year):

	data = {
		'model':'cgm',
		'format':'0', # list
		'year': str(year), 
		'geo_flag':'1', # Geocentric 
		'latitude':str(lat), 
		'longitude':str(long), 
		'height':'0', # height
		'profile':'1', # height profile
		'start': '0.', 
		'stop': '1.', 
		'step': '2.', 
		'vars':['14', '15'] # [CGM  Latitude, deg; CGM Longitude, deg.]
	}

	proxies = { # if needed
	  'https': 'http://172.17.10.2:3128'
	}

	headers = {
		'Connection':'close', 
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
	}

	url = 'https://omniweb.gsfc.nasa.gov/cgi/vitmo/vitmo_model.cgi'		
	
	r = requests.post(url, data=data, proxies=proxies, headers=headers)
	ss = r.text[r.text.index('<pre>')+5 : r.text.index('</pre>')].strip().split('\n')[5].strip().split(' ')
	return (float(ss[0]), float(ss[-1]))

print(geom(49.6754912, 36.2922004, 2018))
