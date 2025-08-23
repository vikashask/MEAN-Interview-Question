# Python Errors and Exception Handling - Comprehensive Tutorial

"""
STEP 1: Understanding Types of Errors
=====================================
1. Syntax Errors - Code doesn't follow Python syntax rules
2. Runtime Errors (Exceptions) - Errors that occur during program execution
3. Logical Errors - Code runs but produces incorrect results
"""

print("=" * 60)
print("STEP 1: TYPES OF ERRORS")
print("=" * 60)

# Example of Syntax Error (commented out because it would prevent execution)
# print("Hello World"  # Missing closing parenthesis - SyntaxError

# Example of Runtime Error (Exception)
try:
    # This will cause a ZeroDivisionError
    result = 10 / 0
except ZeroDivisionError:
    print("Runtime Error Example: Cannot divide by zero!")

# Example of Logical Error
def calculate_average(numbers):
    """This has a logical error - dividing by len+1 instead of len"""
    return sum(numbers) / (len(numbers) + 1)  # Should be len(numbers)

numbers = [10, 20, 30]
print(f"Logical Error Example: Average of {numbers} = {calculate_average(numbers)}")
print(f"Correct Average should be: {sum(numbers) / len(numbers)}")

"""
STEP 2: Basic Exception Handling with try-except
===============================================
"""

print("\n" + "=" * 60)
print("STEP 2: BASIC TRY-EXCEPT")
print("=" * 60)

# Basic try-except structure
def safe_division(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None

print(f"10 / 2 = {safe_division(10, 2)}")
print(f"10 / 0 = {safe_division(10, 0)}")

# Handling multiple specific exceptions
def process_list_item(my_list, index):
    try:
        value = my_list[index]
        return int(value)
    except IndexError:
        print(f"Error: Index {index} is out of range")
        return None
    except ValueError:
        print(f"Error: Cannot convert '{my_list[index]}' to integer")
        return None
    except TypeError:
        print("Error: Invalid data type provided")
        return None

# Testing multiple exception scenarios
test_list = ["10", "20", "hello", "30"]
print(f"\nTesting with list: {test_list}")
print(f"Index 0: {process_list_item(test_list, 0)}")  # Success
print(f"Index 2: {process_list_item(test_list, 2)}")  # ValueError
print(f"Index 5: {process_list_item(test_list, 5)}")  # IndexError

"""
STEP 3: Advanced Exception Handling
==================================
"""

print("\n" + "=" * 60)
print("STEP 3: ADVANCED EXCEPTION HANDLING")
print("=" * 60)

# Using try-except-else-finally
def file_operation_demo(filename):
    file_handle = None
    try:
        # This might raise FileNotFoundError
        file_handle = open(filename, 'r')
        content = file_handle.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{filename}'")
        return None
    else:
        # This runs only if no exception occurred
        print(f"Successfully read file '{filename}'")
    finally:
        # This always runs, regardless of exceptions
        if file_handle:
            file_handle.close()
            print("File closed properly")
        print("File operation completed")

# Test the function
print("Testing file operation:")
result = file_operation_demo("nonexistent.txt")

# Catching all exceptions with Exception
def risky_operation(x, y):
    try:
        # Various operations that might fail
        result = x / y
        my_list = [1, 2, 3]
        value = my_list[int(result)]
        return str(value).upper()
    except Exception as e:
        print(f"An error occurred: {type(e).__name__}: {e}")
        return None

print(f"\nRisky operation result: {risky_operation(6, 2)}")
print(f"Risky operation result: {risky_operation(10, 0)}")

"""
STEP 4: Built-in Exception Types
===============================
"""

print("\n" + "=" * 60)
print("STEP 4: COMMON BUILT-IN EXCEPTIONS")
print("=" * 60)

def demonstrate_common_exceptions():
    """Demonstrate various built-in exception types"""
    
    exceptions_demo = [
        # ZeroDivisionError
        lambda: 1 / 0,
        
        # IndexError
        lambda: [1, 2, 3][5],
        
        # KeyError
        lambda: {"a": 1, "b": 2}["c"],
        
        # ValueError
        lambda: int("hello"),
        
        # TypeError
        lambda: "hello" + 5,
        
        # AttributeError
        lambda: "hello".nonexistent_method(),
        
        # NameError (commented out as it would cause issues)
        # lambda: undefined_variable
    ]
    
    exception_names = [
        "ZeroDivisionError", "IndexError", "KeyError", 
        "ValueError", "TypeError", "AttributeError"
    ]
    
    for i, (exception_func, name) in enumerate(zip(exceptions_demo, exception_names)):
        try:
            exception_func()
        except Exception as e:
            print(f"{i+1}. {name}: {e}")

demonstrate_common_exceptions()

"""
STEP 5: Raising Exceptions
=========================
"""

print("\n" + "=" * 60)
print("STEP 5: RAISING EXCEPTIONS")
print("=" * 60)

def validate_age(age):
    """Function that raises exceptions for invalid input"""
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    
    if age < 0:
        raise ValueError("Age cannot be negative")
    
    if age > 150:
        raise ValueError("Age seems unrealistic (>150)")
    
    return f"Valid age: {age}"

# Testing exception raising
test_ages = [25, -5, 200, "thirty", 45.5]

for age in test_ages:
    try:
        result = validate_age(age)
        print(result)
    except (TypeError, ValueError) as e:
        print(f"Invalid age {age}: {e}")

# Re-raising exceptions
def wrapper_function(age):
    """Wrapper that catches and re-raises exceptions with additional info"""
    try:
        return validate_age(age)
    except ValueError as e:
        print(f"Validation failed in wrapper_function: {e}")
        raise  # Re-raise the same exception
    except TypeError as e:
        print(f"Type error in wrapper_function: {e}")
        # Raise a different exception
        raise ValueError(f"Invalid input type: {type(age).__name__}")

print("\nTesting wrapper function:")
try:
    wrapper_function("invalid")
except Exception as e:
    print(f"Caught exception: {type(e).__name__}: {e}")

"""
STEP 6: Exception Hierarchy and Multiple Inheritance
===================================================
"""

print("\n" + "=" * 60)
print("STEP 6: EXCEPTION HIERARCHY")
print("=" * 60)

# Catching exceptions by hierarchy
def demonstrate_exception_hierarchy():
    test_cases = [
        lambda: 1 / 0,  # ZeroDivisionError
        lambda: [1][2],  # IndexError
        lambda: int("abc"),  # ValueError
    ]
    
    for i, test_func in enumerate(test_cases):
        try:
            test_func()
        except ArithmeticError as e:
            print(f"Test {i+1}: Caught ArithmeticError: {e}")
        except LookupError as e:
            print(f"Test {i+1}: Caught LookupError: {e}")
        except ValueError as e:
            print(f"Test {i+1}: Caught ValueError: {e}")
        except Exception as e:
            print(f"Test {i+1}: Caught general Exception: {e}")

demonstrate_exception_hierarchy()

# Multiple exception types in one except block
def handle_multiple_exceptions(operation):
    try:
        return operation()
    except (ZeroDivisionError, ValueError, TypeError) as e:
        print(f"Caught one of multiple exception types: {type(e).__name__}: {e}")
        return None

print("\nTesting multiple exception handling:")
handle_multiple_exceptions(lambda: 1 / 0)
handle_multiple_exceptions(lambda: int("invalid"))

print("\n" + "=" * 60)
print("TUTORIAL COMPLETED!")
print("=" * 60)
print("Key Takeaways:")
print("1. Use specific exception types when possible")
print("2. Handle exceptions at the appropriate level")
print("3. Use try-except-else-finally for complex error handling")
print("4. Don't catch exceptions you can't handle meaningfully")
print("5. Use raise to propagate exceptions when needed")