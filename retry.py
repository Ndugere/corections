import sqlite3
import functools
import time

def connect_to_database(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("[DB] Trying to connect to the database...")
        try:
            conn = sqlite3.connect("users.db")
            return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"[DB ERROR] Connection failed: {e}")
            raise
        finally:
            conn.close()
            print("[DB] Connection closed.")
    return wrapper


def retry(try_times, delay):
    def decorator_of_the_tryer(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            print("[RETRY] Starting retry logic...")
            tried_times = 0
            while tried_times < try_times:
                try:
                    results = func(conn, *args, **kwargs)
                    if results:
                        print(f"[RETRY] Success on attempt {tried_times + 1}")
                        return results
                    else:
                        tried_times += 1
                        print(f"[RETRY] Empty result. Retrying in {delay} seconds...")
                        time.sleep(delay)
                except Exception as e:
                    print(f"[RETRY] Exception on attempt {tried_times + 1}: {e}")
                    tried_times += 1
                    time.sleep(delay)
            print("[RETRY] Max retries reached. No success.")
            return None
        return wrapper
    return decorator_of_the_tryer


@connect_to_database           
@retry(try_times=3, delay=2)
def get_data(conn):
    print("[QUERY] Executing query...")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Run
users = get_data()
if users:
    for user in users:
        print(user)
else:
    print("No data retrieved.")
