from datetime import date


class KpLoader:
    def load(self, filename):
        data = []
        with open(filename) as file:
            lines = file.readlines()
        for line in lines[1:]:
            d = date(int(line[:4]), int(line[4:6]), int(line[6:8]))
            kp8_ws = [line[9+i*2:11+i*2] for i in range(8)]
            kp8 = [int(x[0]) for x in kp8_ws]
            kp_sum_ws = line[25:28]
            kp_sum = int(kp_sum_ws[:-1].strip())
            ap8 = [int(line[28+i*3:31+i*3]) for i in range(8)]
            ap = int(line[52:].strip())
            data.append(
                {'date': d,
                 'kp8_ws': kp8_ws,
                 'kp8': kp8,
                 'kp_sum_ws': kp_sum_ws,
                 'kp_sum': kp_sum,
                 'ap8': ap8,
                 'ap': ap})
        return data


if __name__ == '__main__':
    kpLoader = KpLoader()
    kp = kpLoader.load('./data/kp.txt')
    print(list(filter(lambda x: x['date'] == date(1997, 11, 23), kp)))
