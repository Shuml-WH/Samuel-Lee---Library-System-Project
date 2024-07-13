import mysql.connector as Conn


try:
    libDB = Conn.connect(
      host="localhost",
      user="root",
      password="stw1321a",
      database="testdb"
    
    )
except Conn.Error as e:
    print("SQL connector error: {}", format(e))
