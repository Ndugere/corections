import sqlite3

def connect_to_database():
    return sqlite3.connect("example.db")

def get_results(connection, lower_limit, upper_limit):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users LIMIT ? OFFSET ?", (upper_limit, lower_limit))
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()
    

def doorer():
    lower_limit = 0
    upper_limit = 10
    conn = connect_to_database()
    count = 1
    try:
        while True:
            results = get_results(conn, lower_limit, upper_limit)
            if not results:
                break
            with open("doc.txt", "a") as file:
                for result in results:
                    file.write(f"{result}   batch {count} \n")
            count += 1
            lower_limit += upper_limit
    finally:
        conn.close()
doorer()