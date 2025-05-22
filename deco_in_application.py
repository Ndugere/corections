import sqlite3
import functools
import datetime

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            query = args[0]
        elif "query" in kwargs:
            query = kwargs["query"]
        with open("log.txt", "a") as file:
            file.write(f"{datetime.datetime.now()}: Query that was run was: {query} \n")
        return func(*args, **kwargs)
    return wrapper
            


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")