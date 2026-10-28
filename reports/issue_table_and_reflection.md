# Lab 5: Static Code Analysis

## 1. Issues Identified and Fixed

| Issue | Tool | Type | Fix applied |
|---|---|---|---|
| Mutable default argument `[]` | Pylint | Bug / code quality | Replaced with `None` and initialized the list inside the function. |
| Global reservation counter | Pylint | Maintainability | Replaced the mutable global counter with `itertools.count()`. |
| Missing module and function documentation | Pylint | Documentation | Added module and function docstrings. |
| Bare exception and silent error handling | Pylint / Bandit | Reliability / security | Added specific exception handling and explicit validation. |
| Shell command using `os.system()` | Bandit | High-severity security issue | Replaced shell execution with Python file operations. |
| Files opened without explicit encoding | Pylint | Portability | Added `encoding="utf-8"`. |
| Files opened without context managers | Pylint | Resource management | Used `with open(...)` to manage file resources. |
| Non-standard function naming | Pylint | Naming convention | Preserved the assigned `logConflicts()` name and documented the naming exception. |
| Long lines and whitespace issues | Pylint / Flake8 | Formatting | Reformatted code and removed trailing whitespace. |
| Unused local variables | Pylint / Flake8 | Code quality | Removed unnecessary variables. |
| Invalid time-slot input | Runtime validation | Reliability | Added validation for time-slot format and valid hour ranges. |
| Insufficient or unknown equipment | Runtime validation | Reliability | Validated equipment availability before updating inventory. |

## 2. Reflection Questions and Answers

### Q1. What is static code analysis?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, maintainability problems, and style violations.

### Q2. What is the difference between Pylint, Bandit, and Flake8?

- **Pylint:** Checks code quality, naming conventions, documentation, and potential programming errors.
- **Bandit:** Identifies common security vulnerabilities in Python code.
- **Flake8:** Checks style violations, whitespace, line lengths, and certain programming errors.

### Q3. What issues did you identify in the original program?

The original program contained a mutable default argument, a global statement, a bare exception, missing docstrings, file-handling issues, unused variables, formatting violations, and a potentially unsafe shell command.

### Q4. How did you address the security issues?

I replaced the shell command with Python file operations and removed the bare exception pattern. I reran Bandit to verify that no security findings remained.

### Q5. Why should mutable default arguments be avoided?

A mutable default object, such as a list, is shared across function calls. This can cause unintended state to persist between calls. Using `None` and initializing a new list inside the function avoids this problem.

### Q6. What did you learn from this lab?

I learned how to use Pylint, Bandit, and Flake8 together to improve code quality, security, and formatting. I also learned to verify changes by rerunning the analysis tools and comparing their reports before and after the fixes.

## 3. Final Results

- Pylint score: 10.00/10
- Bandit: No issues identified
- Flake8: No findings
- Python syntax compilation: Successful
- Program execution: Successful

The final results were recorded after rerunning the analysis tools against the updated Python source.
