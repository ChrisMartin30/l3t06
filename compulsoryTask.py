# Import libraries
import sqlite3
from tabulate import tabulate

# Create database file
db = sqlite3.connect("data/ebookstore.db")
cursor = db.cursor()
print("Connected to bookstore database")

# Create table, use try except to check if table already exists. If it does, remove it and inform user,
# then create new table.
try:
    cursor.execute("""CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)""")
except sqlite3.OperationalError as e:
    print("Previous table not closed properly.\n", e, "\nDeleting previous table.")
    cursor.execute("DROP TABLE books")
    cursor.execute("""CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)""")
finally:
    db.commit()

# Insert given values
stock = [(3001, "A Tale of Two Cities", "Charles Dickens", 30), 
         (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
         (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
         (3004, "The Lord of the Rings", "J.R.R. Tolkein", 37),
         (3005, "Alice in Wonderland", "Lewis Carroll", 12)]

cursor.executemany("""INSERT INTO books(id, Title, Author, Qty) VALUES (?,?,?,?)""", stock)
db.commit()

# Global variables
header = ("id", "Title", "Author", "Qty")


### Functions 

def confirm_changes(confirm_id):
    """Used to display changed record to user and confirm before saving to database"""
    # Prints details about book to be edited.
    # If user confirms then will commit change to database, otherwise will rollback to 
    # previous version.
    
    cursor.execute(f"""SELECT id, Title, Author, Qty FROM books WHERE id = {confirm_id}""")
    book = cursor.fetchone()
    list_book = [book]
    print(tabulate((list_book), headers = header, tablefmt = "grid"))
    
    while True:
        confirm = input("Is this correct (Y/N):\n").lower()
        if confirm == "y" or confirm == "yes":
            db.commit()
            print("Changes saved")
            break
        elif confirm == "n" or confirm == "no":
            db.rollback()
            print("Changes discarded")
            break
        else:
            print("Unrecognised input")


def new_book():
    """Will obtain details about new book from user and add it to database."""
    # new id will be value of last book's ID + 1
    # Retrieve last item's ID, add 1 to get new book's ID num.
    cursor.execute("SELECT id FROM books")
    last_id = cursor.lastrowid
    new_id = last_id + 1
    # Obtain new book details from user. Ensure quantity is an integer and positive.
    new_title = input("New book title:\n")
    new_author = input("New book author:\n")
    while True:
        new_quantity = input("New book quantity:\n")
        try:    
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                print("Negative value entered. Please enter a positive one.")
            else:
                break
        except ValueError:
            print("Please type in the quantity in numbers")
            
    # Insert new book into database, confirm with user with confirm func before commiting change.
    cursor.execute("""INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)""",
                   (new_id, new_title, new_author, new_quantity))
    confirm_changes(new_id)

    print(f"You have added the book {new_title} by {new_author} into the database,",
           f"with {new_quantity} stocked.\nIt has been given the ID {new_id}.\n")


def update_book():
    """Updates information about a book already in the inventory"""
    # Obtain a valid format book id, ensuring it is an integer but giving user option to return to
    # previous menu.
    while True:
        edit_id = input("Please enter the ID of the book to be updated or 0 to return to previous menu:\n")
        if edit_id == "0":
            return
        else:    
            try:
                edit_id = int(edit_id)
                break
            except ValueError:
                print("Please enter the book ID number.")

    # Check if book ID exists in database. If it does not, print statement and return to menu.
    cursor.execute(f"""SELECT id, Title, Author, Qty FROM books WHERE id = {edit_id}""")
    book = cursor.fetchone()
    if book == None:
        print("That book ID is not in the inventory")
        return
    
    # Display book details using tabulate function. Confirm that user wants to update book details.
    while True:
        list_book = [book]
        print(tabulate((list_book), headers = header, tablefmt = "grid"))
        confirm = input("Do you want to edit this book (Y/N):\n").lower()
        if confirm ==  "n" or confirm == "no":
            return
        elif confirm == "y" or confirm == "yes":
            print(f"You have chosen to edit {book[1]}")
            break
        else:
            print("Unrecognised entry")

    # Give user option to edit book details or just quantity in stock.
    # Confirm changes with user before commiting to database.
    while True:
        edit_menu = input("""
Do you want to update:
1. Book Information
2. Quantity in stock
0. Return to previous menu
""")
        if edit_menu == "1":
            # Update book information, obtain new title and author from user.
            # Ask if user wants to keep old Qty, if so use data from database.
            #   If new Qty, ensure it is positive integer.
            edit_title = input("Enter new title:\n")
            edit_author = input("Enter new author:\n")
            while True: 
                edit_quantity = input("New book quantity, or leave blank to retain existing quantity:\n")
                if edit_quantity == "":
                    edit_quantity = book[3]
                    break
                else:
                    try:    
                        edit_quantity = int(edit_quantity)
                        if edit_quantity < 0:
                            print("Negative number entered. Please enter a positive number.")
                        else:
                            break
                    except ValueError:
                        print("Please type in the quantity in numbers")
            # Update database with new information. Confirm with function before committing.
            cursor.execute("""UPDATE books SET Title = ?, Author = ?, Qty = ? WHERE id = ?""", (edit_title, edit_author, edit_quantity, edit_id))
            confirm_changes(edit_id)

        elif edit_menu == "2":
            # User wants to update quantity for book.
            # Ensure new quantity is positive integer.
            while True:
                edit_quantity = input(f"New quantity for {book[1]}:\n")
                try:    
                    edit_quantity = int(edit_quantity)
                    if edit_quantity < 0:
                        print("Negative number entered. Please enter a positive number.")
                    else:
                        break
                except ValueError:
                    print("Please type in the quantity in numbers")
            # Update database and confirm with function before commit.
            cursor.execute("""UPDATE books SET Qty = ? WHERE id = ?""", (edit_quantity, edit_id))
            confirm_changes(edit_id)
            
        elif edit_menu == "0":
            return

        else:
            print("Unrecognised input")


def delete_book():
    """Deletes a specific book from the database"""
    # Obtain the ID of the book to be deleted. Give user an exit option, and 
    # ensure that user has entered an integer.
    while True:
        delete_id = input("""
Delete a book from the database.\nPlease enter the ID number of the book to be deleted:
(Enter 0 to return to previous menu)\n""")
        if delete_id == "0":
            return
        try:
            delete_id = int(delete_id)
            break
        except ValueError:
            print("Please enter the ID number.")
    # Check if book is in database, print message if it is not.
    cursor.execute(f"""SELECT id, Title, Author, Qty FROM books WHERE id = {delete_id}""")
    book = cursor.fetchone()
    if book == None:
        print("That book ID is not in the inventory")
        return
    
    # Confirm that user wants to delete book, if they confirm then commit change to database.
    while True:
        print(tabulate(([book]), headers = header, tablefmt = "grid"))
        confirm = input("Do you want to delete this book (Y/N):\n").lower()
        if confirm ==  "n" or confirm == "no":
            return
        elif confirm == "y" or confirm == "yes":
            print(f"You have deleted {book[1]} from the database")
            cursor.execute("""DELETE FROM books WHERE id = ?""", (delete_id,))
            db.commit()
            break
        else:
            print("Unrecognised entry")
    

def search_book():
    """Searches for specfic book in database"""
    # Present choices to user for what they wish to search for
    while True:
        search_menu = input("""
Would you like to search by
1. ID number
2. Book Title
3. Author
4. Current Stock levels
5. Display full list of inventory
0. Return to previous menu
""")
        if search_menu == "1":
            # Search by ID number
            # Obtain id from user, try except if invalid input, have a quit option.
            while True:
                try:
                    search_id = int(input("Enter book ID number (0 to return to main menu):\n"))
                    break
                except ValueError:
                    print("Please enter a valid number")
            if search_id == 0:
                return
            # Search for book in database, print message if it is not in the database.
            # If it is in database, print details using tabulate function.
            else:
                cursor.execute(f"""SELECT * FROM books WHERE id = {search_id}""")
                book = cursor.fetchone()

                if book == None:
                    print("That book ID is not in the inventory")
                else:
                    print(tabulate(([book]), headers = header, tablefmt = "grid"))

        elif search_menu == "2":
            # Search by Book title
            # Obtain title of book from user, with a quit option.
            while True:                
                search_title = (input("Enter book Title (0 to return to main menu):\n"))
                if search_title == "0":
                    return
                # Search for books in database, use NOCASE to search regardless of case of title
                # Print appropriate message if none found. If book is found, print with tabulate function.
                else:
                    cursor.execute("""SELECT * FROM books WHERE Title = ? COLLATE NOCASE""", (search_title,))
                    book = cursor.fetchall()

                    if len(book) == 0:
                        print(f"That book title - {search_title} - is not in the inventory")
                        break
                    else:
                        print(tabulate((book), headers = header, tablefmt = "grid"))
                        break

        elif search_menu == "3":
            # Search by author
            # Obtain author name from user, allow them option to return to previous menu.
            while True:                
                search_author = (input("Enter Author (0 to return to main menu):\n"))
                if search_author == "0":
                    return
                # Search for author in database, use NOCASE to strip case from search.
                # 1 author may have many books, so fetchall().
                # Print message if nothing found, otherwise display using tabulate.
                else:
                    cursor.execute("""SELECT * FROM books WHERE Author = ? COLLATE NOCASE""", (search_author,))
                    book = cursor.fetchall()

                    if len(book) == 0:
                        print(f"That author - {search_author} - is not in the inventory")
                        break
                    else:
                        print(tabulate((book), headers = header, tablefmt = "grid"))
                        break

        elif search_menu == "4":
            # Search by current stock levels
            # Search by maximum and minimum qty in stock.
            while True:
                search_stock = input("""
Display the book which is 
1. Greatest quantity in inventory
2. Least in inventory
3. Display all stock, sorted by inventory
0. Return to previous menu                
""")
                if search_stock == "1":
                    # User wants book which is greatest in stock
                    # Search database for details of book where qty is MAX, print using tabulate.
                    cursor.execute("""SELECT * FROM books WHERE Qty = (SELECT MAX(Qty) FROM books)""")
                    book = [cursor.fetchone()]
                    print(tabulate((book), headers = header, tablefmt = "grid"))                    
                elif search_stock == "2":
                    # User wants book which is least in stock
                    # Search database for details of book where qty is MIN, print using tabulate.
                    cursor.execute("""SELECT * FROM books WHERE Qty = (SELECT MIN(Qty) FROM books)""")
                    book = [cursor.fetchone()]
                    print(tabulate((book), headers = header, tablefmt = "grid"))
                elif search_stock == "3":
                    # Display all stock, sorted by Qty, then print headed list with tabulate.
                    cursor.execute("""SELECT * FROM books ORDER BY Qty DESC""")
                    current_stock = [book for book in cursor]
                    print(tabulate((current_stock), headers = header, tablefmt = "grid"))

                elif search_stock == "0":
                    break
                else:
                    "Unrecognised input"
            
        elif search_menu == "5":
            # display full inventory
            # Access database, create a current list of books then print with tabulate function.
            cursor.execute("""SELECT id, Title, Author, Qty FROM books""")
            current_stock = [book for book in cursor]
            print(tabulate((current_stock), headers = header, tablefmt = "grid"))
        elif search_menu == "0":
            # return to previous menu
            return
        else:
            print("Unrecognised input.")
        

### Menu

print(tabulate([["Book stock database manager"]], tablefmt= "grid"))

while True:
    menu = input("""
What would you like to do:
1. Enter book
2. Update book
3. Delete book
4. Search book
0. Exit 
""")
    if menu == "1":
        # User wants to enter a new book.
        print("Add a new book")
        new_book()

    elif menu == "2":
        # User wants to update a book's details.
        update_book()
        
    elif menu == "3":
        # User wants to delete a book from the database.
        delete_book()

    elif menu == "4":
        # User wants to search for a book.
        search_book()

    elif menu == "0":
        # User wants to quit, so clear table, close database and quit.
        cursor.execute("""DROP TABLE books""") 
        db.close()
        print("Closing book stock database manager")
        break

    else:
        print("You have made an unavailable choice. Please try again.")


