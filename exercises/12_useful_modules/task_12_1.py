# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess

def ping_ip_addresses(ip_list):
    ok_list = []
    fail_list = []
    for ip in ip_list:
        result = subprocess.run(
            ['ping', '-c', '2', '-n', ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            ok_list.append(ip)
        else:
            fail_list.append(ip)
    return (ok_list, fail_list)

if __name__ == "__main__":
    test_list = ['127.0.0.1', '172.16.1.1', '8.8.8.8', '10.0.143.5']
    print(ping_ip_addresses(test_list))
    
           