import sqlite3

class Database:
    """Handles database functions"""
    
    def __init__(self) -> None:
        self.connection = sqlite3.connect("rps_users.db")
        self.cursor = self.connection.cursor()
        self.create_database()

    def create_database(self):
        query = """CREATE TABLE IF NOT EXISTS users (user_id INTEGER, wins INTEGER, losses INTEGER, 
                    ties INTEGER, winstreak INTEGER, rock INTEGER, paper INTEGER, scissors INTEGER, UNIQUE(user_id))"""
        self.cursor.execute(query)

    def add_user(self, *args: int) -> None:
        for user in args:
            try:
                print(user)
                query = "INSERT INTO users VALUES (?, 0, 0, 0, 0, 0, 0, 0)"
                self.cursor.execute(query, (user,))
                self.connection.commit()
            except sqlite3.IntegrityError:
                pass

    def update_win_loss(self, winner: int, loser: int) -> None:
        win_query = 'UPDATE users SET wins = wins + 1 WHERE user_id = ?'
        streak_query = 'UPDATE users SET winstreak = winstreak + 1 WHERE user_id = ?'
        loss_query = 'UPDATE users SET losses = losses + 1 WHERE user_id = ?'
        self.cursor.execute(win_query, (winner,))
        self.cursor.execute(streak_query, (winner,))
        self.cursor.execute(loss_query, (loser,))
        self.connection.commit()
    
    def update_losses(self, *args: int) -> None:
        loss_query = 'UPDATE users SET losses = losses + 1 WHERE user_id = ?'
        
        for user in args:
            self.cursor.execute(loss_query, (user,))
        self.connection.commit()

