# File I/O Examples in Python

# Writing to a file
try:
    with open("example.txt", "w") as file:
        file.write("Hello, this is a test file.\n")
        file.write("This is the second line.\n")
    print("Successfully wrote to example.txt")
except IOError as e:
    print(f"Error writing to file: {e}")

# Reading from a file
try:
    with open("example.txt", "r") as file:
        content = file.read()
        print("\nContent of example.txt:")
        print(content)
except FileNotFoundError:
    print("Error: example.txt not found.")
except IOError as e:
    print(f"Error reading file: {e}")

# Reading line by line
try:
    with open("example.txt", "r") as file:
        print("\nReading example.txt line by line:")
        for line_num, line in enumerate(file, 1):
            print(f"Line {line_num}: {line.strip()}") # .strip() removes newline characters
except FileNotFoundError:
    print("Error: example.txt not found.")
except IOError as e:
    print(f"Error reading file: {e}")

# Appending to a file
try:
    with open("example.txt", "a") as file:
        file.write("This line was appended.\n")
    print("\nSuccessfully appended to example.txt")
except IOError as e:
    print(f"Error appending to file: {e}")

# Verify append by reading again
try:
    with open("example.txt", "r") as file:
        content = file.read()
        print("\nContent of example.txt after appending:")
        print(content)
except FileNotFoundError:
    print("Error: example.txt not found.")
except IOError as e:
    print(f"Error reading file: {e}")

# Working with different modes: 'x' for exclusive creation
