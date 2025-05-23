import sqlite3
import functools


cached_searches = {}


def connect_to_database(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Connecting to the database...")
        try:
            conn = sqlite3.connect("users.db")
            print("Executing the caching function...")
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
            print("Database connection closed.")
    return wrapper


def caching_results(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        
        if args:
            query = args[0]
        elif 'query' in kwargs:
            query = kwargs['query']
        else:
            query = None
        
        
        if query in cached_searches:
            print(f"[CACHE] Returning cached result for query: {query}")
            return cached_searches[query]
        
        print(f"[DB] No cached result for query: {query}. Executing...")
        results = func(conn, query)
        print(f"[CACHE] Caching result for future use.")
        cached_searches[query] = results
        return results
    return wrapper


@connect_to_database
@caching_results
def search_users(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results


search_users(query="SELECT * FROM users")
search_users(query="SELECT * FROM users") 
