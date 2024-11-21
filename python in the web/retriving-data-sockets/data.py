import socket

# Set up the socket connection
host = 'data.pr4e.org'
port = 80
url = '/intro-short.txt'

# Create a socket
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect((host, port))

# Send the GET request
request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
mysock.send(request.encode())

# Receive and print the response
response = b""
while True:
    data = mysock.recv(512)
    if not data:
        break
    response += data

mysock.close()

# Split and print the headers and body
response_text = response.decode()
headers, body = response_text.split("\r\n\r\n", 1)

print("HTTP Response Headers:\n")
print(headers)
print("\nHTTP Response Body:\n")
print(body)
