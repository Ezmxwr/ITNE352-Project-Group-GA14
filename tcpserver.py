""" import socket
sock_p = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_p.bind(("127.0.0.1", 49993))
sock_p.listen(2)
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
 """
import socket
import threading

def handle_client(client_socket, client_address):
    print('\nAccepted request from', client_address[0], 'with port number', client_address[1])
    
    while True:
        data = client_socket.recv(5000)
        if not data:
            break  # client disconnected
        print("Client sent:", data.decode('ascii'))
        """ response = input("Send to client: ")
        client_socket.send(response.encode('ascii')) """
    
    print('Connection with', client_address, 'closed.')
    client_socket.close()

sock_p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_p.bind(("127.0.0.1", 49993))
sock_p.listen(5)

try:
    while True:
        client_socket, client_address = sock_p.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    sock_p.close()
