# Class attributes vs Instance attributes in Python

class Student:
    # Class attributes (shared by all instances)
    school_name = "Python Academy"
    total_students = 0
    subjects = ["Math", "Science", "English"]
    
    def __init__(self, name, grade):
        # Instance attributes (unique to each instance)
        self.name = name
        self.grade = grade
        
        # Modify class attribute
        Student.total_students += 1
    
    def display_info(self):
        return f"Student: {self.name}, Grade: {self.grade}, School: {Student.school_name}"
    
    @classmethod
    def get_total_students(cls):
        """Class method to get total students"""
        return cls.total_students
    
    @classmethod
    def change_school_name(cls, new_name):
        """Class method to change school name"""
        cls.school_name = new_name

# Creating instances
student1 = Student("Alice", "A")
student2 = Student("Bob", "B")
student3 = Student("Charlie", "A")

# Accessing instance attributes
print(student1.display_info())
print(student2.display_info())

# Accessing class attributes
print(f"School: {Student.school_name}")
print(f"Total students: {Student.get_total_students()}")
print(f"Subjects: {Student.subjects}")

# Modifying class attributes
Student.change_school_name("Advanced Python Academy")
print(f"New school name: {Student.school_name}")

# All instances see the change
print(student1.display_info())

# Adding to class attribute list
Student.subjects.append("History")
print(f"Updated subjects: {Student.subjects}")

# Demonstrating the difference
print(f"student1.school_name: {student1.school_name}")  # Inherited from class
print(f"Student.school_name: {Student.school_name}")    # Class attribute

# If we set instance attribute with same name
student1.school_name = "Individual School"
print(f"student1.school_name: {student1.school_name}")  # Instance attribute
print(f"Student.school_name: {Student.school_name}")    # Class attribute unchanged

# More examples of class attributes
class Counter:
    count = 0  # Class attribute
    
    def __init__(self, name):
        self.name = name  # Instance attribute
        Counter.count += 1  # Increment class attribute
    
    @classmethod
    def get_count(cls):
        return cls.count
    
    @classmethod
    def reset_count(cls):
        cls.count = 0

# Testing Counter class
print(f"Initial count: {Counter.get_count()}")
c1 = Counter("First")
c2 = Counter("Second")
print(f"After creating 2 instances: {Counter.get_count()}")

# Private attributes (convention using underscore)
class Employee:
    company = "Tech Corp"  # Class attribute
    
    def __init__(self, name, salary):
        self.name = name           # Public instance attribute
        self._department = "IT"    # Protected attribute (convention)
        self.__salary = salary     # Private attribute (name mangling)
    
    def get_salary(self):
        return self.__salary
    
    def set_salary(self, new_salary):
        if new_salary > 0:
            self.__salary = new_salary

emp = Employee("John", 50000)
print(f"Name: {emp.name}")
print(f"Department: {emp._department}")
print(f"Salary: {emp.get_salary()}")

# Trying to access private attribute directly (will cause AttributeError)
# print(emp.__salary)  # This would fail

# Accessing private attribute using name mangling
print(f"Salary via name mangling: {emp._Employee__salary}")