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
    return " ".join(pairs)

def process_input(message, DNS_type, ipv6_DNS):
    message_return = ""
    if ipv6_DNS:
        # split up by '.' characters
        message = message.split('.')
        for i in range(len(message)):
            message_out = ' '.join(str(hex(ord(c))[2:]) for c in message[i])
            number_characters = (str(hex(len(message[i]))[2:]) + " ")
            if (len(number_characters) < 3):
                # add a 0
                number_characters = "0" + number_characters
            message_out = number_characters + message_out
            message_return = message_return + message_out + " "

        # now add the normal header to this
        initial = "AA AA 01 00 00 01 00 00 00 00 00 00 "
        final = "00 00 1c 00 01"
        message_return = initial + message_return + final
    else:
        if DNS_type == 1:
            # split up by '.' characters
            message = message.split('.')
            for i in range(len(message)):
                message_out = ' '.join(str(hex(ord(c))[2:]) for c in message[i])
                number_characters = (str(hex(len(message[i]))[2:]) + " ")
                if(len(number_characters)<3):
                    # add a 0
                    number_characters = "0"+number_characters
                message_out = number_characters + message_out
                message_return = message_return + message_out + " "

            #now add the normal header to this
            initial = "AA AA 01 00 00 01 00 00 00 00 00 00 "
            final = "00 00 01 00 01"
            message_return = initial + message_return + final
        elif DNS_type == 2:
            # split up by '.' characters
            message = message.split('.')
            for i in range(len(message)):
                message_out = ' '.join(str(hex(ord(c))[2:]) for c in message[i])
                number_characters = (str(hex(len(message[i]))[2:]) + " ")
                if (len(number_characters) < 3):
                    # add a 0
                    number_characters = "0" + number_characters
                message_out = number_characters + message_out
                message_return = message_return + message_out + " "

            # now add the normal header to this
            initial = "AA AA 01 00 00 01 00 00 00 00 00 00 "
            final = "00 00 0f 00 01" # this one does the mail server query
            message_return = initial + message_return + final
        else:
            # split up by '.' characters
            message = message.split('.')
            for i in reversed(range(len(message))):
                message_out = ' '.join(str(hex(ord(c))[2:]) for c in message[i])
                number_characters = (str(hex(len(message[i]))[2:]) + " ")
                if (len(number_characters) < 3):
                    # add a 0
                    number_characters = "0" + number_characters
                message_out = number_characters + message_out
                message_return = message_return + message_out + " "

            # now add the normal header to this
            initial = "d6 f8 01 00 00 01 " \
                      "00 00 00 00 00 00 "
            final = "07 69 6e 2d 61 64 64 72 04 61 72 " \
                    "70 61 00 00 0c 00 01"
            message_return = initial + message_return + final

    return message_return
        # process the URLs into Hex and pre-append the numbers before the dots

def process_response_ipv4(response, DNS_type, previous_message):
    if DNS_type:
        # the 4 final octets are always the ipv4 from this request
        print("The IPv4 address "+ str(int(response[-8:-6], 16)) + "." + str(int(response[-6:-4], 16)) + "." +
              str(int(response[-4:-2], 16)) + "." + str(int(response[-2:], 16)))
        return ("The IPv4 address "+ str(int(response[-8:-6], 16)) + "." + str(int(response[-6:-4], 16)) + "." +
              str(int(response[-4:-2], 16)) + "." + str(int(response[-2:], 16)))
    else:
        print("The IPv6 address " + str(response[-32:-28]) + ":" + str(response[-28:-24]) + ":" + str(response[-24:-20])
        + ":" + str(response[-20:-16]) + ":" + str(response[-16:-12]) + ":" + str(response[-12:-8])+ ":" +
        str(response[-8:-4]) + ":" + str(response[-4:]))

        return ("The IPv6 address " + str(response[-32:-28]) + ":" + str(response[-28:-24]) + ":" + str(response[-24:-20])
        + ":" + str(response[-20:-16]) + ":" + str(response[-16:-12]) + ":" + str(response[-12:-8])+ ":" +
        str(response[-8:-4]) + ":" + str(response[-4:]))


def convert_hex_ascii(host_name):

    return ''.join([chr(int(''.join(c), 16)) for c in zip(host_name[0::2], host_name[1::2])])




def process_canonical(response, domain_name):
    index_1 = response.find("c00c")
    index_1 = index_1 + 4
    #print(index_1)
    message_flag = int(response[index_1:index_1+4])
    if(message_flag == 1):
        # no domain to process
        print("The host name " + domain_name)
        return ("The host name " + domain_name)
    elif(message_flag == 5):
        #replace upto the first dot on the domain name with the supplied aliase
        split_domain_name = domain_name.split(".")
        word, space, rest = domain_name.partition('.')
        #extract the host name
        # +18 from the c00c
        index_1 = index_1 + 20
        #next 2 characters represent the number of bytes in the name (in hex)
        stop = ""
        host_name_extracted = ""
        while "c0" not in stop:
            host = int(response[index_1:index_1+2], 16)
            host = host * 2
            host_name = response[index_1+2:index_1+2+host]

            host_name_extracted_temp = convert_hex_ascii(host_name)

            index_1 = index_1 + 2 + host

            host_name_extracted = host_name_extracted + convert_hex_ascii(host_name) + "."
            #print(host_name_extracted_temp)


            stop = response[index_1:index_1 + 2]

        # host = int(response[index_1:index_1 + 2], 16)
        # host = host * 2
        # host_name = response[index_1 + 2:index_1 + 2 + host]
        # # stop = host
        # index_1 = index_1 + 2 + host
        # print(response[index_1:index_1 + 2])
        # host_name_extracted = host_name_extracted + "." +convert_hex_ascii(host_name)
        print("The canonical? host name " + host_name_extracted + rest)
        return ("The canonical? host name " + host_name_extracted + rest)

def process_mailserver(response):
    index_1 = response.find("c00c")
    index_1 = index_1 + 4
    # print(index_1)
    message_flag = int(response[index_1:index_1 + 4])

def process_host_name_reverse(response):
    #seek to the 'c00c'
    index_1 = response.find("c00c")
    index_1 = index_1 + 24
    stop = ""
    host_name_extracted = ""
    while "00" not in stop:
        host = int(response[index_1:index_1 + 2], 16)
        host = host * 2
        host_name = response[index_1 + 2:index_1 + 2 + host]

        host_name_extracted_temp = convert_hex_ascii(host_name)

        index_1 = index_1 + 2 + host

        host_name_extracted = host_name_extracted + convert_hex_ascii(host_name) + "."
        #print(host_name_extracted_temp)

        stop = response[index_1:index_1 + 2]
    print("The Host Name " + host_name_extracted)
    return ("The Host Name " + host_name_extracted[:-1])



'''

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

input0 = "eait.uq.edu.au"
input1 = "remote.labs.eait.uq.edu.au"
input2 = "microsoft.com"
input3 = "130.102.71.160"
input4 = "130.102.79.33"
input5 = "mail.google.com"

inpuuut = input1
dns_flag = 1

response = send_udp_message(process_input(inpuuut, dns_flag, 0), "8.8.8.8", 53)

# process the response to extract the information
process_canonical(response, inpuuut)

process_response_ipv4(response,1, process_input(inpuuut, dns_flag, 0))
#print(format_hex(response))

response = send_udp_message(process_input(inpuuut, dns_flag, 1), "8.8.8.8", 53)

# process the response to extract the information
process_response_ipv4(response,0, process_input(inpuuut, dns_flag, 1))


#response = send_udp_message(message, "8.8.8.8", 53) # "2001:4860:4860::8888" ipv6 server

#process the input from a given string simulated by a string

#print(format_hex(response))


inpuuut = input4
dns_flag = 0
#print(process_input(inpuuut, dns_flag, 0))
response = send_udp_message(process_input(inpuuut, dns_flag, 0), "8.8.8.8", 53) # "2001:4860:4860::8888" ipv6 server

# process the response to extract the information
#process_response_ipv4(response,1, process_input(inpuuut, dns_flag, 0))

process_host_name_reverse(response)

#print(format_hex(response))

'''
