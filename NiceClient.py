
import socket
from tkinter import *
from tkinter import ttk ,simpledialog ,messagebox  #simpledialog modules handles dialog boxes   
from threading import Thread
import json

# Global variables
response_data = ""
socket_c = None

def receive_data_from_server(option):
    global response_data
    while True:
        try:
            ms = socket_c.recv(20400).decode("utf-8")
            print(ms)
    
            # Update the text label with the server response
            response_text.config(state=NORMAL)
            response_text.delete('1.0', END)
            response_text.insert(END, ms )
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
        # Send the selected option to the server
        #socket_c.send(option.encode("ascii"))

        if option=='1' or option== '2'or option =='5':
            data_to_send = {'option': option, 'user_input': user_input}
            socket_c.send(json.dumps(data_to_send).encode("utf-8"))
            if option=='5':
                confirmation = messagebox.askyesno("Goodbye server", "Are you sure you want to close the client? (yes/no)")
                if not confirmation:
                     return 
                else:
                    root.destroy()
                

        if option == '3':
            # For option 3, tell the user to enter a depature ICAO code
            user_input = simpledialog.askstring( "Enter Depature IATA code","Please enter the departure IATA      :") 
            data_to_send = {'option': option, 'user_input': user_input}
            socket_c.send(json.dumps(data_to_send).encode("utf-8"))

        elif option == '4':
            # For option 4,tell the user to enter a flight number
            user_input = simpledialog.askstring("Enter Flight IATA code ", "Please enter the flight IATA code:")
            data_to_send = {'option': option, 'user_input': user_input}
            socket_c.send(json.dumps(data_to_send).encode("utf-8"))
      
        # to isplay the user input in a label
        user_input_label.config(text="User Input: {}".format(user_input))

        # Start a thread to continuously receive data from the server
        #look the why file
        receive_thread = Thread(target=receive_data_from_server, args=(option,), daemon=True)
        receive_thread.start()          
        
       
    except Exception as e:
        print("Error communicating with the server:", e)

# Create the main window

root = Tk()

root.title("Flight Information Client")
# Create Button widgets and associate them with corresponding functions
option1 = ttk.Button(root, text='Arrived flights', width=30, command=lambda: communicate_with_server('1',None))
option1.pack(side=TOP, pady=5)
option2 = ttk.Button(root, text='Delayed flights', width=30, command=lambda: communicate_with_server('2',None))
option2.pack(side=TOP, pady=5)
option3 = ttk.Button(root, text='All flights from a specific city', width=30,command=lambda: communicate_with_server('3'))
option3.pack(side=TOP, pady=5)
option4 = ttk.Button(root, text='Details of a particular flight', width=30,command=lambda: communicate_with_server('4'))
option4.pack(side=TOP, pady=5)
option5 = ttk.Button(root, text='Quit', style='B5.TButton', command=lambda: communicate_with_server('5') )
option5.pack(side='top', anchor=SE, padx=10, pady=10)

# Add a label to display the entered input
user_input_label = Label(root, text="", font=('Helvetica', 12))
user_input_label.pack(side=TOP, pady=5)
organiRight = Label(root,width=3, text='',state=DISABLED)
organiRight.pack(side='right')
organiLeft = Label(root,width=3, text='',state=DISABLED)
organiLeft.pack(side='left')
# Create a Text widget with scroller to display server responses
response_frame = Frame(root)
response_frame.pack(side=TOP, pady=10)
response_text = Text(response_frame, wrap=WORD, width=90, height=30)
response_text.pack(side=LEFT, pady=10)
scrollbar = Scrollbar(response_frame, command=response_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
response_text.config(yscrollcommand=scrollbar.set)
response_text.config(state=DISABLED)

style = ttk.Style()
style.theme_use('classic')
style.configure('TButton', background='lightgray', font=('Helvetica', 10))
style.configure('B5.TButton', foreground='white', background='red', font=('Helvetica', 12, 'bold'))
root.update()

# Connect to the server
socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_c.connect(("127.0.0.1", 49993))


# Start the Tkinter event loop
root.mainloop()




