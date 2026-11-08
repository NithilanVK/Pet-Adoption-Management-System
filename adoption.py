import sqlite3
from datetime import date

def connectDB():
    con=sqlite3.connect("pet_adoption.db")
    con.execute("PRAGMA foreign_keys = ON")
    return con

def submit_request():
    con=None
    try:
        pet_id=int(input("Enter pet ID: "))
        adopter_id=int(input("Enter adopter ID: "))
        con=connectDB()
        cursor=con.cursor()
        cursor.execute(
            "SELECT name, adoption_status FROM Pet WHERE pet_id = ?",
            (pet_id,)
        )
        pet=cursor.fetchone()
        if pet is None:
            print("Pet not found.")
            return
        if pet[1]!="Available":
            print("This pet is not available for adoption.")
            return
        cursor.execute(
            "SELECT name FROM Adopter WHERE adopter_id = ?",
            (adopter_id,)
        )
        adopter=cursor.fetchone()
        if adopter is None:
            print("Adopter not found.")
            return
        cursor.execute("""
            SELECT request_id FROM Adoption_Request
            WHERE pet_id = ? AND adopter_id = ?
            AND status = 'Pending'
        """, (pet_id, adopter_id))
        if cursor.fetchone():
            print("A pending request already exists for this pet and adopter.")
            return
        cursor.execute("""
            INSERT INTO Adoption_Request
            (pet_id, adopter_id, request_date, status)
            VALUES (?, ?, ?, 'Pending')
        """, (pet_id, adopter_id, date.today().isoformat()))
        con.commit()
        print("Adoption request submitted successfully!")
        print("Request ID:", cursor.lastrowid)
    except ValueError:
        print("Pet ID and adopter ID must be integers.")
    except sqlite3.Error as e:
        if con is not None:
            con.rollback()
        print("Database error:", e)
    finally:
        if con is not None:
            con.close()

def view_requests():
    con=connectDB()
    try:
        cursor=con.cursor()
        cursor.execute("""
            SELECT ar.request_id, p.name, a.name,
                   ar.request_date, ar.status
            FROM Adoption_Request ar
            JOIN Pet p ON ar.pet_id = p.pet_id
            JOIN Adopter a ON ar.adopter_id = a.adopter_id
            ORDER BY ar.request_id DESC
        """)
        requests=cursor.fetchall()
        if not requests:
            print("No adoption requests found.")
            return
        print("\n--- ADOPTION REQUESTS ---")
        for request in requests:
            print(
                f"Request ID: {request[0]} | "
                f"Pet: {request[1]} | "
                f"Adopter: {request[2]} | "
                f"Date: {request[3]} | "
                f"Status: {request[4]}"
            )
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        con.close()

def review_request():
    con=None
    try:
        request_id=int(input("Enter request ID to review: "))
        decision=input(
            "Enter decision (approve/reject): "
        ).strip().lower()
        if decision not in ("approve", "reject"):
            print("Invalid decision.")
            return
        con=connectDB()
        cursor=con.cursor()
        cursor.execute("BEGIN IMMEDIATE")
        cursor.execute("""
            SELECT pet_id, status
            FROM Adoption_Request
            WHERE request_id = ?
        """, (request_id,))
        
        request=cursor.fetchone()
        if request is None:
            print("Request not found.")
            con.rollback()
            return
        pet_id, status=request
        if status!="Pending":
            print("Only pending requests can be reviewed.")
            con.rollback()
            return
        if decision=="approve":
            cursor.execute("""
                SELECT adoption_status FROM Pet
                WHERE pet_id = ?
            """, (pet_id,))
            pet=cursor.fetchone()
            if pet is None or pet[0]!="Available":
                print("This pet is no longer available.")
                con.rollback()
                return
            cursor.execute("""
                UPDATE Pet
                SET adoption_status = 'Adopted'
                WHERE pet_id = ? AND adoption_status = 'Available'
            """, (pet_id,))
            if cursor.rowcount!=1:
                print("Could not approve: pet is unavailable.")
                con.rollback()
                return
            cursor.execute("""
                UPDATE Adoption_Request
                SET status = 'Approved'
                WHERE request_id = ?
            """, (request_id,))
            cursor.execute("""
                UPDATE Adoption_Request
                SET status = 'Rejected'
                WHERE pet_id = ?
                AND request_id != ?
                AND status = 'Pending'
            """, (pet_id, request_id))
            con.commit()
            print("Request approved! Pet status updated to Adopted.")
        else:
            cursor.execute("""
                UPDATE Adoption_Request
                SET status = 'Rejected'
                WHERE request_id = ?
            """, (request_id,))
            con.commit()
            print("Request rejected.")
    except ValueError:
        print("Request ID must be an integer.")
    except sqlite3.Error as e:
        if con is not None:
            con.rollback()
        print("Database error:", e)
    finally:
        if con is not None:
            con.close()

def main():
    while True:
        print("\n===== ADOPTION MANAGEMENT =====")
        print("1. Submit Adoption Request")
        print("2. View All Requests")
        print("3. Review Request")
        print("4. Exit")
        choice=input("Enter your choice: ").strip()
        if choice=="1":
            submit_request()
        elif choice=="2":
            view_requests()
        elif choice=="3":
            review_request()
        elif choice=="4":
            print("Exiting Adoption Management.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()