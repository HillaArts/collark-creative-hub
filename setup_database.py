import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"collark purchases database"

    sql_create_purchases_table = """ CREATE TABLE IF NOT EXISTS purchases (
                                        purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        user_id INTEGER NOT NULL,
                                        product_id INTEGER NOT NULL,
                                        quantity INTEGER DEFAULT 1,
                                        price DECIMAL(10, 2) NOT NULL,
                                        purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        status TEXT DEFAULT 'completed',
                                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create purchases table
        create_table(conn, sql_create_purchases_table)
    else:
        print("Error! cannot create the database connection.")

    conn.close()

if __name__ == '__main__':
    main()