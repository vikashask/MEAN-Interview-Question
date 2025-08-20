# module_usage_examples.py - Demonstrating different ways to import and use modules

"""
This file demonstrates various ways to import and use Python modules.
It shows different import styles and their use cases.
"""

print("=== Module Import Examples ===\n")

# 1. Import entire module
print("1. Import entire module:")
import math_operations

# Access module attributes using module.attribute syntax
print(f"PI from math_operations: {math_operations.PI}")
print(f"Adding 5 + 3: {math_operations.add(5, 3)}")
print(f"Circle area (radius=4): {math_operations.circle_area(4)}")

# Create instance of class from module
calc = math_operations.Calculator()
result = calc.calculate("multiply", 6, 7)
print(f"Calculator result: {result}")
print()

# 2. Import specific functions/classes
print("2. Import specific functions:")
from string_utilities import capitalize_words, reverse_string, TextAnalyzer

text = "hello world python programming"
print(f"Original: {text}")
print(f"Capitalized: {capitalize_words(text)}")
print(f"Reversed: {reverse_string(text)}")

analyzer = TextAnalyzer(text)
print(f"Word count: {analyzer.summary()['word_count']}")
print()

# 3. Import with alias
print("3. Import with alias:")
import math_operations as math_ops
import string_utilities as str_utils

print(f"Using alias - E constant: {math_ops.E}")
print(f"Using alias - Word count: {str_utils.count_words('Python is awesome')}")
print()

# 4. Import specific items with alias
print("4. Import specific items with alias:")
from math_operations import Calculator as Calc, PI as pi_value
from string_utilities import word_frequency as word_freq

calculator = Calc()
calculator.calculate("add", 10, 20)
print(f"PI value: {pi_value}")
print(f"Word frequency: {word_freq('python is great python is fun')}")
print()

# 5. Import all (use with caution!)
print("5. Import all from string_utilities (demonstration only):")
from string_utilities import *

# Now we can use functions directly without module prefix
sample_text = "Python Programming Language"
print(f"Is palindrome: {is_palindrome('racecar')}")
print(f"Acronym: {create_acronym(sample_text)}")
print()

# 6. Conditional imports
print("6. Conditional imports:")
try:
    import numpy as np
    print("NumPy is available")
    # Use numpy functions here
except ImportError:
    print("NumPy is not installed, using alternative approach")
    # Use alternative implementation

# 7. Import from different locations
print("\n7. Import from standard library:")
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Current time: {datetime.now()}")

# Using collections
word_count = Counter(['apple', 'banana', 'apple', 'cherry', 'banana', 'apple'])
print(f"Word count using Counter: {word_count}")

dd = defaultdict(list)
dd['fruits'].append('apple')
dd['fruits'].append('banana')
print(f"Default dict: {dict(dd)}")
print()

# 8. Dynamic imports
print("8. Dynamic imports:")
module_name = "math_operations"
imported_module = __import__(module_name)
print(f"Dynamically imported module version: {imported_module.VERSION}")

# Alternative using importlib (recommended for dynamic imports)
import importlib
dynamic_module = importlib.import_module("string_utilities")
print(f"Dynamic import - capitalize: {dynamic_module.capitalize_words('hello world')}")
print()

# 9. Checking module attributes
print("9. Module introspection:")
print("math_operations module attributes:")
print([attr for attr in dir(math_operations) if not attr.startswith('_')])

print("\nstring_utilities module functions:")
import inspect
functions = [name for name, obj in inspect.getmembers(dynamic_module) 
            if inspect.isfunction(obj) and not name.startswith('_')]
print(functions)
print()

# 10. Module search path
print("10. Module search path (first 3 paths):")
for i, path in enumerate(sys.path[:3]):
    print(f"  {i+1}. {path}")
print("  ...")
print()

# 11. Reloading modules (useful in development)
print("11. Module reloading:")
print(f"Operations count before: {math_operations.get_operation_count()}")
math_operations.add(1, 1)  # Perform an operation
print(f"Operations count after: {math_operations.get_operation_count()}")

# Reload the module (note: this resets the module state)
importlib.reload(math_operations)
print(f"Operations count after reload: {math_operations.get_operation_count()}")
print()

# 12. Working with module documentation
print("12. Module documentation:")
print("math_operations module docstring:")
print(math_operations.__doc__)
print()

print("add function docstring:")
print(math_operations.add.__doc__)
print()

# 13. Best practices demonstration
print("13. Best practices:")

def demonstrate_module_usage():
    """Demonstrate proper module usage in a function."""
    # Import at the top of the function if needed locally
    from math_operations import multiply, divide
    
    try:
        result1 = multiply(10, 5)
        result2 = divide(20, 4)
        return f"Multiply: {result1}, Divide: {result2}"
    except Exception as e:
        return f"Error: {e}"

print(demonstrate_module_usage())

# 14. Checking if module/attribute exists
print("\n14. Safe attribute checking:")
if hasattr(math_operations, 'add'):
    print("✓ math_operations has 'add' function")

if hasattr(math_operations, 'nonexistent_function'):
    print("✓ Function exists")
else:
    print("✗ 'nonexistent_function' does not exist")

# 15. Getting module file location
print(f"\n15. Module file locations:")
print(f"math_operations location: {math_operations.__file__}")
print(f"string_utilities location: {str_utils.__file__}")

print("\n=== Module Usage Examples Complete ===")