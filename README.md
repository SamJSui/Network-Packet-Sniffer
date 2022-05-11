# Network Packet Sniffer

*[thenewboston's](https://www.youtube.com/channel/UCJbPGzawDH1njbqV-D5HqKw) tutorial on making a Network Packet Sniffer in Python*

# Description

This Network Packet Sniffer is developed in Python and was a personal Cybersecurity project to give me a better understanding of how packets work leading up to my Security+ Exam.

# **References**

## Ethernet Frame
![Ethernet Frame](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.dLb583Urux0Xnr9uDs-LtQHaB3%26pid%3DApi&f=1)

The Network Interface Card (NIC) is the physical connection from the device to the network, and the MAC address is uniquely tied to the specific device.

`ethernet_frame()` returns:
- Destination MAC Address 
- Source MAC Address
- Protocol/Type (host to network) of Frame - IPv4 Frame, ARP Request/Response, IPv6 Frame (This program only works with IPv4 Frames)
- And rest of the data

## IPv4 Header
![IP Header](https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/IPv4_Packet-en.svg/1200px-IPv4_Packet-en.svg.png)

From the rest of the data, and if the Ethernet Protocol is 0x08 (or 8), that means the Packet is structured as an IPv4 Packet

`ipv4_packet()` uses bitwise operations to parse the Version and Header Length, as well as returning:
- Time To Live - Amount of time packet is set to exist inside network before being discarded by the router
- Type of IPv4 Protocol - Checks if the packet is a type of ICMP, TCP, or UDP
- Source IP - IPv4 Going
- Target IP - IPv4 Receiving
- And rest of the data

## TCP Header
![TCP Header](https://www.researchgate.net/profile/Aladdin-Masri/publication/280681580/figure/fig23/AS:646094535012354@1531052349639/TCP-Header-In-TCP-protocol-the-flags-field-has-in-important-role-in-the-connection-and.png)

`tcp_segment()` returns: 

When data or a request is sent to the host, the sender specifies which port to receive it in order to have the correct service

- Source Port 
- Destination Port  
- Sequence - This number identifies that there is no data loss or dropped, incrementally increasing
- Acknowledgement - This number tells the server what the next expected sequence number
- And the Flags

## UDP Header
![UDP Header](https://upload.wikimedia.org/wikipedia/commons/0/0c/UDP_header.png)

`udp_segment` (another major internet protocol) returns:
- Source Port -
- Destination Port - 
- Length - Length of UDP header + UDP data
- ~~CheckSum~~ - Used to validate that received message has not been altered

# How to Use

*This Packet Sniffer primarily works on Linux and requires elevated privileges in order to have permissions to capture the packets*
*To make this work on a Windows machine, run your IDE/program as Administrator and use the `sniffer.py` in the Windows directory*

`git clone https://github.com/SamJSui/Network-Packet-Sniffer`

`cd /Network-Packet-Sniffer`

`sudo python3 /Linux/sniffer.py` 

The program will print out formatted information as packets are received!



