import tkinter as tk
import sqlite3
from time import strftime, localtime
import cv2
from PIL import Image, ImageTk

# Function to update the time and date
def update_time_and_date():
    time_str = strftime('%H:%M %p', localtime())
    date_str = strftime('%A, %B %d, %Y', localtime())
    time_label.config(text=time_str)
    date_label.config(text=date_str)
    time_label.after(1000, update_time_and_date)  # Update time every second

# Function to handle register button click event
def register_click():
    root.withdraw()  # Hide the main window
    register_window.deiconify()  # Show the register window

# Function to handle view button click event
def view_click():
    root.withdraw()  # Hide the main window
    view_window.deiconify()  # Show the view window
    display_database_contents()

# Function to display database contents on the view page
def display_database_contents():
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sample_table")
    rows = cursor.fetchall()
    conn.close()

    for row_index, row in enumerate(rows):
        for col_index, col_value in enumerate(row):
            tk.Label(view_window, text=col_value, font=('calibri', 12), bg='white', fg='black').grid(row=row_index, column=col_index, padx=10, pady=5)

# Function to go back to the main window from the view page
def back_to_main_from_view():
    view_window.withdraw()  # Hide the view window
    root.deiconify()  # Show the main window

# Function to go back to the main window from the register page
def back_to_main_from_register():
    register_window.withdraw()  # Hide the register window
    root.deiconify()  # Show the main window

# Function to go to data entry page from the register page
def data_entry_click():
    register_window.withdraw()  # Hide the register window
    data_entry_window.deiconify()  # Show the data entry window

# Function to go back to the register page from the data entry page
def back_to_register_from_data_entry():
    data_entry_window.withdraw()  # Hide the data entry window
    register_window.deiconify()  # Show the register window

# Function to continue from data entry page
def continue_data_entry():
    # Placeholder function for now
    pass

# Function to open camera input
def open_camera():
    global cap
    camera_window.deiconify()  # Show the camera window
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Failed to open camera")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
        camera_label.update()  # Update the camera feed in the GUI
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break
    
    cap.release()
    camera_window.withdraw()  # Hide the camera window

# Function to close camera input
def close_camera():
    global cap
    if cap:
        cap.release()  # Release the camera capture
    cv2.destroyAllWindows()  # Close any remaining camera windows
    camera_window.withdraw()  # Hide the camera window

# Create the main application window
root = tk.Tk()
root.title("Clock GUI")

# Set the window to fullscreen
root.attributes('-fullscreen', True)

# Set background color to white
root.configure(bg='white')

# Create a label widget to display time
time_label = tk.Label(root, font=('calibri', 60, 'bold'), bg='white', fg='black')
time_label.pack(anchor='center', pady=(150, 20))  # Move down the time label

# Create a label widget to display date
date_label = tk.Label(root, font=('calibri', 30), bg='white', fg='black')
date_label.pack(anchor='center', pady=20)  # Move down the date label

# Update the time and date initially
update_time_and_date()

# Create a frame for the buttons
button_frame = tk.Frame(root, bg='white')
button_frame.pack(expand=True)

# Create a register button widget with larger text
register_button = tk.Button(button_frame, text="Register", command=register_click, width=20, height=5, font=('calibri', 24, 'bold'), borderwidth=3)
register_button.pack(side='left', padx=50)  # Increase padding for larger buttons

# Create a view button widget with larger text
view_button = tk.Button(button_frame, text="View", command=view_click, width=20, height=5, font=('calibri', 24, 'bold'), borderwidth=3)
view_button.pack(side='left', padx=50)  # Increase padding for larger buttons

# Create a new window for the register page
register_window = tk.Toplevel(root)
register_window.title("Register Page")
register_window.attributes('-fullscreen', True)  # Set register window to fullscreen
register_window.configure(bg='white')

# Create a label for the register page
register_label = tk.Label(register_window, text="This is the register page", font=('calibri', 24), bg='white', fg='black')
register_label.pack(pady=50)

# Create a button to open camera from the register page
camera_button = tk.Button(register_window, text="Open Camera", command=open_camera, width=15, height=3, font=('calibri', 18, 'bold'), borderwidth=3)
camera_button.pack(pady=50)  # Increase padding for the camera button

# Create a new window for the camera feed
camera_window = tk.Toplevel(root)
camera_window.title("Camera Feed")
camera_window.attributes('-fullscreen', True)  # Set camera window to fullscreen
camera_window.configure(bg='white')

# Create label for camera feed
camera_label = tk.Label(camera_window, bg='white')
camera_label.pack()

# Hide the camera window initially
camera_window.withdraw()

# Create a button to close the camera
close_camera_button = tk.Button(camera_window, text="Close Camera", command=close_camera, font=('calibri', 18), borderwidth=3)
close_camera_button.pack()

# Create a button to go to data entry page from the register page
data_entry_button = tk.Button(register_window, text="Data Entry", command=data_entry_click, width=15, height=3, font=('calibri', 18, 'bold'), borderwidth=3)
data_entry_button.pack()

# Create a button to go back to the main window from the register page
back_button_register = tk.Button(register_window, text="Back to Menu", command=back_to_main_from_register, font=('calibri', 24, 'bold'), borderwidth=3)
back_button_register.place(relx=1.0, rely=0.0, anchor='ne')  # Place the button in the top right corner

# Hide the register window initially
register_window.withdraw()

# Create a new window for the data entry page
data_entry_window = tk.Toplevel(root)
data_entry_window.title("Data Entry Page")
data_entry_window.attributes('-fullscreen', True)  # Set data entry window to fullscreen
data_entry_window.configure(bg='white')

# Create a label for the data entry page
data_entry_label = tk.Label(data_entry_window, text="Data Entry", font=('calibri', 24), bg='white', fg='black')
data_entry_label.pack(pady=50)

# Create input field for product name
product_name_label = tk.Label(data_entry_window, text="Product Name:", font=('calibri', 18), bg='white', fg='black')
product_name_label.pack(pady=(40, 10))
product_name_entry = tk.Entry(data_entry_window, font=('calibri', 16), bd=2, relief=tk.GROOVE)
product_name_entry.pack(pady=10)

# Create input field for expiry date
expiry_date_label = tk.Label(data_entry_window, text="Expiry Date:", font=('calibri', 18), bg='white', fg='black')
expiry_date_label.pack(pady=10)
expiry_date_entry = tk.Entry(data_entry_window, font=('calibri', 16), bd=2, relief=tk.GROOVE)
expiry_date_entry.pack(pady=20)

# Create a button to continue from data entry page
continue_button = tk.Button(data_entry_window, text="Continue", command=continue_data_entry, font=('calibri', 18), borderwidth=3)
continue_button.pack()

# Create a button to go back to the register page from the data entry page
back_button_data_entry = tk.Button(data_entry_window, text="Back to Register", command=back_to_register_from_data_entry, font=('calibri', 18), borderwidth=3)
back_button_data_entry.place(relx=1.0, rely=0.0, anchor='ne')  # Place the button in the top right corner

# Hide the data entry window initially
data_entry_window.withdraw()

# Create a new window for the view page
view_window = tk.Toplevel(root)
view_window.title("View Page")
view_window.attributes('-fullscreen', True)  # Set view window to fullscreen
view_window.configure(bg='white')

# Create a button to go back to the main window from the view page
back_button_view = tk.Button(view_window, text="Back to Menu", command=back_to_main_from_view, font=('calibri', 18), borderwidth=3)
back_button_view.place(relx=1.0, rely=0.0, anchor='ne')  # Place the button in the top right corner

# Run the Tkinter event loop
root.mainloop()