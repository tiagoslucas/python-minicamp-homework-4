import sqlite3

connection = sqlite3.connect('database.db')
print("We're connected!")

connection.execute('CREATE TABLE movies (title TEXT, year INTEGER)')
print('Table created successfully')

connection.close()