# Polymorphism in Python - One Interface, Multiple Forms

# Polymorphism with method overriding
class Shape:
    """Base class for all shapes"""
    
    def __init__(self, name):
        self.name = name
    
    def area(self):
        """Base method to be overridden"""
        raise NotImplementedError("Subclass must implement area method")
    
    def perimeter(self):
        """Base method to be overridden"""
        raise NotImplementedError("Subclass must implement perimeter method")
    
    def describe(self):
        """Common method for all shapes"""
        return f"This is a {self.name}"

class Rectangle(Shape):
    """Rectangle class demonstrating polymorphism"""
    
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self):
        """Override area method for rectangle"""
        return self.width * self.height
    
    def perimeter(self):
        """Override perimeter method for rectangle"""
        return 2 * (self.width + self.height)

class Circle(Shape):
    """Circle class demonstrating polymorphism"""
    
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        """Override area method for circle"""
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        """Override perimeter method for circle"""
        import math
        return 2 * math.pi * self.radius

class Triangle(Shape):
    """Triangle class demonstrating polymorphism"""
    
    def __init__(self, side1, side2, side3):
        super().__init__("Triangle")
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
    
    def area(self):
        """Override area method for triangle using Heron's formula"""
        s = self.perimeter() / 2  # semi-perimeter
        import math
        return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))
    
    def perimeter(self):
        """Override perimeter method for triangle"""
        return self.side1 + self.side2 + self.side3

# Polymorphism in action
def print_shape_info(shape):
    """Function that works with any shape (polymorphism)"""
    print(f"{shape.describe()}")
    print(f"Area: {shape.area():.2f}")
    print(f"Perimeter: {shape.perimeter():.2f}")
    print("-" * 30)

# Create different shapes
shapes = [
    Rectangle(5, 3),
    Circle(4),
    Triangle(3, 4, 5)
]

print("=== Polymorphism with Shapes ===")
for shape in shapes:
    print_shape_info(shape)

# Duck typing - another form of polymorphism
class Dog:
    def speak(self):
        return "Woof!"
    
    def move(self):
        return "Running on four legs"

class Cat:
    def speak(self):
        return "Meow!"
    
    def move(self):
        return "Stalking silently"

class Duck:
    def speak(self):
        return "Quack!"
    
    def move(self):
        return "Swimming in the pond"

class Robot:
    def speak(self):
        return "Beep boop!"
    
    def move(self):
        return "Rolling on wheels"

def make_animal_perform(animal):
    """Function demonstrating duck typing"""
    print(f"Animal says: {animal.speak()}")
    print(f"Animal moves: {animal.move()}")
    print()

print("=== Duck Typing Polymorphism ===")
animals = [Dog(), Cat(), Duck(), Robot()]

for animal in animals:
    make_animal_perform(animal)

# Polymorphism with operators (operator overloading)
class Vector:
    """Vector class demonstrating operator polymorphism"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Override + operator"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Override - operator"""
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Override * operator for scalar multiplication"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __str__(self):
        """Override string representation"""
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):
        """Override == operator"""
        return self.x == other.x and self.y == other.y

print("=== Operator Polymorphism ===")
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1: {v1}")
print(f"v2: {v2}")
print(f"v1 + v2: {v1 + v2}")
print(f"v1 - v2: {v1 - v2}")
print(f"v1 * 3: {v1 * 3}")
print(f"v1 == v2: {v1 == v2}")

# Polymorphism with different data types
def process_data(data):
    """Function that works with different data types"""
    if hasattr(data, '__iter__') and not isinstance(data, (str, bytes)):
        print(f"Processing iterable with {len(data)} items:")
        for item in data:
            print(f"  - {item}")
    else:
        print(f"Processing single item: {data}")
    print()

print("=== Polymorphism with Different Data Types ===")
process_data([1, 2, 3, 4])
process_data("Hello")
process_data(42)
process_data({"a": 1, "b": 2})

# Abstract base class for better polymorphism
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract base class for payment processing"""
    
    @abstractmethod
    def process_payment(self, amount):
        """Abstract method for processing payment"""
        pass
    
    @abstractmethod
    def validate_payment(self, payment_info):
        """Abstract method for validating payment"""
        pass

class CreditCardProcessor(PaymentProcessor):
    """Credit card payment processor"""
    
    def process_payment(self, amount):
        return f"Processing ${amount} via Credit Card"
    
    def validate_payment(self, payment_info):
        return len(payment_info.get('card_number', '')) == 16

class PayPalProcessor(PaymentProcessor):
    """PayPal payment processor"""
    
    def process_payment(self, amount):
        return f"Processing ${amount} via PayPal"
    
    def validate_payment(self, payment_info):
        return '@' in payment_info.get('email', '')

class BankTransferProcessor(PaymentProcessor):
    """Bank transfer payment processor"""
    
    def process_payment(self, amount):
        return f"Processing ${amount} via Bank Transfer"
    
    def validate_payment(self, payment_info):
        return len(payment_info.get('account_number', '')) >= 10

def handle_payment(processor, amount, payment_info):
    """Function that works with any payment processor"""
    if processor.validate_payment(payment_info):
        result = processor.process_payment(amount)
        print(f"✓ {result}")
    else:
        print("✗ Payment validation failed")

print("=== Polymorphism with Payment Processing ===")
processors = [
    CreditCardProcessor(),
    PayPalProcessor(),
    BankTransferProcessor()
]

payment_data = [
    {'card_number': '1234567890123456'},
    {'email': 'user@example.com'},
    {'account_number': '9876543210'}
]

for processor, payment_info in zip(processors, payment_data):
    handle_payment(processor, 100.0, payment_info)

# Method overloading simulation (Python doesn't have true method overloading)
class Calculator:
    """Calculator demonstrating method overloading simulation"""
    
    def add(self, *args):
        """Method that can handle different number of arguments"""
        if len(args) == 2:
            return args[0] + args[1]
        elif len(args) == 3:
            return args[0] + args[1] + args[2]
        else:
            return sum(args)
    
    def multiply(self, a, b=None, c=None):
        """Method with default parameters"""
        if c is not None:
            return a * b * c
        elif b is not None:
            return a * b
        else:
            return a * a  # Square

print("\n=== Method Overloading Simulation ===")
calc = Calculator()
print(f"add(2, 3): {calc.add(2, 3)}")
print(f"add(1, 2, 3): {calc.add(1, 2, 3)}")
print(f"add(1, 2, 3, 4, 5): {calc.add(1, 2, 3, 4, 5)}")
print(f"multiply(5): {calc.multiply(5)}")
print(f"multiply(3, 4): {calc.multiply(3, 4)}")
print(f"multiply(2, 3, 4): {calc.multiply(2, 3, 4)}")