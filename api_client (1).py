import requests

API = "http://127.0.0.1:8000"


def add_book():
    print("\n--- Add Book ---")
    data = {
        "book_id": input("Book ID: "),
        "title": input("Title: "),
        "author": input("Author: "),
        "price": float(input("Price: "))
    }
    print(requests.post(f"{API}/add_book", json=data).json())

def view_books():
    print("\n--- Books ---")
    print(requests.get(f"{API}/view_books").json())

def search_book():
    print("\n--- Search Book ---")
    keyword = input("Enter Book ID or Title: ")
    print(requests.get(f"{API}/search_book", params={"keyword": keyword}).json())

def delete_book():
    print("\n--- Delete Book ---")
    book_id = input("Book ID: ")
    print(requests.delete(f"{API}/delete_book", params={"book_id": book_id}).json())


def update_book():
    print("\n--- Update Book ---")
    data = {
        "book_id": input("Book ID to Update: "),
        "title": input("New Title: "),
        "author": input("New Author: "),
        "price": float(input("New Price: "))
    }
    print(requests.put(f"{API}/update_book", json=data).json())



def add_customer():
    print("\n--- Add Customer ---")
    data = {
        "cust_id": input("Customer ID: "),
        "name": input("Name: ")
    }
    print(requests.post(f"{API}/add_customer", json=data).json())

def view_customers():
    print("\n--- Customers ---")
    print(requests.get(f"{API}/view_customers").json())


def update_customer():
    print("\n--- Update Customer ---")
    data = {
        "cust_id": input("Customer ID to Update: "),
        "name": input("New Name: ")
    }
    print(requests.put(f"{API}/update_customer", json=data).json())


def delete_customer():
    print("\n--- Delete Customer ---")
    cid = input("Customer ID: ")
    print(requests.delete(f"{API}/delete_customer", params={"cust_id": cid}).json())

def buy_book():
    print("\n--- Buy Book ---")
    cust = input("Customer ID: ")
    book = input("Book ID: ")
    print(requests.post(f"{API}/buy_book",
                        params={"cust_id": cust, "book_id": book}).json())


def menu():
    print("\n==============================")
    print("     BOOKSTORE MENU")
    print("==============================")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Delete Book")
    print("5. Update Book")
    print("6. Add Customer")
    print("7. View Customers")
    print("8. Update Customer")
    print("9. Delete Customer")
    print("10. Buy Book")
    print("11. Exit")
    print("==============================")

def main():
    while True:
        menu()
        choice = input("Choice (1-11): ")

        if choice == "1": add_book()
        elif choice == "2": view_books()
        elif choice == "3": search_book()
        elif choice == "4": delete_book()
        elif choice == "5": update_book()
        elif choice == "6": add_customer()
        elif choice == "7": view_customers()
        elif choice == "8": update_customer()
        elif choice == "9": delete_customer()
        elif choice == "10": buy_book()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

    input("\nPress ENTER to close...")

if __name__ == "__main__":
    main()

