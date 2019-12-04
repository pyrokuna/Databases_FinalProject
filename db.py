import mysql.connector

# connecting to a database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "lollipopdb"
)

# creating my cursor and database
my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS lollipopdb")

# looking at all of my current databases to check the one I have created is there
#my_cursor.execute("SHOW DATABASES")
#for db in my_cursor:
#    print(db[0])

my_cursor.execute("CREATE TABLE IF NOT EXISTS Games ("
                    + "game_id INTEGER AUTO_INCREMENT PRIMARY KEY," 
                    + "title VARCHAR(70),"
                    + "description VARCHAR(255),"
                    + "release_year INTEGER(4))"
                )
my_cursor.execute("CREATE TABLE IF NOT EXISTS Genre ("
                    + "genre_id INTEGER AUTO_INCREMENT PRIMARY KEY," 
                    + "genre_name VARCHAR(50))"
                )
# many to many relationship warrants a table for the relation
my_cursor.execute("CREATE TABLE IF NOT EXISTS GameGenre ("
                    + "gg_id INTEGER AUTO_INCREMENT PRIMARY KEY," 
                    + "game_id INTEGER," 
                    + "genre_id INTEGER," 
                    + "FOREIGN KEY (game_id) REFERENCES games(game_id) ON DELETE CASCADE,"
                    + "FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE)"
                )
my_cursor.execute("CREATE TABLE IF NOT EXISTS Platform ("
                    + "plat_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                    + "plat_name VARCHAR(70))"
                )
# many to many relationship warrants a table for the relation
my_cursor.execute("CREATE TABLE IF NOT EXISTS GamePlatform ("
                    + "gp_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                    + "game_id INTEGER,"
                    + "plat_id INTEGER," 
                    + "FOREIGN KEY (game_id) REFERENCES games(game_id) ON DELETE CASCADE,"
                    + "FOREIGN KEY (plat_id) REFERENCES platform(plat_id) ON DELETE CASCADE)"
                )
my_cursor.execute("CREATE TABLE IF NOT EXISTS User ("
                    + "username VARCHAR(70) PRIMARY KEY,"
                    + "password VARCHAR(70))"
                )
# Named Favorites for ease of use but designed for relationship between games and users
my_cursor.execute("CREATE TABLE IF NOT EXISTS Favorites ("
                    + "fav_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                    + "username VARCHAR(70),"
                    + "game_id INTEGER,"
                    + "FOREIGN KEY (username) REFERENCES user(username) ON DELETE CASCADE,"
                    + "FOREIGN KEY (game_id) REFERENCES games(game_id) ON DELETE CASCADE)"
                )


#my_cursor.execute(
#    'INSERT INTO Games (title, description, release_year) VALUES ("The Legend of Zelda: Ocarina Of Time", "The Legend of Zelda: Ocarina of Time is an action-adventure game developed and published by Nintendo.", 1998)'
#)

#my_cursor.execute(
#    'INSERT INTO Genre (genre_name) VALUES ("Action Adventure")'
#)

#my_cursor.execute(
#    'INSERT INTO GameGenre (game_id, genre_id) VALUES (1,1)'
#)

#my_cursor.execute(
#    'INSERT INTO Platform (plat_name) VALUES ("iQue Player")'
#)

#my_cursor.execute(
#    'INSERT INTO GamePlatform (game_id, plat_id) VALUES (1,7)'
#)

#my_cursor.execute('DELETE FROM platform')

mydb.commit()