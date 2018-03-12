#Assignment 1 Part C

import socket


#print header to assignment
print(b"HTTP Protocol Analyzer, Written by <Thomas Evetts>, <43529610>")

#print(b"\r\nURL Requested:")
input_request = input(b"\r\nURL Requested:")
input_request = input_request.encode('utf-8')

print(input_request[2:])

#append the get / http.....
request = b"GET / HTTP/1.1\nHost: " + input_request + b"\n\n"
print(request)
#get the request from the user


#request = b"GET / HTTP/1.1\nHost: www.google.com\n\n" #get this from cmd line
#socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((input_request[4:], 80))
serveripaddr = s.getsockname()[0].encode('utf-8')
serverport = s.getsockname()[1]
print(b"IP Address, Port of the Server: " + serveripaddr + b" ,80")#get the port
myipaddr = socket.gethostbyname(socket.gethostname())
print("IP Address, Port of this client" + myipaddr + ", " + str(serverport))

s.send(request)

#process the response from the website
result = s.recv(1000)
while (len(result) > 0):
    #print(result)
    result = s.recv(10000)
#chase process if result contains a response other than 200 OK
