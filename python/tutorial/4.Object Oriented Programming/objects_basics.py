# Creating and using objects in Python

# Define a simple class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old."

# Creating objects (instances) of the class
person1 = Person("Alice", 30)
person2 = Person("Bob", 25)

# Using the objects
print(person1.introduce())
print(person2.introduce())

# Accessing object attributes
print(f"{person1.name} is {person1.age} years old")
print(f"{person2.name} is {person2.age} years old")