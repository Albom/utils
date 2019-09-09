import pycurl
from io import BytesIO


class Ftp:

    def __init__(self, proxy=None):
        self.proxy = proxy
        self.curl = pycurl.Curl()

    def list(
             self,
             url,
             raw = True,
             mode={
                   'files': True,
                   'directories': True,
                   'types': True
                   }
            ):
        self.curl.setopt(pycurl.URL, url)
        if self.proxy:
            delim = self.proxy.rfind(':')
            proxy_url, proxy_port = self.proxy[:delim], self.proxy[delim+1:]
            proxy_port = int(proxy_port)
            self.curl.setopt(pycurl.PROXY, proxy_url)
            self.curl.setopt(pycurl.PROXYPORT, proxy_port)
            self.curl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
        output = BytesIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, output.write)
        self.curl.perform()
        result = output.getvalue().decode('utf-8')
        lines = list(map(lambda x: x.rstrip('\r\n'),
                     filter(lambda x: len(x) > 0, result.split('\n'))))

        result = []
        if raw:
            result = lines
        else:
            
            for line in lines:
                a = line.split()
                if a:
                    name = a[-1]
                    isdir = a[0].startswith('d')

                    # if 'types' in mode and mode['types']:
                    # if 'directories' in mode and mode['directories']:
                    # if 'files' in mode and mode['files']:
                        
                    result.append(isdir + name)
        return result

if __name__ == '__main__':
    ftp = Ftp('http://172.17.10.2:3128')
    print(ftp.list('ftp://ftp.aiub.unibe.ch/CODE/', raw=False))
