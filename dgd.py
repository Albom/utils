import datetime
import json


class DGD:

    def __init__(self, filename):

        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        self.mid = {}
        self.high = {}
        self.planetary = {}

        for line in lines:
            if line.startswith('#') or line.startswith(':'):
                continue

            d = line[:10].strip()
            d = datetime.date(int(d[:4]), int(d[5:7]), int(d[8:10]))
            d = d.isoformat()

            a = int(line[14:17])
            k = tuple([int(line[17 + 2 * i: 17 + 2 * i + 2])
                       for i in range(0, 8)])
            self.mid.update({d: {'a': a, 'k': k}})

            a = int(line[23 + 14:23 + 17])
            k = tuple([int(line[23 + 17 + 2 * i: 23 + 17 + 2 * i + 2])
                       for i in range(0, 8)])
            self.high.update({d: {'a': a, 'k': k}})

            a = int(line[2 * 23 + 14:2 * 23 + 17])
            k = tuple([int(line[2 * 23 + 17 + 2 * i: 2 * 23 + 17 + 2 * i + 2])
                       for i in range(0, 8)])
            self.planetary.update({d: {'a': a, 'k': k}})

    def json(self):
        return json.dumps({'mid': self.mid,
                           'high': self.high,
                           'planetary': self.planetary})

    def kp(self, date):
        try:
            r = self.planetary[date.isoformat()]['k']
        except Exception:
            return None
        return r

    def ap(self, date):
        try:
            r = self.planetary[date.isoformat()]['a']
        except Exception:
            return None
        return r


if __name__ == '__main__':

    data = DGD('./data/2018Q1_DGD.txt')
    print(data.kp(datetime.date(2018, 1, 30)))
    print(data.ap(datetime.date(2018, 1, 30)))
    print(data.ap(datetime.date(2019, 1, 30)))

    print(data.json())
