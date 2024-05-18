import tkinter as tk
from time import strftime, localtime
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox
import threading
import logging
import json
import os
import datetime
from tkinter import Scrollbar

try:
    from picamera2 import PiCamera
    from picamera2.array import PiRGBArray
    from pyzbar import pyzbar
    PICAMERA_AVAILABLE = True
except ImportError:
    PICAMERA_AVAILABLE = False

keyboard_window = None  # Reference to the keyboard window

# Global variables
picam2 = None  # Declare picamera instance globally
rawCapture = None  # Declare PiRGBArray instance globally
camera_window = None  # Reference to the camera window

# Load data ------------------------------------------------------------
logging.debug("Loading data")

# If file exists then load data
if os.path.exists("FRED-Data.json"):
    with open("FRED-Data.json", "rt") as file:
        data = json.load(file)
        cachedItems = data["cachedItems"]
        database = data["database"]
# If file does not exist then create new file  
else:
    logging.debug("File not found, creating new file")
    cachedItems = [{"barcodeID": "header1", "itemName": "header2"}]  # SQL - cachedItems
    database = [{"barcodeID": "barcodeID", "itemName": "itemName", "dateAdded": "dateAdded", "expiryDate": "expiryDate", "daysLeft": "daysLeft"}]  # SQL - database

    with open("FRED-Data.json", "wt") as file:
        json.dump({"cachedItems": cachedItems, "database": database}, file)

logging.debug(f"cachedItems: {cachedItems}")
logging.debug(f"database: {database}")

# Save data ------------------------------------------------------------
def saveData():  # Save data function
    logging.debug("Saving data")
    with open("FRED-Data.json", "wt") as file:
        json.dump({"cachedItems": cachedItems, "database": database}, file)  # Save data to file

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
    open_camera()  # Open the camera when register button is clicked

# Function to handle view button click event
def view_click():
    root.withdraw()  # Hide the main window
    view_window.deiconify()  # Show the view window
    display_database_contents()  # Display database contents

def display_database_contents():
    def delete_item(index):
        del database[index]
        saveData()
        display_database_contents()  # Refresh the view after deletion

    for widget in view_window.winfo_children():
        widget.destroy()

    # Create a frame to contain the database headings
    headings_frame = tk.Frame(view_window, bg='white', bd=2, relief=tk.SOLID, width=900)  # Adjusted width
    headings_frame.pack(pady=(150, 10), padx=20)  # Adjust padding as needed

    # Add headings for database
    headings = ["Barcode ID", "Item Name", "Date Added", "Expiry Date", "Days Left"]
    for col_index, heading in enumerate(headings):
        label = tk.Label(headings_frame, text=heading, font=('calibri', 12, 'bold'), bg='white', fg='black', bd=1, relief=tk.SOLID, width=18)
        label.grid(row=0, column=col_index, padx=2, pady=2, sticky='nsew')  # Adjust width of labels
       
    # Create a frame to contain the database content with fixed size
    database_frame = tk.Frame(view_window, bg='white', bd=2, relief=tk.SOLID, width=900, height=500)  # Adjusted width and height
    database_frame.pack(pady=(10, 20), padx=20)  # Adjust padding as needed

    # Create a canvas to contain the database content
    canvas = tk.Canvas(database_frame, bg='white', width=880, height=480)  # Adjusted width
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar for vertical scrolling
    scrollbar = Scrollbar(database_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the actual content of the database
    content_frame = tk.Frame(canvas, bg='white')  # No need to specify width and height
    canvas.create_window((0, 0), window=content_frame, anchor='nw')

    # Add data rows
    for row_index, row in enumerate(database, start=1):  # Start with row 1 after headings
        for col_index, col_value in enumerate(row.values()):
            tk.Label(content_frame, text=col_value, font=('calibri', 12), bg='white', fg='black', bd=1, relief=tk.SOLID, width=18).grid(row=row_index, column=col_index, padx=2, pady=2, sticky='nsew')  # Adjust width of labels

        delete_button = tk.Button(content_frame, text="Delete", command=lambda idx=row_index - 1: delete_item(idx), font=('calibri', 10), bg='red', fg='white', width=10)  # Adjust width of button
        delete_button.grid(row=row_index, column=len(row), padx=2, pady=2, sticky='e')  # Reduced padding

    # Update scroll region to make the scrollbar work
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Bind mousewheel to the canvas for scrolling
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    # Create a button to go back to the main window from the view page
    back_button_view = tk.Button(view_window, text="Back to Menu", command=back_to_main_from_view, font=('calibri', 18), borderwidth=3)
    back_button_view.pack(pady=(20, 20))  # Adjust padding if necessary


# Function to go back to the main window from the view page
def back_to_main_from_view():
    view_window.withdraw()  # Hide the view window
    root.deiconify()  # Show the main window

# Function to clear the entry fields
def clear_entry_fields():
    product_name_entry.delete(0, tk.END)
    expiry_date_entry.delete(0, tk.END)

# Function to go to data entry page from the register page
def data_entry_click():
    clear_entry_fields()  # Clear entry fields
    data_entry_window.deiconify()  # Show the data entry window

# Function to go back to the main menu from the data entry page
def back_to_main_menu_from_data_entry():
    data_entry_window.withdraw()  # Hide the data entry window
    close_keyboard()  # Close the keyboard window
    root.deiconify()  # Show the main window
    clear_entry_fields()  # Clear entry fields

# Function to continue from data entry page
def continue_data_entry():
    close_keyboard()  # Close the keyboard window

    # Retrieve entered data
    itemName = product_name_entry.get()
    daysLeft = int(expiry_date_entry.get())

    # Generate barcodeID (This should be replaced by actual barcode scanning logic)
    barcodeID = "1234567890"  # Placeholder

    # Get current date and calculate expiry date
    dateAdded = datetime.datetime.now()
    expiryDate = dateAdded + datetime.timedelta(days=daysLeft)

    # Cull end of date variables to just date
    dateAdded = dateAdded.strftime("%Y-%m-%d")
    expiryDate = expiryDate.strftime("%Y-%m-%d")

    # Check for item name in cachedItems
    for i in cachedItems:  # SQL - get all items from cachedItems
        if i["barcodeID"] == barcodeID:  # SQL - if barcodeID is found
            itemName = i["itemName"]  # SQL - get itemName attached to barcodeID
            logging.debug(f"Item found: {itemName}")  # debug line
            break

    # Get user input for itemName if not found in cachedItems
    if itemName == "":
        itemName = product_name_entry.get()
        cachedItems.append({"barcodeID": barcodeID, "itemName": itemName})  # SQL - add new entry to cachedItems
        logging.debug(f"{cachedItems}")  # debug line

    logging.debug(f"itemName: {itemName} dateAdded: {dateAdded} expiryDate: {expiryDate} daysLeft: {daysLeft}")  # debug line
    # SQL - add new entry to database
    database.append({"barcodeID": barcodeID, "itemName": itemName, "dateAdded": dateAdded, "expiryDate": expiryDate, "daysLeft": daysLeft})

    # Save data to JSON file
    saveData()

    # Hide data entry window and show the camera window again
    data_entry_window.withdraw()
    open_camera()

    # Retrieve entered data
    itemName = product_name_entry.get()
    daysLeft = int(expiry_date_entry.get())

    # Generate barcodeID (This should be replaced by actual barcode scanning logic)
    barcodeID = "1234567890"  # Placeholder

    # Get current date and calculate expiry date
    dateAdded = datetime.datetime.now()
    expiryDate = dateAdded + datetime.timedelta(days=daysLeft)

    # Cull end of date variables to just date
    dateAdded = dateAdded.strftime("%Y-%m-%d")
    expiryDate = expiryDate.strftime("%Y-%m-%d")

    # Check for item name in cachedItems
    for i in cachedItems:  # SQL - get all items from cachedItems
        if i["barcodeID"] == barcodeID:  # SQL - if barcodeID is found
            itemName = i["itemName"]  # SQL - get itemName attached to barcodeID
            logging.debug(f"Item found: {itemName}")  # debug line
            break

    # Get user input for itemName if not found in cachedItems
    if itemName == "":
        itemName = product_name_entry.get()
        cachedItems.append({"barcodeID": barcodeID, "itemName": itemName})  # SQL - add new entry to cachedItems
        logging.debug(f"{cachedItems}")  # debug line

    logging.debug(f"itemName: {itemName} dateAdded: {dateAdded} expiryDate: {expiryDate} daysLeft: {daysLeft}")  # debug line
    # SQL - add new entry to database
    database.append({"barcodeID": barcodeID, "itemName": itemName, "dateAdded": dateAdded, "expiryDate": expiryDate, "daysLeft": daysLeft})

    # Save data to JSON file
    saveData()

    # Hide data entry window and show the camera window again
    data_entry_window.withdraw()
    open_camera()

def barcode_reader():
    global picam2, rawCapture
    try:
        picam2 = PiCamera()
        picam2.resolution = (640, 480)
        picam2.framerate = 32
        rawCapture = PiRGBArray(picam2, size=(640, 480))
        
        for frame in picam2.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
            
            barcodes = pyzbar.decode(image)
            for barcode in barcodes:
                barcodeData = barcode.data.decode("utf-8")
                logging.debug(f"Barcode: {barcodeData}")
                if barcodeData.isdigit():
                    rawCapture.truncate(0)
                    picam2.close()
                    camera_window.withdraw()
                    product_name_entry.insert(0, "Detected Item")  # Placeholder
                    expiry_date_entry.insert(0, "10")  # Placeholder
                    data_entry_click()
                    return  # Remove this line to prevent redundant function call

            rawCapture.truncate(0)
    except Exception as e:
        logging.error(f"Error in barcode reader: {e}")
        messagebox.showerror("Error", "Camera initialization failed. Please enter data manually.")
        close_camera()  # Ensure the data entry window can still be accessed

# Function to open camera input
def open_camera():
    global picam2, rawCapture

    camera_window.deiconify()  # Show the camera window
    threading.Thread(target=barcode_reader, daemon=True).start()

# Function to close camera input
def close_camera():
    global picam2, rawCapture, camera_window
    if picam2:
        picam2.close()  # Close PiCamera
    if rawCapture:
        rawCapture.close()  # Close PiRGBArray
    if camera_window:
        camera_window.withdraw()  # Hide the camera window
    data_entry_click()  # Open the data entry window

def open_keyboard(entry):
    global keyboard_window
    if keyboard_window is None or not keyboard_window.winfo_exists():
        keyboard_window = tk.Toplevel()
        keyboard_window.title("On-Screen Keyboard")
        keyboard_window.attributes('-topmost', True)
        keyboard_window.overrideredirect(True)

        keys = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']]

        button_width = 10  # Increased width
        button_height = 4  # Adjusted height

        for row_idx, row in enumerate(keys):
            row_frame = tk.Frame(keyboard_window)
            row_frame.grid(row=row_idx, column=0, pady=2)
            for col_idx, key in enumerate(row):
                btn = tk.Button(row_frame, text=key, width=button_width, height=button_height, command=lambda k=key: entry.insert(tk.END, k))
                btn.grid(row=0, column=col_idx, padx=2, pady=2)

        bottom_frame = tk.Frame(keyboard_window)
        bottom_frame.grid(row=3, column=0, pady=2)
        
        space_btn = tk.Button(bottom_frame, text='Space', width=button_width * 5, height=button_height, command=lambda: entry.insert(tk.END, ' '))
        space_btn.grid(row=0, column=0, columnspan=5, padx=2, pady=2)

        backspace_btn = tk.Button(bottom_frame, text='Backspace', width=button_width * 5, height=button_height, command=lambda: entry.delete(len(entry.get()) - 1, tk.END))
        backspace_btn.grid(row=0, column=5, columnspan=5, padx=2, pady=2)

        # Create a button to close the keyboard
        close_keyboard_button = tk.Button(keyboard_window, text="✖", font=('calibri', 18), bg='white', command=close_keyboard, fg='red')
        close_keyboard_button.grid(row=3, column=9, columnspan=2, padx=2, pady=2)  # Position the close button


        # Calculate the position of the keyboard window relative to the first input box
        entry_x = entry.winfo_rootx()
        entry_y = entry.winfo_rooty()
        entry_height = entry.winfo_height()

        keyboard_height = keyboard_window.winfo_reqheight()

        keyboard_x = entry_x
        keyboard_y = entry_y - keyboard_height - entry_height - 10  # Adjust vertical position

        # Set the position of the keyboard window
        keyboard_window.geometry(f"+{keyboard_x}+{keyboard_y}")

        # Lower the keyboard on the screen
        keyboard_window.update_idletasks()
        window_width = keyboard_window.winfo_reqwidth()
        window_height = keyboard_window.winfo_reqheight()
        position_right = int(keyboard_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(keyboard_window.winfo_screenheight() / 2 - window_height / 2) + 150  # Adjust vertical position
        keyboard_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

# Function to close the on-screen keyboard
def close_keyboard():
    global keyboard_window
    if keyboard_window is not None and keyboard_window.winfo_exists():
        keyboard_window.destroy()

def updateEntrys():
    logging.debug("Background thread started")
    exTime = 3  # number of days until purged from database
    currentDate = datetime.datetime.now().strftime("%Y-%m-%d")  # Get current date

    while True:
        # Update currentDate in each iteration
        newDate = datetime.datetime.now().strftime("%Y-%m-%d")

        if newDate != currentDate:
            currentDate = newDate  # Update currentDate if it's a new day

            for i in database:
                if i["daysLeft"] != "header5":  # TEMPORARY AS SQL WONT NEED THIS - REMOVE WHEN SQL IS IMPLEMENTED
                    expiryDate = i["expiryDate"]
                    # find the difference between the expiry date and the current date
                    daysLeft = (datetime.datetime.strptime(expiryDate, "%Y-%m-%d") - datetime.datetime.strptime(currentDate, "%Y-%m-%d")).days

                    if daysLeft < -exTime:  # If daysLeft is less than exTime then remove from database
                        database.remove(i)  # delete entry
                        logging.debug(f"Item: {i['itemName']} removed - days left expired")
                        continue
                    else:
                        i["daysLeft"] = daysLeft
                        logging.debug(f"Item: {i['itemName']} daysLeft: {daysLeft}")
                        logging.debug(f"{i}")

                    logging.debug("Next item.....")

            saveData()
        time.sleep(86400)  # sleep for 24 hours

# Note: You may need to adjust the sleep duration (86400 seconds = 24 hours) depending on your requirements.

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
# Update time and date
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

# Create a new window for the camera feed
camera_window = tk.Toplevel(root)
camera_window.title("Camera Feed")
camera_window.attributes('-fullscreen', True)  # Set camera window to fullscreen
camera_window.configure(bg='white')

# Create label for camera feed
camera_label = tk.Label(camera_window, bg='white')
camera_label.pack(anchor='center', expand=True)  # Centralize the camera feed label

# Create a button to close the camera
close_camera_button = tk.Button(camera_window, text="Close Camera", command=close_camera, font=('calibri', 18), borderwidth=3)
close_camera_button.pack(pady=10)  # Center the button below the camera

# Hide the camera window initially
camera_window.withdraw()

# Create a new window for the data entry page
data_entry_window = tk.Toplevel(root)
data_entry_window.title("Data Entry Page")
data_entry_window.attributes('-fullscreen', True)  # Set data entry window to fullscreen
data_entry_window.configure(bg='white')

# Create a label for the data entry page
data_entry_label = tk.Label(data_entry_window, text="Data Entry", font=('calibri', 24), bg='white', fg='black')
data_entry_label.pack(pady=(50, 10))  # Increased top padding

# Create input field for product name
product_name_label = tk.Label(data_entry_window, text="Product Name:", font=('calibri', 18), bg='white', fg='black')
product_name_label.pack(pady=(50, 10))  # Increased top padding

product_name_entry = tk.Entry(data_entry_window, font=('calibri', 16), bd=2, relief=tk.GROOVE)
product_name_entry.pack(pady=10)

# Bind the on-screen keyboard to the product name entry field
product_name_entry.bind("<Button-1>", lambda event: open_keyboard(product_name_entry))

# Create input field for expiry date
expiry_date_label = tk.Label(data_entry_window, text="Expiry Date:", font=('calibri', 18), bg='white', fg='black')
expiry_date_label.pack(pady=10)

expiry_date_entry = tk.Entry(data_entry_window, font=('calibri', 16), bd=2, relief=tk.GROOVE)
expiry_date_entry.pack(pady=10)

# Bind the on-screen keyboard to the expiry date entry field
expiry_date_entry.bind("<Button-1>", lambda event: open_keyboard(expiry_date_entry))

# Create a button to continue from data entry page
continue_button = tk.Button(data_entry_window, text="Continue", command=continue_data_entry, font=('calibri', 18), borderwidth=3)
continue_button.pack(pady=50)  # Increased top padding

# Create a button to go back to the main menu from the data entry page
back_button_data_entry = tk.Button(data_entry_window, text="Back to Menu", command=back_to_main_menu_from_data_entry, font=('calibri', 18), borderwidth=3)
back_button_data_entry.place(relx=1.0, rely=1.0, anchor='se')  # Place the button in the bottom right corner

# Hide the data entry window initially
data_entry_window.withdraw()

# Create a new window for the view page
view_window = tk.Toplevel(root)
view_window.title("View Page")
view_window.attributes('-fullscreen', True)  # Set view window to fullscreen
view_window.configure(bg='white')

# Create a button to go back to the main window from the view page
back_button_view = tk.Button(view_window, text="Back to Menu", command=back_to_main_from_view, font=('calibri', 18), borderwidth=3)
back_button_view.place(relx=1.0, rely=1.0, anchor='se')  # Place the button in the bottom right corner

# Hide the view window initially
view_window.withdraw()

# Run the Tkinter event loop
root.mainloop()
