from datetime import datetime, timedelta


class Author:
    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality

    def __str__(self):
        return f"{self.name} ({self.nationality})"

class Book:
    def __init__(self, title, author, publication_date):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.is_borrowed = False

    def __str__(self):
        return f"'{self.title}' by {self.author} (Published: {self.publication_date})"


class Patron:
    def __init__(self, name):
        self.name = name
        self.borrowing_history = []
        self.current_loans = []

    def __str__(self):
        return self.name
class Library:
    def __init__(self):
        self.books = [] 
        self.authors = []
        self.patrons = []

    def add_author(self, name, nationality):
        if any(author.name == name for author in self.authors):
            raise ValueError(f"Author '{name}' already exists.")
        author = Author(name, nationality)
        self.authors.append(author)
        return author

    def add_book(self, title, author_name, publication_date):
        if any(book.title == title for book in self.books):
            raise ValueError(f"Book '{title}' already exists in the library.")
        author = next((a for a in self.authors if a.name == author_name), None)
        if not author:
            raise ValueError(f"Author '{author_name}' not found. Please add the author first.")
        book = Book(title, author, publication_date)
        self.books.append(book)
    def add_patron(self, name):
        if any(patron.name == name for patron in self.patrons):
            raise ValueError(f"Patron '{name}' already exists.")
        patron = Patron(name)
        self.patrons.append(patron)
        return patron
    def loan_book(self, book_title, patron_name, loan_days=14):
        book = next((b for b in self.books if b.title == book_title and not b.is_borrowed), None)
        if not book:
            raise ValueError(f"Book '{book_title}' is either not available or currently borrowed.")
        patron = next((p for p in self.patrons if p.name == patron_name), None)
        if not patron:
            raise ValueError(f"Patron '{patron_name}' not found.")
        
        due_date = datetime.now() + timedelta(days=loan_days)
        loan_record = {
            "book": book,
            "loan_date": datetime.now(),
            "due_date": due_date
        }
        patron.current_loans.append(loan_record)
        patron.borrowing_history.append(loan_record)
        book.is_borrowed = True
        print(f"Book '{book_title}' loaned to {patron_name} until {due_date.date()}.")
    def return_book(self, book_title, patron_name):
        patron = next((p for p in self.patrons if p.name == patron_name), None)
        if not patron:
            raise ValueError(f"Patron '{patron_name}' not found.")
        loan_record = next((l for l in patron.current_loans if l["book"].title == book_title), None)
        if not loan_record:
            raise ValueError(f"Book '{book_title}' is not currently borrowed by {patron_name}.")
        
        patron.current_loans.remove(loan_record)
        loan_record["book"].is_borrowed = False
        print(f"Book '{book_title}' returned by {patron_name}.")

    def query_books(self):
        return self.books
    def query_authors(self):
        return self.authors

    def query_patrons(self):
        return [{"name": patron.name, "current_loans": len(patron.current_loans)} for patron in self.patrons]

    def check_overdue_loans(self):
        overdue_loans = []
        for patron in self.patrons:
            for loan in patron.current_loans:
                if loan["due_date"] < datetime.now():
                    overdue_loans.append({
                        "patron": patron.name,
                        "book": loan["book"].title,
                        "due_date": loan["due_date"]
                    })
        return overdue_loans
# Example usage:
library = Library()

# Add authors
library.add_author("J.K. Rowling", "British")
library.add_author("Miguel de Cervantes", "Spanish")
library.add_author("Rosalía de Castro", "Spanish")

# Add books
library.add_book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "1997")
library.add_book("El Quijote", "Miguel de Cervantes", "1605")
library.add_book("Cantares Gallegos", "Rosalía de Castro", "1863")
# Add patrons
library.add_patron("Maria")
library.add_patron("Luis")
# Loan books
library.loan_book("Harry Potter and the Sorcerer's Stone", "Maria")

# Querying
print("Books in Library:")
for book in library.query_books():
    print(book)
print("\nAuthors in Library:")
for author in library.query_authors():
    print(author)

print("\nPatrons in Library:")
for patron in library.query_patrons():
    print(patron)

#Overdue loans
print("\n Overdue Loans:")
overdue_loans = library.check_overdue_loans()
if overdue_loans:
    for overdue in overdue_loans:
        print(f"{overdue['patron']} has an overdue Book: '{overdue['book']}' (Due: {overdue['due_date'].date()})")
else:
    print("No Overdue loans.")
#Return Books
library.return_book("Harry Potter and the Sorcerer's Stone", "Maria")
