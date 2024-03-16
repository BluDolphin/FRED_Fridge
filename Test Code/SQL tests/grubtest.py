import sqlite3
import time

#setup
connection1 = sqlite3.connect("inventory.db")
connection2 = sqlite3.connect("cache.db")
cursor1 = connection1.cursor()
cursor2 = connection2.cursor()

#create table and add values
cursor1.execute("CREATE TABLE inventory (id INTEGER PRIMARY KEY, itemname TEXT FOREIGN KEY, currentdate GETDATE(), expirationdate DATE, daysleft INTEGER)") 
cursor1.execute("INSERT INTO inventory VALUES (1, 'boobs')")
cursor1.execute("INSERT INTO inventory VALUES (2, 'cuttlefish')")
rows = cursor1.execute("SELECT id, itemname, currentdate FROM inventory").fetchall()
print(rows)

print(connection.total_changes)