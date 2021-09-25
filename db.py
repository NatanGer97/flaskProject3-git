## create db script
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "1234"
)
my_cursor = db.cursor()

my_cursor.execute("CREATE DATABASE users") #

my_cursor.execute("SHOW DATABASES")

for d in my_cursor:
    print(d)


# my_cursor.execute("SHOW DATABASES")
#
# for db in my_cursor:
#     print(db)