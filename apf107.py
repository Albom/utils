from datetime import date


class APF107:

    def load(self, filename):
        data = []
        with open(filename, 'r') as file:
            lines = file.readlines()

        for line in lines:
            year = int(line[:3])
            year += 2000 if year < 58 else 1900
            month = int(line[3:6])
            day = int(line[6:9])
            current_date = date(year, month, day)

            ap = []
            for i in range(8):
                ap.append(int(line[9+3*i:12+3*i]))

            ap_d = int(line[33:36])

            f107_d = float(line[39:44])
            f107_81 = float(line[44:49])
            f107_365 = float(line[49:54])

            data.append({
                'date': current_date,
                'ap': ap,
                'ap_d': ap_d,
                'f107_d': f107_d,
                'f107_81': f107_81,
                'f107_365': f107_365
                })
        return data


if __name__ == '__main__':
    a = APF107()
    data = a.load('./data/apf107.dat')
    print(data)
