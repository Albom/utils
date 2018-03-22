
import sys
import requests

if __name__ == '__main__':

    proxies = {  # if needed
              'http': 'http://172.17.10.2:3128'
            }

    headers = {
            'Accept': 'application/x-bibtex;q=1'
        }

    url = 'http://dx.doi.org/' + sys.argv[1]
    r = requests.get(url, proxies=proxies, headers=headers)

    print(r.text)
