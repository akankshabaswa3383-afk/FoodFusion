
import sqlite3

DB_NAME = "foodfusion.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            language TEXT DEFAULT 'English'
        )
    """)

    # Food menu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            ingredients TEXT,
            allergens TEXT,
            image TEXT
        )
    """)

    # Customized meals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custom_meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            meal_name TEXT,
            selected_ingredients TEXT,
            total_price REAL
        )
    """)

    # Customer orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            food_name TEXT,
            quantity INTEGER,
            total_price REAL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pending'
        )
    """)

    # Customer preferences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            food_preference TEXT,
            budget REAL,
            favourite_category TEXT
        )
    """)

    # Recommendation history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            recommended_food TEXT,
            recommendation_reason TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("FoodFusion database created successfully!")
    print("All tables are ready.")
