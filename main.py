"""_summary_
this is the main file for the progam
For now going to use placeholders for SQL and for the GUI
"""
import datetime
import logging
logging.basicConfig(level=logging.DEBUG)

#TEMP DATABASE 
cachedItems = [{"barcodeID": "header1", "itemName": "header2"}] #SQL - cachedItems
database = [{"barcodeID": "header1", "itemName": "header2", "dateAdded": "header3", "expiryDate": "header4", "daysLeft": "header5"}] #SQL - database

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
    database.append({"barcodeID": barcodeID, "itemName": itemName, "dateAdded": dateAdded, "expiryDate": expiryDate, "daysLeft": daysLeft}) #SQL - add new entry to database
    
    mainMenu()

def viewItems():
    print("Viewing items")
    # Placeholder for SQL
    mainMenu()
    
mainMenu()