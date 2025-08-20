

# Number Examples in Python

# Integer
a = 10
b = 3
print("Integer a:", a)
print("Integer b:", b)

# Float
x = 10.5
y = 2.5
print("Float x:", x)
print("Float y:", y)

# Complex number
c = 3 + 4j
print("Complex c:", c)
print("Real part:", c.real)
print("Imaginary part:", c.imag)

# Basic arithmetic
print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("Division:", a / b)
print("Floor Division:", a // b)
print("Modulus:", a % b)
print("Exponentiation:", a ** b)

# Mixed type operations
print("Addition (int + float):", a + x)

# Using built-in functions
print("Absolute value:", abs(-7))
print("Round value:", round(3.14159, 2))
print("Power function:", pow(2, 5))

# Using math module
import math
print("Square root:", math.sqrt(16))
print("Ceiling:", math.ceil(3.2))
print("Floor:", math.floor(3.8))
print("Factorial:", math.factorial(5))
print("Pi value:", math.pi)

# Type conversions
num_str = "100"
print("String to int:", int(num_str))
print("String to float:", float(num_str))
print("Int to float:", float(a))
print("Float to int:", int(x))