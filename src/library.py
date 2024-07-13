import mysql.connector
from src import dbConn
from src import book
from datetime import date
from src import ui

class Library:
    # def __init__(self):
    #pass

    # Implement library management methods here

    
    def borrowBook(bookTitle: str):
        # check if book is borrowed
        checkBook = book.Book(bookTitle)
        bookAvailability = checkBook.checkBookAvailability()
        if bookAvailability == 1:
            # Insert borrow record into DB
            dbCursor = dbConn.libDB.cursor()
            sql = "INSERT INTO borrow_record (bookTitle, borrowDate, isReturn) VALUES (%s, %s, %s)"
            val = (bookTitle, date.today(), "No")
            try:
                dbCursor.execute(sql, val)
                dbConn.libDB.commit()
                print("Book borrowed successfully")
            except dbConn.Conn.Error as e:
                print("SQL problem {}",format(e.msg))
                print("Cannot update borrow record")
            finally:
                input("Press any key to return to menu")
                ui.ui.startUI()
        elif bookAvailability == 0:
            print("The book has been borrowed")
            input("Press any key to return to menu")
            ui.ui.startUI() # return to main page

        else:
            print("Book does not exist in Library Database")
            input("Press any key to return to menu")
            ui.ui.startUI() # return to main page
    
    
    def returnBook(bookTitle: str):
        # check if book is borrowed
        checkBook = book.Book(bookTitle)
        bookAvailability = checkBook.checkBookAvailability()
        if bookAvailability == 0:
            # Update Borrow record DB
            dbCursor = dbConn.libDB.cursor()
            sql = "UPDATE borrow_record SET returnDate = %s, isReturn = %s WHERE bookTitle = %s"
            val = (date.today(), "Yes", bookTitle)
            try:    
                dbCursor.execute(sql, val)
                dbConn.libDB.commit()
                print("Book returned successfully")
            except dbConn.Conn.Error as e:
                print("SQL problem {}",format(e.msg))
                print("Cannot update book return record")
            finally:
                input("Press any key to return to menu")
                ui.ui.startUI() # return to main page

        elif bookAvailability == 1:
            print("Book has not been borrowed")
            input("Press any key to return to menu")
            ui.ui.startUI() # return to main page
        else:
            print("Book does not exist in Library Database")
            input("Press any key to return to menu")
            ui.ui.startUI() # return to main page


    def selectAllBook():       
        sql = "SELECT * FROM book_list"
        dbConn1 = dbConn.libDB
        dbCursor = dbConn1.cursor()
        dbCursor.execute(sql)
        result = dbCursor.fetchall()
        for record in result:
            print("Title: ", record[1], )
            print("Author: ", record[2], )
            print("Genre: ", record[3], )
            print("Release year: ", record[4], "\n")
        print("Search completed")
        print(len(result), " results found")
        print("---------------------------------------")
        input("Press any key to return to menu")
        ui.ui.searchBookUI()
    
    def selectBookByTitle(title: str):
        sql = """
                SELECT title, author, genre, releaseYear,
                CASE 
                    WHEN borrowDate IS NULL THEN 'Available'
                    WHEN isReturn = 'Yes' THEN 'Available'
                    ELSE 'Borrowed'
                END AS Availability
                FROM book_list
                LEFT JOIN borrow_record ON book_list.title = borrow_record.bookTitle
                WHERE title like %s
                """
        val = ('%'+title+'%',)
        dbConn1 = dbConn.libDB
        dbCursor = dbConn1.cursor()
        dbCursor.execute(sql,val)
        result = dbCursor.fetchall()       
        itemNum = 1
        for record in result:
            print("Item Number: ", itemNum)
            print("Title: ", record[0], )
            print("Author: ", record[1], )
            print("Genre: ", record[2], )
            print("Release year: ", record[3])
            print("Availability: ", record[4], "\n")
            itemNum += 1
        print("Search completed")
        print(len(result), " results found")
        print("---------------------------------------")
        selectNum = input("To select book to borrow, Enter 1, else enter any other key to return to menu: ")
        if selectNum == "1":
            selectedBook = Library.selectBookbByItemNum(result)
            print(selectedBook, type(selectedBook))
            Library.confirmCheckOut(selectedBook)
        else:
            ui.ui.searchBookUI()


# old script
        #         # Select book to check-OUT / borrow
        # optionCheckOut = str(input("To check-out book by inputing item Number, Enter 1 \nTo check-out book by inputing title, Enter 2 \n else enter other key to return to Main page:  "))
        # if optionCheckOut == "1":  # check-out book by selecting item number of the list
        #     itemSelect = int(input("Enter Item Number to check-in book: "))
        #     if itemSelect < itemNum:
        #         resultBookTitle = list(map(lambda x: x[1], result))  # map function to select title from tuple and list it
        #         checkOutBookTitle = resultBookTitle[itemSelect - 1]
        #         resultBookAuthor = list(map(lambda x: x[2], result))
        #         checkOutBookAuthor = resultBookAuthor[itemSelect - 1]
        #         print("Confirm Book to check-out: ")
        #         print("Title: ", checkOutBookTitle)
        #         print("Author: ", checkOutBookAuthor)
        #         confirmCheckOut = input("Type uppercase 'Y' to confirm, or other key to return to main page: ")
        #         if confirmCheckOut == "Y":
        #             Library.borrowBook(checkOutBookTitle)
        # elif optionCheckOut == "2": 
        #     checkOutBookTitle1 = input("Enter Book Title to check-Out")
        #     Library.borrowBook(checkOutBookTitle1)
        # else:
        #     ui.ui.searchBookUI()




    def selectBookByAuthor(author: str):
        sql = """
                SELECT title, author, genre, releaseYear,
                CASE 
                    WHEN borrowDate IS NULL THEN 'Available'
                    WHEN isReturn = 'Yes' THEN 'Available'
                    ELSE 'Borrowed'
                END AS Availability
                FROM book_list
                LEFT JOIN borrow_record ON book_list.title = borrow_record.bookTitle
                WHERE author like %s
                """
        val = ('%'+author+'%',)
        dbConn1 = dbConn.libDB
        dbCursor = dbConn1.cursor()
        dbCursor.execute(sql,val)
        result = dbCursor.fetchall()
   
        itemNum = 1
        for record in result:
            print("Item Number: ", itemNum)
            print("Title: ", record[0], )
            print("Author: ", record[1], )
            print("Genre: ", record[2], )
            print("Release year: ", record[3])
            print("Availability: ", record[4], "\n")
            itemNum += 1
        print("Search completed")
        print(len(result), " results found")
        print("---------------------------------------")
        selectNum = input("To select book to borrow, Enter 1, else enter any other key to return to menu: ")
        if selectNum == "1":
            selectedBook = Library.selectBookbByItemNum(result)
            print(selectedBook, type(selectedBook))
            Library.confirmCheckOut(selectedBook)
        else:
            ui.ui.searchBookUI()


    def selectBookByGenre(genre: str):
        sql = """
                SELECT title, author, genre, releaseYear,
                CASE 
                    WHEN borrowDate IS NULL THEN 'Available'
                    WHEN isReturn = 'Yes' THEN 'Available'
                    ELSE 'Borrowed'
                END AS Availability
                FROM book_list
                LEFT JOIN borrow_record ON book_list.title = borrow_record.bookTitle
                WHERE genre like %s
                """
        val = ('%'+genre+'%',)
        dbConn1 = dbConn.libDB
        dbCursor = dbConn1.cursor()
        dbCursor.execute(sql,val)
        result = dbCursor.fetchall()
   
        itemNum = 1
        for record in result:
            print("Item Number: ", itemNum)
            print("Title: ", record[0], )
            print("Author: ", record[1], )
            print("Genre: ", record[2], )
            print("Release year: ", record[3])
            print("Availability: ", record[4], "\n")
            itemNum += 1
        print("Search completed")
        print(len(result), " results found")
        print("---------------------------------------")
        selectNum = input("To select book to borrow, Enter 1, else enter any other key to return to menu: ")
        if selectNum == "1":
            selectedBook = Library.selectBookbByItemNum(result)
            print(selectedBook, type(selectedBook))
            Library.confirmCheckOut(selectedBook)
        else:
            ui.ui.searchBookUI()




    def selectBookByreleaseYear(releaseYear: str):
            sql = """
                SELECT title, author, genre, releaseYear,
                CASE 
                    WHEN borrowDate IS NULL THEN 'Available'
                    WHEN isReturn = 'Yes' THEN 'Available'
                    ELSE 'Borrowed'
                END AS Availability
                FROM book_list
                LEFT JOIN borrow_record ON book_list.title = borrow_record.bookTitle
                WHERE releaseYear like %s
                """
            val = ('%'+releaseYear+'%',)
            dbConn1 = dbConn.libDB
            dbCursor = dbConn1.cursor()
            dbCursor.execute(sql,val)
            result = dbCursor.fetchall()
    
            itemNum = 1
            for record in result:
                print("Item Number: ", itemNum)
                print("Title: ", record[0], )
                print("Author: ", record[1], )
                print("Genre: ", record[2], )
                print("Release year: ", record[3])
                print("Availability: ", record[4], "\n")
                itemNum += 1
            print("Search completed")
            print(len(result), " results found")
            print("---------------------------------------")
            selectNum = input("To select book to borrow, Enter 1, else enter any other key to return to menu: ")
            if selectNum == "1":
                selectedBook = Library.selectBookbByItemNum(result)
                print(selectedBook, type(selectedBook))
                Library.confirmCheckOut(selectedBook)
            else:
                ui.ui.searchBookUI()


    def selectBookAvailable():
        sql = """
                SELECT title, author, genre, releaseYear,
                CASE 
                    WHEN borrowDate IS NULL THEN 'Available'
                    WHEN isReturn = 'Yes' THEN 'Available'
                    ELSE 'Borrowed'
                END AS Availability
                FROM book_list
                LEFT JOIN borrow_record ON book_list.title = borrow_record.bookTitle
                WHERE (borrowDate IS NULL OR isReturn = 'Yes')
                
                """
        dbConn1 = dbConn.libDB
        dbCursor = dbConn1.cursor()
        dbCursor.execute(sql)
        result = dbCursor.fetchall()
        itemNum = 1
        for record in result:
            print("Item Number: ", itemNum)
            print("Title: ", record[0], )
            print("Author: ", record[1], )
            print("Genre: ", record[2], )
            print("Release year: ", record[3])
            print("Availability: ", record[4], "\n")
            itemNum += 1
        print("Search completed")
        print(len(result), " results found")
        print("---------------------------------------")
        selectNum = input("To select book to borrow, Enter 1, else enter any other key to return to menu: ")
        if selectNum == "1":
            selectedBook = Library.selectBookbByItemNum(result)
            print(selectedBook, type(selectedBook))
            Library.confirmCheckOut(selectedBook)
        else:
            ui.ui.searchBookUI()


        

    def selectBookBorrowed():
        sql = """
                SELECT title, author, genre, releaseYear,
                CASE 
                    WHEN borrowDate IS NULL THEN 'Available'
                    WHEN isReturn = 'Yes' THEN 'Available'
                    ELSE 'Borrowed'
                END AS Availability
                FROM book_list
                LEFT JOIN borrow_record ON book_list.title = borrow_record.bookTitle
                WHERE isReturn = 'No'
                
                """
        dbConn1 = dbConn.libDB
        dbCursor = dbConn1.cursor()
        dbCursor.execute(sql)
        result = dbCursor.fetchall()
        itemNum = 1
        for record in result:
            print("Item Number: ", itemNum)
            print("Title: ", record[0], )
            print("Author: ", record[1], )
            print("Genre: ", record[2], )
            print("Release year: ", record[3])
            print("Availability: ", record[4], "\n")
            itemNum += 1 
        print("Search completed")
        print(len(result), " results found")
        print("--------------------------------------- \n")


        selectNum = input("To select book to return, Enter 1, else enter any other key to return to menu: ")
        if selectNum == "1":
            selectedBook = Library.selectBookbByItemNum(result)
            print(selectedBook, type(selectedBook))
            Library.confirmCheckIn(selectedBook)
        else:
            ui.ui.searchBookUI()


    def selectBookbByItemNum(result: tuple):
        itemNum = len(result)
        itemSelect = int(input("Enter Item Number to select the book: "))
        if itemSelect <= itemNum:
            resultBookTitle = list(map(lambda x: x[0], result))  # map function to select title from tuple and list it
            selectedBookTitle = str(resultBookTitle[itemSelect - 1])
            resultBookAuthor = list(map(lambda x: x[1], result))
            selectedBookAuthor = resultBookAuthor[itemSelect - 1]
            print(selectedBookTitle, " by ", selectedBookAuthor, " selected")
            # selectedBook1 = [selectedBookTitle, selectedBookAuthor]
            return selectedBookTitle


    def confirmCheckOut(selectedBookCheckOut: str):
        print("Enter 'Y' to confirm, or enter any key to cancel and return to menu: ")
        confirmCheckOut1 = input()
        bookTitle = str(selectedBookCheckOut)
        if confirmCheckOut1 == "Y":
            Library.borrowBook(bookTitle)
        else:
            print("Press enter to Return to menu")
            input()
            ui.ui.searchBookUI()
        
    def confirmCheckIn(selectedBookCheckIn: str):
        print("Enter 'Y' to confirm return book, or enter any key to cancel and return to menu: ")
        confirmCheckOut1 = input()
        bookTitle = str(selectedBookCheckIn)
        if confirmCheckOut1 == "Y":
            Library.returnBook(bookTitle)
        else:
            print("Press enter to Return to menu")
            input()
            ui.ui.searchBookUI()

        