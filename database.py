import sqlite3 

#Open database
conn = sqlite3.connect('base.db')

#Create table
conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		username TEXT,
		email TEXT
		)''')

conn.execute('''CREATE TABLE last
		(userId INTEGER PRIMARY KEY, 
        username TEXT,
        number TEXT,
        email TEXT,
        address TEXT,
        price TEXT,
        age TEXT,
        gender TEXT,
        month TEXT
		)''')


conn.close()

