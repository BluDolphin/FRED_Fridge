import sqlite3

con = sqlite3.connect("Databasetest.db")
cur = con.cursor()
res=cur.execute("SELECT * FROM cacheditems")
res.fetchall()