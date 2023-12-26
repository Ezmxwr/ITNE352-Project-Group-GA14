import socket
from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from threading import Thread
import json

# Global variables
response_data = ""
socket_c = None


def receive_data_from_server(option): #new
    global response_data
    while True:
        try:

            chunk = socket_c.recv(1024).decode('ascii')
            if not chunk:
                break
            response_data += chunk
    
            # Update the text label with the server response
            response_text.config(state=NORMAL)
            response_text.delete('1.0', END)
            response_text.insert(END, "Server Response for Option {}:\n".format(option))

            try:

                if response_data.strip():
                # Attempt to parse the received data as JSON
                    """ json_objects = response_data.split('\n===') #new
                    for json_obj in json_objects:#new """
                    decoded_response = json.loads(response_data)

                    # Handle different types of responses
                    if isinstance(decoded_response, list):
                        for item in decoded_response:
                            response_text.insert(END, "\n===\n")
                            for key, value in item.items():
                                response_text.insert(END, "{}: {}\n".format(key, value))
                    else:
                        response_text.insert(END, str(decoded_response))
                else:
                               # Handle the case when response_data is empty
                    response_text.insert(END, "No data received from the server.")
            except json.JSONDecodeError as e:
                response_text.insert(END, "Error decoding server response: {}\n".format(e))
            
            response_text.config(state=DISABLED)

        except Exception as e:
            print("Error receiving data from the server:", e)
            break


def communicate_with_server(option , user_input= None):
    global socket_c, response_data
    response_data = ""
    print(option)
    print(user_input)
    try:
        # Send the username to the server
        socket_c.send(username.encode("ascii"))

        # Send the selected option to the server
        #socket_c.send(option.encode("ascii"))

        if option=='1' or option== '2'or option =='5':
            data_to_send = {'option': option, 'user_input': user_input}
            socket_c.send(json.dumps(data_to_send).encode("ascii"))
            if option=='5':
                root.destroy

        # If needed, prompt the user for additional input
        if option == '3':
            # For option 3, tell the user to enter a city name
            user_input = simpledialog.askstring("Enter City", "Please enter the city name:") 
        elif option == '4':
            user_input = simpledialog.askstring("Enter Flight Number", "Please enter the flight number:")
        
        # to isplay the user input in a label
        user_input_label.config(text="User Input: {}".format(user_input))

        # Start a thread to continuously receive data from the server
        receive_thread = Thread(target=receive_data_from_server, args=(option,), daemon=True)
        receive_thread.start()

    except Exception as e:
        print("Error communicating with the server:", e)

# Create the main window
root = Tk()

root.title("Flight Information Client")

# Create Button widgets and associate them with corresponding functions
option1 = ttk.Button(root, text='Arrived flights', width=30, command=lambda: communicate_with_server('1'))
option1.pack(side=TOP, pady=5)
option2 = ttk.Button(root, text='Delayed flights', width=30, command=lambda: communicate_with_server('2'))
option2.pack(side=TOP, pady=5)
option3 = ttk.Button(options_frame, text='All flights from a specific city', width=30, command=lambda: show_options_after_username_entry('3'))
option3.pack(side=TOP, pady=5)
option4 = ttk.Button(options_frame, text='Details of a particular flight', width=30, command=lambda: show_options_after_username_entry('4'))
option4.pack(side=TOP, pady=5)
option5 = ttk.Button(root, text='Quit', style='B5.TButton', command=root.destroy)
option5.pack(side='top', anchor=SE, padx=10, pady=10)
# Add a label to display the entered input
user_input_label = Label(root, text="", font=('Helvetica', 12))
user_input_label.pack(side=TOP, pady=10) # i think no need for it, what u think?

#  Text widget with a scroller to display server responses
response_text = Text(options_frame, wrap=WORD, width=60, height=50)
response_text.pack(side=LEFT, pady=10)
scrollbar = Scrollbar(options_frame, command=response_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
response_text.config(yscrollcommand=scrollbar.set)
response_text.config(state=DISABLED)
style = ttk.Style()
style.theme_use('classic')
style.configure('TButton', background='lightgray', font=('Helvetica', 10))
style.configure('B5.TButton', foreground='white', background='red', font=('Helvetica', 12, 'bold'))
root.update()
socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Connect to the server
socket_c.connect(("127.0.0.1", 49993))


# Start the Tkinter event loop
root.mainloop()
