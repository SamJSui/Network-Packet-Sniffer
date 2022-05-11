import socket
import struct
import textwrap

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t '
DATA_TAB_2 = '\t\t '
DATA_TAB_3 = '\t\t\t '
DATA_TAB_4 = '\t\t\t\t '

def main():

    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        raw_data, addr = conn.recvfrom(65536) # Whenever socket receives data, it is stored in raw_data and addr
        dest_mac, src_mac, eth_protocol, data = ethernet_frame(raw_data) # Taking the data from socket and passing it into ethernet_frame() function
        print("\nEthernet Frame:")
        print(TAB_1 + "Destination: {}, Source: {}, Protocol: {}".format(dest_mac, src_mac, eth_protocol))
        # 8 for IPv4
        if eth_protocol == 8:
            (version, header_length, time_to_live, protocol, src, target, data) = ipv4_packet(data)
            print(TAB_1 + "IPv4 Packet:")
            print(TAB_2 + "Version: {}, Header Length: {}, Time To Live: {}".format(version, header_length, time_to_live))
            print(TAB_2 + "Protocol: {}, Source: {}, Target: {}".format(protocol, src, target))

            # ICMP
            if protocol == 1:
                icmp_type, code, checksum, data = icmp_packet(data)
                print(TAB_1 + "ICMP Packet:")
                print(TAB_2 + "Type: {}, Code: {}, Checksum: {}".format(icmp_type, code, checksum))
                print(TAB_2 + "Date:")
                print(format_multi_line(DATA_TAB_3, data))

            # TCP
            elif protocol == 6:
                src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data = tcp_segment(data)
                print(TAB_1 + "TCP Segment:")
                print(TAB_2 + "Source Port: {}, Destination Port: {}", format(src_port, dest_port))
                print(TAB_2 + "Sequence: {}, Acknowledgement: {}", format(sequence, acknowledgement))
                print(TAB_2 + "Flags:")
                print(TAB_3 + "URG: {}, ACK: {}, PSH: {}, RST: {}, SYN: {}, FIN: {}".format(flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
                print(TAB_2 + data)
                print(format_multi_line(DATA_TAB_3, data))

            # UDP
            elif protocol == 17:
                src_port, dest_port, length, data = udp_segment(data)
                print(TAB_1 + "UDP Segment:")
                print(TAB_2 + "Source Port: {}, Destination Port: {}, Length: {}".format(src_port, dest_port, length))
                print(format_multi_line(DATA_TAB_3, data))

            else:
                print(TAB_1 + "Data:")
                print((format_multi_line(DATA_TAB_2, data)))
        else:
            print(TAB_1 + "Data:")
            print((format_multi_line(DATA_TAB_2, data)))

# Unpacks Ethernet Data
def ethernet_frame(data):
    dest_mac, src_mac, protocol = struct.unpack("! 6s 6s H", data[:14]) # Convert from Big Endian to Little Endian
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(protocol), data[14:]

# Returns formatted MAC Addr
def get_mac_addr(bytes_addr):
    bytes_str = map("{:02x}".format, bytes_addr) # Each byte of the mac address is formatted to two decimal places
    mac_addr = ":".join(bytes_str).upper() # Combines all the formatted bytes_str's with a ':'
    return mac_addr

# Unpacks IPv4 Data
def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4 # Shift the version_header_length byte to get the 4 left-most bits
    header_length = (version_header_length & 15) * 4
    time_to_live, protocol, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, time_to_live, protocol, ipv4(src), ipv4(target), data[header_length:]

# Returns formatted IPv4 Addr
def ipv4(addr):
    return '.'.join(map(str, addr))

# Unpacks ICMP packet
def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack("! B B H", data[:4])
    return icmp_type, code, checksum, data[4:]

# Unpacks TCP Segment
def tcp_segment(data):
    src_port, dest_port, sequence, acknowledgement, offset_reserved_flags = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) << 2
    flag_urg = (offset_reserved_flags & 0x1f) >> 5
    flag_ack = (offset_reserved_flags & 0xf) >> 5
    flag_psh = (offset_reserved_flags & 0x8) >> 5
    flag_rst = (offset_reserved_flags & 0x4) >> 5
    flag_syn = (offset_reserved_flags & 0x2) >> 5
    flag_fin = (offset_reserved_flags & 0x1) >> 5
    return src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]

# Unpacks UDP Segment
def udp_segment(data):
    src_port, dest_port, size = struct.unpack("! H H 2x H", data[:8])
    return src_port, dest_port, size, data[8:]

# Properly Formats
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r"\x{:02x}".format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

main()
