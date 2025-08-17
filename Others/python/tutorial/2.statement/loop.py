# For loop example
print("For loop example:")
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
  print(fruit)

#Check if any number in a list is even

def is_even(num_list):
    for num in num_list:
        if num % 2 == 0:
            return True
    return False
print("Is there an even number in the list?", is_even([1, 3, 5, 7, 8]))
  

# Return all even numbers in a list
def get_even_numbers(num_list):
    even_numbers = []
    for num in num_list:
        if num % 2 == 0:
            even_numbers.append(num)
    return even_numbers
print("Even numbers in the list:", get_even_numbers([1, 2, 3]))



# While loop example
print("\nWhile loop example:")
count = 0
while (count < 3):
  count = count + 1
  print("Hello Geek")
