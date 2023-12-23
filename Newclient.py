import socket
from tkinter import *
from tkinter import ttk


# Function to handle communication with the server for option 1
def communicate_for_option1():
    socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_c.connect(("127.0.0.1", 49993))
    print("\nThe request for option 1 has been sent")
    try:
        # Send the selected option to the server
        socket_c.send('1'.encode("ascii"))

        # Receive the response from the server
        response_data = socket_c.recv(2048).decode('ascii')
        print("Received from server: {}".format(response_data))

        # Update the text label with the server response
        response_text.config(state=NORMAL) #The state option => the widget becomes editable, meaning you can insert or delete text
        response_text.delete('1.0', END)# to clears the widget after each chose
        response_text.insert(END, "Server Response for Option 1:\n")
        # Parse and display the information in a structured way
        try:
            response_list = eval(response_data) 
            for item in response_list:
                response_text.insert(END, "\n===\n")
                for key, value in item.items():
                    response_text.insert(END, "{}: {}\n".format(key, value))
        except Exception as e: 
            response_text.insert(END, "Error parsing server response: {}\n".format(e)) #Error Handling
        
        response_text.config(state=DISABLED)

    except SystemExit:
        socket_c.close()


# Function to handle communication with the server for option 2
def communicate_for_option2():
    print("just fot testing option 2")

# Create the main window
root = Tk()
root.title("Flight Information Client")

# Create Button widgets and associate them with corresponding functions
option1 = ttk.Button(root, text='Arrived flights', width=20, command=communicate_for_option1)
option1.pack(side=TOP, pady=5)
option2 = ttk.Button(root, text='Delayed flights', width=20, command=communicate_for_option2)
option2.pack(side=TOP, pady=5)
option3 = ttk.Button(root, text='All flights from a specific city', width=30)
option3.pack(side=TOP, pady=5)
option4 = ttk.Button(root, text='Details of a particular flight', width=30)
option4.pack(side=TOP, pady=5)
option5 = ttk.Button(root, text='Quit', style='B5.TButton',command=root.destroy) #, command=root.destroy this whats make it close
option5.pack(side=RIGHT, anchor=SE, padx=10, pady=10)  # Add padding and place in the bottom-right corner

# Create a Text widget to display server responses
response_text = Text(root, wrap=WORD, width=60, height=20)
response_text.pack(side=TOP, pady=10)
response_text.config(state=DISABLED)

style = ttk.Style()
style.theme_use('classic')
style.configure('TButton', background='lightgray', font=('Helvetica', 10))
style.configure('B5.TButton', foreground='white', background='red', font=('Helvetica', 12, 'bold'))

root.mainloop()
