import socket
import threading
import requests
import json

def get_flights_from_api(arr_icao):
    try:
        params = {
            'access_key': 'fcd54fda53bc3908921d2821cca1cbb7',
            'arr_icao': arr_icao,
            'limit': 100
        }

        api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

        if api_result.status_code == 200:
            json_res = api_result.json()
            flights = json_res.get('data', [])
            with open('Group_GA14.json', 'w') as file:
                json.dump(flights, file, indent=4)
            print("Data retrieved successfully.")
            return flights
        else:
            print(f"Error getting data from API. Status Code: {api_result.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        return []


def response(selected_option,user_input):
    print("Client requested data for option:", selected_option)

    # Retrieve data once when the server starts
    with open('Group_GA14.json', 'r') as ofile:
        flights = json.load(ofile)

    selected_info =""
    for flight in flights:
        # Process flight data based on the selected option
        if selected_option == '1':
          
          if flight ['flight_status'] =='landed':
                        selected_info += f"***Here are your required information about arrived flights ✅***\n"
                        selected_info += f"Flight IATA code: {flight['flight']['iata']}\n"
                        selected_info += f"Departure Airport: {flight['departure']['airport']}\n"
                        selected_info += f"Arrival Time: {flight['arrival']['estimated']}\n"
                        selected_info += f"Arrival Terminal: {flight['arrival']['terminal']}\n"
                        selected_info+= f"Arrival Gate: {flight['arrival']['gate']}\n"
                        selected_info += "\n"
                        selected_info += "┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴"

            
        elif selected_option == '2':
          if flight['arrival']['delay'] != None:
                      selected_info += f"***Here are your required information about delayed flights ⏱️***\n"
                      selected_info += f"Flight IATA code: {flight['flight']['iata']}\n"
                      selected_info += f"Departure Airport: {flight['departure']['airport']}\n"
                      selected_info += f"Original departure Time: {flight['departure']['actual']}\n"
                      selected_info += f"Estimated Arrival Time: {flight['arrival']['estimated']}\n"
                      selected_info += f"Arrival terminal: {flight['departure']['terminal']}\n"
                      selected_info += f"delay : {flight['departure']['delay']}\n"
                      selected_info += f"Arrival Gate: {flight['arrival']['gate']}\n"
                      selected_info += "\n"
                      selected_info += "┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴"

        elif selected_option=='3':
            if flight['departure']['iata'] == user_input:
                        selected_info += f"***Required information about specific airport/city 👇***\n"
                        selected_info += f"Flight IATA code: {flight['flight']['iata']}\n"
                        selected_info += f"Departure Airport: {flight['departure']['airport']}\n"
                        selected_info += f"Original departure Time: {flight['departure']['actual']}\n"
                        selected_info += f"Estimated Arrival Time: {flight['arrival']['estimated']}\n"
                        selected_info += f"Arrival Gate: {flight['arrival']['gate']}\n"
                        selected_info += f"Departure Gate: {flight['departure']['gate']}\n"
                        selected_info += f"flight_status: {flight['flight_status']}\n"
                        selected_info += "\n"
                        selected_info += "┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴"
                
        elif selected_option=='4':
            if flight['flight']['iata'] == user_input:    
                        
                        selected_info += f"***Here are your required information about this flight 📅***\n"
                        selected_info += f"Flight IATA code: {flight['flight']['iata']}\n"
                        selected_info += f"Departure Airport: {flight['departure']['airport']}\n"
                        selected_info += f"Departure Gate: {flight['departure']['gate']}\n"
                        selected_info += f"Departure terminal: {flight['departure']['terminal']}\n"
                        selected_info += f"Arrival airport: {flight['arrival']['airport']}\n"
                        selected_info += f"Arrival Gate: {flight['arrival']['gate']}\n"
                        selected_info += f"Arrival terminal: {flight['arrival']['terminal']}\n"
                        selected_info += f"flight_status: {flight['flight_status']}\n"
                        selected_info += f"schaduled Departure time: {flight['departure']['scheduled']}\n"
                        selected_info += f"scheduled arrival time: {flight['arrival']['scheduled']}\n"
                        selected_info += "┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴┬┴┬┴┤├┬┴┬┴"
                        
                    


       

    print("===")
    return selected_info

def handle_client(client_socket, client_address):
    username = client_socket.recv(1024).decode('ascii')  # Receive and print the username
    print('\nAccepted request from',username, 'with port number', client_address[1])
    
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
                client_socket.sendall(response_data.encode('utf-8')) # new
                 
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
