# advanced_math.py - Advanced mathematical operations

"""
Advanced mathematical operations for complex calculations.
"""

import math
import cmath
from typing import List, Tuple, Union

class ComplexCalculator:
    """Calculator for complex number operations."""
    
    def __init__(self):
        self.history = []
    
    def add_complex(self, z1: complex, z2: complex) -> complex:
        """Add two complex numbers."""
        result = z1 + z2
        self.history.append(f"{z1} + {z2} = {result}")
        return result
    
    def multiply_complex(self, z1: complex, z2: complex) -> complex:
        """Multiply two complex numbers."""
        result = z1 * z2
        self.history.append(f"{z1} * {z2} = {result}")
        return result
    
    def get_magnitude(self, z: complex) -> float:
        """Get magnitude (absolute value) of complex number."""
        return abs(z)
    
    def get_phase(self, z: complex) -> float:
        """Get phase angle of complex number in radians."""
        return cmath.phase(z)
    
    def to_polar(self, z: complex) -> Tuple[float, float]:
        """Convert complex number to polar form (magnitude, phase)."""
        return cmath.polar(z)
    
    def from_polar(self, magnitude: float, phase: float) -> complex:
        """Create complex number from polar coordinates."""
        return cmath.rect(magnitude, phase)

def matrix_operations():
    """Collection of basic matrix operations."""
    
    def add_matrices(matrix1: List[List[float]], matrix2: List[List[float]]) -> List[List[float]]:
        """Add two matrices."""
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
        
        result = []
        for i in range(len(matrix1)):
            row = []
            for j in range(len(matrix1[0])):
                row.append(matrix1[i][j] + matrix2[i][j])
            result.append(row)
        return result
    
    def multiply_matrix_scalar(matrix: List[List[float]], scalar: float) -> List[List[float]]:
        """Multiply matrix by scalar."""
        result = []
        for row in matrix:
            new_row = [element * scalar for element in row]
            result.append(new_row)
        return result
    
    def transpose_matrix(matrix: List[List[float]]) -> List[List[float]]:
        """Transpose a matrix."""
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    
    return {
        'add': add_matrices,
        'multiply_scalar': multiply_matrix_scalar,
        'transpose': transpose_matrix
    }

def calculate_derivatives():
    """Numerical derivative calculations."""
    
    def numerical_derivative(func, x: float, h: float = 1e-7) -> float:
        """Calculate numerical derivative using central difference."""
        return (func(x + h) - func(x - h)) / (2 * h)
    
    def gradient_descent_step(func, x: float, learning_rate: float = 0.01) -> float:
        """Perform one step of gradient descent."""
        gradient = numerical_derivative(func, x)
        return x - learning_rate * gradient
    
    return {
        'derivative': numerical_derivative,
        'gradient_step': gradient_descent_step
    }