import os
import sqlite3
import re
import yaml
import glob



def switches_yaml2sql(db_filename, yaml_filename):
    with open(yaml_filename) as f:
        input_dict = yaml.safe_load(f)

    db_exists = os.path.exists(db_filename)

    if not db_exists:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return 1

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


def dhcp_snooping_txt2sql(db_filename, data_filenames):
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


if __name__ == "__main__":
    # data_filename = glob.glob("*_dhcp_snooping.txt")
    data_filename = glob.glob("new_data/*_dhcp_snooping.txt")
    db_filename = 'dhcp_snooping.db'
    yaml_filename = 'switches.yml'
    switches_yaml2sql(db_filename, yaml_filename)
    dhcp_snooping_txt2sql(db_filename, data_filename)

