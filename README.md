# L3T06

# Compulsory Task 2

The steps of this task is to
> - Create a GitHub Repository
> - Push any Project that you created in the previous level to this remote repository.
> - Add a detailed README file for the project you have pushed to the GitHub.

To accomplish this I have decided to push the L2T13 Capstone Project Task to GitHub.


## Capstone Project
The aim of the project was to create a "bookstore database program". The program was designed to allow the clerk to **enter** data about new books into the database, **update** book information, **delete** books from the database and **search** to find the availability of books in the database.

### Languages used
Python was used to write it, and I used SQLite to manage the database. 

### Functions created
Functions were created to perform tasks including
- A *new_book* function 
    - This takes details from the user, verifies that the data is of a suitable format, then adds it to the database.
- An *update_book* function 
    - This allows a user to select a book using the book ID number, then edit either information about the book or modify inventory levels.
- A *delete_book* function
    - This allowed the user to delete a book from the database.
- A *search_book* function
    - This allowed a user to search the database using
        - The book ID number
        - The book Title
        - An Author
    - It also allowed the user to display current stock levels, and the books which were either greatest or least in stock in the inventory.
- A *confirm_changes* function
    - This displays to the user details of what is about to be edited and allows the user to confirm or rollback changes.


## Using the program
To use the program I have run the python file using [Visual Studio Code](https://code.visualstudio.com).
When running, the following image should be seen at start.

![Screenshot of start menu](/images/start_screen.png)


If the previous table was not closed correctly, a message saying:

```
Previous table not closed properly
table books already exists
Deleting previous table
```

Should be displayed. The program should then start as normal.

<a name="always_exit"></a>To prevent seeing this message, the user should __always__ exit the program through use of the exit option, rather than a keyboard interrupt.


### Adding a new book to the inventory
To add a new book to the inventory, the user should select option 1 from the start menu. Then the user enters the **Book Title**, the **Author** and the **Quantity in Stock** (*using numerals*) as shown in the screenshot below.

![Screenshot of new book screen](/images/new_book.png)

The user then is asked to confirm the details when shown a summary with a Y/N option. If the user chooses "Y" the new book is added to the database, otherwise the changes are discarded.

### Updating book details
To update book details, the user should select option 2 from the start menu. The user then enters the book ID number, confirms the details with a Y/N option, and then can choose to update either the book details or the stock information. After making changes, the user is again asked to confirm the changes before they are commited to the database.

### Deleting a book
To delete a book, the user should select option 3 from the start menu. Then the user enters the ID number of the book to be deleted, the book's details are displayed and the user is asked to confirm before the entry is deleted from the database.

### Search for a book
To search fpr a book, the user should select option 4 from the start menu. The user is then presented with a list of options on what to search for. The user can choose from
- Book ID number
- Book Title
- Author
- Stock levels
    - Either the book which has the greatest quantity in stock, or the least. 

The user can also choose to display the entire inventory.


## Exiting the program
If the user wants to exit the program the user should select option 0 from the start menu. It is important to do this, as it will commit changes to the database and close it in a suitable manner.
If this is not done, changes may not be saved and there may be the issues mentioned [earlier](#always_exit) when opening the program subsequently.

## Credits
This task was done thanks to the guidance provided by HyperionDev.
