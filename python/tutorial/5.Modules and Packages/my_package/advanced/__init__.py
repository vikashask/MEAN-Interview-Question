# __init__.py - Subpackage initialization

"""
Advanced utilities subpackage for my_package.
Contains specialized mathematical and statistical functions.
"""

from .advanced_math import ComplexCalculator, matrix_operations
from .statistics import StatisticalAnalyzer

__all__ = ['ComplexCalculator', 'matrix_operations', 'StatisticalAnalyzer']