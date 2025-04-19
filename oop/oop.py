"""
Dictionary-based OOP implementation - minimal core with inheritance, polymorphism, and method dispatch
"""

# Core OOP machinery
def make(cls, *args, **kwargs):
    """Create a new instance of a class"""
    return cls["_new"](*args, **kwargs)

def call(thing, method_name, *args, **kwargs):
    """Call a method on an instance or class"""
    is_instance = thing.get("_is_instance", False)
    method = find(thing["_class"] if is_instance else thing, method_name)
    
    if hasattr(method, "__is_static__"):
        return method(*args, **kwargs)
    elif hasattr(method, "__is_class__"):
        return method(thing["_class"] if is_instance else thing, *args, **kwargs)
    else:
        return method(thing, *args, **kwargs)

def find(cls, method_name):
    """Find a method in a class or its parent classes"""
    cached = look_in_cache(cls, method_name)
    if cached is not None:
        return cached
    
    current_cls = cls
    while current_cls is not None:
        if method_name in current_cls:
            current_cls["cache"][method_name] = current_cls[method_name]
            return current_cls[method_name]
        current_cls = current_cls["parent"]
    
    raise NotImplementedError(f"Method '{method_name}' not found")

def look_in_cache(cls, method_name):
    """Cache lookup helper"""
    if "cache" in cls and method_name in cls["cache"]:
        return cls["cache"][method_name]
    return None

def type_(thing):
    """Get the type (class name) of an instance or class"""
    is_instance = thing.get("_is_instance", False)
    return thing["_class"]["_classname"] if is_instance else thing["_classname"]

def isinstance_(thing, parent):
    """Check if an instance is an instance of a given class"""
    current_class = thing["_class"]
    while current_class is not None:
        if current_class == parent:
            return True
        current_class = current_class["parent"]
    return False

# Method decorators
def mark_as_static(func):
    """Mark a method as static"""
    func.__is_static__ = True
    return func

def mark_as_class(func):
    """Mark a method as a class method"""
    func.__is_class__ = True
    return func

# Base Object class
def new_object():
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

# Shape class
def shape_new(name):
    shape = make(Object)
    shape.update({
        "name": name,
        "_class": Shape
    })
    return shape

def density(thing, weight):
    return weight / call(thing, "area")

Shape = {
    "_classname": "Shape",
    "parent": Object,
    "density": density,
    "_new": shape_new,
    "cache": {}
}

# Square class
def square_new(name, side):
    square = make(Shape, name)
    square.update({
        "_class": Square,
        "side": side
    })
    return square

def square_perimeter(thing):
    return thing["side"] * 4

def square_area(thing):
    return thing["side"] ** 2

def is_larger_than(thing, size):
    return call(thing, "area") > size

@mark_as_static
def multiply_by_two(x):
    return 2 * x

@mark_as_class
def get_description(cls):
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

# Example usage
if __name__ == "__main__":
    square = make(Square, "my_square", 5)
    
    # Test methods
    perimeter = call(square, "perimeter")
    is_larger = call(square, "is_larger_than", 20)
    shape_density = call(square, "density", 3)
    
    print(f"Square: {square['name']}, perimeter: {perimeter}, larger than 20: {is_larger}, density: {shape_density}")
    
    # Static and class methods
    doubled = call(square, "multiply_by_two", 3)
    description = call(Square, "get_description")
    
    print(f"Double 3: {doubled}, Description: {description}")
    print(f"Type: {type_(square)}, Is Shape: {isinstance_(square, Shape)}")
    print(f"Cache: {square['_class']['cache']}")