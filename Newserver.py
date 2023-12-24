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
import requests
import json

def response(selected_option):
    print("Client requested data for option:", selected_option)
    with open('Group_GA14.json', 'r') as ofile:
        json_res = json.load(ofile)

    flights = json_res.get('data', [])
    
    selected_info = []

    for flight in flights:
        if selected_option == '1' and flight['flight']['iata'] == "PR3502":
            selected_info.append({
                'IATA code': flight['flight']['iata'],
                'departure airport': flight['departure']['airport'],
                'original departure time': flight['departure']['scheduled'],
                'status': flight['flight_status']
            })
        elif selected_option == '2' and flight['flight']['iata'] == "BA6180": # there is an issue here...
            selected_info.append({
                'IATA code': flight['flight']['iata'],
                'departure airport': flight['departure']['airport'],
                'original departure time': flight['departure']['scheduled'],
                'estimated arrival time': flight['arrival']['estimated'],
                'delay': flight['arrival']['delay'],
                'terminal': flight['arrival']['terminal'],
                'gate': flight['arrival']['gate'],
                'status': flight['flight_status']
            }) 
   
    print("===")
    return json.dumps(selected_info, indent=4)
    
   


def handle_client(client_socket, client_address):
    print('\nAccepted request from', client_address[0], 'with port number', client_address[1])

    while True:
        data = client_socket.recv(5000)
        if not data:
            break  # client disconnected
        

        option = data.decode('ascii')
        print("Client sent option:", option)

        if option in ('1', '2'):
            response(data)  #call the def with the client option
        elif option == '5':
            print("Closing connection with", client_address)
            break

        response_data = response(option)
        print("Sending response to client:", response_data)
        client_socket.send(response_data.encode('ascii'))

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

