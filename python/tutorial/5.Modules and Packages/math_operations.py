# math_operations.py - A simple module example

"""
This module provides basic mathematical operations.
This is the module docstring that describes what the module does.
"""

# Module-level variables (constants)
PI = 3.14159
E = 2.71828
VERSION = "1.0.0"

# Private variable (by convention, starts with underscore)
_internal_counter = 0

def add(a, b):
    """Add two numbers and return the result."""
    global _internal_counter
    _internal_counter += 1
    return a + b

def subtract(a, b):
    """Subtract second number from first and return the result."""
    global _internal_counter
    _internal_counter += 1
    return a - b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    global _internal_counter
    _internal_counter += 1
    return a * b

def divide(a, b):
    """Divide first number by second and return the result."""
    global _internal_counter
    _internal_counter += 1
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

def power(base, exponent):
    """Calculate base raised to the power of exponent."""
    global _internal_counter
    _internal_counter += 1
    return base ** exponent

def circle_area(radius):
    """Calculate area of a circle given its radius."""
    global _internal_counter
    _internal_counter += 1
    return PI * radius ** 2

def circle_circumference(radius):
    """Calculate circumference of a circle given its radius."""
    global _internal_counter
    _internal_counter += 1
    return 2 * PI * radius

def get_operation_count():
    """Return the number of operations performed."""
    return _internal_counter

def reset_counter():
    """Reset the operation counter."""
    global _internal_counter
    _internal_counter = 0

# Class in a module
class Calculator:
    """A simple calculator class."""
    
    def __init__(self):
        self.history = []
    
    def calculate(self, operation, a, b=None):
        """Perform calculation and store in history."""
        if operation == "add" and b is not None:
            result = add(a, b)
        elif operation == "subtract" and b is not None:
            result = subtract(a, b)
        elif operation == "multiply" and b is not None:
            result = multiply(a, b)
        elif operation == "divide" and b is not None:
            result = divide(a, b)
        elif operation == "square":
            result = power(a, 2)
        else:
            raise ValueError("Invalid operation or missing parameters")
        
        # Store in history
        self.history.append({
            'operation': operation,
            'inputs': [a] if b is None else [a, b],
            'result': result
        })
        
        return result
    
    def get_history(self):
        """Return calculation history."""
        return self.history
    
    def clear_history(self):
        """Clear calculation history."""
        self.history = []

# Function that runs when module is executed directly
def main():
    """Main function for testing the module."""
    print("Testing math_operations module:")
    print(f"PI = {PI}")
    print(f"E = {E}")
    
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"15 / 3 = {divide(15, 3)}")
    print(f"2^3 = {power(2, 3)}")
    
    print(f"Circle area (radius=5): {circle_area(5)}")
    print(f"Circle circumference (radius=5): {circle_circumference(5)}")
    
    print(f"Operations performed: {get_operation_count()}")
    
    # Test Calculator class
    calc = Calculator()
    calc.calculate("add", 10, 5)
    calc.calculate("multiply", 3, 4)
    calc.calculate("square", 5)
    
    print("\nCalculator history:")
    for entry in calc.get_history():
        print(f"  {entry}")

# This block runs only when the script is executed directly
# Not when it's imported as a module
if __name__ == "__main__":
    main()