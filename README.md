# Lab5_Static_Code_Analysis

Reflection – Lab 5: Static Code Analysis

1) Easiest vs Hardest Fixes:
The simplest fixes were replacing print() statements with logging and removing the mutable default argument.
The trickiest part was dealing with the bare except: statements — figuring out which exact exceptions to catch without breaking the logic took the most time.

2) False Positives:
Some of the tool warnings weren’t actual problems.
For example, Pylint complained about the logging format even though it worked fine, and Flake8 mainly flagged long lines that didn’t impact functionality.

3) Integration in Workflow:
If used regularly, these tools fit best through GitHub Actions or pre-commit hooks.
That way, code gets scanned automatically before committing or pushing, preventing bad practices early in the development process.

4) Improvements Observed:
After cleaning up the issues, the code now feels more structured and secure.
Input checks and proper error handling make it more robust, and logging helps with debugging and monitoring.

# Static Code Analysis Issues Table (Original `inventory_system.py`)

| **Issue** | **Category** | **Line(s)** | **Explanation** | **Resolution** |
|-----------|--------------|-------------|----------------|----------------|
| **Use of `eval()`** | Security Risk | 59 | Using `eval("print('eval used')")` can execute arbitrary code, posing a serious security threat. | Removed the `eval()` call. Replaced with a safe function call or `logger.info()` for output. |
| **Bare `except:` block** | Error Handling | 15–20 | The `removeItem` function swallows all exceptions due to a generic `except:` and `pass`, hiding potential errors. | Catch specific exceptions such as `KeyError` or `ValueError` and log unexpected exceptions instead of ignoring them. |
| **Mutable default argument (`logs=[]`)** | Maintainability / Code Quality | 11 | Using a mutable default list means all calls share the same object, leading to unintended side effects. | Changed the default to `None` and initialized a new list inside the function (`if logs is None: logs = []`). |
| **Lack of input validation** | Logic / Runtime Errors | 51–52 | Calling `addItem(123, "ten")` with mismatched types (`int + str`) triggers a `TypeError`. | Added type checks with `isinstance()` to ensure correct data types before performing operations. |
| **File opened without context manager** | Resource Management | 25–34 | Using `open()` without `with` can leave files unclosed, causing resource leaks. | Rewritten to use `with open(file) as f:` for proper file handling and automatic closure. |
| **Improper use of global variable (`stock_data`)** | Design / Architecture | Multiple | Multiple functions modify a global variable without encapsulation, risking thread-safety issues. | Encapsulated inventory management in a class or via controlled functions to minimize global state. |
| **No `__main__` check** | Code Structure | 58 | Script executes immediately on import, making it non-modular and hard to reuse. | Added `if __name__ == "__main__": main()` to allow modular execution. |
| **Using `print()` instead of logging** | Maintainability / Best Practice | 37, 38 | Direct `print()` calls are less manageable and flexible than logging. | Replaced `print()` statements with Python’s `logging` module (`logger.info()`) for structured output. |
