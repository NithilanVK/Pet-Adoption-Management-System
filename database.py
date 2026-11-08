print("Database script started!")

import sqlite3

def connectDB():
    con=sqlite3.connect("pet_adoption.db")
    con.execute("PRAGMA foreign_keys = ON")
    return con

def createTables():
    con=connectDB()
    cursor=con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Pet(
                   pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   species TEXT NOT NULL,
                   breed TEXT,
                   age INTEGER,
                   gender TEXT,
                   vaccinated INTEGER DEFAULT 0,
                   adoption_status TEXT DEFAULT 'Available',
                   fee REAL DEFAULT 0.0)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Adopter(
                   adopter_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   phone TEXT NOT NULL,
                   email TEXT NOT NULL,
                   address TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Adoption_Request(
                   request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   pet_id INTEGER NOT NULL,
                   adopter_id INTEGER NOT NULL,
                   request_date TEXT NOT NULL,
                   status TEXT DEFAULT 'Pending',
                   FOREIGN KEY (pet_id) REFERENCES Pet(pet_id),
                   FOREIGN KEY (adopter_id) REFERENCES Adopter(adopter_id))""")
    con.commit()
    con.close()

if __name__=="__main__":
    createTables()
    print("Database and Tables are created!")