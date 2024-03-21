"""_summary_
this is the main file for the progam
For now going to use placeholders for SQL and for the GUI
"""
import logging
logging.basicConfig(level=logging.DEBUG)

import json
import os
import threading
import datetime
import time

import cv2
from pyzbar import pyzbar

#Try to setup the pi camera if running on pi
try:
    from picamera2 import Picamera2
    picam2 = Picamera2()         
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
    picam2.configure(camera_config)
except:
    logging.debug("Not running on pi")


#LOAD DATA ------------------------------------------------------------
logging.debug("Loading data")

#If file exist then load data
if os.path.exists("FRED-Data.json"): 
    with open("FRED-Data.json", "rt") as file:
        data = json.load(file)
        cachedItems = data["cachedItems"]
        database = data["database"]    
        
#If file does not exist then create new file  
else:
    logging.debug("File not found, creating new file")
    cachedItems = [{"barcodeID": "header1", "itemName": "header2"}] #SQL - cachedItems
    database = [{"barcodeID": "barcodeID", "itemName": "itemName", "dateAdded": "dateAdded", "expiryDate": "expiryDate", "daysLeft": "daysLeft"}] #SQL - database

    with open("FRED-Data.json", "wt") as file:
        json.dump({"cachedItems": cachedItems, "database": database}, file)

logging.debug(f"cachedItems: {cachedItems}")
logging.debug(f"database: {database}")

#PROGRAM START ========================================================
#CODE FOR FOREGROUND --------------------------------------------------
def mainMenu(): 
    logging.debug("Saving data")
    with open("FRED-Data.json", "wt") as file: 
        json.dump({"cachedItems": cachedItems, "database": database}, file) #Save data to file
        
    print("Welcome to the main menu")
    print("1. Add new item")
    print("2. View items")
    print("q. Quit")
    if (choice := input(">")) == "1":
        addNewItem()
    elif choice == "2":
        viewItems()
    elif choice == "q":
        quit()
    else:
        print("Invalid input")
        mainMenu()
       
def addNewItem():
    #variables for this function
    barcodeID = ""
    itemName = ""
    dateAdded = ""
    expiryDate = ""
    daysLeft = ""
    

    # Get barcode from user
    # Will try to use pi camera to get barcode
    # If not on the pi then manual input
    try :
        barcodeID = getBarcode() # Call function to get barcode
    except:
        barcodeID = input("enter barcode: ")
    
    # check for item name in cachedItems
    # For each item in the cachedItems 
    for i in cachedItems: #SQL - get all items from cachedItems
        if i["barcodeID"] == barcodeID: # SQL - if barcodeID is found 
            itemName = i["itemName"] #SQL - get itemName attached to barcodeID
            logging.debug(f"Item found: {itemName}") # debug line
            break
        
        
    #Get user input for itemName if not found in cachedItems
    if itemName == "":
        itemName = input("Enter item name: ")
        cachedItems.append({"barcodeID": barcodeID, "itemName": itemName}) #SQL - add new entry to cachedItems
        logging.debug(f"{cachedItems}") #debug line
    
    
    daysLeft = int(input("Enter days until expiry: ")) #Get user input for expiryDate
    
    dateAdded = datetime.datetime.now() #Get current date
    expiryDate = dateAdded + datetime.timedelta(days=daysLeft) #Get expiryDate = dateAdded + daysLeft
    
    #Cull end of date variables to just date
    dateAdded = dateAdded.strftime("%Y-%m-%d")
    expiryDate = expiryDate.strftime("%Y-%m-%d")
    
    
    logging.debug(f"itemName: {itemName} dateAdded: {dateAdded} expiryDate: {expiryDate} daysLeft: {daysLeft}") #debug line
    #SQL - add new entry to database
    database.append({"barcodeID": barcodeID, "itemName": itemName, "dateAdded": dateAdded, "expiryDate": expiryDate, "daysLeft": daysLeft}) 
    
    mainMenu()

def viewItems():
    # Placeholder for GUI and SQL
    # No point in making a command line interface for this
    # The GUI will be completely different
    for i in database:
        print(i["barcodeID"], i["itemName"], i["dateAdded"], i["daysLeft"])
        
    mainMenu()
    
#Code FOR BARCODE DETECTION/ READING ----------------------------------

#WILL ONLY WORK ON THE PI
def getBarcode():
    # Take an image every second and read data
    while True:
        picam2.start()
        picam2.capture_file("Barcode.jpg")
        
        # Read the image from the provided file path
        image = cv2.imread("Barcode.jpg")
        # Decode barcodes from the image using pyzbar
        barcodes = pyzbar.decode(image)
        # Iterate through detected barcodes and extract data from the barcode 
        for barcode in barcodes:
            # uses UTF-8 encoding
            barcodeData = barcode.data.decode("utf-8")
            logging.debug(f"Barcode: {barcodeData}")
            if barcodeData.isdigit():
                picam2.stop()
                return(barcodeData)
    
        time.sleep(1)
    
#CODE FOR BACKGROUND --------------------------------------------------
def updateEntrys():
    logging.debug("Background thread started")
    exTime = 3 #number of days until pruged from database 
    yesterdate = datetime.datetime.now().strftime("%Y-%m-%d") 
    
    time.sleep(20)
    
    while True:
        currentDate = datetime.datetime.now()
        
        if currentDate.strftime("%Y-%m-%d") == yesterdate:
            time.sleep(600) #sleep for 10 mins
            continue #loop
        
        for i in database:
            if i["daysLeft"] != "header5":#TEMPORARY AS SQL WONT NEED THIS - REMOVE WHEN SQL IS IMPLEMENTED
                
                
                expiryDate = i["expiryDate"]
                
                #find the difference between the expiry date and the current date
                currentDate = currentDate.strftime("%Y-%m-%d") 
                daysLeft = (datetime.datetime.strptime(expiryDate, "%Y-%m-%d") - datetime.datetime.strptime(currentDate, "%Y-%m-%d")).days
                
                if daysLeft < -exTime: #If daysLeft is less than exTime then remove from database
                    database.remove(i) #delete entry 
                    logging.debug(f"Item: {i['itemName']} removed - days left expired")
                    continue
                else:                
                    i["daysLeft"] = daysLeft
                    logging.debug(f"Item: {i['itemName']} daysLeft: {daysLeft}")
                    logging.debug(f"{i}")
                
                logging.debug("Next item.....")
        yesterdate = currentDate

#Initialisation -------------------------------------------------------

BackThread=threading.Thread(target=updateEntrys).start() #create background thread
mainMenu() #Load GUI