import binascii
import socket


def send_udp_message(message, address, port):
    """send_udp_message sends a message to UDP server

    message should be a hexadecimal encoded string
    """
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET6
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")


def format_hex(hex):
    """format_hex returns a pretty version of a hex string"""
    octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)

def process_input(message, DNS_type):
    message_out = ""
    if DNS_type:
        # split up by '.' characters
        message = message.split('.')
        for i in range(len(message)):
            message_out = ' '.join(str(hex(ord(c))[2:]) for c in message[i])
            print(message_out)

        # process the URLs into Hex and pre-append the numbers before the dots

message = "AA AA 01 00 00 01 00 00 00 00 00 00 " \
"07 65 78 61 6d 70 6c 65 03 63 6f 6d 00 00 01 00 01"

# "AA AA 09 00 00 01 00 00 00 00 00 00 " \
message_ipaddr = "00 01 01 00 00 01 00 00 00 00 00 00" \
                 "04 82 66 47 a0 00 00 01 00 01"

# this one works bois for inverse request
message_ipaddr_rev = "d6 f8 01 00 00 01" \
                     "00 00 00 00 00 00 03 31 36 30 02 37 31 03 31 30" \
                     "32 03 31 33 30 07 69 6e 2d 61 64 64 72 04 61 72" \
                     "70 61 00 00 0c 00 01"

message_2 = "00 01 01 00 00 01 00 00  00 00 00 00 03 77 77 77" \
            "06 67 6f 6f 67 6c 65 03  63 6f 6d 00 00 01 00 01"

response = send_udp_message(message_ipaddr_rev, "8.8.8.8", 53) # "2001:4860:4860::8888" ipv6 server

#process the input from a given string simulated by a string

input0 = "eait.uq.edu.au"
input1 = "remote.labs.eait.uq.edu.au"
input2 = "microsoft.com"
input3 = "130.102.79.33"
process_input(input0, 1)

print(format_hex(response))