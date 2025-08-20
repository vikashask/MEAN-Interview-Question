# *args
# The special syntax *args in function definitions in python is used to pass a variable number of arguments to a function.
# It is used to pass a non-keyworded, variable-length argument list.
# The name `args` is just a convention, you can use any name, e.g., *myargs.

print("-- *args example --")

# This function takes a variable number of arguments and returns 5% of their sum.
def myfunc(*args):
    print(f"Arguments received as a tuple: {args}")
    return sum(args) * 0.05

print(f"Result: {myfunc(40, 60)}")
print(f"Result: {myfunc(10, 20, 30, 40, 50, 60)}")


# **kwargs
# The special syntax **kwargs in function definitions in python is used to pass a keyworded, variable-length argument list.
# A keyword argument is where you provide a name to the variable as you pass it into the function.
# **kwargs is a dictionary of the keyword arguments passed to the function.
# The name `kwargs` is a convention, you can use any name, e.g., **mykwargs.

print("\n-- **kwargs example --")

def my_kwargs_func(**kwargs):
    print(f"Arguments received as a dictionary: {kwargs}")
    if 'fruit' in kwargs:
        print(f"My fruit of choice is {kwargs['fruit']}")
    else:
        print("I did not find any fruit here.")

my_kwargs_func(fruit='apple', veggie='lettuce')
my_kwargs_func(food='sushi')


# Combined *args and **kwargs
# You can use both *args and **kwargs in the same function, but *args must appear before **kwargs.

print("\n-- Combined *args and **kwargs example --")

def combined_func(*args, **kwargs):
    print(f"I would like {args[0]} {kwargs['food']}.")

combined_func(10, 20, 30, fruit='orange', food='eggs', animal='dog')

# The order of arguments is: standard arguments, *args, **kwargs
def another_combined_func(a, b, *args, **kwargs):
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"args = {args}")
    print(f"kwargs = {kwargs}")

another_combined_func(1, 2, 3, 4, 5, name="Gemini", version="1.0")
