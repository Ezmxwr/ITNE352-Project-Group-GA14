import socket
socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_c.connect(("127.0.0.1", 49997))
print("\nThe request has been sent")
try:
    while True:
        x = input("send to server")
        socket_c.send(x.encode("ascii"))
        x2= socket_c.recv(2048)
        print("recieved from server..<",x2.decode('ascii'))
except SystemExit:
    socket_c.close()
