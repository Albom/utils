'''
Created on March 27, 2018

@author: Albom
'''

from utils.dgd import DGD
from datetime import date, timedelta

if __name__ == '__main__':

    data = DGD('./data/2018Q1_DGD.txt')

    hours = list()
    days = set()

    d = date(2018, 1, 1)

    while True:
        kp = data.kp(d)
        if kp is None:
            break

        for h, k in enumerate(kp):
            if k == 0:
                n_day = '{:03d}'.format(d.timetuple().tm_yday)
                days.add(n_day)
                for i in range(0, 3):
                    n_hour = chr(i + 3 * h + ord('A'))
                    hours.append(n_day + n_hour)

        d += timedelta(days=1)

    days = list(days)
    days.sort()

    print(days)
    print(hours)
