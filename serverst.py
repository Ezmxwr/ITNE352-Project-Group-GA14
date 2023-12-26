import socket
import threading
import requests
import json

def get_flights_from_api(arr_icao):
     
    params = {
        'access_key': 'fcd54fda53bc3908921d2821cca1cbb7',
        'arr_icao': arr_icao,
        'limit': 100
    }

    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

    if api_result.status_code == 200:
        json_res = api_result.json()
        flights = json_res.get('data', [])
        with open('Group_GA14.json','w') as file:
            json.dump(flights,file,indent=4)
        print("ok")
    else:
        print(f"Error getting data from API. Status Code: {api_result.status_code}")
        return []

def response(selected_option,user_input):
    print("Client requested data for option:", selected_option)

    # Retrieve data once when the server starts
    with open('Group_GA14.json', 'r') as ofile:
        flights = json.load(ofile)

    selected_info = []
    for flight in flights:
        # Process flight data based on the selected option
        if selected_option == '1':
            selected_info.append({
                'Flight Code (IATA)': flight['flight']['iata'],
                'Departure Airport': flight['departure']['airport'],
                'Arrival Airport':flight['arrival']['airport'],
                'Arrival Time': flight['arrival']['scheduled'],
                'Arrival Terminal': flight['arrival']['terminal'],
                'Arrival Gate': flight['arrival']['gate']
            })
        elif selected_option == '2':
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
        elif selected_option=='3':
            if flight['departure']['icao'] == user_input:
                    selected_info.append({
                        'IATA code': flight['flight']['iata'],
                        'departure airport': flight['departure']['airport'],
                        'original departure time': flight['departure']['scheduled'],
                        'estimated arrival time': flight['arrival']['estimated'],
                        'departure gate': flight['departure']['gate'],
                        'arrival gate': flight['arrival']['gate'],
                        'status': flight['flight_status']
                    })
        elif selected_option=='4':
            if flight['flight']['number'] == user_input:    
                    selected_info.append({
                    'Flight Code (IATA)': flight['flight']['iata'],
                    'Departure Airport': flight['departure']['airport'],
                    'Departure Gate': flight['departure']['gate'],
                    'Departure Terminal': flight['departure']['terminal'],
                    'Arrival Airport': flight['arrival']['airport'],
                    'Arrival Gate': flight['arrival']['gate'],
                    'Arrival Terminal': flight['arrival']['terminal'],
                    'Status': flight['flight_status'],
                    'Scheduled Departure Time': flight['departure']['scheduled'],
                    'Scheduled Arrival Time': flight['arrival']['scheduled']
                    })


       

    print("===")
    return json.dumps(selected_info, indent=4)

def handle_client(client_socket, client_address):
    print('\nAccepted request from', client_address[0], 'with port number', client_address[1])
    user_name = client_socket.recv(1024).decode('ascii')
    print("Client's Name:", user_name)

    try:
     while True:
        data = client_socket.recv(8192)
        if not data:    
            break   # client disconnected

        received_data = json.loads(data.decode('ascii'))  # Decode the received JSON data
        if isinstance(received_data, dict):
            option = received_data.get('option')
            user_input = received_data.get('user_input') 
        
        print("Client sent option:", option)
        if option =='1' or option =='2' or option =='3' or option =='4':
                # Get response data based on the selected option and arr_icao
                response_data = response(str(option),user_input)
                print(response_data)
                
                client_socket.send(json.dumps(response_data).encode('ascii')) # new
                # Send response data to the client in chunks
                """ for i in range(0, len(response_data), 1024):
                    chunk = response_data[i:i + 1024]
                    print("Sending response chunk to client:", chunk)
                    client_socket.send(json.dumps(chunk).encode('ascii'))  """
        if option == '5':
                print("Closing connection with", client_address)
                break
    except Exception as e:
        print("Error handling client:", e)

    finally:
        print('Connection with', client_address, 'closed.')
        client_socket.close()
     

sock_p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_p.bind(("127.0.0.1", 49993))
sock_p.listen(5)
arr_icao = input("Enter the departure airport code (arr_icao): ")
get_flights_from_api(arr_icao)
print("DONE ✅")


try:
    while True:
        client_socket, client_address = sock_p.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    sock_p.close()
