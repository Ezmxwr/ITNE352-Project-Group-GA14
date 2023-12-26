
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
        if selected_option == '1':
            selected_info.append({
                'Flight Code (IATA)': flight['flight']['iata'],
                'Departure Airport': flight['departure']['airport'],
                'Arrival Time': flight['arrival']['scheduled'],
                'Arrival Terminal': flight['arrival']['terminal'],
                'Arrival Gate': flight['arrival']['gate']
            })
        elif selected_option == '2' : # there is NO 😜 issue here
            selected_info.append({
                'Flight Code (IATA)': flight['flight']['iata'],
                'Departure Airport': flight['departure']['airport'],
                'Departure Time': flight['departure']['scheduled'],
                'Estimated Arrival Time': flight['arrival']['estimated'],
                'Delay': flight['arrival']['delay'],
                'Terminal': flight['arrival']['terminal'],
                'Gate': flight['arrival']['gate'],
                'Status': flight['flight_status']
            }) 
   
    print("===")
    return json.dumps(selected_info, indent=4)
    
   


def handle_client(client_socket, client_address):
    print('\nAccepted request from', client_address[0], 'with port number', client_address[1])
    user_name = client_socket.recv(1024).decode('ascii')
    print("Client's Name:", user_name)
    while True:
        data = client_socket.recv(8192)
        if not data:    
            break  # client disconnected
        

        option = data.decode('ascii')
        print("Client sent option:", option)

        if option =='1':
            response_data = response(option)  #call the def with the client option
            #client_socket.send("whattttttttt".encode('ascii'))
            for i in range(0, len(response_data), 1024):
                chunk = response_data[i:i + 1024]
                print("Sending response chunk to client:", chunk)
                client_socket.send(chunk.encode('ascii'))
        elif option == '2':
            response_data = response(option)  #call the def with the client option
            #client_socket.send("whattttttttt".encode('ascii'))
            for i in range(0, len(response_data), 1024):
                chunk = response_data[i:i + 1024]
                print("Sending response chunk to client:", chunk)
                client_socket.send(chunk.encode('ascii'))
        elif option == '5':
            print("Closing connection with", client_address)
            break

        
        #response_data = response(option)
        """ print("Sending response to client:", response_data)
        client_socket.sendall(response_data.encode('ascii')) """

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

