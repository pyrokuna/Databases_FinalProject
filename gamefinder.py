import tkinter as tk
from tkinter import messagebox
import re
import db   # importing our own module
import sys

"""
Ryan Gutierrez
Zachary Gutierrez
12-3-19
GUI/frot-end of database
NOT3!!!! Help from the following:
    https://www.youtube.com/watch?v=Xt6SqWuMSA8
"""

def menu():
    """
    Print Menu for "admin"
    """
    print("------- Admin Menu -------")
    print("I: insert a record")
    print("U: update a record")
    print("D: delete a record")
    print("Q: exit\n")

# Running the program as "admin" in the command prompt to access inserting, updating, and deleting records
# because we don't want users to have access to change the core database, only their favorites list
if len(sys.argv) > 1 and sys.argv[1] == "-adm":
    while True:
        menu()
        menu_choice = input("lollipopDB/menu choice> ")
        if menu_choice == "I" or menu_choice == "i":
            title = input("Enter a title of a video game: ")
            descr = input("Enter a small game description(<255char): ")
            year = int(input("Enter the game's release year: "))
            db.my_cursor.execute(
                f'INSERT INTO Games (title, description, release_year) VALUES ("{title}", "{descr}", {year})'
            )
            db.mydb.commit()

            genres = input("Enter the genre(s) in a comma seperated list: ")
            genres = genres.split(', ')
            for x in genres:
                db.my_cursor.execute(f'SELECT genre_name FROM lollipopdb.genre WHERE genre_name = "{x}"')
                res = db.my_cursor.fetchall()
                if len(res) == 0:
                    # add to database
                    db.my_cursor.execute(f'INSERT INTO Genre (genre_name) VALUES ("{x}")')
                    db.mydb.commit()
                # linking the genre to the game previously input
                #  extracting game_id
                db.my_cursor.execute(f'SELECT game_id FROM lollipopdb.games WHERE title = "{title}"')
                gameID = db.my_cursor.fetchone()
                gameID = int(gameID[0])
                #  extracting genre_id
                db.my_cursor.execute(f'SELECT genre_id FROM lollipopdb.genre WHERE genre_name = "{x}"')
                genreID = db.my_cursor.fetchone()
                genreID = int(genreID[0])
                #  linking genre(s) to game
                db.my_cursor.execute( f'INSERT INTO GameGenre (game_id, genre_id) VALUES ({gameID},{genreID})')  

            platforms = input("Enter the platform(s) in a comma seperated list: ")
            platforms = platforms.split(', ')
            for x in platforms:
                db.my_cursor.execute(f'SELECT plat_name FROM lollipopdb.platform WHERE plat_name = "{x}"')
                res = db.my_cursor.fetchall()
                if len(res) == 0:
                    # add to database
                    db.my_cursor.execute(f'INSERT INTO platform (plat_name) VALUES ("{x}")')
                    db.mydb.commit()
                # linking the platform to the game previously input
                #  extracting game_id
                db.my_cursor.execute(f'SELECT game_id FROM lollipopdb.games WHERE title = "{title}"')
                gameID = db.my_cursor.fetchone()
                gameID = int(gameID[0])
                #  extracting platform_id
                db.my_cursor.execute(f'SELECT plat_id FROM lollipopdb.platform WHERE plat_name = "{x}"')
                platID = db.my_cursor.fetchone()
                platID = int(platID[0])
                #  linking platform(s) to game
                db.my_cursor.execute( f'INSERT INTO gameplatform (game_id, plat_id) VALUES ({gameID},{platID})')

            db.mydb.commit()
        elif menu_choice == "U" or menu_choice == "u":
            title = input("Title of game you would like to update: ")
            # check if game with title exists in DB
            db.my_cursor.execute(f'SELECT title FROM lollipopdb.games WHERE title = "{title}"')
            res = db.my_cursor.fetchall()
            if len(res) > 0:
                up_param = input("Update (T)itle, (D)escription, or (Y)ear: ")
                if up_param == "t" or up_param == "T":
                    new_param = input("Updated title: ")
                    db.my_cursor.execute(f'UPDATE lollipopdb.games SET title = "{new_param}" WHERE title = "{title}"')
                if up_param == "d" or up_param == "D":
                    new_param = input("Updated description: ")
                    db.my_cursor.execute(f'UPDATE lollipopdb.games SET description = "{new_param}" WHERE title = "{title}"')
                if up_param == "y" or up_param == "Y":
                    new_param = int(input("Updated year: "))
                    db.my_cursor.execute(f'UPDATE lollipopdb.games SET release_year = {new_param} WHERE title = "{title}"')
                db.mydb.commit()
            # case where no game with given title exists in DB
            else:
                print("**ERROR: No game of the given title exists in the database.")
        elif menu_choice == "D" or menu_choice == "d":
            title = input("Title of game you would like to delete: ")
            # check if game with title exists in DB
            db.my_cursor.execute(f'SELECT title FROM lollipopdb.games WHERE title = "{title}"')
            res = db.my_cursor.fetchall()
            if len(res) > 0:
                db.my_cursor.execute(f'DELETE FROM lollipopdb.games WHERE title = "{title}"')
            else:
                print("**ERROR: No game of the given title exists in the database.")
            db.mydb.commit()
        elif menu_choice == "Q" or menu_choice == "q":
            exit()


# ---------------------------------- Start of GUI/user section ----------------------------------
def confirm_register():
    """
    Logic of what registration does
    - takes care of the logic of the registration function
    """
    confirm_username = username.get()
    confirm_pass = password.get()

    # ensures that the registering user gives a password and username
    if len(confirm_pass) == 0 or len(confirm_username) == 0:
        messagebox.showerror("Error", "Must enter a username AND password.")
        erase_username.delete(0, tk.END)
        erase_pass.delete(0, tk.END)
        return
    # if username already being used, don't allow creation of profile
    db.my_cursor.execute(f'SELECT username FROM lollipopdb.user WHERE username = "{confirm_username}"')
    res = db.my_cursor.fetchall()
    if len(res) > 0:
        messagebox.showerror("Error", "Username already exists in database, a unique username is required.")
        erase_username.delete(0,tk.END)
        erase_pass.delete(0, tk.END)
        return
    # add user to DB
    else:
        db.my_cursor.execute(f'INSERT INTO user (username, password) VALUES ("{confirm_username}", "{confirm_pass}")')
        db.mydb.commit()
        register_screen.destroy()


def register_window():
    """
    Design of Registration Window
    - allows a user with no account to create one
    """
    global register_screen
    global username
    global password
    global erase_username
    global erase_pass
    username = tk.StringVar()
    password = tk.StringVar()

    # create login screen essentials
    register_screen = tk.Toplevel(origin_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    # create buttons and entry objects for registration
    tk.Label(register_screen, text="Please enter details below").pack()
    tk.Label(register_screen, text="").pack()
    tk.Label(register_screen, text="Username *").pack()
    erase_username = tk.Entry(register_screen, textvariable=username)
    erase_username.pack()
    tk.Label(register_screen, text="Password *").pack()
    erase_pass = tk.Entry(register_screen, textvariable=password, show="*")
    erase_pass.pack()
    tk.Label(register_screen, text="").pack()
    # goto the register logic function
    tk.Button(
        register_screen,
        text="Register",
        height="2",
        width="30",
        command=confirm_register,
    ).pack()


def confirm_login():
    """
    Login Logic Functions
    - takes care of the logic of the login function
    """
    global User
    global Pass
    confirm_username = username_login.get()
    confirm_password = password_login.get()

    # ensure the account exists
    db.my_cursor.execute(f'SELECT username FROM lollipopdb.user WHERE username = "{confirm_username}"')
    res = db.my_cursor.fetchall()
    if len(res) > 0:
        # if login is successful, move onto the main window design function
        db.my_cursor.execute(f'SELECT * FROM lollipopdb.user WHERE (username = "{confirm_username}" AND password = "{confirm_password}")')
        res = db.my_cursor.fetchall()
        if len(res) > 0:
            User = confirm_username
            Pass = confirm_password
            login_screen.destroy()
            origin_screen.destroy()
            main_window()
        # if username is correct and login is unsuccessful, throw error due to password and force user to retry
        else:
            messagebox.showerror("Error", "The password is incorrect")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
    # if the account does not exist, throw an error and force user to retry
    else:
        messagebox.showerror("Error", "No account exists with the given e-mail.")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)


def login_window():
    """
    Design of the Login Window
    - allows a user of an existing account to login
    """
    global login_screen
    global username_login
    global password_login
    global username_entry
    global password_entry

    # create login screen essentials
    login_screen = tk.Toplevel(origin_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")

    username_login = tk.StringVar()
    password_login = tk.StringVar()

    # creat login screen buttons and entry objects that accept strings
    tk.Label(login_screen, text="Please enter details below").pack()
    tk.Label(login_screen, text="").pack()
    tk.Label(login_screen, text="Username *").pack()
    username_entry = tk.Entry(login_screen, textvariable=username_login)
    username_entry.pack()
    tk.Label(login_screen, text="").pack()
    tk.Label(login_screen, text="Password *").pack()
    password_entry = tk.Entry(login_screen, textvariable=password_login, show="*")
    password_entry.pack()
    tk.Label(login_screen, text="").pack()
    # goto the login logic function
    tk.Button(
        login_screen, text="Login", height="2", width="30", command=confirm_login
    ).pack()


def add():
    add_record = listbox.get(listbox.curselection())
    if len(add_record) == 0:
        messagebox.showwarning("Warning", "You must select a record to favorite.")
    add_record = add_record[0]

    # linking the user to the favorite selection
    #  extracting game_id
    db.my_cursor.execute(f'SELECT game_id FROM lollipopdb.games WHERE title = "{add_record}"')
    gameID = db.my_cursor.fetchone()
    gameID = int(gameID[0])
    db.my_cursor.execute(f'SELECT title FROM lollipopdb.games INNER JOIN favorites ON (games.game_id = favorites.game_id) INNER JOIN user ON (user.username = favorites.username) WHERE title = "{add_record}" AND favorites.username = "{User}"')
    res = db.my_cursor.fetchall()
    if len(res) == 0:
        #  linking user to game(s)
        db.my_cursor.execute( f'INSERT INTO favorites (username, game_id) VALUES ("{User}",{gameID})')
        db.mydb.commit()
    else:
        messagebox.showerror("Error", "The game selected is already in your favorites.")

def remove():
    rem_record = listbox.get(listbox.curselection())
    if len(rem_record) == 0:
        messagebox.showwarning("Warning", "You must select a record to favorite.")
    rem_record = rem_record[0]
    
    # check if item exists in the favorites table
    db.my_cursor.execute(f'SELECT title FROM lollipopdb.games INNER JOIN favorites ON (games.game_id = favorites.game_id) INNER JOIN user ON (user.username = favorites.username) WHERE title = "{rem_record}" AND favorites.username = "{User}"')
    res = db.my_cursor.fetchall()
    if len(res) > 0:
        db.my_cursor.execute(f'SELECT game_id FROM lollipopdb.games WHERE title = "{rem_record}"')
        gameID = db.my_cursor.fetchone()
        gameID = int(gameID[0])
        db.my_cursor.execute(f'DELETE FROM lollipopdb.favorites WHERE game_id = {gameID} AND username = "{User}"')
    else:
        messagebox.showerror("Error", "The game selected is not in your favorites.")
    db.mydb.commit()

    listbox.delete(0, tk.END)
    db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games INNER JOIN favorites ON (games.game_id = favorites.game_id) INNER JOIN user ON (user.username = favorites.username) WHERE user.username = "{User}"')
    res = db.my_cursor.fetchall()
    for x in res:
        listbox.insert(tk.END, x)

def show_fav():
    listbox.delete(0, tk.END)
    db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games INNER JOIN favorites ON (games.game_id = favorites.game_id) INNER JOIN user ON (user.username = favorites.username) WHERE user.username = "{User}"')
    res = db.my_cursor.fetchall()
    for x in res:
        listbox.insert(tk.END, x)

def search():
    rYear_en = rYear_entry.get()
    genre_sel = genre_selected.get()
    plat_sel = plat_selected.get()

    rYear_enB = True
    genre_selB = True
    plat_selB = True

    if len(rYear_en) == 0:
        rYear_enB = False
    if genre_sel == "None":
        genre_selB = False
    if plat_sel == "None":
        plat_selB = False

    # if all search parameters are empty give warning
    if not rYear_enB and not genre_selB and not plat_selB:
        messagebox.showinfo("Attention", "You must use at least one of the parameters to get a good search.")
    # if not query
    else:
        # delete everything in the listbox
        listbox.delete(0, tk.END)
        # query kinds based on how many fields are filled in
        if rYear_enB and not genre_selB and not plat_selB:
            db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games WHERE release_year = {rYear_en}')
            res = db.my_cursor.fetchall()
            for x in res:
                listbox.insert(tk.END, x)
        elif not rYear_enB and genre_selB and not plat_selB:
            db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games INNER JOIN gamegenre ON (games.game_id = gamegenre.game_id) INNER JOIN genre ON (genre.genre_id = gamegenre.genre_id) WHERE genre.genre_name = "{genre_sel}"')
            res = db.my_cursor.fetchall()
            for x in res:
                listbox.insert(tk.END, x)
        elif not rYear_enB and not genre_selB and plat_selB:
            db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games INNER JOIN gameplatform ON (games.game_id = gameplatform.game_id) INNER JOIN platform ON (platform.plat_id = gameplatform.plat_id) WHERE platform.plat_name = "{plat_sel}"')
            res = db.my_cursor.fetchall()
            for x in res:
                listbox.insert(tk.END, x)
        elif rYear_enB and genre_selB and not plat_selB:
            db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games INNER JOIN gamegenre ON (games.game_id = gamegenre.game_id) INNER JOIN genre ON (genre.genre_id = gamegenre.genre_id) WHERE genre.genre_name = "{genre_sel}" AND release_year = {rYear_en}')
            res = db.my_cursor.fetchall()
            for x in res:
                listbox.insert(tk.END, x)
        elif rYear_enB and not genre_selB and plat_selB:
            db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games INNER JOIN gameplatform ON (games.game_id = gameplatform.game_id) INNER JOIN platform ON (platform.plat_id = gameplatform.plat_id) WHERE platform.plat_name = "{plat_sel}" AND release_year = {rYear_en}')
            res = db.my_cursor.fetchall()
            for x in res:
                listbox.insert(tk.END, x)
        elif not rYear_enB and genre_selB and plat_selB:
            db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games INNER JOIN gameplatform ON (games.game_id = gameplatform.game_id) INNER JOIN platform ON (platform.plat_id = gameplatform.plat_id) INNER JOIN gamegenre ON (games.game_id = gamegenre.game_id) INNER JOIN genre ON (genre.genre_id = gamegenre.genre_id) WHERE platform.plat_name = "{plat_sel}" AND genre.genre_name = "{genre_sel}"')
            res = db.my_cursor.fetchall()
            for x in res:
                listbox.insert(tk.END, x)
        else:
            db.my_cursor.execute(f'SELECT title, release_year, description FROM lollipopdb.games INNER JOIN gameplatform ON (games.game_id = gameplatform.game_id) INNER JOIN platform ON (platform.plat_id = gameplatform.plat_id) INNER JOIN gamegenre ON (games.game_id = gamegenre.game_id) INNER JOIN genre ON (genre.genre_id = gamegenre.genre_id) WHERE platform.plat_name = "{plat_sel}" AND genre.genre_name = "{genre_sel}" AND release_year = {rYear_en}')
            res = db.my_cursor.fetchall()
            for x in res:
                listbox.insert(tk.END, x)


def main_window():
    """
    Design function for Main Window
    - Will allow for input of items and seeing the items in a list of up to 10 items
    """
    # item variables
    global main_screen
    global listbox
    global rYear_entry
    global genre_selected
    global plat_selected

    # create essential pieces/geometry of the window
    main_screen = tk.Tk()
    main_screen.geometry("1200x675")
    # main_screen.resizable(width=False, height=False)
    main_screen.title("GameFinder")

    # making the background of the window and the line to split up the sides
    left_frame = tk.Frame(main_screen, bg="beige", width=598, height=675)
    middle_frame = tk.Frame(main_screen, bg="black", width=4, height=675)
    right_frame = tk.Frame(main_screen, bg="beige", width=598, height=675)
    left_frame.place(x=0, y=0)
    middle_frame.place(x=598, y=0)
    right_frame.place(x=602, y=0)

    # creating the widgets for the left frame
    # release year entry section
    rYear_entry = tk.StringVar()
    tk.Label(
        left_frame, text="Parameters for Search:", bg="beige", font=("Calibri", 18)
    ).place(x=299 - 125, y=0)
    tk.Label(
        left_frame, text="Release Year", bg="beige", font=("Calibri", 16)
    ).place(x=299 - 70, y=100)
    ry_entry = tk.Entry(left_frame, textvariable=rYear_entry)
    ry_entry.place(x=299 - 75, y=150)
    
    # Genre drop down menu section
    tk.Label(
        left_frame, text="Genre", bg="beige", font=("Calibri", 16)
    ).place(x=299 - 40, y=200)
    # drop down menu for genre
    db.my_cursor.execute('SELECT genre_name FROM lollipopdb.genre')
    gres = db.my_cursor.fetchall()
    gen_list = []
    gen_list.append("None")
    for i, x in enumerate(gres):
        gen_list.append(gres[i][0])
    genre_selected = tk.StringVar()
    genre_selected.set("None")

    tk.OptionMenu(left_frame, genre_selected, *gen_list).place(x=299 - 47, y=250)

    # Platform drop down menu section
    tk.Label(
        left_frame, text="Platform", bg="beige", font=("Calibri", 16)
    ).place(x=299 - 50, y=300)
    # drop down menu for genre
    db.my_cursor.execute('SELECT plat_name FROM lollipopdb.platform')
    pres = db.my_cursor.fetchall()
    plat_list = []
    plat_list.append("None")
    for i, x in enumerate(pres):
        plat_list.append(pres[i][0])
    plat_selected = tk.StringVar()
    plat_selected.set("None")

    tk.OptionMenu(left_frame, plat_selected, *plat_list).place(x=299 - 47, y=350)

    # goto search
    tk.Button(left_frame, text="Search", height="2", width="30", command=search).place(
        x=299 - 115, y=420
    )

    # creating widgets for the right frame
    tk.Label(
        right_frame,
        text="List of Games in the DB",
        bg="beige",
        font=("Calibri", 16),
    ).place(x=299 - 90, y=0)
    listbox = tk.Listbox(right_frame, width=92, height=36)
    listbox.place(x=299 - 280, y=30)
    tk.Button(
        right_frame, text="Add to Favorites", height="2", width="24", command=add
    ).place(x=299 - 280, y=625)
    tk.Button(
        right_frame, text="Remove from Favorites", height="2", width="24", command=remove
    ).place(x=299 - 92, y=625)
    tk.Button(
        right_frame, text="Show Favorites", height="2", width="24", command=show_fav
    ).place(x=299 + 95, y=625)

    # FOR TESTING:
    main_screen.mainloop()


def start_screen():
    """
    Design of the Start Window
    - Two options:
        * Login allows a user of an existing account to login
        * Register allows a user without an accoun tot create one
    """
    # Create Screen essentials
    global origin_screen
    origin_screen = tk.Tk()
    origin_screen.geometry("900x506")
    origin_screen.title("Login if you have an account or Register if you don't")
    origin_screen.resizable(height=None, width=None)

    # Buttons and Labels added to screen
    tk.Label(
        text="Login or Register",
        bg="grey",
        width="300",
        height="2",
        font=("Calibri", 13),
    ).pack()
    tk.Label(text="").pack()
    tk.Button(
        text="Login", height="2", width="30", command=login_window
    ).pack()  # goto login function
    tk.Label(text="").pack()
    tk.Button(
        text="Register", height="2", width="30", command=register_window
    ).pack()  # goto register function

    origin_screen.mainloop()


start_screen()
#main_window()

# close the connection to the database
db.mydb.close()