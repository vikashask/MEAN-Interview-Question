# Write a function that capitalizes the first and fourth letters of a name
def capitalize_name(name):
    if len(name) < 4:
        return "Name must be at least 4 characters long."
    # Capitalize the first and fourth letters
    name_list = list(name)
    name_list[0] = name_list[0].upper()
    name_list[3] = name_list[3].upper()
    return ''.join(name_list)   

# Example usage
print(capitalize_name("john"))  # Output: "John"
print(capitalize_name("alice"))  # Output: "AlIcE"

def old_macdonald(name):
    if len(name) > 3:
        return name[:3].capitalize() + name[3:].capitalize()
    else:
        return 'Name is too short!'
print(old_macdonald('macdonald'))