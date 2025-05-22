def ask_for_permission(func):
    def wrapper():
        print("Ask for permision ")
        results = func()
        print("Done")
        if results is not None:
            return results
    return wrapper

@ask_for_permission
def caller():
    return "Hello"


results = caller()

if results:
    print(results)