


# Python Functions

# A function is a block of reusable code that performs a specific task.
# Functions help to organize code, reduce duplication, and improve readability.

# Defining a simple function
def greet():
    print("Hello, welcome to Python functions!")

# Calling the function
greet()

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")
greet_person("Bob")

# Function with return value
def add(a, b):
    return a + b

result = add(5, 3)
print("Sum:", result)

# Function with default parameter
def power(base, exponent=2):
    return base ** exponent

print("Square of 4:", power(4))
print("Cube of 4:", power(4, 3))

# Function with keyword arguments
def introduce(name, age, city):
    print(f"My name is {name}, I am {age} years old, and I live in {city}.")

introduce(age=30, name="Charlie", city="New York")

# Function with variable-length arguments (*args)
def sum_all(*args):
    return sum(args)

print("Sum of all numbers:", sum_all(1, 2, 3, 4, 5))

# Function with keyword variable-length arguments (**kwargs)
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Daisy", age=25, city="London")

# Lambda (anonymous) function
square = lambda x: x ** 2
print("Square using lambda:", square(6))