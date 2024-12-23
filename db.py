import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Підключення до бази даних
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cursor = conn.cursor()


def create_user_data(chat_id, user_data):
    user_info = user_data[chat_id]
    cursor.execute(
        """
        INSERT INTO user_data (user_id, username, user_firstname, user_lastname, gender, weight, height, age, activity_level, target, calories)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            chat_id,
            user_info.get("username", ""),
            user_info.get("user_firstname", ""),
            user_info.get("user_lastname", ""),
            user_info["gender"],
            user_info["weight"],
            user_info["height"],
            user_info["age"],
            user_info["activity_level"],
            user_info["target"],
            user_info["calories"]
        )
    )
    conn.commit()


def update_user_data(chat_id, user_data):
    user_info = user_data[chat_id]
    cursor.execute(
        """
        UPDATE user_data
        SET username = %s,
            user_firstname = %s,
            user_lastname = %s,
            gender = %s,
            weight = %s,
            height = %s,
            age = %s,
            activity_level = %s,
            target = %s,
            calories = %s
        WHERE user_id = %s
        """,
        (
            user_info.get("username", ""),
            user_info.get("user_firstname", ""),
            user_info.get("user_lastname", ""),
            user_info["gender"],
            user_info["weight"],
            user_info["height"],
            user_info["age"],
            user_info["activity_level"],
            user_info["target"],
            user_info["calories"],
            chat_id
        )
    )
    conn.commit()


def user_exists(chat_id):
    cursor.execute(
        """
        SELECT 1 FROM user_data WHERE user_id = %s
        """,
        (chat_id,)
    )
    return cursor.fetchone() is not None


def get_user_calories(chat_id):
    cursor.execute(
        """
        SELECT calories
        FROM user_data
        WHERE user_id = %s
        """,
        (chat_id,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def close_db():
    cursor.close()
    conn.close()
