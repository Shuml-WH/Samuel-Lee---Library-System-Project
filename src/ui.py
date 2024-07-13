from src import library

class ui:
    def startUI():
        print("**************************************\n")
        print("Welcome to THe Library System")
        print("To search book, Enter 1")
        print("To borrow / check-out book, Enter 2")
        print("to return / check-in book, Enter 3")
        print("FOr Librarian config, Enter 4")
        print("To Exit this system, Enter 9")
        selectNum = int(input("Enter here : "))
        print("----------------------------------")
        try:
            if selectNum == 1:
                
                ui.searchBookUI()
            
            elif selectNum == 2:
                bookTitle = str(input("Enter title of the book to be borrowed, or type 0 to return : "))
                if bookTitle == "0":
                    ui.startUI()
                else:
                    library.Library.borrowBook(bookTitle)
            
            elif selectNum == 3:
                bookTitle = str(input("Enter title of the book to be returned, or type 0 to return : "))
                if bookTitle == "0":
                    ui.startUI()
                else:
                    library.Library.returnBook(bookTitle)
            
            elif selectNum == 4:
                ui.librarianUI()

            elif selectNum == 9:
                exit()
                
            else:
                print("Wrong input")
                ui.startUI()


        except TypeError as e:
            print("Error in your input, {} ", format(e))
            ui.startUI()


        except ValueError as e:
            print("Error in your input, {} ", format(e))
            ui.startUI()




    def searchBookUI():
        print("---------------------------------")
        print("Search book menu")
        print("To search book by book title, Enter 1")
        print("To search book by author, Enter 2")
        print("To search book by genre, Enter 3")
        print("To search book by release year, Enter 4 ")
        print("To search all available books, Enter 5")
        print("To search all books, Enter 6")
        print("To return to previous page, Enter any other number: ")
        selectNum1 = int(input("Enter here : "))
        print("----------------------------------")
        try:
            if selectNum1 == 1:
                searchTitle = str(input("Enter Book Title: "))
                # searchBook = library.book.Book(searchTitle)
                library.Library.selectBookByTitle(searchTitle)


            elif selectNum1 == 2:
                searchAuthor = str(input("Enter Author : "))
                library.Library.selectBookByAuthor(searchAuthor)


            elif selectNum1 == 3:
                searchGenre = str(input("Enter Genre : "))
                library.Library.selectBookByGenre(searchGenre)

            
            elif selectNum1 == 4:
                try:
                    searchReleaseYear = str(input("Enter Release Year : "))
                    library.Library.selectBookByreleaseYear(searchReleaseYear)
                except TypeError as e1:
                    print("Input Error: {}", format(e1))
                    ui.searchBookUI()
                
            elif selectNum1 == 5:
                library.Library.selectBookAvailable()


            elif selectNum1 == 6:
                library.Library.selectAllBook()
                
            else:
                ui.startUI()
            
        except TypeError as e:
            print("Error in your input, {} ", format(e))
            ui.startUI()
        


    def librarianUI():
        print("---------------------------------")
        print("Librarian Config menu")
        print("To add a book, Enter 1")
        print("To delete a book, Enter 2")
        print("To search all borrowed book, Enter 3")
        print("To return to main menu, Enter other number")
        selectNum2 = int(input("Enter here : "))
        print("----------------------------------")
        try:
            if selectNum2 == 1:
                newTitle = str(input("Enter new book title : "))
                newAuthor = str(input("Enter the author of the new book : "))
                newGenre = str(input("Enter the genre of the new book : "))
                newReleaseYear = str(input("Enter the release year of the new book : "))
                newBook = library.book.Book(newTitle, newAuthor, newGenre, newReleaseYear)
                newBook.addNewBook()

            elif selectNum2 == 2:
                delTitle = str(input("Enter title  of the bookto be deleted : "))
                delAuthor = str(input("Enter book author of the book to be deleted : "))
                delBook = library.book.Book(delTitle, delAuthor)
                checkBook = delBook.checkBookExist()
                if checkBook == 0:
                    print("This book does not exist in Library")
                    input("Press any key to return to Librarian Config menu")
                    ui.librarianUI()
                else:
                    delBook.removeBook()
                    

            elif selectNum2 == 3:
                library.Library.selectBookBorrowed()
                print("To check-in book, Enter 1")
                print("To return to menu, Enter 2")
                selectNum3 = int(input("Enter here : "))

            else:
                ui.startUI()


        except TypeError as e:
            print("Error in your input, {} ", format(e))
            ui.startUI()