from database import Database
import logging
from datetime import date


class MemberOperations:
    def __init__(self):
        self.db = Database()

    def add_member(self, name, email):
        self.db.connect()
        query = "INSERT INTO members (name, email, join_date) VALUES (?, ?, ?)"
        self.db.execute_query(query, (name, email, date.today()))
        self.db.disconnect()
        logging.info(f"Added member: {name}")

    def update_member(self, member_id, name, email):
        self.db.connect()
        query = "UPDATE members SET name=?, email=? WHERE member_id=?"
        self.db.execute_query(query, (name, email, member_id))
        self.db.disconnect()
        logging.info(f"Updated member ID: {member_id}")

    def delete_member(self, member_id):
        self.db.connect()
        query = "DELETE FROM members WHERE member_id=?"
        self.db.execute_query(query, (member_id,))
        self.db.disconnect()
        logging.info(f"Deleted member ID: {member_id}")

    def search_members(self, keyword):
        self.db.connect()
        query = "SELECT * FROM members WHERE name LIKE ? OR email LIKE ?"
        result = self.db.fetch_all(query, (f"%{keyword}%", f"%{keyword}%"))
        self.db.disconnect()
        return result

    def get_all_members(self):
        self.db.connect()
        query = "SELECT * FROM members"
        result = self.db.fetch_all(query)
        self.db.disconnect()
        return result
