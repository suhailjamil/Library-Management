from database import Database
from book_operations import BookOperations
from member_operations import MemberOperations
from transaction_operations import TransactionOperations
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class LibraryManagementSystem:
    def __init__(self):
        self.db = Database()
        self.book_ops = BookOperations()
        self.member_ops = MemberOperations()
        self.transaction_ops = TransactionOperations()

    def initialize_database(self):
        self.db.connect()
        self.db.create_tables()
        self.db.disconnect()

    def run(self):
        self.initialize_database()
        while True:
            print("\nLibrary Management System")
            print("1. Book Operations")
            print("2. Member Operations")
            print("3. Transaction Operations")
            print("4. Reports")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.book_menu()
            elif choice == '2':
                self.member_menu()
            elif choice == '3':
                self.transaction_menu()
            elif choice == '4':
                self.report_menu()
            elif choice == '5':
                print("Thank you for using the Library Management System!")
                break
            else:
                print("Invalid choice. Please try again.")

    def book_menu(self):
        while True:
            print("\nBook Operations")
            print("1. Add Book")
            print("2. Update Book")
            print("3. Delete Book")
            print("4. Search Books")
            print("5. View All Books")
            print("6. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                title = input("Enter book title: ")
                author = input("Enter author name: ")
                isbn = input("Enter ISBN: ")
                quantity = int(input("Enter quantity: "))
                self.book_ops.add_book(title, author, isbn, quantity)
            elif choice == '2':
                book_id = int(input("Enter book ID to update: "))
                title = input("Enter new title: ")
                author = input("Enter new author name: ")
                isbn = input("Enter new ISBN: ")
                quantity = int(input("Enter new quantity: "))
                self.book_ops.update_book(
                    book_id, title, author, isbn, quantity)
            elif choice == '3':
                book_id = int(input("Enter book ID to delete: "))
                self.book_ops.delete_book(book_id)
            elif choice == '4':
                keyword = input("Enter search keyword: ")
                results = self.book_ops.search_books(keyword)
                for book in results:
                    print(book)
            elif choice == '5':
                books = self.book_ops.get_all_books()
                for book in books:
                    print(book)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def member_menu(self):
        while True:
            print("\nMember Operations")
            print("1. Add Member")
            print("2. Update Member")
            print("3. Delete Member")
            print("4. Search Members")
            print("5. View All Members")
            print("6. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter member name: ")
                email = input("Enter member email: ")
                self.member_ops.add_member(name, email)
            elif choice == '2':
                member_id = int(input("Enter member ID to update: "))
                name = input("Enter new name: ")
                email = input("Enter new email: ")
                self.member_ops.update_member(member_id, name, email)
            elif choice == '3':
                member_id = int(input("Enter member ID to delete: "))
                self.member_ops.delete_member(member_id)
            elif choice == '4':
                keyword = input("Enter search keyword: ")
                results = self.member_ops.search_members(keyword)
                for member in results:
                    print(member)
            elif choice == '5':
                members = self.member_ops.get_all_members()
                for member in members:
                    print(member)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def transaction_menu(self):
        while True:
            print("\nTransaction Operations")
            print("1. Borrow Book")
            print("2. Return Book")
            print("3. View Borrowed Books")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                book_id = int(input("Enter book ID: "))
                member_id = int(input("Enter member ID: "))
                if self.transaction_ops.borrow_book(book_id, member_id):
                    print("Book borrowed successfully.")
                else:
                    print("Failed to borrow book.")
            elif choice == '2':
                transaction_id = int(input("Enter transaction ID: "))
                if self.transaction_ops.return_book(transaction_id):
                    print("Book returned successfully.")
                else:
                    print("Failed to return book.")
            elif choice == '3':
                borrowed_books = self.transaction_ops.get_borrowed_books()
                if borrowed_books:
                    print("\nBorrowed Books:")
                    for book in borrowed_books:
                        print(
                            f"Title: {book[0]}, Borrowed By: {book[1]}, Borrow Date: {book[2]}")
                else:
                    print("No books are currently borrowed.")
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def report_menu(self):
        while True:
            print("\nReports")
            print("1. View Overdue Books")
            print("2. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                days_overdue = int(
                    input("Enter number of days overdue (default is 14): ") or 14)
                overdue_books = self.transaction_ops.get_overdue_books(
                    days_overdue)
                if overdue_books:
                    print("\nOverdue Books:")
                    for book in overdue_books:
                        print(
                            f"Title: {book[0]}, Borrowed By: {book[1]}, Borrow Date: {book[2]}, Days Borrowed: {int(book[3])}")
                else:
                    print("No overdue books found.")
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    system = LibraryManagementSystem()
    system.run()
