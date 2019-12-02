import mysql.connector

# connecting to a database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    port = 3306,
)

# creating my cursor and database
my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS testdb")

# looking at all of my current databases to check the one I have created is there
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db[0])

# close the connection to the database
mydb.close()