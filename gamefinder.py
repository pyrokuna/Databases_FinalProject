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

    # ensures that the registering user gives a password
    if len(confirm_pass) == 0 or len(confirm_username) == 0:
        messagebox.showerror("Error", "Must enter a username AND password.")
        erase_username.delete(0, tk.END)
        erase_pass.delete(0, tk.END)
        return
    # if e-mail already being used, don't allow creation of profile
    # ADD CODE HERE
    # test that the given username is in the correct format
    elif not re.match(r"\S+@\S+\.\S+", confirm_username):
        messagebox.showerror(
            "Error",
            "E-mail is not in correct format.\nmust be <name>@<website>.<domain>",
        )
        erase_username.delete(0, tk.END)
        erase_pass.delete(0, tk.END)
        return

    # LOGIC OF ACTUAL REGISTRATION: ADDING USER TO DB


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
    tk.Label(register_screen, text="E-mail *").pack()
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
    confirm_username = username_login.get()
    confirm_password = password_login.get()

    # ensure the account exists
    if (
        "<some logic>"
    ):  ################################################################################
        # if login is successful, move onto the main window design function
        if (
            "test_pass" == confirm_password
        ):  ###########################################################
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
    tk.Label(login_screen, text="E-mail *").pack()
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


def delete_item():
    """
    Delete amazon item
    """
    print("Probably gone")


def add_item():
    """
    Add an amazon item
    """
    print("Probably gone")


def main_window():
    """
    Design function for Main Window
    - Will allow for input of items and seeing the items in a list of up to 10 items
    """
    # item variables
    global main_screen
    global item_url
    global item_desired_price
    global listbox
    global url_entry
    global desired_price_entry

    # create essential pieces/geometry of the window
    main_screen = tk.Tk()
    main_screen.geometry("1200x675")
    # main_screen.resizable(width=False, height=False)
    main_screen.title("Price Drop Notification")

    item_url = tk.StringVar()
    item_desired_price = tk.StringVar()

    # making the background of the window and the line to split up the sides
    left_frame = tk.Frame(main_screen, bg="beige", width=598, height=675)
    middle_frame = tk.Frame(main_screen, bg="black", width=4, height=675)
    right_frame = tk.Frame(main_screen, bg="beige", width=598, height=675)
    left_frame.place(x=0, y=0)
    middle_frame.place(x=598, y=0)
    right_frame.place(x=602, y=0)

    # creating the widgets for the left frame
    tk.Label(
        left_frame, text="URL of Desired Item", bg="beige", font=("Calibri", 16)
    ).place(x=299 - 95, y=180)
    url_entry = tk.Entry(left_frame, textvariable=item_url)
    url_entry.place(x=299 - 70, y=210)
    tk.Label(
        left_frame,
        text="Desired Price of Desired Item",
        bg="beige",
        font=("Calibri", 16),
    ).place(x=299 - 135, y=260)
    desired_price_entry = tk.Entry(left_frame, textvariable=item_desired_price)
    desired_price_entry.place(x=299 - 70, y=290)
    # goto add_item
    tk.Button(left_frame, text="Add", height="2", width="30", command=add_item).place(
        x=299 - 115, y=320
    )

    # creating widgets for the right frame
    tk.Label(
        right_frame,
        text="Items You Are Currently Watching",
        bg="beige",
        font=("Calibri", 16),
    ).place(x=299 - 130, y=50)
    listbox = tk.Listbox(right_frame, width=50, height=30)
    listbox.place(x=299 - 135, y=80)
    tk.Button(
        right_frame, text="Delete Item", height="2", width="30", command=delete_item
    ).place(x=299 - 95, y=570)

    # FOR TESTING:
    # main_screen.mainloop()


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


#start_screen()

# close the connection to the database
db.mydb.close()