# Exception Handling Best Practices and Interview Questions

"""
STEP 11: Best Practices for Exception Handling
=============================================
This file covers industry best practices and common interview questions
about Python exception handling.
"""

print("=" * 60)
print("STEP 11: BEST PRACTICES")
print("=" * 60)

"""
Best Practice 1: Be Specific with Exception Types
================================================
"""

# ❌ BAD: Catching all exceptions broadly
def bad_exception_handling():
    try:
        data = {"name": "John", "age": 25}
        return data["salary"]  # KeyError
    except Exception as e:
        print("Something went wrong")
        return None

# ✅ GOOD: Specific exception handling
def good_exception_handling():
    try:
        data = {"name": "John", "age": 25}
        return data["salary"]
    except KeyError as e:
        print(f"Missing required field: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        return None

print("Testing exception specificity:")
print(f"Bad approach: {bad_exception_handling()}")
print(f"Good approach: {good_exception_handling()}")

"""
Best Practice 2: Don't Suppress Exceptions Without Good Reason
=============================================================
"""

# ❌ BAD: Silent failures
def bad_silent_failure(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        pass  # Silent failure - very bad!

# ✅ GOOD: Proper error handling and logging
import logging
logging.basicConfig(level=logging.INFO)

def good_error_handling(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return None
    except PermissionError:
        logging.error(f"Permission denied: {filename}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error reading {filename}: {e}")
        return None

"""
Best Practice 3: Use Context Managers for Resource Management
============================================================
"""

# ❌ BAD: Manual resource management
def bad_resource_management():
    try:
        file = open("data.txt", "r")
        data = file.read()
        file.close()  # Might not execute if exception occurs
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

# ✅ GOOD: Context managers ensure cleanup
def good_resource_management():
    try:
        with open("data.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

"""
Best Practice 4: Exception Documentation and Type Hints
======================================================
"""

from typing import Optional, List, Union

def process_numbers(numbers: List[Union[int, float]]) -> Optional[float]:
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numeric values
        
    Returns:
        Average of the numbers, or None if calculation fails
        
    Raises:
        TypeError: If numbers is not a list or contains non-numeric values
        ValueError: If the list is empty
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    try:
        total = sum(numbers)
        return total / len(numbers)
    except TypeError as e:
        raise TypeError("All elements must be numeric") from e

# Testing documented function
test_cases = [
    [1, 2, 3, 4, 5],
    [],
    "not a list",
    [1, 2, "three", 4],
]

for i, test_case in enumerate(test_cases):
    try:
        result = process_numbers(test_case)
        print(f"Test {i+1}: Average = {result}")
    except (TypeError, ValueError) as e:
        print(f"Test {i+1}: {type(e).__name__}: {e}")

"""
STEP 12: Common Interview Questions and Answers
==============================================
"""

print("\n" + "=" * 60)
print("STEP 12: INTERVIEW QUESTIONS")
print("=" * 60)

"""
Q1: What's the difference between syntax errors and exceptions?
"""

print("Q1: Syntax Errors vs Exceptions")
print("-" * 40)

# Syntax Error Example (commented out)
# if True
#     print("Missing colon")  # SyntaxError

# Exception Example
def demo_exception():
    try:
        return 1 / 0  # ZeroDivisionError (runtime exception)
    except ZeroDivisionError:
        return "Caught runtime exception"

print("Exception example:", demo_exception())

"""
Q2: How do you create and use custom exceptions?
"""

print("\nQ2: Custom Exceptions")
print("-" * 40)

class InvalidAgeError(Exception):
    """Custom exception for invalid age values"""
    def __init__(self, age, message="Invalid age provided"):
        self.age = age
        self.message = message
        super().__init__(f"{message}: {age}")

def validate_person_age(age):
    if age < 0:
        raise InvalidAgeError(age, "Age cannot be negative")
    if age > 150:
        raise InvalidAgeError(age, "Age seems unrealistic")
    return f"Valid age: {age}"

for test_age in [25, -5, 200]:
    try:
        print(validate_person_age(test_age))
    except InvalidAgeError as e:
        print(f"Custom exception caught: {e}")

"""
Q3: What is the purpose of else and finally in try-except blocks?
"""

print("\nQ3: else and finally clauses")
print("-" * 40)

def demonstrate_else_finally(divide_by_zero=False):
    try:
        if divide_by_zero:
            result = 10 / 0
        else:
            result = 10 / 2
        print(f"Calculation result: {result}")
    except ZeroDivisionError:
        print("Cannot divide by zero!")
    else:
        print("else: No exception occurred")
    finally:
        print("finally: This always executes")

print("Case 1: Normal execution")
demonstrate_else_finally(False)

print("\nCase 2: Exception occurs")
demonstrate_else_finally(True)

"""
Q4: How do you handle multiple exceptions?
"""

print("\nQ4: Multiple Exception Handling")
print("-" * 40)

def handle_multiple_exceptions(data, index):
    try:
        # Might raise IndexError
        item = data[index]
        # Might raise ValueError
        number = int(item)
        # Might raise ZeroDivisionError
        result = 100 / number
        return result
    except IndexError:
        return "Index out of range"
    except ValueError:
        return "Cannot convert to integer"
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except (TypeError, AttributeError) as e:
        return f"Data type error: {e}"

# Test cases for multiple exceptions
test_data = [
    (["1", "2", "5"], 1),      # Success case
    (["1", "2", "5"], 5),      # IndexError
    (["1", "abc", "5"], 1),    # ValueError
    (["1", "0", "5"], 1),      # ZeroDivisionError
    (None, 0),                 # TypeError
]

for data, index in test_data:
    result = handle_multiple_exceptions(data, index)
    print(f"Data: {data}, Index: {index} -> {result}")

"""
Q5: What is exception chaining and when should you use it?
"""

print("\nQ5: Exception Chaining")
print("-" * 40)

class BusinessLogicError(Exception):
    """High-level business logic exception"""
    pass

def low_level_operation(value):
    """Low-level operation that might fail"""
    if value < 0:
        raise ValueError("Negative values not allowed")
    return value * 2

def high_level_operation(value):
    """High-level operation that uses low-level operations"""
    try:
        return low_level_operation(value)
    except ValueError as e:
        # Chain the exception to preserve context
        raise BusinessLogicError(f"Business rule violation for value {value}") from e

# Test exception chaining
try:
    result = high_level_operation(-5)
except BusinessLogicError as e:
    print(f"High-level error: {e}")
    print(f"Original cause: {e.__cause__}")
    print(f"Exception chain: {e.__class__.__name__} -> {e.__cause__.__class__.__name__}")

"""
STEP 13: Performance Considerations
==================================
"""

print("\n" + "=" * 60)
print("STEP 13: PERFORMANCE CONSIDERATIONS")
print("=" * 60)

import time

# Performance comparison: EAFP vs LBYL
def eafp_approach(data, key):
    """Easier to Ask for Forgiveness than Permission"""
    try:
        return data[key]
    except KeyError:
        return None

def lbyl_approach(data, key):
    """Look Before You Leap"""
    if key in data:
        return data[key]
    return None

# Performance test
test_dict = {str(i): i for i in range(1000)}
missing_keys = [str(i) for i in range(1000, 1100)]

print("Performance comparison (100 operations each):")

# Test EAFP with existing keys
start_time = time.time()
for key in list(test_dict.keys())[:100]:
    eafp_approach(test_dict, key)
eafp_time_hit = time.time() - start_time

# Test LBYL with existing keys
start_time = time.time()
for key in list(test_dict.keys())[:100]:
    lbyl_approach(test_dict, key)
lbyl_time_hit = time.time() - start_time

print(f"EAFP (key exists): {eafp_time_hit:.6f} seconds")
print(f"LBYL (key exists): {lbyl_time_hit:.6f} seconds")

# Test with missing keys
start_time = time.time()
for key in missing_keys[:100]:
    eafp_approach(test_dict, key)
eafp_time_miss = time.time() - start_time

start_time = time.time()
for key in missing_keys[:100]:
    lbyl_approach(test_dict, key)
lbyl_time_miss = time.time() - start_time

print(f"EAFP (key missing): {eafp_time_miss:.6f} seconds")
print(f"LBYL (key missing): {lbyl_time_miss:.6f} seconds")

print("\n" + "=" * 60)
print("COMPLETE TUTORIAL SUMMARY")
print("=" * 60)

summary = """
KEY CONCEPTS LEARNED:
1. Types of Errors: Syntax, Runtime (Exceptions), Logical
2. Basic Exception Handling: try-except blocks
3. Advanced Handling: else, finally, multiple exceptions
4. Built-in Exception Types: ValueError, TypeError, etc.
5. Custom Exceptions: Creating domain-specific error types
6. Exception Context Managers: Resource cleanup
7. Exception Chaining: Preserving error context
8. Best Practices: Specific handling, documentation, logging
9. Performance: EAFP vs LBYL approaches
10. Real-world Patterns: Retry logic, monitoring

INTERVIEW TIPS:
- Understand the exception hierarchy in Python
- Know when to use custom exceptions vs built-in ones
- Explain the difference between errors and exceptions
- Demonstrate proper resource cleanup with context managers
- Show understanding of exception chaining and context preservation
- Discuss performance implications of exception handling
"""

print(summary)