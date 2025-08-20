# math_utils.py - Mathematics utilities submodule

"""
Mathematical utility functions for the my_package package.
"""

import math
from typing import Union, List

def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers."""
    return a + b

def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Subtract second number from first."""
    return a - b

def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply two numbers."""
    return a * b

def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """Divide first number by second."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def factorial(n: int) -> int:
    """Calculate factorial of a number."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return math.factorial(n)

def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """Calculate base raised to the power of exponent."""
    return base ** exponent

def square_root(n: Union[int, float]) -> float:
    """Calculate square root of a number."""
    if n < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(n)

def gcd(a: int, b: int) -> int:
    """Calculate Greatest Common Divisor."""
    return math.gcd(a, b)

def lcm(a: int, b: int) -> int:
    """Calculate Least Common Multiple."""
    return abs(a * b) // gcd(a, b)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci(n: int) -> List[int]:
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

class MathCalculator:
    """Advanced calculator class."""
    
    def __init__(self):
        self.history = []
    
    def calculate(self, operation: str, *args) -> Union[int, float]:
        """Perform calculation and store in history."""
        operations = {
            'add': lambda x, y: add(x, y),
            'subtract': lambda x, y: subtract(x, y),
            'multiply': lambda x, y: multiply(x, y),
            'divide': lambda x, y: divide(x, y),
            'power': lambda x, y: power(x, y),
            'sqrt': lambda x: square_root(x),
            'factorial': lambda x: factorial(int(x))
        }
        
        if operation not in operations:
            raise ValueError(f"Unknown operation: {operation}")
        
        try:
            result = operations[operation](*args)
            self.history.append({
                'operation': operation,
                'args': args,
                'result': result
            })
            return result
        except Exception as e:
            raise ValueError(f"Error in {operation}: {e}")
    
    def get_history(self) -> List[dict]:
        """Get calculation history."""
        return self.history
    
    def clear_history(self):
        """Clear calculation history."""
        self.history = []