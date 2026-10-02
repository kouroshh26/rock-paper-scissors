import sqlite3


def get_connection():
    connection = sqlite3.connect("game.db")
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_score INTEGER,
            computer_score INTEGER,
            winner TEXT
        )
    """)

    connection.commit()
    connection.close()

def save_game(user_score, computer_score, winner, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO games(user_score, computer_score, winner, status)
        VALUES(?, ?, ?, ?)
    """, (user_score, computer_score, winner, status))

    connection.commit()
    connection.close()

def get_games():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM games
        WHERE status = ?
    """,("finished",))

    games = cursor.fetchall()

    connection.close()

    return games

def delete_game(game_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM games
        WHERE id = ?
    """, (game_id,))

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted

def delete_all_games():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM games
    """)

    connection.commit()
    connection.close()

def add_status_column():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        ALTER TABLE games
        ADD COLUMN status TEXT
    """)

    connection.commit()
    connection.close()

def update_old_games_status():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE games
        SET status = ?
        WHERE status IS NULL
    """, ("finished",))

    connection.commit()
    connection.close()

def get_saved_game():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM games
        WHERE status = ?
        ORDER BY id DESC
        LIMIT 1
    """, ("playing",))

    game = cursor.fetchone()

    connection.close()

    return game

def update_game(game_id, user_score, computer_score, winner, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE games
        SET user_score = ?,
            computer_score = ?,
            winner = ?,
            status = ?
        WHERE id = ?
    """, (user_score, computer_score, winner, status, game_id))

    connection.commit()
    connection.close()

def cancel_active_game():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE games
        SET status = ?
        WHERE status = ?
    """,("cancelled", "playing"))

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    saved_game = get_saved_game()
    print(saved_game)
    games = get_games()
    print(games)