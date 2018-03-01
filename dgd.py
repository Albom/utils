import datetime


def load_dgd(filename):

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    mid = {}
    high = {}
    planetary = {}

    for line in lines:
        if line.startswith('#') or line.startswith(':'):
            continue

        d = line[:10].strip()
        d = datetime.date(int(d[:4]), int(d[5:7]), int(d[8:10]))

        ap = int(line[14:17])
        kp = tuple([int(line[17 + 2 * i : 17 + 2 * i + 2]) for i in range(0, 8)])
        mid.update({d: {'ap': ap, 'kp': kp}})

        ap = int(line[23 + 14:23 + 17])
        kp = tuple([int(line[23 + 17 + 2 * i : 23 + 17 + 2 * i + 2]) for i in range(0, 8)])
        high.update({d: {'ap': ap, 'kp': kp}})

        ap = int(line[2 * 23 + 14:2 * 23 + 17])
        kp = tuple([int(line[2 * 23 + 17 + 2 * i : 2 * 23 + 17 + 2 * i + 2]) for i in range(0, 8)])
        planetary.update({d: {'ap': ap, 'kp': kp}})

    return {'mid': mid, 'high': high, 'planetary': planetary}


data = load_dgd('./data/2018Q1_DGD.txt')
print(data['planetary'][datetime.date(2018, 1, 30)]['kp'])
