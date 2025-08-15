


# String Examples in Python

# Creating strings
single_quote_str = 'Hello'
double_quote_str = "World"
multi_line_str = """This is
a multi-line
string."""

print(single_quote_str)
print(double_quote_str)
print(multi_line_str)

# String concatenation
full_str = single_quote_str + " " + double_quote_str
print("Concatenated:", full_str)

# Indexing and slicing
print("First character:", full_str[0])
print("Last character:", full_str[-1])
print("Slice [0:5]:", full_str[0:5])

# String repetition
repeat_str = single_quote_str * 3
print("Repeated:", repeat_str)

# String methods
sample_str = "  Python Programming  "
print("Uppercase:", sample_str.upper())
print("Lowercase:", sample_str.lower())
print("Title case:", sample_str.title())
print("Stripped:", sample_str.strip())
print("Replaced:", sample_str.replace("Python", "Java"))

# Membership check
print("'Python' in sample_str:", "Python" in sample_str)
print("'Java' not in sample_str:", "Java" not in sample_str)

# String formatting
name = "Alice"
age = 30
print("My name is {} and I am {} years old.".format(name, age))
print(f"My name is {name} and I am {age} years old.")

# Splitting and joining
words = sample_str.strip().split(" ")
print("Split into words:", words)
joined_str = "-".join(words)
print("Joined with hyphen:", joined_str)