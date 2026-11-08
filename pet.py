import sqlite3

def connectDB():
    return sqlite3.connect("pet_adoption.db")

def add_pet():
    name=input("Enter pet name: ").strip()
    species=input("Enter species (Dog/Cat/etc.): ").strip()
    breed=input("Enter breed: ").strip()
    try:
        age=int(input("Enter age in years: "))
        if age<0:
            print("Age cannot be negative.")
            return
        gender=input("Enter gender: ").strip()
        vaccinated_input=input("Vaccinated? (yes/no): ").strip().lower()
        if vaccinated_input not in ("yes", "no"):
            print("Enter yes or no.")
            return
        vaccinated=1 if vaccinated_input=="yes" else 0
        fee=float(input("Enter adoption fee: "))
        if fee<0:
            print("Fee cannot be negative.")
            return
        if not name or not species:
            print("Name and species are required.")
            return
        con=connectDB()
        cursor=con.cursor()
        cursor.execute("""
            INSERT INTO Pet (name, species, breed, age, gender, vaccinated, fee) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, species, breed, age, gender, vaccinated, fee))
        con.commit()
        print("Pet added successfully!")
        print("Generated Pet ID:", cursor.lastrowid)
        con.close()
    except ValueError:
        print("Invalid input. Enter a valid age and fee.")
    except sqlite3.Error as e:
        print("Database error:", e)

def view_pets():
    con=connectDB()
    cursor=con.cursor()
    cursor.execute("SELECT * FROM Pet")
    pets=cursor.fetchall()
    if not pets:
        print("No pets found.")
    else:
        print("\n--- PET LIST ---")
        for pet in pets:
            print(
                f"ID: {pet[0]} | Name: {pet[1]} | "
                f"Species: {pet[2]} | Breed: {pet[3]} | "
                f"Age: {pet[4]} | Gender: {pet[5]} | "
                f"Vaccinated: {'Yes' if pet[6] else 'No'} | "
                f"Status: {pet[7]} | Fee: Rs. {pet[8]:.2f}"
            )
    con.close()

def search_pet():
    try:
        pet_id = int(input("Enter pet ID to search: "))
        con=connectDB()
        cursor=con.cursor()
        cursor.execute(
            "SELECT * FROM Pet WHERE pet_id = ?", (pet_id,))
        pet=cursor.fetchone()
        con.close()
        if pet:
            print("\nPet found:")
            print("ID:", pet[0])
            print("Name:", pet[1])
            print("Species:", pet[2])
            print("Breed:", pet[3])
            print("Age:", pet[4])
            print("Gender:", pet[5])
            print("Vaccinated:", "Yes" if pet[6] else "No")
            print("Status:", pet[7])
            print("Fee: Rs.", pet[8])
        else:
            print("Pet not found.")
    except ValueError:
        print("Pet ID must be an integer.")
    except sqlite3.Error as e:
        print("Database error:", e)

def update_pet():
    try:
        pet_id=int(input("Enter pet ID to update: "))
        con=connectDB()
        cursor=con.cursor()
        cursor.execute(
            "SELECT * FROM Pet WHERE pet_id = ?", (pet_id,)
        )
        pet=cursor.fetchone()
        if not pet:
            print("Pet not found.")
            con.close()
            return
        print("Press Enter to keep an existing value.")
        name=input(f"Name [{pet[1]}]: ").strip() or pet[1]
        species=input(f"Species [{pet[2]}]: ").strip() or pet[2]
        breed=input(f"Breed [{pet[3] or ''}]: ").strip() or pet[3]
        age_input=input(f"Age [{pet[4]}]: ").strip()
        gender=input(f"Gender [{pet[5] or ''}]: ").strip() or pet[5]
        vaccinated_input=input(
            f"Vaccinated (yes/no) [{'yes' if pet[6] else 'no'}]: "
        ).strip().lower()
        fee_input=input(f"Fee [{pet[8]}]: ").strip()
        age=int(age_input) if age_input else pet[4]
        fee=float(fee_input) if fee_input else pet[8]
        if age<0 or fee<0:
            print("Age and fee cannot be negative.")
            con.close()
            return
        if vaccinated_input=="yes":
            vaccinated=1
        elif vaccinated_input=="no":
            vaccinated=0
        elif vaccinated_input=="":
            vaccinated=pet[6]
        else:
            print("Enter yes or no for vaccination.")
            con.close()
            return
        cursor.execute("""
            UPDATE Pet
            SET name = ?, species = ?, breed = ?, age = ?,
                gender = ?, vaccinated = ?, fee = ?
            WHERE pet_id = ?
        """, (name, species, breed, age, gender, vaccinated, fee, pet_id))
        con.commit()
        con.close()
        print("Pet updated successfully!")
    except ValueError:
        print("Invalid age, fee, or pet ID.")
    except sqlite3.Error as e:
        print("Database error:", e)

def delete_pet():
    try:
        pet_id=int(input("Enter pet ID to delete: "))
        con=connectDB()
        cursor=con.cursor()
        cursor.execute(
            "SELECT * FROM Pet WHERE pet_id = ?", (pet_id,)
        )
        pet=cursor.fetchone()
        if not pet:
            print("Pet not found.")
            con.close()
            return
        if pet[7]=="Adopted":
            print("An adopted pet cannot be deleted.")
            con.close()
            return
        confirm=input(
            f"Delete {pet[1]}? (yes/no): "
        ).strip().lower()
        if confirm=="yes":
            cursor.execute(
                "DELETE FROM Pet WHERE pet_id = ?", (pet_id,)
            )
            con.commit()
            print("Pet deleted successfully!")
        else:
            print("Deletion cancelled.")
        con.close()
    except ValueError:
        print("Pet ID must be an integer.")
    except sqlite3.Error as e:
        print("Database error:", e)

def main():
    while True:
        print("\n===== PET MANAGEMENT SYSTEM =====")
        print("1. Add Pet")
        print("2. View All Pets")
        print("3. Search Pet")
        print("4. Update Pet")
        print("5. Delete Pet")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice=="1":
            add_pet()
        elif choice=="2":
            view_pets()
        elif choice=="3":
            search_pet()
        elif choice=="4":
            update_pet()
        elif choice=="5":
            delete_pet()
        elif choice=="6":
            print("Exiting Pet Management System.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")

if __name__ == "__main__":
    main()