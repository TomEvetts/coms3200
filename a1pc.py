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
print(b"Reply Code: "+result[9:12])
status = int(result[9:12])
print(status)

if(status == 100):
    print("Reply Code Meaning: Continue")
elif(status == 101):
    print("Reply Code Meaning: Switching Protocols")
elif(status == 102):
    print("Reply Code Meaning: Processing")
elif(status == 200):
    print("Reply Code Meaning: OK")
elif(status == 201):
    print("Reply Code Meaning: Created")
elif(status == 202):
    print("Accepted")
elif(status == 203):
    print("Reply Code Meaning: Non-authoritative Information")
elif(status == 204):
    print("Reply Code Meaning: No Content")
elif(status == 205):
    print("Reply Code Meaning: Reset Content")
elif(status == 206):
    print("Reply Code Meaning: Partial Content")
elif(status == 207):
    print("Reply Code Meaning: Multi-Status")
elif(status == 208):
    print("Reply Code Meaning: Already Reported")
elif(status == 226):
    print("Reply Code Meaning: IM Used")

elif(status == 300):
    print("Reply Code Meaning: Multiple Choices")
elif(status == 301):
    print("Reply Code Meaning: Moved Permanently")
elif(status == 302):
    print("Reply Code Meaning: Found")
elif(status == 303):
    print("Reply Code Meaning: See Other")
elif(status == 304):
    print("Reply Code Meaning: Not Modified")
elif(status == 305):
    print("Reply Code Meaning: Use Proxy")
elif(status == 307):
    print("Reply Code Meaning: Temporary Redirect")
elif(status == 308):
    print("Reply Code Meaning: Permanent Redirect")

elif(status == 400):
    print("Reply Code Meaning: Bad Request")
elif(status == 401):
    print("Reply Code Meaning: Unauthorized")
elif(status == 402):
    print("Reply Code Meaning: Payment Required")
elif(status == 403):
    print("Reply Code Meaning: Forbidden")
elif(status == 404):
    print("Reply Code Meaning: Not Found")
elif(status == 405):
    print("Reply Code Meaning: Method Not Allowed")
elif(status == 406):
    print("Reply Code Meaning: Not Acceptable")
elif(status == 407):
    print("Reply Code Meaning: Proxy Authentication Required")
elif(status == 408):
    print("Reply Code Meaning: Request Timeout")
elif(status == 409):
    print("Reply Code Meaning: Conflict")
elif(status == 410):
    print("Reply Code Meaning: Gone")
elif(status == 411):
    print("Reply Code Meaning: Length Required")
elif(status == 412):
    print("Reply Code Meaning: Precondition Failed")
elif(status == 413):
    print("Reply Code Meaning: Payload Too Large")
elif(status == 414):
    print("Reply Code Meaning: Request-URI Too Long")
elif(status == 415):
    print(" UReply Code Meaning:nsupported Media Type")
elif(status == 416):
    print("Reply Code Meaning: Requested Range Not Satisfiable")
elif(status == 417):
    print("Reply Code Meaning: Expectation Failed")
elif(status == 418):
    print("Reply Code Meaning: I'm a teapot")   
elif(status == 421):
    print("Reply Code Meaning: Misdirected Request")
elif(status == 422):
    print("Reply Code Meaning: Unprocessable Entity")
elif(status == 423):
    print("Reply Code Meaning: Locked")
elif(status == 424):
    print("Reply Code Meaning: Failed Dependency")
elif(status == 426):
    print("Reply Code Meaning: Upgrade Required")
elif(status == 428):
    print("Reply Code Meaning: Precondition Required")
elif(status == 429):
    print("Reply Code Meaning: Too Many Requests")
elif(status == 431):
    print("Reply Code Meaning: Request Header Fields Too Large")
elif(status == 444):
    print("Reply Code Meaning: Connection Closed Without Response")
elif(status == 451):
    print("Reply Code Meaning: Unavailable For Legal Reasons")
elif(status == 499):
    print("Reply Code Meaning: Client Closed Request")

elif(status == 500):
    print("Reply Code Meaning: Internal Server Error")
elif(status == 501):
    print("Reply Code Meaning: Not Implemented")
elif(status == 502):
    print("Reply Code Meaning: Bad Gateway")
elif(status == 503):
    print("Reply Code Meaning: Service Unavailable")
elif(status == 504):
    print("Reply Code Meaning: Gateway Timeout")
elif(status == 505):
    print("Reply Code Meaning: HTTP Version Not Supported")
elif(status == 506):
    print("Reply Code Meaning: Variant Also Negotiates")
elif(status == 507):
    print("Reply Code Meaning: Insufficient Storage")
elif(status == 508):
    print("Reply Code Meaning: Loop Detected")
elif(status == 510):
    print("Reply Code Meaning: Not Extended")
elif(status == 511):
    print("Reply Code Meaning: Network Authentication Required")
elif(status == 599):
    print("Reply Code Meaning: Network Connect Timeout Error")

while (len(result) > 0):
    #print(result)
    result = s.recv(10000)
#chase process if result contains a response other than 200 OK
