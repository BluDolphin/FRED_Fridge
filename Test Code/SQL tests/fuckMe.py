import sqlite3
import time

#setup
connection1 = sqlite3.connect("aquarium.db")
connection2 = sqlite3.connect("cache.db")
cursor1 = connection1.cursor()
cursor2 = connection2.cursor()

#create table and add values
cursor1.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)") 
cursor1.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
cursor1.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")
rows = cursor1.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)

time.sleep(3)
#change value
target_fish_name = "Jamie"
rows = cursor1.execute("SELECT name, species, tank_number FROM fish WHERE name = ?",(target_fish_name,),).fetchall()
print(rows)

time.sleep(3)
#update value command
new_tank_number = 2
moved_fish_name = "Sammy"
cursor1.execute("UPDATE fish SET tank_number = ? WHERE name = ?",(new_tank_number, moved_fish_name))

rows = cursor1.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)

time.sleep(3)
#delete value
released_fish_name = "Sammy"
cursor1.execute(
    "DELETE FROM fish WHERE name = ?",
    (released_fish_name,)
)

#print(connection.total_changes)