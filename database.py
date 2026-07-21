import sqlite3
import hashlib
from datetime import datetime


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

        user_id INTEGER,

        budget INTEGER,

        priority TEXT,

        room_type TEXT,


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
    room_type
):

    conn = get_connection()

    cursor = conn.cursor()


    # delete old preference

    cursor.execute(
    """
    DELETE FROM preferences

    WHERE user_id=?

    """,

    (user_id,)
    )


    cursor.execute(
    """
    INSERT INTO preferences

    (
        user_id,
        budget,
        priority,
        room_type
    )

    VALUES
    (?,?,?,?)

    """,

    (
        user_id,
        budget,
        priority,
        room_type
    )

    )


    conn.commit()

    conn.close()



# =========================
# LOAD PREFERENCE
# =========================

def load_preferences(
    user_id
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
    """
    SELECT

    budget,
    priority,
    room_type


    FROM preferences


    WHERE user_id=?

    """,

    (user_id,)
    )


    result = cursor.fetchone()


    conn.close()



    if result:

        return {

            "budget": result[0],

            "priority": result[1],

            "room_type": result[2]

        }


    return None




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