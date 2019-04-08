
from lxml import etree
from datetime import datetime

if __name__ == '__main__':

    with open('d:/WP937_20170317(076)_SAO.XML') as file:
        xml = file.read()

    root = etree.fromstring(xml)

    data = []

    for record_list in root.getchildren():
        if record_list.tag == 'SAORecord':
            time = record_list.get('StartTimeUTC', '-1')
            for record in record_list.getchildren():
                if record.tag == 'CharacteristicList':
                    line = {}
                    for characteristic in record.getchildren():
                        if characteristic.tag == 'URSI':
                            if characteristic.get('ID', '-1') == '00':
                                line['foF2'] = characteristic.get('Val', '-1')
                                line['foF2_flag'] = characteristic.get('Flag', '-1')

                            elif characteristic.get('ID', '-1') == '92':
                                line['hmF2'] = characteristic.get('Val', '-1')
                                line['hmF2_flag'] = characteristic.get('Flag', '-1')
                    if line:
                        line['time'] = time
                        data.append(line)

    with open('out.txt', 'w') as file:
        include_all = False
        for line in data:
            time = datetime.strptime(line['time'], '%Y-%m-%d -%j %H:%M:%S.%f')
            s = '{:30s} {:8.3f} {:8.3f} {:10s} {:8.3f} {:10s}\n'.format(
                line['time'],
                time.hour + time.minute/60.0 + time.second/3600.0,
                float(line['foF2']) if 'foF2' in line else -1,
                line['foF2_flag'] if 'foF2_flag' in line else '-1',
                float(line['hmF2']) if 'hmF2' in line else -1,
                line['hmF2_flag'] if 'hmF2_flag' in line else '-1')
            if line['foF2_flag'] == 'edited' or include_all:
                file.write(s)
