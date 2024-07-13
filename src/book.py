import src.dbConn as dbConn
from src import ui
from src import library

class Book:
    def __init__(self, title: str, author: str = None, genre:str = None, releaseYear: int = None):
        self.title = title
        self.author = author
        self.genre = genre
        self.releaseYear = releaseYear



    def addNewBook(self):
        dbBookTitle = self.title
        dbBookAuthor = self.author
        dbBookGenre = self.genre
        dbBookReleaseYear = self.releaseYear
        dbConn1 = dbConn.libDB
        try:
            dbCursor = dbConn1.cursor()
            sql = "INSERT INTO book_list (title, author, genre , releaseYear) VALUES (%s, %s, %s, %s)"
            val = (dbBookTitle, dbBookAuthor, dbBookGenre, dbBookReleaseYear)
            dbCursor.execute(sql, val)
            dbConn1.commit()
            print("Book added to database successfully")
        except dbConn.Conn.Error as e:
            print("SQL problem {}",format(e.msg))
            print("Cannot Add New book")
        finally:
            print("Press any key to return to menu")
            ui.ui.librarianUI()




    def checkBookExist(self):
        # return 0 if the book does not exist
        # Else return 1
        dbBookTitle = self.title 
        val = (dbBookTitle,)
        sql = "SELECT title, author FROM book_list WHERE title = %s"
        dbConn1 = dbConn.libDB
        dbCursor = dbConn1.cursor()
        dbCursor.execute(sql,val)
        result = dbCursor.fetchall()
        if dbCursor.rowcount == 0:
            return 0
        else:
            return 1


            



    def selectBorrowRecord(self):
        dbBookTitle = self.title
        val = (dbBookTitle)
        sql = "SELECT * FROM borrow_record WHERE bookTitle = %s"
        dbConn1 = dbConn.libDB
        try:
            dbCursor = dbConn1.cursor()
            dbCursor.execute(sql, val)
            result = dbCursor.fetchall()

            if dbCursor.rowcount == 0:
                print("No Result")
            else:
                for record in result:
                        print("Book Title: ", record[1], )
                        print("Borrowed Date: ", record[2], )
                        print("Returned Date: ", record[3], )
                        print("Book returned?: ", record[4], "\n")
                print("Search completed")

        except dbConn.Conn.Error as e:
            print("SQL Error: {}", format(e))



    def removeBook(self):
        checkBook = self.checkBookExist()
        if checkBook == 0:
            print(self.title, " does not exist in this Library")
        else:
            dbBookTitle = self.title
            sql = "DELETE FROM book_list WHERE title = %s"
            val = (dbBookTitle,)
            dbConn1 = dbConn.libDB
            try:
                dbCursor = dbConn1.cursor()
                dbCursor.execute(sql, val)
                dbConn1.commit()
                print("Successfully deleted", dbBookTitle)
            except dbConn.Conn.Error as e:
                print("SQL problem {}",format(e.msg))
                print("Cannot Delete book")


    def checkBookAvailability(self):
        # Return Null if book does not exist
        # Return 0 if book borrowed
        # Return 1 if book available
        checkBook = self.checkBookExist()
        if checkBook == 0:
            print(self.title, " does not exist in this Library")
        else:
            dbBookTitle = self.title
            val = (dbBookTitle,)
            sql = "SELECT isReturn FROM borrow_record WHERE bookTitle = %s ORDER BY borrowNum DESC LIMIT 1"
            dbConn1 = dbConn.libDB
            try:
                dbCursor = dbConn1.cursor()
                dbCursor.execute(sql, val)
                result = dbCursor.fetchone()

                if result is None or result[0] == "Yes":
                    return 1
                else:
                    return 0

            except dbConn.Conn.Error as e:
                print("SQL problem: {}".format(e.msg))




# old script


    # def selectBookByTitle(self):
    #     checkBook = self.checkBookExist()
    #     if checkBook == 0:
    #         print(self.title, " does not exist in this Library")
    #     else:
    #         dbBookTitle = self.title 
    #         val = (dbBookTitle,)
    #         sql = "SELECT * FROM book_list WHERE title = %s"
    #         dbConn1 = dbConn.libDB
    #         dbCursor = dbConn1.cursor()
    #         dbCursor.execute(sql,val)
    #         result = dbCursor.fetchall()

    #         itemNum = 1
    #         for record in result:
    #             print("Item Number: ", itemNum)
    #             print("Title: ", record[0], )
    #             print("Author: ", record[1], )
    #             print("Genre: ", record[2], )
    #             print("Release year: ", record[3])
    #             print("Availability: ", record[4], "\n")
    #             itemNum += 1
    #         print("Search completed")
    #         print(len(result), " results found")
    #         print("---------------------------------------")
    #                 # Select book to check-OUT / borrow
    #         optionCheckOut = str(input("To check-out book by inputing item Number, Enter 1 \nTo check-out book by inputing title, Enter 2 \n else enter other key to return to Main page:  "))
    #         if optionCheckOut == "1":  # check-out book by selecting item number of the list
    #             itemSelect = int(input("Enter Item Number to check-in book: "))
    #             if itemSelect < itemNum:
    #                 resultBookTitle = list(map(lambda x: x[0], result))  # map function to select title from tuple and list it
    #                 checkOutBookTitle = resultBookTitle[itemSelect - 1]
    #                 resultBookAuthor = list(map(lambda x: x[1], result))
    #                 checkOutBookAuthor = resultBookAuthor[itemSelect - 1]
    #                 print("Confirm Book to check-out: ") # to borrow book
    #                 print("Title: ", checkOutBookTitle)
    #                 print("Author: ", checkOutBookAuthor)
    #                 confirmCheckOut = input("Type uppercase 'Y' to confirm, or other key to return to main page: ")
    #                 if confirmCheckOut == "Y":
    #                     library.Library.borrowBook(checkOutBookTitle)
    #         elif optionCheckOut == "2": # check-in book by entering book title
    #             checkOutBookTitle1 = input("Enter Book Title to check-Out")
    #             library.Library.borrowBook(checkOutBookTitle1)
        
            # if not dbCursor.rowcount:
            #     print("No Result")
            # else:
            #     for record in result:
            #         print("Title: ", record[1], )
            #         print("Author: ", record[2], )
            #         print("Genre: ", record[3], )
            #         print("Release year: ", record[4], "\n")
            #         bookTitle = str(record[1])
            #         Book.checkBookAvailability(Book(bookTitle))
            #     print("Search completed")