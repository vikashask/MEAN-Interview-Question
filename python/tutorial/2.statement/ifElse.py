# If-Else Examples in Python

# Basic if-else statement
x = 10
if x > 5:
    print("x is greater than 5")
else:
    print("x is not greater than 5")

# Elif (else if) statement
y = 7
if y > 10:
    print("y is greater than 10")
elif y > 5:
    print("y is greater than 5 but not greater than 10")
else:
    print("y is 5 or less")

# Nested if-else
age = 25
has_license = True

if age >= 18:
    if has_license:
        print("Eligible to drive")
    else:
        print("Not eligible to drive (no license)")
else:
    print("Not old enough to drive")

# Ternary operator (conditional expression)
temperature = 28
status = "Hot" if temperature > 25 else "Cold"
print(f"The weather is: {status}")

# Using logical operators in if statements
a = 5
b = 10
c = 15

if a < b and b < c:
    print("a is less than b, and b is less than c")

if a == 5 or b == 5:
    print("Either a or b is 5")

if not (a > b):
    print("a is not greater than b")

# Example with user input
# user_input = input("Enter a number: ")
# try:
#     num = int(user_input)
#     if num % 2 == 0:
#         print(f"{num} is an even number.")
#     else:
#         print(f"{num} is an odd number.")
# except ValueError:
#     print("Invalid input. Please enter an integer.")
