from fastapi import FastAPI, Query
from pydantic import BaseModel
import os

app = FastAPI(
    title="Bookstore API",
    description="Bookstore management with TXT file storage.",
    version="1.0.0"
)

BOOK_FILE = "books.txt"
CUSTOMER_FILE = "customers.txt"


def ensure_files():
    for file in [BOOK_FILE, CUSTOMER_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                pass

ensure_files()


class Book(BaseModel):
    book_id: str
    title: str
    author: str
    price: float

class Customer(BaseModel):
    cust_id: str
    name: str


def read_books():
    books = []
    with open(BOOK_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("|")
                if len(parts) == 4:
                    book_id, title, author, price = parts
                    books.append({
                        "book_id": book_id,
                        "title": title,
                        "author": author,
                        "price": float(price)
                    })
    return books

def write_books(books):
    with open(BOOK_FILE, "w") as f:
        for b in books:
            f.write(f"{b['book_id']}|{b['title']}|{b['author']}|{b['price']}\n")

def read_customers():
    customers = []
    with open(CUSTOMER_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("|")
                if len(parts) == 2:
                    cust_id, name = parts
                    customers.append({
                        "cust_id": cust_id,
                        "name": name
                    })
    return customers

def write_customers(customers):
    with open(CUSTOMER_FILE, "w") as f:
        for c in customers:
            f.write(f"{c['cust_id']}|{c['name']}\n")




@app.post("/add_book")
def add_book(book: Book):
    books = read_books()
    books.append(book.dict())
    write_books(books)
    return {"message": "Book added", "total": len(books)}


@app.get("/view_books")
def view_books():
    return {"books": read_books()}


@app.get("/search_book")
def search_book(keyword: str = Query(...)):
    books = read_books()
    matches = [b for b in books if keyword.lower() in b["title"].lower()
               or keyword == b["book_id"]]
    return {"matches": matches, "found": len(matches)}


@app.delete("/delete_book")
def delete_book(book_id: str = Query(...)):
    books = read_books()
    updated = [b for b in books if b["book_id"] != book_id]

    if len(updated) == len(books):
        return {"message": "Book NOT found"}

    write_books(updated)
    return {"message": "Book deleted", "remaining": len(updated)}


@app.put("/update_book")
def update_book(book: Book):
    books = read_books()
    for b in books:
        if b["book_id"] == book.book_id:
            b.update(book.dict())
            write_books(books)
            return {"message": "Book updated successfully"}
    return {"error": "Book not found"}


@app.post("/add_customer")
def add_customer(cust: Customer):
    customers = read_customers()
    customers.append(cust.dict())
    write_customers(customers)
    return {"message": "Customer added", "total": len(customers)}


@app.get("/view_customers")
def view_customers():
    return {"customers": read_customers()}


@app.put("/update_customer")
def update_customer(cust: Customer):
    customers = read_customers()
    for c in customers:
        if c["cust_id"] == cust.cust_id:
            c.update(cust.dict())
            write_customers(customers)
            return {"message": "Customer updated successfully"}
    return {"error": "Customer not found"}


@app.delete("/delete_customer")
def delete_customer(cust_id: str = Query(...)):
    customers = read_customers()
    updated = [c for c in customers if c["cust_id"] != cust_id]

    if len(updated) == len(customers):
        return {"message": "Customer NOT found"}

    write_customers(updated)
    return {"message": "Customer deleted", "remaining": len(updated)}


@app.post("/buy_book")
def buy_book(cust_id: str = Query(...), book_id: str = Query(...)):
    customers = read_customers()
    books = read_books()

    cust = next((c for c in customers if c["cust_id"] == cust_id), None)
    book = next((b for b in books if b["book_id"] == book_id), None)

    if not cust:
        return {"error": "Customer not found"}
    if not book:
        return {"error": "Book not found"}

    return {"message": "Purchase successful", "customer": cust, "book": book}


