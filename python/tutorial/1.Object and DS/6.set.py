

# Set Examples in Python

# Creating sets
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}
mixed_set = {1, "hello", 3.14, True}

print("Fruits set:", fruits)
print("Numbers set:", numbers)
print("Mixed set:", mixed_set)

# Creating an empty set (use set(), not {})
empty_set = set()
print("Empty set:", empty_set)

# Adding elements
fruits.add("orange")
print("After adding orange:", fruits)

# Updating with multiple elements
fruits.update(["mango", "grape"])
print("After update:", fruits)

# Removing elements
fruits.remove("banana")
print("After removing banana:", fruits)

# Discard (no error if element not found)
fruits.discard("kiwi")
print("After discard (kiwi):", fruits)

# Pop (removes and returns an arbitrary element)
removed_item = fruits.pop()
print("Popped item:", removed_item)
print("After pop:", fruits)

# Set operations
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

print("Union:", set_a | set_b)
print("Intersection:", set_a & set_b)
print("Difference (A - B):", set_a - set_b)
print("Symmetric difference:", set_a ^ set_b)

# Subset and Superset
print("A is subset of B:", set_a.issubset(set_b))
print("A is superset of B:", set_a.issuperset(set_b))

# Set comprehension
squares = {x ** 2 for x in range(1, 6)}
print("Squares set:", squares)