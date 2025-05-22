import sqlite3
import functools
import datetime
import time

# Define keys or parameter indexes considered sensitive (adjust as needed)
SENSITIVE_KEYS = {'password', 'ssn', 'credit_card'}

def mask_param(param):
    """Mask sensitive parameters (example: replace with ****)"""
    if isinstance(param, str) and len(param) > 4:
        # Just a simple mask showing first and last char
        return param[0] + "***" + param[-1]
    return "***"  # generic mask for other types or short strings

def safe_log_params(params, param_keys=None):
    """Mask sensitive parameters by key or by index"""
    safe_params = []
    if param_keys:  # dictionary style (named parameters)
        for key, val in params.items():
            if key.lower() in SENSITIVE_KEYS:
                safe_params.append((key, mask_param(val)))
            else:
                safe_params.append((key, val))
    else:  # positional parameters (list/tuple)
        for i, val in enumerate(params):
            # Just mask all string params as example, or customize further
            if isinstance(val, str) and len(val) > 4:
                safe_params.append(mask_param(val))
            else:
                safe_params.append(val)
    return safe_params

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query and parameters
        query = None
        params = None

        # Assuming first positional is query, second is parameters (common pattern)
        if args:
            query = args[0]
            if len(args) > 1:
                params = args[1]
        else:
            query = kwargs.get('query', None)
            params = kwargs.get('params', None)

        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            success = True
            return result
        except Exception as e:
            success = False
            error_msg = str(e)
            raise
        finally:
            elapsed_time = time.time() - start_time
            timestamp = datetime.datetime.now()

            # Prepare safe params for logging
            if params is not None:
                # Handle dict or list/tuple parameters
                if isinstance(params, dict):
                    safe_params = safe_log_params(params, param_keys=True)
                else:
                    safe_params = safe_log_params(params)
            else:
                safe_params = None

            with open("log.txt", "a") as file:
                if success:
                    file.write(f"{timestamp}: SUCCESS - Query ran in {elapsed_time:.4f} seconds: {query}\n")
                    if safe_params is not None:
                        file.write(f"Parameters: {safe_params}\n")
                else:
                    file.write(f"{timestamp}: ERROR - Query failed after {elapsed_time:.4f} seconds: {query}\n")
                    if safe_params is not None:
                        file.write(f"Parameters: {safe_params}\n")
                    file.write(f"Error message: {error_msg}\n")

    return wrapper


@log_queries
def fetch_all_users(query, params=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Usage example:
try:
    users = fetch_all_users(
        query="SELECT * FROM users WHERE username = ? AND password = ?",
        params=("john_doe", "secret_password123")
    )
    print(users)
except Exception as e:
    print(f"Database error: {e}")
