PyLint and Vulture detect unused functions, classes, and imports and can warn about unused methods. They are developer tools to assist with code quality and optimization.

USAGE:

- Install pylint and vulture:
  pip install pylint vulture

- Run them from the root repository directory:
  python -m pylint src/ > lint/pylint.txt
  python -m vulture src/ > lint/vulture.txt
