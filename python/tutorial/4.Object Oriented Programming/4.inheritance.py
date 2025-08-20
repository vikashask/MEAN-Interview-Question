# Inheritance in Python - Parent and Child Classes

# Base class (Parent class)
class Animal:
    """Base class representing a generic animal"""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.is_alive = True
    
    def eat(self):
        return f"{self.name} is eating"
    
    def sleep(self):
        return f"{self.name} is sleeping"
    
    def make_sound(self):
        return f"{self.name} makes a sound"
    
    def __str__(self):
        return f"{self.name} is a {self.species}"

# Child class inheriting from Animal
class Dog(Animal):
    """Dog class inheriting from Animal"""
    
    def __init__(self, name, breed):
        # Call parent constructor
        super().__init__(name, "Dog")
        self.breed = breed
    
    # Override parent method
    def make_sound(self):
        return f"{self.name} barks: Woof! Woof!"
    
    # New method specific to Dog
    def fetch(self):
        return f"{self.name} is fetching the ball"
    
    def wag_tail(self):
        return f"{self.name} is wagging its tail"

# Another child class
class Cat(Animal):
    """Cat class inheriting from Animal"""
    
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color
    
    # Override parent method
    def make_sound(self):
        return f"{self.name} meows: Meow! Meow!"
    
    # New methods specific to Cat
    def purr(self):
        return f"{self.name} is purring"
    
    def climb(self):
        return f"{self.name} is climbing a tree"

# Bird class with additional features
class Bird(Animal):
    """Bird class inheriting from Animal"""
    
    def __init__(self, name, wing_span):
        super().__init__(name, "Bird")
        self.wing_span = wing_span
        self.can_fly = True
    
    def make_sound(self):
        return f"{self.name} chirps: Tweet! Tweet!"
    
    def fly(self):
        if self.can_fly:
            return f"{self.name} is flying with {self.wing_span}cm wingspan"
        return f"{self.name} cannot fly"

# Multiple levels of inheritance
class Mammal(Animal):
    """Intermediate class for mammals"""
    
    def __init__(self, name, species, body_temperature=37):
        super().__init__(name, species)
        self.body_temperature = body_temperature
        self.is_warm_blooded = True
    
    def regulate_temperature(self):
        return f"{self.name} maintains body temperature at {self.body_temperature}°C"

class Elephant(Mammal):
    """Elephant class inheriting from Mammal"""
    
    def __init__(self, name, weight):
        super().__init__(name, "Elephant")
        self.weight = weight
    
    def make_sound(self):
        return f"{self.name} trumpets loudly!"
    
    def spray_water(self):
        return f"{self.name} sprays water with its trunk"

# Examples of inheritance
print("=== Basic Inheritance Examples ===")

# Create instances
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers", "Orange")
bird = Bird("Robin", 25)

# Inherited methods
print(dog.eat())        # From Animal
print(cat.sleep())      # From Animal
print(bird.eat())       # From Animal

# Overridden methods
print(dog.make_sound())  # Overridden in Dog
print(cat.make_sound())  # Overridden in Cat
print(bird.make_sound()) # Overridden in Bird

# Child-specific methods
print(dog.fetch())
print(cat.purr())
print(bird.fly())

print("\n=== Multi-level Inheritance ===")
elephant = Elephant("Dumbo", 5000)
print(elephant.make_sound())           # Overridden method
print(elephant.regulate_temperature()) # From Mammal
print(elephant.eat())                  # From Animal
print(elephant.spray_water())          # Own method

# Using isinstance() and issubclass()
print(f"\nIs dog an Animal? {isinstance(dog, Animal)}")
print(f"Is dog a Dog? {isinstance(dog, Dog)}")
print(f"Is Dog a subclass of Animal? {issubclass(Dog, Animal)}")
print(f"Is Elephant a subclass of Mammal? {issubclass(Elephant, Mammal)}")

# Method Resolution Order (MRO)
print(f"\nDog MRO: {Dog.__mro__}")
print(f"Elephant MRO: {Elephant.__mro__}")

# Multiple Inheritance Example
class Swimmer:
    """Mixin class for swimming ability"""
    
    def swim(self):
        return f"{self.name} is swimming"

class Flyer:
    """Mixin class for flying ability"""
    
    def fly(self):
        return f"{self.name} is flying"

class Duck(Animal, Swimmer, Flyer):
    """Duck class with multiple inheritance"""
    
    def __init__(self, name):
        super().__init__(name, "Duck")
    
    def make_sound(self):
        return f"{self.name} quacks: Quack! Quack!"

# Multiple inheritance example
duck = Duck("Donald")
print(f"\n=== Multiple Inheritance ===")
print(duck.make_sound())  # From Duck
print(duck.swim())        # From Swimmer
print(duck.fly())         # From Flyer
print(duck.eat())         # From Animal

print(f"Duck MRO: {Duck.__mro__}")

# Abstract base class example (more advanced)
from abc import ABC, abstractmethod

class Vehicle(ABC):
    """Abstract base class for vehicles"""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    @abstractmethod
    def start_engine(self):
        """Abstract method that must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def stop_engine(self):
        """Abstract method that must be implemented by subclasses"""
        pass
    
    def get_info(self):
        """Concrete method available to all subclasses"""
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    """Car class implementing abstract Vehicle"""
    
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)
        self.doors = doors
    
    def start_engine(self):
        return f"{self.get_info()} engine started with a roar!"
    
    def stop_engine(self):
        return f"{self.get_info()} engine stopped"

class Motorcycle(Vehicle):
    """Motorcycle class implementing abstract Vehicle"""
    
    def __init__(self, brand, model, engine_cc):
        super().__init__(brand, model)
        self.engine_cc = engine_cc
    
    def start_engine(self):
        return f"{self.get_info()} ({self.engine_cc}cc) engine started with a growl!"
    
    def stop_engine(self):
        return f"{self.get_info()} engine stopped"

print(f"\n=== Abstract Base Class ===")
car = Car("Toyota", "Camry", 4)
motorcycle = Motorcycle("Honda", "CBR", 600)

print(car.start_engine())
print(motorcycle.start_engine())
print(car.get_info())

# Cannot instantiate abstract class
# vehicle = Vehicle("Generic", "Model")  # This would raise TypeError