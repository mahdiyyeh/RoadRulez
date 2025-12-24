"""
Database Manager class to handle all SQLite database operations.
"""
import sqlite3


class DatabaseManager:
    """Manages all database operations for the application."""
    
    def __init__(self, db_path="userdatabase.db"):
        self.db_path = db_path
        self.conn = None
        self.cur = None
    
    def connect(self):
        """Establishes a connection to the database."""
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
    
    def close(self):
        """Closes the database connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        self.cur = None
        self.conn = None
    
    def create_tables(self):
        """Creates all required tables in the database if they don't exist."""
        self.connect()
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS Users
                        (username TEXT PRIMARY KEY,
                        name TEXT,
                        age INTEGER,
                        email TEXT,
                        password TEXT,
                        user_coins INTEGER)""")
            
            self.cur.execute("""CREATE TABLE IF NOT EXISTS Level_1_times
                        (id INTEGER PRIMARY KEY autoincrement,
                        username TEXT,
                        time REAL,
                        FOREIGN KEY (username) REFERENCES Users(username))""")
            
            self.cur.execute("""CREATE TABLE IF NOT EXISTS Level_2_times
                        (id INTEGER PRIMARY KEY autoincrement,
                        username TEXT,
                        time REAL,
                        FOREIGN KEY (username) REFERENCES Users(username))""")
            
            self.cur.execute("""CREATE TABLE IF NOT EXISTS Level_3_times
                        (id INTEGER PRIMARY KEY autoincrement,
                        username TEXT,
                        time REAL,
                        FOREIGN KEY (username) REFERENCES Users(username))""")
            self.conn.commit()
        finally:
            self.close()
    
    def delete_user_account(self, username):
        """Deletes a user account and all associated data."""
        self.connect()
        try:
            value = [username]
            self.cur.execute("""DELETE FROM Users WHERE username=?""", value)
            self.cur.execute("""DELETE FROM Level_1_times WHERE username=?""", value)
            self.cur.execute("""DELETE FROM Level_2_times WHERE username=?""", value)
            self.cur.execute("""DELETE FROM Level_3_times WHERE username=?""", value)
            self.conn.commit()
        finally:
            self.close()
    
    def get_level_leaderboard(self, level_num, username, sort_func):
        """Gets top 5 times for a specific level and user."""
        self.connect()
        try:
            value = [username]
            table_name = f"Level_{level_num}_times"
            self.cur.execute(f"""SELECT time FROM {table_name} WHERE username = ? ORDER BY id """, value)
            items = self.cur.fetchall()
            sorted_items = sort_func(items)
            top_5 = sorted_items[:5]
            return top_5
        finally:
            self.close()
    
    def get_l1_leaderboard(self, username, sort_func):
        """Gets Level 1 leaderboard for a user."""
        return self.get_level_leaderboard(1, username, sort_func)
    
    def get_l2_leaderboard(self, username, sort_func):
        """Gets Level 2 leaderboard for a user."""
        return self.get_level_leaderboard(2, username, sort_func)
    
    def get_l3_leaderboard(self, username, sort_func):
        """Gets Level 3 leaderboard for a user."""
        self.connect()
        try:
            value = [username]
            self.cur.execute("""SELECT time FROM Level_3_times WHERE username = ?""", value)
            items = self.cur.fetchall()
            sorted_items = sort_func(items)
            top_5 = sorted_items[:5]
            return top_5
        finally:
            self.close()
    
    def get_highscore(self, level_num, username, sort_func=None):
        """Gets the best (lowest) time for a specific level and user."""
        self.connect()
        try:
            value = [username]
            if level_num == 1:
                # Use aggregate function for level 1
                self.cur.execute("""SELECT min(time) FROM Level_1_times WHERE username = ?""", value)
                item = self.cur.fetchone()
                return item[0] if item[0] is not None else None
            else:
                table_name = f"Level_{level_num}_times"
                self.cur.execute(f"""SELECT time FROM {table_name} WHERE username = ? ORDER BY id """, value)
                items = self.cur.fetchall()
                if items and sort_func:
                    sorted_items = sort_func(items)
                    return sorted_items[0][0] if sorted_items else None
                return None
        finally:
            self.close()
    
    def insert_level_time(self, level_num, username, time):
        """Inserts a level completion time into the database."""
        self.connect()
        try:
            table_name = f"Level_{level_num}_times"
            value = [username, time]
            self.cur.execute(f"""INSERT INTO {table_name}(username, time) VALUES (?,?)""", value)
            self.conn.commit()
        finally:
            self.close()
    
    def insert_user(self, username, name, age, email, password, user_coins):
        """Inserts a new user into the database."""
        self.connect()
        try:
            value = [username, name, age, email, password, user_coins]
            self.cur.execute("""INSERT INTO Users VALUES (?,?,?,?,?,?)""", value)
            self.conn.commit()
        finally:
            self.close()
    
    def update_user_name(self, username, name):
        """Updates a user's name in the database."""
        self.connect()
        try:
            value = [name, username]
            self.cur.execute("""UPDATE Users SET name = ? WHERE username = ?""", value)
            self.conn.commit()
        finally:
            self.close()
    
    def update_user_coins(self, username, coins):
        """Updates a user's coin count in the database."""
        self.connect()
        try:
            value = [coins, username]
            self.cur.execute("""UPDATE Users SET user_coins = ? WHERE username = ?""", value)
            self.conn.commit()
        finally:
            self.close()
    
    def update_user_password(self, username, password):
        """Updates a user's password in the database."""
        self.connect()
        try:
            value = [password, username]
            self.cur.execute("""UPDATE Users SET password = ? WHERE username = ?""", value)
            self.conn.commit()
        finally:
            self.close()
    
    def get_user_details(self, username, password):
        """Gets user details for login verification."""
        self.connect()
        try:
            value = [username, password]
            self.cur.execute("""SELECT name, age, email, user_coins FROM Users WHERE username = ? AND password = ?""", value)
            item = self.cur.fetchone()
            return item
        finally:
            self.close()
    
    def check_username_exists(self, username):
        """Checks if a username already exists in the database."""
        self.connect()
        try:
            value = [username]
            self.cur.execute("""SELECT COUNT(*) FROM Users WHERE username = ?""", value)
            item = self.cur.fetchone()
            return item[0] > 0
        finally:
            self.close()
    
    def verify_login(self, username, password):
        """Verifies login credentials and returns user data if valid."""
        self.connect()
        try:
            value = [username, password]
            self.cur.execute("""SELECT username, password FROM Users WHERE username = ? AND password = ?""", value)
            item = self.cur.fetchone()
            return item
        finally:
            self.close()
