from scapy.all import *


def divide():
    return "----------------------------------------------------------<br>"


class Attacker:
    def __init__(self, ip, port):
        ip = ip
        ports = []
        ports.append(port)
        incomplete_ports = []

    def add_port(self, port):
        ports.append(port)

    def add_incomplete_port(self, port):
        incomplete_ports.append(port)


def check_for_xmas(packets):
    xmas_packets = 0
    attackers = list()
    attacked_ip_list = list()
    ip_source = str()
    string = str()

    for packet in packets:
        if TCP in packet and packet[TCP].flags == 0x29:
            xmas_packets = xmas_packets + 1
            if len(attackers) != 0:
                for attacker in attackers:
                    if attacker.ip == packet[IP].src:
                        ip_source = packet[IP].src
                        attacked_ip_list.append(packet[IP].dst)

            else:
                temp = Attacker(packet[IP].src, packet[TCP].dport)
                attackers.append(temp)

    attacked_ip_list = list(set(attacked_ip_list))

    if xmas_packets < 100:
        string += "<font color='green'>Сканирование XMAS: не обнаружено</font><br>"

    else:
        string += f"<font color='red'>Сканирование XMAS:  обнаружена активность</font><br>"
        string += f"IP адрес атакующего: {ip_source}<br>IP адреса атакуемых:<br>"
        for attacker in attacked_ip_list:
            string += f'{attacker}<br>'

    return string


def check_for_udp(packets):
    udp_packets = 0
    attackers = []
    attacked_ip_list = list()
    ip_source = str()
    string = str()

    for packet in packets:
        if UDP in packet and packet[UDP].len == 8:
            udp_packets = udp_packets + 1
            if len(attackers) != 0:
                for attacker in attackers:
                    if attacker.ip == packet[IP].src:
                        ip_source = packet[IP].src
                        attacked_ip_list.append(packet[IP].dst)
            else:
                temp = Attacker(packet[IP].src, packet[UDP].dport)
                attackers.append(temp)

    attacked_ip_list = list(set(attacked_ip_list))

    if udp_packets < 100:
        string += "<font color='green'>Сканирование UDP: не обнаружено</font><br>"
    else:
        string += f"<font color='red'>Сканирование UDP: обнаружена активность.</font><br>"
        string += f"IP адрес атакующего: {ip_source}<br>IP адреса атакуемых:<br>"
        for attacker in attacked_ip_list:
            string += f"{attacker}<br>"

    return string


def check_for_null(packets):
    null_packets = 0
    attackers = []
    attacked_ip_list = list()
    ip_source = str()
    string = str()

    for packet in packets:
        if TCP in packet and packet[TCP].flags == 0x0:
            null_packets = null_packets + 1
            if len(attackers) != 0:
                for attacker in attackers:
                    if attacker.ip == packet[IP].src:
                        ip_source = packet[IP].src
                        attacked_ip_list.append(packet[IP].dst)
                    else:
                        temp = Attacker(packet[IP].src, packet[TCP].dport)
                        attackers.append(temp)
            else:
                temp = Attacker(packet[IP].src, packet[TCP].dport)
                attackers.append(temp)

    attacked_ip_list = list(set(attacked_ip_list))

    if null_packets < 100:
        string += "<font color='green'>Сканирование NULL: не обнаружено</font><br>"
    else:
        string += f"<font color='red'>Сканирование NULL: обнаружена активность.</font><br>"
        string += f"IP адрес атакующего: {ip_source}<br>IP адреса атакуемых:<br>"
        for attacker in attacked_ip_list:
            string += f'{attacker}<br>'

    return string


def check_for_half(packets):
    half_packets = 0
    half_packets_complete = 0
    half_packets_incomplete = 0
    attackers = []
    attacked_ip_list = list()
    string = str()
    ip_source = str()

    for current, packet in enumerate(packets):
        if TCP in packet and packet[TCP].flags == 0x002:
            if current < (len(packets) - 1):
                if TCP in packets[current + 1] and (packets[current + 1])[TCP].flags == 0x012:
                    if current < (len(packets) - 2):
                        if TCP in packets[current + 2] and (packets[current + 2])[TCP].flags == 0x004:
                            half_packets_complete = half_packets_complete + 1
                            half_packets = half_packets + 1
                            if len(attackers) != 0:
                                for attacker in attackers:
                                    if attacker.ip == packet[IP].src:
                                        ip_source = packet[IP].src
                                        attacked_ip_list.append(packet[IP].dst)
                                    else:
                                        temp = Attacker(
                                            packet[IP].src, packet[TCP].dport)
                                        attackers.append(temp)
                            else:
                                temp = Attacker(
                                    packet[IP].src, packet[TCP].dport)
                                attackers.append(temp)
                elif TCP in packets[current + 1] and (packets[current + 1])[TCP].flags == 0x014:
                    half_packets_incomplete = half_packets_incomplete + 1
                    half_packets = half_packets + 1
                    if len(attackers) != 0:
                        for attacker in attackers:
                            if attacker.ip == packet[IP].src:
                                ip_source = packet[IP].src
                                attacked_ip_list.append(packet[IP].dst)
                            else:
                                temp = Attacker(
                                    packet[IP].src, packet[TCP].dport)
                                attackers.append(temp)
                    else:
                        temp = Attacker(packet[IP].src, packet[TCP].dport)
                        temp.add_incomplete_port(packet[TCP].dport)
                        attackers.append(temp)

    attacked_ip_list = list(set(attacked_ip_list))

    if half_packets < 100:
        string += "<font color='green'>Сканирование Half: не обнаружено</font><br>"
    else:
        string += f"<font color='red'>Сканирование Half: обнаружена активность.</font><br>"
        string += f"IP адрес атакующего: {ip_source}<br>IP адреса атакуемых:<br>"
        for attacker in attacked_ip_list:
            if attacker.startswith('192.168'):
                string += f'{attacker}<br>'

    return string


def check_for_icmp(packets):
    icmp_packets = 0
    icmp = []
    string = str()

    for packet in packets:
        if ICMP in packet:
            if packet[ICMP].type == 8:
                icmp_packets = icmp_packets + 1
                icmp.append([packet[IP].src, packet[IP].dst])
    if icmp_packets < 100:
        string += "<font color='green'>Сканирование ICMP: не обнаружено</font><br>"
    else:
        string += f"<font color='red'>Сканирование ICMP: обнаружена активность.</font><br>"
        for x in icmp:
            string += f"ICMP пакеты. Источник: {x[0]}, Цель: {x[1]}<br>"

    return string


def all_check(path):
    packets = rdpcap(path)

    liner = divide()
    xmas_print = check_for_xmas(packets)
    udp_print = check_for_udp(packets)
    null_print = check_for_null(packets)
    half_print = check_for_half(packets)
    icmp_print = check_for_icmp(packets)

    return str(liner+xmas_print+liner+udp_print+liner+null_print+liner+half_print+liner+icmp_print+liner)
