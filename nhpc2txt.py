from datetime import datetime, timedelta
from os import walk

directory = './430/'
filenames = []
for (dp, dn, fn) in walk(directory):
    filenames.extend(fn)
    break

filenames.sort()

for filename in filenames:
    if filename.endswith('.421'):
        print(filename, end='\t')
        with open(directory+filename, 'r') as file:
            data = file.readlines()

        dt = data[4]
        dt = (dt[2:6], dt[9:11], dt[11:13], dt[13:15], dt[15:17])
        year, month, day, hour, minute = [int(x) for x in dt]
        date = datetime(year, month, day, hour, minute)

        n1 = int(data[1][31:34])
        n2 = int(data[1][34:37])
        n3 = int(data[1][37:40])
        
        if (n1 == n2) and (n1 == n3):
            n_lines_1 = n1//15 + (1 if n1%15 != 0 else 0)
            n_lines_2 = n1//15 + (1 if n1%15 != 0 else 0)
            n_lines_3 = n1//15 + (1 if n1%15 != 0 else 0)
            
            alt = []
            for n in range(n_lines_1):
                alt += [float(x) for x in data[-1-n_lines_3-n_lines_2-n_lines_1+n].split()]

            ne_norm = []
            for n in range(n_lines_2):
                ne_norm += [float(x) for x in data[-1-n_lines_3-n_lines_2+n].split()]

            ne = []
            for n in range(n_lines_3):
                ne += [float(x) for x in data[-1-n_lines_3+n].split()]

            alt_max = alt[-1]
            ne_max = ne[-1]
            for h in [x for x in range(n1)][-1::-1]:
                if ne[h] < ne_max:
                    break
                else:
                    ne_max = ne[h]
                    alt_max = alt[h]
            print(alt_max, ne_max)

        else:
            exit(-1)

        with open(directory+'all.max', 'a') as file:
            file.write('{}\t{}\t{:3d}\t{:9.5f}\t{:8.1f}\t{:e}\n'.format(
                filename, date.isoformat(), date.timetuple().tm_yday, date.hour + date.minute/60.0, alt_max, ne_max))
