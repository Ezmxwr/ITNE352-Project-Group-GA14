import socket
sock_p = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_p.bind(("127.0.0.1", 49997))
sock_p.listen(9)
try:
    sock_a, sockname = sock_p.accept()
    print('\nAccepted request from', sockname[0] ,'with port number', sockname[1])
    while True:
        x = sock_a.recv(5000)
        print("client send ..>",x.decode('ascii'))
        x1 = input("send to client")    
        sock_a.send(x1.encode('ascii'))
except SystemExit:
    sock_p.close()
    sock_a.close()
