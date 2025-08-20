


# List Examples in Python

# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed_list = [1, "hello", 3.14, True]

print("Fruits:", fruits)
print("Numbers:", numbers)
print("Mixed:", mixed_list)

# Indexing and slicing
print("First fruit:", fruits[0])
print("Last fruit:", fruits[-1])
print("Slice [1:3]:", fruits[1:3])

# Modifying lists
fruits[1] = "blueberry"
print("Modified fruits:", fruits)

# Adding elements
fruits.append("orange")
print("After append:", fruits)

fruits.insert(1, "mango")
print("After insert:", fruits)

# Removing elements
fruits.remove("apple")
print("After remove:", fruits)

popped_item = fruits.pop()
print("Popped item:", popped_item)
print("After pop:", fruits)

# List methods
numbers.extend([6, 7, 8])
print("Extended numbers:", numbers)

numbers.sort()
print("Sorted numbers:", numbers)

numbers.reverse()
print("Reversed numbers:", numbers)

# Checking membership
print("'banana' in fruits:", "banana" in fruits)
print("'mango' in fruits:", "mango" in fruits)

# List comprehension
squares = [n ** 2 for n in numbers]
print("Squares:", squares)

# Nested lists
nested = [[1, 2], [3, 4], [5, 6]]
print("Nested list:", nested)
print("First element of second list:", nested[1][0])