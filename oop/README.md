# Dict-Based OOP

Minimal implementation of OOP concepts using Python dictionaries.

## Core

- `make(cls, *args)`: Create instances
- `call(obj, method, *args)`: Execute methods
- `find(cls, method)`: Method lookup with caching

## Example

```python
# Instance creation and method calls
square = make(Square, "my_square", 5)
perimeter = call(square, "perimeter")  # 20
doubled = call(square, "multiply_by_two", 4)  # 8
description = call(Square, "get_description")  # class description

# Type checking
type_(square)  # "Square"
isinstance_(square, Shape)  # True
```

