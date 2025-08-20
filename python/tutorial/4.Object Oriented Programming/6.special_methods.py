# Special Methods (Magic Methods) in Python Classes

# Special methods allow customization of class behavior
class Book:
    """Book class demonstrating various special methods"""
    
    def __init__(self, title, author, pages, price):
        """Constructor - called when creating an instance"""
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
    
    def __str__(self):
        """String representation for end users"""
        return f"'{self.title}' by {self.author}"
    
    def __repr__(self):
        """String representation for developers"""
        return f"Book('{self.title}', '{self.author}', {self.pages}, {self.price})"
    
    def __len__(self):
        """Return length (number of pages)"""
        return self.pages
    
    def __eq__(self, other):
        """Equality comparison"""
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False
    
    def __lt__(self, other):
        """Less than comparison (by price)"""
        return self.price < other.price
    
    def __le__(self, other):
        """Less than or equal comparison"""
        return self.price <= other.price
    
    def __gt__(self, other):
        """Greater than comparison"""
        return self.price > other.price
    
    def __ge__(self, other):
        """Greater than or equal comparison"""
        return self.price >= other.price
    
    def __add__(self, other):
        """Addition - combine books into a collection"""
        if isinstance(other, Book):
            return BookCollection([self, other])
        return NotImplemented
    
    def __hash__(self):
        """Make object hashable (for use in sets/dicts)"""
        return hash((self.title, self.author))
    
    def __bool__(self):
        """Boolean evaluation"""
        return self.pages > 0
    
    def __getitem__(self, key):
        """Make object subscriptable"""
        if key == 0:
            return self.title
        elif key == 1:
            return self.author
        elif key == 2:
            return self.pages
        elif key == 3:
            return self.price
        else:
            raise IndexError("Book index out of range")
    
    def __setitem__(self, key, value):
        """Allow item assignment"""
        if key == 0:
            self.title = value
        elif key == 1:
            self.author = value
        elif key == 2:
            self.pages = value
        elif key == 3:
            self.price = value
        else:
            raise IndexError("Book index out of range")
    
    def __contains__(self, item):
        """Support 'in' operator"""
        return item.lower() in self.title.lower() or item.lower() in self.author.lower()
    
    def __call__(self):
        """Make object callable"""
        return f"Reading '{self.title}' by {self.author}"

class BookCollection:
    """Collection class for managing multiple books"""
    
    def __init__(self, books=None):
        self.books = books or []
    
    def __len__(self):
        """Return number of books"""
        return len(self.books)
    
    def __getitem__(self, index):
        """Support indexing and slicing"""
        return self.books[index]
    
    def __setitem__(self, index, value):
        """Support item assignment"""
        self.books[index] = value
    
    def __delitem__(self, index):
        """Support item deletion"""
        del self.books[index]
    
    def __iter__(self):
        """Make object iterable"""
        return iter(self.books)
    
    def __reversed__(self):
        """Support reversed() function"""
        return reversed(self.books)
    
    def __contains__(self, book):
        """Support 'in' operator"""
        return book in self.books
    
    def __add__(self, other):
        """Support + operator for combining collections"""
        if isinstance(other, BookCollection):
            return BookCollection(self.books + other.books)
        elif isinstance(other, Book):
            return BookCollection(self.books + [other])
        return NotImplemented
    
    def __str__(self):
        return f"BookCollection with {len(self.books)} books"
    
    def __repr__(self):
        return f"BookCollection({self.books})"

# Examples of special methods in action
print("=== Special Methods Demo ===")

# Create book instances
book1 = Book("Python Programming", "John Doe", 500, 29.99)
book2 = Book("Data Science", "Jane Smith", 400, 34.99)
book3 = Book("Python Programming", "John Doe", 500, 29.99)  # Same as book1

# __str__ and __repr__
print(f"str(book1): {str(book1)}")
print(f"repr(book1): {repr(book1)}")

# __len__
print(f"len(book1): {len(book1)} pages")

# __eq__ (equality)
print(f"book1 == book2: {book1 == book2}")
print(f"book1 == book3: {book1 == book3}")

# Comparison operators
print(f"book1 < book2: {book1 < book2}")
print(f"book1 > book2: {book1 > book2}")

# __bool__
empty_book = Book("", "", 0, 0)
print(f"bool(book1): {bool(book1)}")
print(f"bool(empty_book): {bool(empty_book)}")

# __getitem__ and __setitem__ (subscriptable)
print(f"book1[0]: {book1[0]}")  # title
print(f"book1[1]: {book1[1]}")  # author
book1[3] = 25.99  # Change price
print(f"Updated price: {book1[3]}")

# __contains__ (in operator)
print(f"'Python' in book1: {'Python' in book1}")
print(f"'Java' in book1: {'Java' in book1}")

# __call__ (callable object)
print(f"book1(): {book1()}")

# __hash__ (hashable objects)
book_set = {book1, book2, book3}
print(f"Unique books in set: {len(book_set)}")

# __add__ (addition)
collection = book1 + book2
print(f"Combined books: {collection}")

print("\n=== BookCollection Special Methods ===")

# Create collection
books = BookCollection([book1, book2])

# __len__
print(f"len(books): {len(books)}")

# __getitem__ (indexing)
print(f"books[0]: {books[0]}")

# __iter__ (iteration)
print("Iterating through books:")
for book in books:
    print(f"  - {book}")

# __contains__
print(f"book1 in books: {book1 in books}")

# __add__
more_books = BookCollection([Book("Machine Learning", "AI Expert", 600, 45.99)])
all_books = books + more_books
print(f"Combined collections: {all_books}")

# Context manager example
class FileManager:
    """File manager demonstrating context manager special methods"""
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Enter context manager"""
        print(f"Opening file: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context manager"""
        print(f"Closing file: {self.filename}")
        if self.file:
            self.file.close()
        if exc_type:
            print(f"Exception occurred: {exc_value}")
        return False  # Don't suppress exceptions

print("\n=== Context Manager Special Methods ===")

# Using context manager
try:
    with FileManager("test.txt", "w") as f:
        f.write("Hello, World!")
    print("File operations completed successfully")
except Exception as e:
    print(f"Error: {e}")

# Arithmetic operations class
class Money:
    """Money class demonstrating arithmetic special methods"""
    
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency
    
    def __add__(self, other):
        """Addition"""
        if isinstance(other, Money) and other.currency == self.currency:
            return Money(self.amount + other.amount, self.currency)
        return NotImplemented
    
    def __sub__(self, other):
        """Subtraction"""
        if isinstance(other, Money) and other.currency == self.currency:
            return Money(self.amount - other.amount, self.currency)
        return NotImplemented
    
    def __mul__(self, factor):
        """Multiplication by scalar"""
        if isinstance(factor, (int, float)):
            return Money(self.amount * factor, self.currency)
        return NotImplemented
    
    def __rmul__(self, factor):
        """Right multiplication (factor * money)"""
        return self.__mul__(factor)
    
    def __truediv__(self, divisor):
        """Division"""
        if isinstance(divisor, (int, float)) and divisor != 0:
            return Money(self.amount / divisor, self.currency)
        return NotImplemented
    
    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"
    
    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

print("\n=== Arithmetic Special Methods ===")

money1 = Money(100.50)
money2 = Money(25.25)

print(f"money1: {money1}")
print(f"money2: {money2}")
print(f"money1 + money2: {money1 + money2}")
print(f"money1 - money2: {money1 - money2}")
print(f"money1 * 2: {money1 * 2}")
print(f"3 * money2: {3 * money2}")
print(f"money1 / 2: {money1 / 2}")

# Property and descriptor special methods
class Temperature:
    """Temperature class with property-like behavior"""
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    def __get__(self, obj, objtype=None):
        """Descriptor get method"""
        if obj is None:
            return self
        return self._celsius
    
    def __set__(self, obj, value):
        """Descriptor set method"""
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = value
    
    def __delete__(self, obj):
        """Descriptor delete method"""
        self._celsius = 0

# Metaclass example (advanced)
class SingletonMeta(type):
    """Metaclass for creating singleton classes"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """Database class using singleton pattern"""
    
    def __init__(self):
        self.connection = "Connected to database"
    
    def query(self, sql):
        return f"Executing: {sql}"

print("\n=== Singleton Pattern with Metaclass ===")
db1 = Database()
db2 = Database()
print(f"db1 is db2: {db1 is db2}")
print(f"db1.connection: {db1.connection}")

# Cleanup
try:
    import os
    if os.path.exists("test.txt"):
        os.remove("test.txt")
        print("Cleaned up test file")
except:
    pass