# Software Design From Scratch

This repository contains implementations of various software design concepts and tools built from scratch. The goal is to deeply understand these concepts by implementing them with minimal dependencies, revealing how they work under the hood.

## Why Build From Scratch?

Building core concepts from scratch helps to:

- Gain deeper understanding of fundamental principles
- Demystify "magic" in software libraries and frameworks
- Learn how to make better design decisions in your own code
- Appreciate the elegance of well-designed software systems

## Implemented Projects

### [Object-Oriented Programming](./oop/README.md)
A minimal implementation of OOP principles using only Python dictionaries and functions. Demonstrates inheritance, polymorphism, and method dispatch without using Python's built-in class system.

### [Pattern Matching](./matching/)
Text pattern matching engine supporting literals, wildcards (`Any`), and alternatives (`Either`). Includes caching and memoization for performance optimization.

### [DataFrame Implementation](./per/)
From-scratch implementation of a pandas-like DataFrame with row-based storage. Supports filtering, selection, column operations, and equality checking.

### [Parser & Tokenizer](./parser/)
Complete parsing system with tokenization and recursive descent parsing. Converts string patterns into executable pattern matching objects.

### [Decorators](./decorator/)
Function decorator implementations including file-based logging decorators that track function calls and arguments.

### [Hash-Based Tools](./hash/)
File duplicate detection using SHA256 hashing with configurable chunk sizes for efficient duplicate file identification.

### [Language Interpreter](./interpreter/)
Simple programming language interpreter supporting arithmetic operations, variable bindings, conditionals, and function calls with environment management.

### [Protocol Implementations](./protocols/)
From-scratch implementations of Python protocols:
- **Context Managers**: Custom `__enter__`/`__exit__` implementations including exception handling and timing
- **Iterators**: Custom iteration protocols

### [HTML/DOM Validator](./validator/)
HTML parsing and validation tools using BeautifulSoup integration for DOM tree traversal and analysis.

### [File Operations](./file/)
File system utilities including migration tools and file manipulation helpers with comprehensive test coverage.

### [Code Analysis Tools](./lint/)
Static analysis tools for detecting unused variables, duplicate dictionary keys, and other code quality issues.

### [Closure Examples](./closures/)
Demonstrations of closure patterns and lexical scoping in Python.

## Key Design Principles

Each implementation follows these principles:

- **Minimal Dependencies**: Use only standard library when possible
- **Educational Focus**: Code is written for clarity and understanding
- **Test Coverage**: Most modules include comprehensive tests
- **Progressive Complexity**: Start simple, add features incrementally
- **Real-World Utility**: Solve actual problems, not just toy examples

## Getting Started

```bash
# Clone the repository
git clone <repository-url>
cd software_design

# Install dependencies (minimal)
pip install -r requirements.txt

# Run tests for specific modules
python -m pytest file/tests/
python -m pytest per/test_main.py

# Try the examples
python oop/oop.py
python hash/brute_force.py file1.txt file2.txt
python interpreter/main.py
```

## Project Structure

- Each directory contains a focused implementation
- Most modules include their own test files
- README files provide specific documentation where needed
- Examples demonstrate practical usage

This repository serves as both a learning resource and a collection of useful utilities built with deep understanding of their underlying principles.