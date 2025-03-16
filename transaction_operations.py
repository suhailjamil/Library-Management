from database import Database
import logging
from datetime import date


class TransactionOperations:
    def __init__(self):
        self.db = Database()

    def borrow_book(self, book_id, member_id):
        self.db.connect()
        # Check if book is available
        query = "SELECT quantity FROM books WHERE book_id = ?"
        result = self.db.fetch_all(query, (book_id,))
        if result and result[0][0] > 0:
            # Update book quantity
            update_query = "UPDATE books SET quantity = quantity - 1 WHERE book_id = ?"
            self.db.execute_query(update_query, (book_id,))
            # Create transaction record
            insert_query = "INSERT INTO transactions (book_id, member_id, borrow_date) VALUES (?, ?, ?)"
            self.db.execute_query(
                insert_query, (book_id, member_id, date.today()))
            self.db.disconnect()
            logging.info(
                f"Book ID {book_id} borrowed by Member ID {member_id}")
            return True
        else:
            self.db.disconnect()
            logging.warning(
                f"Book ID {book_id} is not available for borrowing")
            return False

    def return_book(self, transaction_id):
        self.db.connect()
        # Get transaction details
        query = "SELECT book_id FROM transactions WHERE transaction_id = ? AND return_date IS NULL"
        result = self.db.fetch_all(query, (transaction_id,))
        if result:
            book_id = result[0][0]
            # Update book quantity
            update_book_query = "UPDATE books SET quantity = quantity + 1 WHERE book_id = ?"
            self.db.execute_query(update_book_query, (book_id,))
            # Update transaction record
            update_transaction_query = "UPDATE transactions SET return_date = ? WHERE transaction_id = ?"
            self.db.execute_query(update_transaction_query,
                                  (date.today(), transaction_id))
            self.db.disconnect()
            logging.info(
                f"Book ID {book_id} returned for Transaction ID {transaction_id}")
            return True
        else:
            self.db.disconnect()
            logging.warning(
                f"Invalid or already returned Transaction ID {transaction_id}")
            return False

    def get_borrowed_books(self):
        self.db.connect()
        query = """
        SELECT b.title, m.name, t.borrow_date
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN members m ON t.member_id = m.member_id
        WHERE t.return_date IS NULL
        """
        result = self.db.fetch_all(query)
        self.db.disconnect()
        return result

    def get_overdue_books(self, days_overdue=14):
        self.db.connect()
        query = """
        SELECT b.title, m.name, t.borrow_date, julianday('now') - julianday(t.borrow_date) as days_borrowed
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN members m ON t.member_id = m.member_id
        WHERE t.return_date IS NULL AND julianday('now') - julianday(t.borrow_date) > ?
        """
        result = self.db.fetch_all(query, (days_overdue,))
        self.db.disconnect()
        return result
