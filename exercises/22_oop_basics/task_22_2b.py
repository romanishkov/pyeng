# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
import telnetlib
import time
from textfsm import clitable



class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b"Username")
        self._write_line(username)
        self.telnet.read_until(b"Password")
        self._write_line(password)
        index, m, output = self.telnet.expect([b">", b"#"])
        if index == 0:
            self._write_line("enable")
            self.telnet.read_until(b"Password")
            self._write_line(secret)
            self.telnet.read_until(b"#", timeout=5)
        self. _write_line("terminal length 0")
        self. telnet.read_until(b"#", timeout=5)
        time.sleep(3)
        self.telnet.read_very_eager()

    def _write_line(self, line):
        self.telnet.write(line.encode("ascii") + b"\n")

    def send_show_command(self, command, parse=True, templates='templates', index='index1'):
        self._write_line(command)
        command_result = self.telnet.read_until(b"#", timeout=5).decode("ascii")
        if parse:
            attributes_dict = {"Command": command}
            cli_table = clitable.CliTable(index, templates)
            cli_table.ParseCmd(command_result, attributes_dict)
            out_list = [dict(zip(cli_table.header, row)) for row in cli_table]
            return out_list
        else:
            return command_result

    def send_config_commands(self, commands):
        self._write_line("conf t")
        if type(commands) == str:
            self._write_line(commands)
        elif type(commands) == list:
            for command in commands:
                self._write_line(command)
        self._write_line("end")
        time.sleep(3)
        return self.telnet.read_very_eager().decode("ascii")


if __name__ == "__main__":
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
    command_test = 'logging 10.1.1.1'
    commands_test = ['interface loop55', 'ip address 5.5.5.5 255.255.255.255']
    r1 = CiscoTelnet(**r1_params)
    print(r1.send_config_commands(commands_test))