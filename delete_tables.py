import os
import psycopg2
DATABASE_URL = os.environ.get('DATABASE_URL', "dbname='ATSDUMMY1' user='postgres' host='localhost' password='Chirayu@123'")

def connect_to_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        print("Connection error: ", e)
        return None

def drop_all_tables(conn):
    cur = conn.cursor()
    try:
        cur.execute("SET session_replication_role = 'replica';")
        cur.execute("""
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public';
        """)
        tables = cur.fetchall()
        for table in tables:
            cur.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")
        cur.execute("SET session_replication_role = 'origin';")

        conn.commit()
        print("All tables dropped successfully.")
    except psycopg2.Error as e:
        print("Failed to drop tables: ", e)
        conn.rollback()

if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        drop_all_tables(conn)
        conn.close()
