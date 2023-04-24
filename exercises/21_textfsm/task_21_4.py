# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
from textfsm import clitable
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import yaml


def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            output = ssh.send_command(command)
        return output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

def send_and_parse_show_command(
        device_dict, command, templates_path='templates', index_file='index'):
    attributes_dict = {"Command": command, "Vendor": device_dict["device_type"]}
    command_output = send_show_command(device_dict, command)
    cli_table = clitable.CliTable(index_file, templates_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    out_list = [dict(zip(cli_table.header, row)) for row in cli_table]
    return out_list


# вызов функции должен выглядеть так
if __name__ == "__main__":
    command_test = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for d in devices:
        print(send_and_parse_show_command(d, command_test))
