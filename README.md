# FRED - Food Reminder for Expiry Dates  
FRED is a small device wich will assist users in meal planning and preventing food waste 

The user will present the barcodes of food items to FRED, where the ID will be recored along with the item name(user input), the current date, and how many days until expiry(user input).
This data will be stored into an SQL database.

For example:
| barcodeID  | itemName | dateAdded | expiryDate | daysLeft |
| ---------- | -------- | --------- | ---------- | -------- |
|  48136481  |   Steak  |  18/02/24 |  24/02/24  |    6     |
|  84613584  |  Chicken |  15/02/24 |  19/02/24  |    1     |

At the beginning of each day FRED will update the daysLeft field to be correct. This will pass onto the GUI to indicate to the user how far the item is until its expiry date.


![image](https://github.com/BluDolphin/FRED_Fridge/assets/115663810/4d67d54e-2730-4838-bcbc-4a5ee7240caa)



### Key dates
![image](https://github.com/BluDolphin/The-Inator/assets/115663810/7841a238-6689-4285-ab5f-e7535e55c450)
