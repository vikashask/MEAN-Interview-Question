

# Tuple Examples in Python

# Creating tuples
fruits = ("apple", "banana", "cherry")
numbers = (1, 2, 3, 4, 5)
mixed_tuple = (1, "hello", 3.14, True)

print("Fruits tuple:", fruits)
print("Numbers tuple:", numbers)
print("Mixed tuple:", mixed_tuple)

# Single-element tuple (note the comma)
single_element = ("one",)
print("Single element tuple:", single_element)
print("Type:", type(single_element))

# Indexing and slicing
print("First fruit:", fruits[0])
print("Last fruit:", fruits[-1])
print("Slice [1:3]:", fruits[1:3])

# Immutability demonstration
try:
    fruits[0] = "mango"
except TypeError as e:
    print("Error (tuples are immutable):", e)

# Tuple methods
print("Count of 2 in numbers:", numbers.count(2))
print("Index of 'cherry':", fruits.index("cherry"))

# Tuple unpacking
person = ("Alice", 30, "New York")
name, age, city = person
print("Name:", name)
print("Age:", age)
print("City:", city)

# Nested tuples
nested_tuple = ((1, 2), (3, 4), (5, 6))
print("Nested tuple:", nested_tuple)
print("First element of second tuple:", nested_tuple[1][0])

# Using tuples for multiple return values
def min_and_max(values):
    return (min(values), max(values))

result = min_and_max([5, 2, 8, 1, 9])
print("Min and Max:", result)