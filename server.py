
import socket
import threading
import requests
import json

# Function to retrieve flights from the AviationStack API
def get_flights_from_api(arr_icao):
    try:
        params = {
            'access_key': '920a8cb87dca6877977c72cb68b4e1bb',
            'arr_icao': arr_icao,
            'limit': 100
        }

        api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

        if api_result.status_code == 200:
            json_res = api_result.json()
            flights = json_res.get('data', [])
            with open('Group_GA14.json', 'w') as file:
                json.dump(flights, file, indent=4)
            print("Data retrieved successfully.✅")
            return flights
        else:
            print(f"Error getting data from API. Status Code: {api_result.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        return []

# Function to process the selected option and generate a response
def response(selected_option, user_input):
    try:
        # Retrieve data once when the server starts
        with open('Group_GA14.json', 'r') as ofile:
            flights = json.load(ofile)

        selected_info = "."
        for flight in flights:
            # Process flight data based on the selected option
            if selected_option == '1':
                if flight['flight_status'] == 'landed':
                    selected_info += f"***Here are your required information about arrived flights ✅***\n"
                    selected_info += f"\n"
                    selected_info += f"Flight IATA code: {flight['flight']['iata']}\n"
                    selected_info += f"Departure Airport: {flight['departure']['airport']}\n"
                    selected_info += f"Arrival Time: {flight['arrival']['estimated']}\n"
                    selected_info += f"Arrival Terminal: {flight['arrival']['terminal']}\n"
                    selected_info += f"Arrival Gate: {flight['arrival']['gate']}\n"
                    selected_info += "\n"
                    selected_info += "=====================================\n"
            elif selected_option == '2':
                if flight['arrival']['delay'] is not None:
                    selected_info += f"***Here are your required information about delayed flights ⏱️***\n"
                    selected_info += f"\n"
                    selected_info += f"Flight IATA code: {flight['flight']['iata']}\n"
                    selected_info += f"Departure Airport: {flight['departure']['airport']}\n"
                    selected_info += f"Original departure Time: {flight['departure']['actual']}\n"
                    selected_info += f"Estimated Arrival Time: {flight['arrival']['estimated']}\n"
                    selected_info += f"Arrival terminal: {flight['departure']['terminal']}\n"
                    selected_info += f"delay : {flight['arrival']['delay']}\n"
                    selected_info += f"Arrival Gate: {flight['arrival']['gate']}\n"
                    selected_info += "\n"
                    selected_info += "=====================================\n"
            elif selected_option == '3':
                if flight['departure']['iata'] == user_input:
                    selected_info += f"***Required information about specific airport/city 👇***\n"
                    selected_info += f"\n"
                    selected_info += f"Flight IATA code: {flight['flight']['iata']}\n"
                    selected_info += f"Departure Airport: {flight['departure']['airport']}\n"
                    selected_info += f"Original departure Time: {flight['departure']['actual']}\n"
                    selected_info += f"Estimated Arrival Time: {flight['arrival']['estimated']}\n"
                    selected_info += f"Arrival Gate: {flight['arrival']['gate']}\n"
                    selected_info += f"Departure Gate: {flight['departure']['gate']}\n"
                    selected_info += f"flight_status: {flight['flight_status']}\n"
                    selected_info += "\n"
                    selected_info += "=====================================\n"
            elif selected_option == '4':
                if flight['flight']['iata'] == user_input:
                    selected_info += f"***Here are your required information about this flight 📅***\n"
                    selected_info += f"\n"
                    selected_info += f"Flight IATA code: {flight['flight']['iata']}\n"
                    selected_info += f"Departure Airport: {flight['departure']['airport']}\n"
                    selected_info += f"Departure Gate: {flight['departure']['gate']}\n"
                    selected_info += f"Departure terminal: {flight['departure']['terminal']}\n"
                    selected_info += f"Arrival airport: {flight['arrival']['airport']}\n"
                    selected_info += f"Arrival Gate: {flight['arrival']['gate']}\n"
                    selected_info += f"Arrival terminal: {flight['arrival']['terminal']}\n"
                    selected_info += f"flight_status: {flight['flight_status']}\n"
                    selected_info += f"scheduled Departure time: {flight['departure']['scheduled']}\n"
                    selected_info += f"scheduled arrival time: {flight['arrival']['scheduled']}\n"
                    selected_info += "=====================================\n"
    except FileNotFoundError:
        selected_info = "Error: File not found."
    except json.JSONDecodeError:
        selected_info = "Error: Unable to decode JSON file."
    except Exception as e:
        selected_info = f"An unexpected error occurred: {str(e)}"
        
    return selected_info

# Function to handle a client's request
def handle_client(client_socket):

    username = None

    try:
        username = client_socket.recv(1024).decode('ascii')  # Receive and print the username
        print('\nAccepted request from', username)
        while True:
            data = client_socket.recv(8192)
            if not data:    
                break   # client disconnected

            received_data = json.loads(data.decode('ascii'))  # Decode the received JSON data
            if isinstance(received_data, dict):
                option = received_data.get('option')
                user_input = received_data.get('user_input') 

            if option in {'1', '2', '3', '4'}:
                if option == '1':
                    print("Request from:", username, "\nType of Request: All arrived flights \n --------------")
                if option == '2':
                    print("Request from:", username, "\nType of Request: All delayed flights \n--------------")
                if option == '3':
                    print("Request from:", username, "\nType of Request: All flights from a specific city\n", " Departure IATA:", user_input, "\n--------------")
                if option == '4':
                    print("Request from:", username, "\nType of Request: Details of a particular flight\n", "Flight IATA:", user_input, "\n--------------")

                # Get response data based on the selected option and user_input
                response_data = response(option, user_input)
                client_socket.sendall(response_data.encode('utf-8'))

            if option == '5':   
                print("Closing connection with", username, "....⏱️")
                break

    except ConnectionResetError:
        print('Connection with', username, 'closed .') 
    except Exception as e:
        print('An error occurred:', e)
    finally:
        if username is not None:
            print("connection with", username ,"closed .")
        client_socket.close()


# Set up the server socket
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(("127.0.0.1", 49993))
sock_server.listen(5)
arr_icao = input("Enter the arrival airport code (arr_icao): ")
get_flights_from_api(arr_icao)

try:
    while True:
        client_socket, client_address = sock_server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

except KeyboardInterrupt:
    print("\nReceived Ctrl+C, Server shutting down...\n")
finally:
    sock_server.close()