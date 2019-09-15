import pycurl
from io import BytesIO


class Ftp:

    class ListMode:
        FILES_ONLY = 1
        DIRECTORIES_ONLY = 2
        ALL = 3
        MODES = set([FILES_ONLY, DIRECTORIES_ONLY, ALL])

    def __init__(self, proxy=None):
        self.proxy = proxy
        self.curl = pycurl.Curl()

    def list(
             self,
             url,
             raw = False,
             mode = ListMode.ALL
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

        for line in lines:
            columns = line.split()
            if columns:
                name = columns[-1]
                isdir = columns[0].startswith('d')
                s = line if raw else name
                if (mode == self.ListMode.DIRECTORIES_ONLY) and isdir:
                    result.append(s)
                elif (mode == self.ListMode.FILES_ONLY) and not isdir:
                    result.append(s)
                elif mode == self.ListMode.ALL:
                    result.append(s)
                elif mode not in self.ListMode.MODES:
                    format = 'ListMode value: {}. Should be {}'
                    message = format.format(mode, self.ListMode.MODES)
                    raise ValueError(message)

        return result

if __name__ == '__main__':
    ftp = Ftp()
    print(ftp.list('ftp://ftp.aiub.unibe.ch/CODE/',
                   raw=False,
                   mode=Ftp.ListMode.DIRECTORIES_ONLY))
