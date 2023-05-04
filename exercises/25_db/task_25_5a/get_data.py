import sqlite3
import sys
from tabulate import tabulate

db_filename = 'dhcp_snooping.db'

query_dict = {
    'vlan': 'select mac, ip, interface, switch, active, last_active from dhcp where vlan = ?',
    'mac': 'select vlan, ip, interface, switch, active, last_active from dhcp where mac = ?',
    'ip': 'select vlan, mac, interface, switch, active, last_active from dhcp where ip = ?',
    'interface': 'select vlan, mac, ip, switch, active, last_active from dhcp where interface = ?',
    'switch': 'select vlan, mac, ip, interface, active, last_active from dhcp where switch = ?',
    'active': 'select vlan, mac, ip, interface, switch, last_active from dhcp where active = ?'
}
arg_num = len(sys.argv) - 1
if arg_num == 0:
    query = 'select * from dhcp'
    conn = sqlite3.connect(db_filename)
    print('В таблице dhcp такие записи:\n')
    print('Активные записи:\n')
    result_active = conn.execute(query + ' where active = 1')
    print(tabulate(result_active))
    result_inactive = conn.execute(query + ' where active = 0')
    out_list = []
    for row in result_inactive:
        out_list.append(row)
    if out_list:
        print('\nНеактивные записи:\n')
        print(tabulate(out_list))

elif arg_num == 2:
    key, value = sys.argv[1:]
    keys = query_dict.keys()

    if not key in keys:
        print('Данный параметр не поддерживается.')
        print('Допустимые значения параметров: {}'.format(', '.join(keys)))
    else:
        conn = sqlite3.connect(db_filename)
        conn.row_factory = sqlite3.Row

        print('\nИнформация об устройствах с такими параметрами: ', key, value)

        query = query_dict[key]
        print('Активные записи:\n')
        result_active = conn.execute(query + ' and active = 1', (value,))
        print(tabulate(result_active))
        result_inactive = conn.execute(query + ' and active = 0', (value,))
        out_list = []
        for row in result_inactive:
            out_list.append(row)
        if out_list:
            print('\nНеактивные записи:\n')
            print(tabulate(out_list))

else:
    print('Пожалуйста, введите два или ноль аргументов')




