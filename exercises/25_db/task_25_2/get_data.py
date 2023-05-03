import sqlite3
import sys
from tabulate import tabulate

db_filename = 'dhcp_snooping.db'

query_dict = {
    'vlan': 'select mac, ip, interface, switch from dhcp where vlan = ?',
    'mac': 'select vlan, ip, interface, switch from dhcp where mac = ?',
    'ip': 'select vlan, mac, interface, switch from dhcp where ip = ?',
    'interface': 'select vlan, mac, ip, switch from dhcp where interface = ?',
    'switch': 'select vlan, mac, ip, interface from dhcp where switch = ?'
}
arg_num = len(sys.argv) - 1
if arg_num == 0:
    query = 'select * from dhcp'
    conn = sqlite3.connect(db_filename)
    print('В таблице dhcp такие записи:')
    print(tabulate(conn.execute(query)))
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
        result = conn.execute(query, (value,))
        print(tabulate(result))
else:
    print('Пожалуйста, введите два или ноль аргументов')





