"""
Object-Oriented Programming in Python Using Dictionaries

This module implements OOP principles using Python dictionaries rather than classes.
It includes implementations for inheritance, polymorphism, method calls, and static/class methods.

Classes are represented as dictionaries with methods as function references.
Instances are dictionaries with a reference to their class and instance-specific attributes.
"""

# ----- Core OOP Functions -----

def make(cls, *args, **kwargs):
    """
    Create a new instance of a class.
    
    Args:
        cls: Class dictionary to instantiate
        *args, **kwargs: Arguments to pass to the class constructor
        
    Returns:
        A new instance dictionary
    """
    return cls["_new"](*args, **kwargs)

def call(thing, method_name, *args, **kwargs):
    """
    Call a method on an instance or class.
    
    Args:
        thing: Instance or class dictionary
        method_name: Name of the method to call
        *args, **kwargs: Arguments to pass to the method
        
    Returns:
        Result of the method call
    """
    is_instance = thing.get("_is_instance", False)
    
    # Find the method in the class hierarchy
    if is_instance:
        method = find(thing["_class"], method_name)
    else:
        method = find(thing, method_name)
    
    # Handle different method types (static, class, instance)
    if hasattr(method, "__is_static__"):
        return method(*args, **kwargs)
    elif hasattr(method, "__is_class__"):
        return method(thing["_class"] if is_instance else thing, *args, **kwargs)
    else:
        return method(thing, *args, **kwargs)

def find(cls, method_name):
    """
    Find a method in a class or its parent classes.
    Uses method caching for efficiency.
    
    Args:
        cls: Class dictionary
        method_name: Name of the method to find
        
    Returns:
        Method function if found
        
    Raises:
        NotImplementedError: If method not found in class hierarchy
    """
    # Check the cache first
    cached_method = look_in_cache(cls, method_name)
    if cached_method is not None:
        return cached_method
    
    # Search through class hierarchy
    current_cls = cls
    while current_cls is not None:
        if method_name in current_cls:
            # Cache the method for future lookups
            current_cls["cache"][method_name] = current_cls[method_name]
            return current_cls[method_name]
        current_cls = current_cls["parent"]
    
    raise NotImplementedError(f"Method '{method_name}' not found")

def look_in_cache(cls, method_name):
    """
    Look for a method in the class cache.
    
    Args:
        cls: Class dictionary
        method_name: Name of the method to find
        
    Returns:
        Cached method if found, None otherwise
    """
    if "cache" in cls and method_name in cls["cache"]:
        return cls["cache"][method_name]
    return None

# ----- Type and Instance Checking -----

def type_(thing):
    """
    Get the type (class name) of an instance or class.
    
    Args:
        thing: Instance or class dictionary
        
    Returns:
        The class name as a string
    """
    is_instance = thing.get("_is_instance", False)
    if is_instance:
        return thing["_class"]["_classname"]
    else:
        return thing["_classname"]

def isinstance_(thing, parent):
    """
    Check if an instance is an instance of a given class or its subclasses.
    
    Args:
        thing: Instance dictionary to check
        parent: Class dictionary to check against
        
    Returns:
        True if thing is an instance of parent, False otherwise
    """
    current_class = thing["_class"]
    while current_class is not None:
        if current_class == parent:
            return True
        current_class = current_class["parent"]
    return False

# ----- Method Decorators -----

def mark_as_static(func):
    """
    Decorator to mark a method as static.
    Static methods don't receive 'self' or 'cls' as the first argument.
    
    Args:
        func: Function to mark as static
        
    Returns:
        Decorated function
    """
    func.__is_static__ = True
    return func

def mark_as_class(func):
    """
    Decorator to mark a method as a class method.
    Class methods receive the class as the first argument.
    
    Args:
        func: Function to mark as a class method
        
    Returns:
        Decorated function
    """
    func.__is_class__ = True
    return func

# ----- Base Object Class -----

def new_object():
    """
    Constructor for the Object class.
    
    Returns:
        A new Object instance
    """
    return {
        "_class": Object,
        "_is_instance": True
    }

Object = {
    "_classname": "Object",
    "parent": None,
    "_new": new_object,
    "cache": {}
}

# ----- Shape Class -----

def shape_new(name):
    """
    Constructor for the Shape class.
    
    Args:
        name: Name of the shape
        
    Returns:
        A new Shape instance
    """
    shape = make(Object)
    shape.update({
        "name": name,
        "_class": Shape
    })
    return shape

def density(thing, weight):
    """
    Calculate the density of a shape.
    
    Args:
        thing: Shape instance
        weight: Weight of the shape
        
    Returns:
        Density calculated as weight / area
    """
    return weight / call(thing, "area")

Shape = {
    "_classname": "Shape",
    "parent": Object,
    "density": density,
    "_new": shape_new,
    "cache": {}
}

# ----- Square Class -----

def square_new(name, side):
    """
    Constructor for the Square class.
    
    Args:
        name: Name of the square
        side: Length of the square's side
        
    Returns:
        A new Square instance
    """
    square = make(Shape, name)
    square.update({
        "_class": Square,
        "side": side
    })
    return square

def square_perimeter(thing):
    """
    Calculate the perimeter of a square.
    
    Args:
        thing: Square instance
        
    Returns:
        Perimeter of the square
    """
    return thing["side"] * 4

def square_area(thing):
    """
    Calculate the area of a square.
    
    Args:
        thing: Square instance
        
    Returns:
        Area of the square
    """
    return thing["side"] ** 2

def is_larger_than(thing, size):
    """
    Check if the square's area is larger than given size.
    
    Args:
        thing: Square instance
        size: Size to compare against
        
    Returns:
        True if square's area is larger than size, False otherwise
    """
    return call(thing, "area") > size

@mark_as_static
def multiply_by_two(x):
    """
    Static method example that doubles a value.
    
    Args:
        x: Value to double
        
    Returns:
        Doubled value
    """
    return 2 * x

@mark_as_class
def get_description(cls):
    """
    Class method example that returns the class description.
    
    Args:
        cls: Class dictionary
        
    Returns:
        Description of the class
    """
    return cls["description"]

Square = {
    "_classname": "Square",
    "parent": Shape,
    "_new": square_new,
    "area": square_area,
    "perimeter": square_perimeter,
    "is_larger_than": is_larger_than,
    "multiply_by_two": multiply_by_two,
    "get_description": get_description,
    "description": "A four-sided polygon with equal sides and angles",
    "cache": {}
}

# ----- Main Example -----

if __name__ == "__main__":
    # Create a square instance
    square = make(Square, "my_square", 5)
    
    # Test instance methods
    comparison_area = 20
    perimeter = call(square, "perimeter")
    is_larger = call(square, "is_larger_than", comparison_area)
    shape_density = call(square, "density", 3)
    
    # Print instance method results
    print(f"Square name: {square['name']}, perimeter: {perimeter}")
    print(f"Square name: {square['name']}, is larger than {comparison_area}: {is_larger}")
    print(f"Square name: {square['name']}, density: {shape_density}")
    
    # Test static method
    value = 3
    doubled = call(square, "multiply_by_two", value)
    doubled_via_class = call(Square, "multiply_by_two", value)
    print(f"Double {value} via instance: {doubled}")
    print(f"Double {value} via class: {doubled_via_class}")
    
    # Test class method
    description = call(Square, "get_description")
    print(f"Square description: {description}")
    
    # Test type and instance checking
    print(f"Type of square is: {type_(square)}")
    print(f"Is square instance of Shape: {isinstance_(square, Shape)}")
    
    # Check cache contents
    print(f"Cache contents: {square['_class']['cache']}")