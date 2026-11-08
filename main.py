from pet import add_pet, view_pets, search_pet, update_pet, delete_pet
from adopter import add_adopter, view_adopters, search_adopter, update_adopter, delete_adopter
from adoption import submit_request, view_requests, review_request

while True:
    print("\n===== PET ADOPTION MANAGEMENT SYSTEM =====")
    print("1. Pet Management")
    print("2. Adopter Management")
    print("3. Adoption Requests")
    print("4. Exit")
    choice=input("Enter your choice: ")
    if choice=="1":
        while True:
            print("\n--- PET MANAGEMENT ---")
            print("1. Add Pet")
            print("2. View Pets")
            print("3. Search Pet")
            print("4. Update Pet")
            print("5. Delete Pet")
            print("6. Back to Main Menu")
            ch=input("Enter your choice: ")
            if ch=="1":
                add_pet()
            elif ch=="2":
                view_pets()
            elif ch=="3":
                search_pet()
            elif ch=="4":
                update_pet()
            elif ch=="5":
                delete_pet()
            elif ch=="6":
                break
            else:
                print("Invalid choice!")
    elif choice=="2":
        while True:
            print("\n--- ADOPTER MANAGEMENT ---")
            print("1. Add Adopter")
            print("2. View Adopters")
            print("3. Search Adopter")
            print("4. Update Adopter")
            print("5. Delete Adopter")
            print("6. Back to Main Menu")
            ch=input("Enter your choice: ")
            if ch=="1":
                add_adopter()
            elif ch=="2":
                view_adopters()
            elif ch=="3":
                search_adopter()
            elif ch=="4":
                update_adopter()
            elif ch=="5":
                delete_adopter()
            elif ch=="6":
                break
            else:
                print("Invalid choice!")
    elif choice=="3":
        while True:
            print("\n--- ADOPTION REQUESTS ---")
            print("1. Submit Request")
            print("2. View Requests")
            print("3. Review Request")
            print("4. Back to Main Menu")
            ch=input("Enter your choice: ")
            if ch=="1":
                submit_request()
            elif ch=="2":
                view_requests()
            elif ch=="3":
                review_request()
            elif ch=="4":
                break
            else:
                print("Invalid choice!")
    elif choice=="4":
        print("Thank you for using the Pet Adoption Management System!")
        break
    else:
        print("Invalid choice! Please try again.")