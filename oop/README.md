# Dictionary-Based OOP Implementation

This project implements Object-Oriented Programming principles using Python dictionaries, demonstrating how OOP concepts work under the hood.

## Core Concepts

- **Classes**: Dictionaries with methods (functions) and attributes (key-value pairs)
- **Inheritance**: Implemented via `parent` references in class dictionaries
- **Polymorphism**: Methods are looked up dynamically in the inheritance chain
- **Method Types**: Instance methods, static methods, and class methods

## Key Functions

- `make(cls, *args)`: Create new instances
- `call(obj, method, *args)`: Execute methods on objects
- `find(cls, method)`: Locate methods in the class hierarchy with caching

## Example

```python
# Create an instance
square = make(Square, "my_square", 5)

# Call instance method
perimeter = call(square, "perimeter")  # Returns 20

# Call static method
doubled = call(square, "multiply_by_two", 4)  # Returns 8

# Call class method
description = call(Square, "get_description")  # Returns class description
```

This implementation demonstrates how OOP concepts can be implemented from scratch using only dictionaries and functions, providing insight into how OOP languages work under the hood.

