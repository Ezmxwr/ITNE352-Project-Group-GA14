import socket
from tkinter import *
from tkinter import ttk
import sys

# Function to handle communication with the server for option 1
def communicate_for_option1():
    socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_c.connect(("127.0.0.1", 49993))
    print("\nThe request for option 1 has been sent")
    try:
        # Send the selected option to the server
        socket_c.send('1'.encode("ascii"))

        # Receive the response from the server
        response = socket_c.recv(2048).decode('ascii')
        print("Received from server: {}".format(response))

        # Update the label text with the server response
        response_label.config(text="Server Response for Option 1: {}".format(response))

    except SystemExit:
        socket_c.close()

# Create the main window
root = Tk()

# Create Button widgets and associate them with corresponding functions
option1 = ttk.Button(root, text='Arrived flights', width=20, command=communicate_for_option1)
option1.pack(side=TOP, pady=5)

# Create a Label widget to display server responses
response_label = Label(root, text="Server Response: ")
response_label.pack(side=TOP, pady=10)

style = ttk.Style()
style.theme_use('classic')
style.configure('TButton', background='lightgray', font=('Helvetica', 10))

root.mainloop()
