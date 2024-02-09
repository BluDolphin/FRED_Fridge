import datetime
data = [{"Item": "", "expiry": "", "currentDate": ""}]

def start():
    data[0]["Item"] = input("Enter the item: ")
    
    expiryTime = int(input("Enter days until expiry: "))  # Convert input to int
  
    currentDate = datetime.datetime.now()  #Get current date 
    data[0]["currentDate"] = currentDate.strftime("%Y-%m-%d") #Set current date
    

    expiryDate = currentDate + datetime.timedelta(days=expiryTime) #Get expiry, expiryTime+currentDate = expiryDate
    data[0]["expiry"] = expiryDate.strftime("%Y-%m-%d") #Set expiry date
    
    print(data) #Print data
    
    while str(currentDate) < str(data[0]["expiry"]):
        currentDate = currentDate + datetime.timedelta(days=1)
        print(currentDate.strftime("%Y-%m-%d"))
        if str(currentDate) < str(data[0]["expiry"]):
            print("Item not expired")
    print("Item expired")
    
    
start()