
list = [x for x in range(10)]
print("List of numbers from 0 to 9:", list)

word = [x for x in "Python"]
print("List of characters in 'Python':", word)

# square of numbers

squares = [x**2 for x in range(10)]
print("List of squares from 0 to 9:", squares)

# Check for even numbers in a range
evens = [x for x in range(20) if x % 2 == 0]
print("List of even numbers from 0 to 19:", evens)

# Convert Celsius to Fahrenheit
celsius = [0, 10, 20, 30, 40]
fahrenheit = [(temp * 9/5) + 32 for temp in celsius]
print("Celsius to Fahrenheit:", fahrenheit)