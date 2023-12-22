from tkinter import *
from tkinter import ttk

# Create the main window
root = Tk()

# Create a Button widget and pack it into the window
option1 = ttk.Button(root, text='Arrived flights', width=20)
option1.pack(side=TOP, pady=5)
option2 = ttk.Button(root, text='Delayed flights', width=20)
option2.pack(side=TOP, pady=5)
option3 = ttk.Button(root, text='All flights from a specific city', width=30)
option3.pack(side=TOP, pady=5)
option4 = ttk.Button(root, text='Details of a particular flight', width=30)
option4.pack(side=TOP, pady=5)
option5 = ttk.Button(root, text='Quit', style='B5.TButton', command=root.destroy) #, command=root.destroy this whats make it close
option5.pack(side=RIGHT, anchor=SE, padx=10, pady=10)  # Add padding and place in the bottom-right corner

# to change the theme
style = ttk.Style()
style.theme_use('classic')
style.configure('TButton', background='lightgray', font=('Helvetica', 10))
style.configure('B5.TButton', foreground='white', background='red', font=('Helvetica', 12, 'bold'))

# Start the Tkinter event loop
root.mainloop()
