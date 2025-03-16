import sqlite3
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Database:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info("Connected to the database successfully.")
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            logging.info("Disconnected from the database.")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error executing query: {e}")
            self.conn.rollback()

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching data: {e}")
            return []

    def create_tables(self):
        books_table = """
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            quantity INTEGER NOT NULL
        )
        """
        members_table = """
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            join_date DATE
        )
        """
        transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            borrow_date DATE,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES books (book_id),
            FOREIGN KEY (member_id) REFERENCES members (member_id)
        )
        """
        self.execute_query(books_table)
        self.execute_query(members_table)
        self.execute_query(transactions_table)
        logging.info("Tables created successfully.")
