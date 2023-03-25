# Style Guide

This style guide aims to maintain code readability, quality, and maintainability.It incorporates best practices and focuses on a "universal design" approach to make the code understandable to both experts and non-experts.

## General Guidelines

0. Use SOLID principles to design your code whenever possible.

0.5 Write code that will be easy to understand by people without experience in this programming language or project 

1. **Include Google-formatted docstrings**: Use Google-style docstrings for functions, methods, and classes to provide clear and concise documentation.

2. **Type hints**: Use input and return type hints for functions and methods to improve code readability and facilitate better tooling support.

3. **Keyword arguments**: Prefer using keyword arguments over simple arguments for functions and methods to improve code clarity.

4. **Private methods and attributes**: Use leading underscores to denote private methods and attributes in classes, and use `@property` decorators when appropriate.

5. **Descriptive names**: Use full words in variable and class names instead of abbreviations (e.g., `database` instead of `db`).

6. **PEP8 and `black` formatting**: Follow PEP8 and `black` code formatting guidelines to maintain consistency and readability.


8. **Keep functions and methods short**: Aim to keep functions and methods concise, ideally not exceeding 15-20 lines of code.

9. **Modularize code**: Organize code into modules and packages to maintain a clean and organized codebase.

10. **Minimal comments**: Avoid comments if possible.

11. **Error handling**: Use appropriate error handling techniques, such as `try` and `except` blocks, to handle exceptions and provide meaningful error messages to users.

12. **Write tests**: Write unit tests to ensure the correct functioning of your code.

13. **Code reviews**: Perform code reviews with team members or peers to maintain a high-quality codebase.
