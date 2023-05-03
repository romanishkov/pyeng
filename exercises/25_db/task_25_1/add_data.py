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
    result = []

    for data_filename in data_filenames:
        with open(data_filename) as data:
            for line in data:
                match = regex.search(line)
                if match:
                    result.append((*match.groups(), data_filename.split('_')[0]))

    print('Inserting DHCP Snooping data')
    conn = sqlite3.connect(db_filename)

    for row in result:
        try:
            with conn:
                row_host = row
                query = '''insert into dhcp (mac, ip, vlan, interface, switch)
                           values (?, ?, ?, ?, ?)'''
                conn.execute(query, row_host)
                print(row_host)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)

    conn.close()


if __name__ == "__main__":
    data_filename = glob.glob("*_dhcp_snooping.txt")
    db_filename = 'dhcp_snooping.db'
    yaml_filename = 'switches.yml'
    switches_yaml2sql(db_filename, yaml_filename)
    dhcp_snooping_txt2sql(db_filename, data_filename)

