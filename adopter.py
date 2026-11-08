import sqlite3

def connectDB():
    return sqlite3.connect("pet_adoption.db")

def add_adopter():
    name=input("Enter adopter name: ").strip()
    phone=input("Enter phone number: ").strip()
    email=input("Enter email: ").strip()
    address=input("Enter address: ").strip()
    if not name or not phone:
        print("Name and phone number are required.")
        return
    con=connectDB()
    cursor=con.cursor()
    try:
        cursor.execute("""
            INSERT INTO Adopter (name, phone, email, address)
            VALUES (?, ?, ?, ?)
        """, (name, phone, email, address))
        con.commit()
        print("Adopter registered successfully!")
        print("Adopter ID:", cursor.lastrowid)
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        con.close()

def view_adopters():
    con=connectDB()
    cursor=con.cursor()
    try:
        cursor.execute("SELECT * FROM Adopter")
        adopters=cursor.fetchall()
        if not adopters:
            print("No adopters registered yet.")
            return
        print("\n--- REGISTERED ADOPTERS ---")
        for adopter in adopters:
            print(
                f"ID: {adopter[0]} | Name: {adopter[1]} | "
                f"Phone: {adopter[2]} | Email: {adopter[3]} | "
                f"Address: {adopter[4]}"
            )
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        con.close()

def search_adopter():
    try:
        adopter_id=int(input("Enter adopter ID: "))
        con=connectDB()
        cursor=con.cursor()
        cursor.execute(
            "SELECT * FROM Adopter WHERE adopter_id = ?",
            (adopter_id,)
        )
        adopter=cursor.fetchone()
        if adopter:
            print("\nAdopter found:")
            print("ID:", adopter[0])
            print("Name:", adopter[1])
            print("Phone:", adopter[2])
            print("Email:", adopter[3])
            print("Address:", adopter[4])
        else:
            print("Adopter not found.")
    except ValueError:
        print("Adopter ID must be an integer.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if "con" in locals():
            con.close()

def update_adopter():
    try:
        adopter_id=int(input("Enter adopter ID to update: "))
        con=connectDB()
        cursor=con.cursor()
        cursor.execute(
            "SELECT * FROM Adopter WHERE adopter_id = ?",
            (adopter_id,)
        )
        adopter=cursor.fetchone()
        if not adopter:
            print("Adopter not found.")
            return
        print("Press Enter to retain the current value.")
        name=input(f"Name [{adopter[1]}]: ").strip() or adopter[1]
        phone=input(f"Phone [{adopter[2]}]: ").strip() or adopter[2]
        email=input(
            f"Email [{adopter[3] or ''}]: "
        ).strip() or adopter[3]
        address=input(
            f"Address [{adopter[4] or ''}]: "
        ).strip() or adopter[4]
        cursor.execute("""
            UPDATE Adopter
            SET name = ?, phone = ?, email = ?, address = ?
            WHERE adopter_id = ?
        """, (name, phone, email, address, adopter_id))
        con.commit()
        print("Adopter updated successfully!")
    except ValueError:
        print("Adopter ID must be an integer.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if "con" in locals():
            con.close()

def delete_adopter():
    try:
        adopter_id=int(input("Enter adopter ID to delete: "))
        con=connectDB()
        cursor=con.cursor()
        cursor.execute(
            "SELECT name FROM Adopter WHERE adopter_id = ?",
            (adopter_id,)
        )
        adopter=cursor.fetchone()
        if not adopter:
            print("Adopter not found.")
            return
        cursor.execute("""
            SELECT COUNT(*) FROM Adoption_Request
            WHERE adopter_id = ?
        """, (adopter_id,))
        request_count=cursor.fetchone()[0]
        if request_count>0:
            print("Cannot delete: this adopter has adoption requests.")
            return
        confirm=input(
            f"Delete adopter {adopter[0]}? (yes/no): "
        ).strip().lower()
        if confirm=="yes":
            cursor.execute(
                "DELETE FROM Adopter WHERE adopter_id = ?",
                (adopter_id,)
            )
            con.commit()
            print("Adopter deleted successfully!")
        else:
            print("Deletion cancelled.")
    except ValueError:
        print("Adopter ID must be an integer.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if "con" in locals():
            con.close()

def main():
    while True:
        print("\n===== ADOPTER MANAGEMENT =====")
        print("1. Register Adopter")
        print("2. View All Adopters")
        print("3. Search Adopter")
        print("4. Update Adopter")
        print("5. Delete Adopter")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice=="1":
            add_adopter()
        elif choice=="2":
            view_adopters()
        elif choice=="3":
            search_adopter()
        elif choice=="4":
            update_adopter()
        elif choice=="5":
            delete_adopter()
        elif choice=="6":
            print("Exiting Adopter Management.")
            break
        else:
            print("Invalid choice. Try again.")

            
if __name__ == "__main__":
    main()