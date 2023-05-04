import os
import sqlite3
import re
import yaml
from tabulate import tabulate
from datetime import datetime, timedelta


def create_db(db_filename, schema_filename):
    db_exists = os.path.exists(db_filename)

    conn = sqlite3.connect(db_filename)

    if not db_exists:
        print('Создаю базу данных...')
        with open(schema_filename, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        print('Done')
    else:
        print('База данных существует')

    conn.close()


def add_data_switches(db_filename, yaml_filenames):
    db_exists = os.path.exists(db_filename)

    if not db_exists:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return 1

    for yaml_filename in yaml_filenames:
        with open(yaml_filename) as f:
            input_dict = yaml.safe_load(f)

        print('Inserting switches data')
        conn = sqlite3.connect(db_filename)

        for hostname, location in input_dict['switches'].items():
            try:
                with conn:
                    query = '''insert into switches (hostname, location)
                                   values (?, ?)'''
                    conn.execute(query, (hostname, location))
                    print(hostname, location)
            except sqlite3.IntegrityError as e:
                print('Error occured: ', e)

    conn.close()


def add_data(db_filename, data_filenames):
    regex = re.compile(r'(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    db_exists = os.path.exists(db_filename)
    if not db_exists:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return 1

    if type(data_filenames) == str:
        data_filenames = [data_filenames]

    print('Inserting DHCP Snooping data')
    conn = sqlite3.connect(db_filename)

    for data_filename_i in data_filenames:
        data_filename = os.path.basename(data_filename_i)
        result = []
        host = data_filename.split('_')[0]
        with open(data_filename_i) as data:
            for line in data:
                match = regex.search(line)
                if match:
                    result.append((*match.groups(), host, 1))
        preupd_query = 'update dhcp set active = 0 where switch = (?)'
        conn.execute(preupd_query, (host,))
        now = datetime.utcnow().replace(microsecond=0)
        week_ago = now - timedelta(days=7)
        del_old_query = 'delete from dhcp where last_active < ?'
        conn.execute(del_old_query, (str(week_ago),))

        for row in result:
            print(row)
            try:
                with conn:
                    query = '''replace into dhcp (mac, ip, vlan, interface, switch, active, last_active)
                               values (?, ?, ?, ?, ?, ?, datetime('now'))'''
                    conn.execute(query, row)
                    print(row)
            except sqlite3.IntegrityError as e:
                print('Error occured: ', e)
    conn.close()


def get_all_data(db_filename):
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


def get_data(db_filename, key, value):
    query_dict = {
        'vlan': 'select mac, ip, interface, switch, active, last_active from dhcp where vlan = ?',
        'mac': 'select vlan, ip, interface, switch, active, last_active from dhcp where mac = ?',
        'ip': 'select vlan, mac, interface, switch, active, last_active from dhcp where ip = ?',
        'interface': 'select vlan, mac, ip, switch, active, last_active from dhcp where interface = ?',
        'switch': 'select vlan, mac, ip, interface, active, last_active from dhcp where switch = ?',
        'active': 'select vlan, mac, ip, interface, switch, last_active from dhcp where active = ?'
    }
    keys = query_dict.keys()
    if key not in keys:
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
