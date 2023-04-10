# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
fail = False
ip_address = input("введите ip-адрес: ")
ip_list = ip_address.split(".")
if len(ip_list) != 4:
    fail = True
else:
    for octet in ip_list:
        if not (octet.isdigit() and int(octet) in range(256)):
            fail = True
            break
if fail:
    print("Неправильный IP-адрес")
else:
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
