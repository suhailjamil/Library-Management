from database import Database
import logging


class BookOperations:
    def __init__(self):
        self.db = Database()

    def add_book(self, title, author, isbn, quantity):
        self.db.connect()
        query = "INSERT INTO books (title, author, isbn, quantity) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (title, author, isbn, quantity))
        self.db.disconnect()
        logging.info(f"Added book: {title} by {author}")

    def update_book(self, book_id, title, author, isbn, quantity):
        self.db.connect()
        query = "UPDATE books SET title=?, author=?, isbn=?, quantity=? WHERE book_id=?"
        self.db.execute_query(query, (title, author, isbn, quantity, book_id))
        self.db.disconnect()
        logging.info(f"Updated book ID: {book_id}")

    def delete_book(self, book_id):
        self.db.connect()
        query = "DELETE FROM books WHERE book_id=?"
        self.db.execute_query(query, (book_id,))
        self.db.disconnect()
        logging.info(f"Deleted book ID: {book_id}")

    def search_books(self, keyword):
        self.db.connect()
        query = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?"
        result = self.db.fetch_all(
            query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        self.db.disconnect()
        return result

    def get_all_books(self):
        self.db.connect()
        query = "SELECT * FROM books"
        result = self.db.fetch_all(query)
        self.db.disconnect()
        return result
