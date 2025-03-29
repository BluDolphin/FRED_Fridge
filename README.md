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

## Contributors 
- Harrison - https://www.linkedin.com/in/h-morgan/
- Lachlan - https://www.linkedin.com/in/lachlan-churchland-2615362b3/
- Finlay - https://www.linkedin.com/in/finlay-rastall/
- Archie - https://www.linkedin.com/in/archie-butcher-6a94822b4/
- Harman - https://www.linkedin.com/in/harman-samra17/

## Poster
![1716300325064-fc074a08-752a-40ee-9658-1c8e4a6845a2D_1](https://github.com/user-attachments/assets/e70209d0-e13c-4555-81a3-4e49cdba9353)

## Flow Chart
![image](https://github.com/BluDolphin/FRED_Fridge/assets/115663810/4d67d54e-2730-4838-bcbc-4a5ee7240caa)
## LCD Panel Diagram
![null (2)](https://github.com/BluDolphin/FRED_Fridge/assets/115663810/a0c3e4dd-e66c-442d-9110-1b7d47a745f2)
