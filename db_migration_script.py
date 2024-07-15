import sqlite3

# Connect to the database
connection = sqlite3.connect('db.sqlite3')

# Create a cursor

cursor = connection.cursor()

# backup the database
with open('chinook_dump.sql', 'r', encoding='utf-8') as file:
    dump = file.read()
    cursor.executescript(dump)