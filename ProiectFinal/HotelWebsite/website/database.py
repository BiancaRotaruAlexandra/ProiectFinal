import sqlite3


def create_table():
    conn = sqlite3.connect("Hotel.db")
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS customers
                        (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT DEFAULT '',
                        surname TEXT DEFAULT '',
                        email TEXT UNIQUE NOT NULL,
                        phone TEXT UNIQUE NOT NULL
                        )
                        ''')

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS rooms
                        (
                        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room_type TEXT NOT NULL,
                        room_number TEXT UNIQUE NOT NULL,
                        price INTEGER NOT NULL
                        )  
                        ''')

        cursor.execute('''
                                CREATE TABLE IF NOT EXISTS reservations
                                (
                                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                customer_id INTEGER,
                                room_id INTEGER,
                                final_price INTEGER,
                                check_in DATE NOT NULL,
                                check_out DATE NOT NULL,
                                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                                FOREIGN KEY (room_id) REFERENCES rooms(room_id)
                                )
                                ''')
        conn.commit()

    except sqlite3.InternalError as e:
        print(f"Eroare de integritate: {e}")
    except sqlite3.Error as e:
        print(f"Eroare: {e}")
    finally:
        conn.close()


#create_table()


def insert_rooms():
    try:
        conn = sqlite3.connect("Hotel.db")
        cursor = conn.cursor()
        room = 'Deluxe'
        number = '405'
        price = 200

        cursor.execute('INSERT INTO rooms (room_type, room_number, price) VALUES (?, ?, ?)',
                       (room, number, price))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

def insert_customer():
    try:
        conn = sqlite3.connect("Hotel.db")
        cursor = conn.cursor()
        nume = 'idk'
        prenume = 'idk'
        numar = '9864630881'
        email = 'idk@gmail.com'
        cursor.execute('INSERT INTO customers (name, surname, email, phone) VALUES (?, ?, ?, ?)',
                       (nume, prenume, email, numar))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

#insert_customer()
#insert_rooms()


def create_reviews_table():
    conn = sqlite3.connect("Reviews.db")
    cursor = conn.cursor()

    try:
        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS reviews
                            (
                            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            room TEXT,
                            rating INTEGER,
                            description TEXT
                            )
                            ''')
        conn.commit()
    except sqlite3.InternalError as e:
        print(f"Eroare de integritate: {e}")
    except sqlite3.Error as e:
        print(f"Eroare: {e}")
    finally:
        conn.close()

create_reviews_table()
