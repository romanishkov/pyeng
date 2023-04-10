# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
fail = True
while fail:
    ip_address = input("введите ip-адрес: ")
    ip_list = ip_address.split(".")
    if len(ip_list) != 4:
        fail = True
    else:
        for octet in ip_list:
            if not (octet.isdigit() and int(octet) in range(256)):
                fail = True
                break
            else:
                fail = False
    if not fail:
        break
    print("Неправильный IP-адрес")
        
if ip_address == "255.255.255.255":
    print("local broadcast")
elif ip_address == "0.0.0.0":
    print("unassigned")
elif 1 <= int(ip_list[0]) <= 223:
    print("unicast")
elif 224 <= int(ip_list[0]) <= 239:
    print("multicast")
else:
    print("unused")