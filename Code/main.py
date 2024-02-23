"""_summary_
this is the main file for the progam
For now going to use placeholders for SQL and for the GUI
"""
import threading
import datetime
import time

import logging
logging.basicConfig(level=logging.DEBUG)

#TEMP DATABASE 
cachedItems = [{"barcodeID": "header1", "itemName": "header2"}] #SQL - cachedItems
database = [{"barcodeID": "header1", "itemName": "header2", "dateAdded": "header3", "expiryDate": "header4", "daysLeft": "header5"}] #SQL - database

#CODE FOR FOREGROUND --------------------------------------
def mainMenu():
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


    #Placeholder for BARCODE INPUT
    #FOR NOW MANUAL INPUT
    barcodeID = input("enter barcode: ")
    
    
    #for each item in the cachedItems 
    for i in cachedItems: #SQL - get all items from cachedItems
        if i["barcodeID"] == barcodeID:
            itemName = i["itemName"] #SQL - get itemName from cachedItems
            logging.debug(f"Item found: {itemName}") #debug line
            break
        
    #Get user input for itemName if not found in cachedItems
    if itemName == "":
        itemName = input("Enter item name: ")
        cachedItems.append({"barcodeID": barcodeID, "itemName": itemName}) #SQL - add new entry to cachedItems
        logging.debug(f"{cachedItems}") #debug line
    
    
    daysLeft = int(input("Enter days until expiry: ")) #Get user input for expiryDate
    
    dateAdded = datetime.datetime.now() #Get current date
    expiryDate = dateAdded + datetime.timedelta(days=daysLeft) #Get expiryDate = dateAdded + daysLeft
    
    #Cull end of variables to just date
    dateAdded = dateAdded.strftime("%Y-%m-%d")
    expiryDate = expiryDate.strftime("%Y-%m-%d")
    
    
    logging.debug(f"itemName: {itemName} dateAdded: {dateAdded} expiryDate: {expiryDate} daysLeft: {daysLeft}") #debug line
    #SQL - add new entry to database
    database.append({"barcodeID": barcodeID, "itemName": itemName, "dateAdded": dateAdded, "expiryDate": expiryDate, "daysLeft": daysLeft}) 
    
    mainMenu()

def viewItems():
    #Placeholder for GUI and SQL
    #no point in making a command line interface for this
    #the GUI will be completely different
    for i in database:
        print(i["barcodeID"], i["itemName"], i["dateAdded"], i["daysLeft"])
        
    mainMenu()
    
#CODE FOR BACKGROUND --------------------------------------
def updateEntrys():
    exTime = 3 #number of days until pruged from database 
    yesterdate = datetime.datetime.now().strftime("%Y-%m-%d") 
    
    time.sleep(20)
    logging.debug("Background thread started")
    
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

#Initialisation -------------------------------------------

BackThread=threading.Thread(target=updateEntrys).start() #create background thread

mainMenu() #Load GUI