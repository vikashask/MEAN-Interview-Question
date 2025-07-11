try:
    a = int(input("Enter your age: "))
    print(a)    
except ValueError:
    print("Please enter a valid number")