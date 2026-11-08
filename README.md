Pet Adoption Management System

A terminal-based Pet Adoption Management System developed using Python and SQLite to manage pet records, adopter information, and adoption requests.

About the Project

The Pet Adoption Management System is a database-driven Python application designed to simplify the process of managing pet adoption records.

It provides a structured way to maintain information about available pets, adopters, and adoption requests. SQLite is used as the database to store information persistently.

The project demonstrates Python programming concepts along with database connectivity and SQL operations.

Features

- **Pet Management:** Maintain pet details and adoption availability.
- **Adopter Management:** Store and manage adopter information.
- **Adoption Requests:** Record and manage adoption requests.
- **Database Integration:** Store application data using SQLite.
- **Adoption Status Tracking:** Track whether pets are available or adopted.
- **Request Status Management:** Maintain the status of adoption requests.

Technologies Used

- Programming Language: Python
- Database: SQLite
- Database Connectivity: Python `sqlite3` module
- Interface: Command-Line / Terminal Interface
- IDE: Visual Studio Code

Database Design

The application uses SQLite with the following main tables:

1. Pet
Stores information about pets.

- `pet_id`
- `name`
- `species`
- `breed`
- `age`
- `adoption_status`
- `fee`

2. Adopter
Stores information about people interested in adopting pets.

- `adopter_id`
- `name`
- `contact`
- `address`

3. Adoption_Request
Stores adoption request details.

- `request_id`
- `pet_id`
- `adopter_id`
- `request_date`
- `status`

The database uses primary keys and foreign keys to maintain relationships between tables.

Requirements

- Python 3.x
- SQLite3
- Any Python IDE or code editor (VS Code recommended)

How to Run

1. Clone or download this repository.
2. Extract the project folder.
3. Open the project folder in Visual Studio Code.
4. Ensure Python is installed.
5. Open the terminal in the project directory.
6. Run the main application Python file.

py main.py

Replace `main.py` with the actual name of your main application file if it is different.

The SQLite database is used to store application records.

Concepts Demonstrated

- Python Data Types
- Lists, Tuples, Sets and Dictionaries
- Functions and Modules
- Conditional Statements and Loops
- Exception Handling
- Database Connectivity
- SQL Queries (INSERT, SELECT, UPDATE, DELETE)
- Primary Keys and Foreign Keys
- Data Persistence using SQLite

## 🎯 Project
