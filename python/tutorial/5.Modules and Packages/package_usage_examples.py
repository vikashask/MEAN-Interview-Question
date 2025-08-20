# package_usage_examples.py - Comprehensive package usage demonstration

"""
This file demonstrates how to use Python packages and their submodules.
Shows various import styles and real-world usage patterns.
"""

print("=== Python Packages and Modules Tutorial ===\n")

# 1. Import from main package level
print("1. Importing from package level:")
import my_package

# Use package-level functions (imported in __init__.py)
result = my_package.add(10, 5)
print(f"Package-level add: {result}")

# Get package information
info = my_package.get_package_info()
print(f"Package info: {info}")
print()

# 2. Import specific modules from package
print("2. Importing specific modules:")
from my_package import math_utils, file_utils, data_utils

# Use math utilities
factorial_result = math_utils.factorial(5)
print(f"Factorial of 5: {factorial_result}")

fibonacci_seq = math_utils.fibonacci(10)
print(f"Fibonacci sequence (10 terms): {fibonacci_seq}")

# Use data utilities
processor = data_utils.DataProcessor([1, 2, 3, 4, 5, 100, 2, 3])
stats = processor.get_statistics()
print(f"Data statistics: {stats}")
print()

# 3. Import from subpackage
print("3. Importing from subpackage:")
from my_package.advanced import ComplexCalculator, StatisticalAnalyzer, matrix_operations

# Complex number calculations
complex_calc = ComplexCalculator()
z1 = complex(3, 4)
z2 = complex(1, 2)
result = complex_calc.add_complex(z1, z2)
print(f"Complex addition: {z1} + {z2} = {result}")
print(f"Magnitude of {z1}: {complex_calc.get_magnitude(z1)}")

# Statistical analysis
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25]  # 25 is an outlier
stats_analyzer = StatisticalAnalyzer(data)
summary = stats_analyzer.summary_statistics()
print(f"Statistical summary: {summary}")

# Matrix operations
matrix_ops = matrix_operations()
matrix1 = [[1, 2], [3, 4]]
matrix2 = [[5, 6], [7, 8]]
matrix_sum = matrix_ops['add'](matrix1, matrix2)
print(f"Matrix addition result: {matrix_sum}")
print()

# 4. Different import styles
print("4. Different import styles:")

# Import with alias
from my_package.math_utils import MathCalculator as Calc
from my_package.file_utils import FileManager as FM

calculator = Calc()
calc_result = calculator.calculate("power", 2, 8)
print(f"Calculator result (2^8): {calc_result}")

# File operations
file_manager = FM("./temp_data")
sample_data = {"name": "John", "age": 30, "city": "New York"}
file_manager.save_data("sample.json", sample_data, "json")
print("Saved sample data to JSON file")

try:
    loaded_data = file_manager.load_data("sample.json", "json")
    print(f"Loaded data: {loaded_data}")
except FileNotFoundError:
    print("File not found - this is expected in some environments")
print()

# 5. Working with module search paths
print("5. Module and package introspection:")
import sys
import inspect

# Check package location
print(f"my_package location: {my_package.__file__}")
print(f"Package version: {my_package.__version__}")

# List package contents
print("Package contents:")
package_contents = [item for item in dir(my_package) if not item.startswith('_')]
print(f"  {package_contents}")

# Get module documentation
print(f"\nmath_utils module doc: {math_utils.__doc__}")
print()

# 6. Dynamic package usage
print("6. Dynamic package operations:")

# Get all functions in a module
math_functions = [name for name, obj in inspect.getmembers(math_utils) 
                 if inspect.isfunction(obj) and not name.startswith('_')]
print(f"Functions in math_utils: {math_functions}")

# Get all classes in a module
data_classes = [name for name, obj in inspect.getmembers(data_utils) 
               if inspect.isclass(obj) and not name.startswith('_')]
print(f"Classes in data_utils: {data_classes}")
print()

# 7. Error handling with packages
print("7. Error handling:")

try:
    # This will raise an error
    result = math_utils.divide(10, 0)
except ValueError as e:
    print(f"Caught expected error: {e}")

try:
    # This will also raise an error
    bad_factorial = math_utils.factorial(-5)
except ValueError as e:
    print(f"Caught factorial error: {e}")
print()

# 8. Real-world usage example
print("8. Real-world usage example - Data Analysis Pipeline:")

# Step 1: Generate sample data
import random
sample_data = [random.gauss(50, 10) for _ in range(100)]  # Normal distribution
sample_data.extend([100, 101, 102])  # Add some outliers

# Step 2: Process data
processor = data_utils.DataProcessor(sample_data)
cleaned_data = processor.clean_data()

# Step 3: Statistical analysis
analyzer = StatisticalAnalyzer(cleaned_data)
analysis_results = analyzer.summary_statistics()

print("Data Analysis Results:")
print(f"  Sample size: {analysis_results['count']}")
print(f"  Mean: {analysis_results['mean']:.2f}")
print(f"  Standard deviation: {analysis_results['std_dev']:.2f}")
print(f"  Outliers detected: {analysis_results['outliers_count']}")

# Step 4: Save results
results_to_save = {
    "analysis_date": "2024-01-01",
    "sample_size": analysis_results['count'],
    "statistics": {
        "mean": round(analysis_results['mean'], 2),
        "std_dev": round(analysis_results['std_dev'], 2),
        "median": round(analysis_results['median'], 2)
    }
}

try:
    file_manager.save_data("analysis_results.json", results_to_save)
    print("  Results saved to analysis_results.json")
except Exception as e:
    print(f"  Could not save results: {e}")
print()

# 9. Package namespace demonstration
print("9. Package namespace:")

# Show how packages create namespaces
print(f"my_package.add function: {my_package.add}")
print(f"math_utils.add function: {math_utils.add}")
print(f"Are they the same? {my_package.add is math_utils.add}")

# This works because __init__.py imports add from math_utils
print(f"my_package.add(3, 7) = {my_package.add(3, 7)}")
print(f"math_utils.add(3, 7) = {math_utils.add(3, 7)}")
print()

# 10. Best practices demonstration
print("10. Best practices:")

def analyze_dataset(data_file: str, output_file: str):
    """Example function showing good package usage practices."""
    try:
        # Import at function level if needed conditionally
        from my_package.advanced.statistics import StatisticalAnalyzer
        
        # Use context managers when available
        fm = FM("./analysis_output")
        
        # Validate inputs
        if not data_file.endswith(('.json', '.csv', '.txt')):
            raise ValueError("Unsupported file format")
        
        # Process data with error handling
        analyzer = StatisticalAnalyzer([1, 2, 3, 4, 5])  # Sample data
        results = analyzer.summary_statistics()
        
        # Save results
        fm.save_data(output_file, results)
        return f"Analysis complete. Results saved to {output_file}"
        
    except Exception as e:
        return f"Analysis failed: {e}"

print(analyze_dataset("data.json", "results.json"))

# Clean up temporary files
try:
    file_manager.cleanup_backups()
    print("Cleaned up temporary files")
except:
    print("No temporary files to clean")

print("\n=== Package Tutorial Complete ===")
print("\nKey Concepts Covered:")
print("- Module imports and usage")
print("- Package structure and __init__.py")
print("- Subpackages and nested imports")
print("- Different import styles and aliases")
print("- Package introspection and documentation")
print("- Error handling with packages")
print("- Real-world usage patterns")
print("- Best practices for package organization")