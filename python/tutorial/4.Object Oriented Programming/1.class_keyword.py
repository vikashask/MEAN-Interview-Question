# Understanding the class keyword in Python

# Basic class definition
class Vehicle:
    """A simple vehicle class"""
    pass  # Empty class body

# Class with constructor
class Car:
    """Car class demonstrating class keyword usage"""
    
    def __init__(self, brand, model):
        """Constructor method"""
        self.brand = brand
        self.model = model
    
    def display_info(self):
        """Method to display car information"""
        return f"Car: {self.brand} {self.model}"

# Creating instances
car1 = Car("Toyota", "Camry")
car2 = Car("Honda", "Civic")

print(car1.display_info())
print(car2.display_info())

# Class with multiple methods
class Calculator:
    """Simple calculator class"""
    
    def __init__(self):
        """Initialize calculator"""
        self.result = 0
    
    def add(self, number):
        """Add a number"""
        self.result += number
        return self
    
    def subtract(self, number):
        """Subtract a number"""
        self.result -= number
        return self
    
    def get_result(self):
        """Get the current result"""
        return self.result

# Using the calculator
calc = Calculator()
result = calc.add(10).subtract(3).get_result()
print(f"Calculator result: {result}")

# Class naming conventions and best practices
class BankAccount:  # Use PascalCase for class names
    """Best practices for class definition"""
    
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder  # Use snake_case for attributes
        self.balance = initial_balance
    
    def deposit(self, amount):
        """Method names should be descriptive"""
        self.balance += amount
        return f"Deposited ${amount}. New balance: ${self.balance}"
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return f"Withdrawn ${amount}. New balance: ${self.balance}"
        return "Insufficient funds"

# Example usage
account = BankAccount("John Doe", 1000)
print(account.deposit(500))
print(account.withdraw(200))