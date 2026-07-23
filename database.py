import sqlite3
import hashlib
from datetime import datetime
import pandas as pd


DATABASE_NAME = "users.db"



# =========================
# DATABASE CONNECTION
# =========================

def get_connection():

    conn = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )

    return conn



# =========================
# CREATE TABLES
# =========================

def init_database():

    conn = get_connection()

    cursor = conn.cursor()


    # -------------------------
    # Users Table
    # -------------------------

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        email TEXT UNIQUE,

        password_hash TEXT,

        created_at TEXT

    )
    """
    )


    # -------------------------
    # Preferences Table
    # -------------------------

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS preferences (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE NOT NULL,

        budget INTEGER,

        priority TEXT,

        room_type TEXT,

        max_drive_time INTEGER,

        max_transit_time INTEGER,

        preferred_neighborhood  TEXT DEFAULT CURRENT_TIMESTAMP,

        updated_at TEXT,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """
    )


    # -------------------------
    # Favorites Table
    # -------------------------

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS favorites (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        listing_id INTEGER,

        saved_time TEXT,
        
        UNIQUE(user_id, listing_id),
        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """
    )


    conn.commit()

    conn.close()

    migrate_preferences_table()

# =========================
# PASSWORD HASH
# =========================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



# =========================
# CREATE USER
# =========================

def create_user(
    username,
    email,
    password
):

    conn = get_connection()

    cursor = conn.cursor()


    password_hash = hash_password(
        password
    )


    try:

        cursor.execute(
        """
        INSERT INTO users
        (
            username,
            email,
            password_hash,
            created_at
        )

        VALUES
        (?,?,?,?)

        """,

        (
            username,
            email,
            password_hash,
            datetime.now().isoformat()
        )

        )


        conn.commit()

        user_id = cursor.lastrowid


    except sqlite3.IntegrityError:

        user_id = None



    conn.close()


    return user_id



# =========================
# LOGIN USER
# =========================

def authenticate_user(
    username,
    password
):

    conn = get_connection()

    cursor = conn.cursor()


    password_hash = hash_password(
        password
    )


    cursor.execute(
    """
    SELECT id
    FROM users

    WHERE username=?
    AND password_hash=?

    """,

    (
        username,
        password_hash
    )

    )


    result = cursor.fetchone()


    conn.close()



    if result:

        return result[0]

    else:

        return None




# =========================
# SAVE PREFERENCE
# =========================

def save_preferences(
    user_id,
    budget,
    priority,
    room_type,
    max_drive_time,
    max_transit_time,
    preferred_neighborhood,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO preferences (
            user_id,
            budget,
            priority,
            room_type,
            max_drive_time,
            max_transit_time,
            preferred_neighborhood,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)

        ON CONFLICT(user_id)
        DO UPDATE SET
            budget = excluded.budget,
            priority = excluded.priority,
            room_type = excluded.room_type,
            max_drive_time = excluded.max_drive_time,
            max_transit_time = excluded.max_transit_time,
            preferred_neighborhood = excluded.preferred_neighborhood,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            int(user_id),
            int(budget),
            priority,
            room_type,
            int(max_drive_time),
            int(max_transit_time),
            preferred_neighborhood,
        ),
    )

    conn.commit()
    conn.close()



# =========================
# LOAD PREFERENCE
# =========================

def load_preferences(user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            budget,
            priority,
            room_type,
            max_drive_time,
            max_transit_time,
            preferred_neighborhood,
            updated_at
        FROM preferences
        WHERE user_id = ?
        """,
        (int(user_id),),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "budget": row["budget"],
        "priority": row["priority"],
        "room_type": row["room_type"],
        "max_drive_time": row["max_drive_time"],
        "max_transit_time": row["max_transit_time"],
        "preferred_neighborhood": row["preferred_neighborhood"],
        "updated_at": row["updated_at"],
    }




# =========================
# SAVE FAVORITE
# =========================

def save_favorite(
    user_id,
    listing_id
):

    listing_id = int(listing_id)
    
    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT OR IGNORE INTO favorites
        (
            user_id,
            listing_id
        )
        VALUES (?,?)
        """,
        (
            user_id,
            listing_id
        )
    )


    conn.commit()

    conn.close()



# =========================
# LOAD FAVORITES
# =========================

def load_favorites(user_id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT listing_id
        FROM favorites
        WHERE user_id=?
        """,
        (
            user_id,
        )
    )


    rows = cursor.fetchall()


    conn.close()


    return [
        int(row[0])
        for row in rows
    ]




# =========================
# REMOVE FAVORITE
# =========================

def remove_favorite(
    user_id,
    listing_id
):

    
    listing_id = int(listing_id)
    conn = get_connection()


    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM favorites
        WHERE user_id=?
        AND listing_id=?
        """,
        (
            user_id,
            listing_id
        )
    )


    conn.commit()

    conn.close()


# =========================
# Helper Functions
# =========================

def get_all_users():

    conn = get_connection()

    df = pd.read_sql_query(

        """
        SELECT *
        FROM users
        """,

        conn

    )

    conn.close()

    return df


def get_all_favorites():

    conn = get_connection()

    df = pd.read_sql_query(

        """
        SELECT *
        FROM favorites
        """,

        conn

    )

    conn.close()

    return df


def get_all_preferences():

    conn = get_connection()

    df = pd.read_sql_query(

        """
        SELECT *
        FROM preferences
        """,

        conn

    )

    conn.close()

    return df

def get_database_summary():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    users = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM favorites"
    )

    favorites = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM preferences"
    )

    preferences = cursor.fetchone()[0]


    conn.close()


    return {

        "users": users,

        "favorites": favorites,

        "preferences": preferences

    }

def migrate_preferences_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(preferences)")
    existing_columns = {
        row[1] for row in cursor.fetchall()
    }

    columns_to_add = {
        "max_drive_time": "INTEGER",
        "max_transit_time": "INTEGER",
        "preferred_neighborhood": "TEXT",
        "updated_at": "TEXT",
    }

    for column_name, column_type in columns_to_add.items():
        if column_name not in existing_columns:
            cursor.execute(
                f"""
                ALTER TABLE preferences
                ADD COLUMN {column_name} {column_type}
                """
            )

    # 清理可能存在的重复 preference
    cursor.execute(
        """
        DELETE FROM preferences
        WHERE id NOT IN (
            SELECT MAX(id)
            FROM preferences
            GROUP BY user_id
        )
        """
    )

    # 给 user_id 增加唯一约束效果
    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_preferences_user_id
        ON preferences(user_id)
        """
    )

    conn.commit()
    conn.close()





