# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""


import yaml
from netmiko import ConnectHandler
from task_20_5 import create_vpn_config
from pprint import pprint
import re


def find_tun_num(src, dst):
    nums = [int(num) for num in re.findall(r"Tunnel(\d+)", src + dst)]
    if not nums:
        return 0
    diff = set(range(min(nums), max(nums) + 1)) - set(nums)
    if diff:
        return min(diff)
    else:
        return max(nums) + 1


def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    with ConnectHandler(**src_device_params) as src, ConnectHandler(
            **dst_device_params
    ) as dst:
        src.enable()
        dst.enable()
        tunnels_src = src.send_command("sh run | include ^interface Tunnel")
        tunnels_dst = dst.send_command("sh run | include ^interface Tunnel")
        vpn_data_dict['tun_num'] = find_tun_num(tunnels_src, tunnels_dst)
        src_cfg, dst_cfg = create_vpn_config(src_template, dst_template, vpn_data_dict)
        src_output = src.send_config_set(src_cfg.split('\n'))
        dst_output = dst.send_config_set(dst_cfg.split('\n'))
    return src_output, dst_output


if __name__ == "__main__":
    template1_file = "templates/gre_ipsec_vpn_1.txt"
    template2_file = "templates/gre_ipsec_vpn_2.txt"
    data = {
        "tun_num": None,
        "wan_ip_1": "192.168.100.1",
        "wan_ip_2": "192.168.100.2",
        "tun_ip_1": "10.0.1.1 255.255.255.252",
        "tun_ip_2": "10.0.1.2 255.255.255.252",
    }
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    pprint(configure_vpn(devices[0], devices[1], template1_file, template2_file, data))
