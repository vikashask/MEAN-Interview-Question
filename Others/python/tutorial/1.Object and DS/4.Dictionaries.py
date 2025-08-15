


# Dictionary Examples in Python

# Creating dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

print("Person:", person)

# Accessing values
print("Name:", person["name"])
print("Age:", person.get("age"))

# Modifying values
person["age"] = 31
print("Updated age:", person)

# Adding new key-value pairs
person["email"] = "alice@example.com"
print("After adding email:", person)

# Removing items
removed_value = person.pop("city")
print("Removed city:", removed_value)
print("After removal:", person)

# Using popitem() (removes last inserted)
last_item = person.popitem()
print("Last item removed:", last_item)
print("After popitem:", person)

# Checking keys and values
print("'name' in person:", "name" in person)
print("'city' in person:", "city" in person)

# Looping through dictionary
for key, value in person.items():
    print(f"{key}: {value}")

# Dictionary methods
keys = person.keys()
values = person.values()
items = person.items()
print("Keys:", keys)
print("Values:", values)
print("Items:", items)

# Merging dictionaries
other_info = {"country": "USA", "age": 32}
person.update(other_info)
print("After update:", person)

# Dictionary comprehension
squares = {x: x ** 2 for x in range(1, 6)}
print("Squares dict:", squares)