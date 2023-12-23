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
from tkinter import *
from tkinter import ttk
import socket
import threading
import requests
import json

def response(client_socket=None):
    print("Client request these data")
    with open('Group_GA14.json','r') as ofile:
      json_res=json.load(ofile)

    flights = json_res.get('data',[])

    selected_info = []
    for flight in flights:
      if flight['flight']['iata'] =="PR3502" :
            selected_info.append({
                'IATA code': flight['flight']['iata'],
                'departure airport': flight['departure']['airport'],
                'original departure time': flight['departure']['scheduled'],
                'status': flight['flight_status']
            })

    with open('clientrequestt.json', 'w') as file:
            json.dump(selected_info, file,indent=4) 

    print("===")
    if client_socket:
        # Send the response to the connected client
        client_socket.send(json.dumps(selected_info).encode('ascii'))

def handle_client(client_socket, client_address):
    print('\nAccepted request from', client_address[0], 'with port number', client_address[1])
    
    while True:
        data = client_socket.recv(5000)
        if not data:
            break  # client disconnected
        elif data.decode('ascii')=='1':
            response() #first option: Arrived flights
        print("Client sent:", data.decode('ascii'))
        
        if data.decode('ascii')=='5':
            print("Closing connection with", client_address)
            break # if the client close quit

        """ response = input("Send to client: ")
        client_socket.send(response.encode('ascii')) """
    
    print('Connection with', client_address, 'closed.')
    client_socket.close()


#---------------------------------------------------------------
def start_server():
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


#-----------------------
# Create the main window
root = Tk()

# Create a Button widget and pack it into the window
option1 = ttk.Button(root, text='Arrived flights', width=20)
option1.pack(side=TOP, pady=5 )
option1.config(command=lambda: response())
option2 = ttk.Button(root, text='Delayed flights', width=20)
option2.pack(side=TOP, pady=5)
option3 = ttk.Button(root, text='All flights from a specific city', width=30)
option3.pack(side=TOP, pady=5)
option4 = ttk.Button(root, text='Details of a particular flight', width=30)
option4.pack(side=TOP, pady=5)
option5 = ttk.Button(root, text='Quit', style='B5.TButton') #, command=root.destroy this whats make it close
option5.pack(side=RIGHT, anchor=SE, padx=10, pady=10)  # Add padding and place in the bottom-right corner
option5.config(command=lambda: response_quit())

# Add the response_quit function
def response_quit():
    print("Closing connection with the client")
    root.destroy()  # Close the Tkinter window


# to change the theme
style = ttk.Style()
style.theme_use('classic')
style.configure('TButton', background='lightgray', font=('Helvetica', 10))
style.configure('B5.TButton', foreground='white', background='red', font=('Helvetica', 12, 'bold'))


# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Start the Tkinter event loop
root.mainloop()


