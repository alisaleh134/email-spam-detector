import sqlite3


DATABASE_NAME = "spam_detector.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            prediction TEXT NOT NULL,
            spam_probability REAL NOT NULL,
            probability_level TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_prediction(message, prediction, spam_probability, probability_level):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            message,
            prediction,
            spam_probability,
            probability_level
        )
        VALUES (?, ?, ?, ?)
    """, (
        message,
        prediction,
        spam_probability,
        probability_level
    ))

    connection.commit()
    connection.close()


def get_predictions():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT message, prediction, spam_probability,
               probability_level, created_at
        FROM predictions
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    connection.close()

    return predictions


def get_statistics():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE prediction = 'spam'
    """)
    spam = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE prediction = 'ham'
    """)
    ham = cursor.fetchone()[0]

    connection.close()

    return total, spam, ham


def clear_predictions():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM predictions")

    connection.commit()
    connection.close()


# Create database/table
create_database()