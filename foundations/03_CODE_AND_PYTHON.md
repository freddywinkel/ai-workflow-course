# Foundation 3 — Reading Code and First Python

## Outcome

You can read a small Python function, identify its inputs and output, run a
small test, and recognise when AI-generated code is still unexplained.

## What code is

Code is a precise set of instructions written for a computer. It is stored as
text. A Python file normally ends in `.py`. Python reads the syntax, executes
the instructions, and either produces a result or raises an error.

Programming errors are normal:

- a **syntax error** means the text is not valid Python;
- a **runtime error** occurs while valid code is running;
- a **logic error** produces the wrong result without necessarily crashing.

A program that runs is not automatically correct or safe.

## Small Python building blocks

```python
state = "received"
retry_count = 0
is_approved = False
```

These variables give names to values. Python types include:

- `str`: text;
- `int`: whole number;
- `float`: approximate decimal number;
- `bool`: `True` or `False`;
- `None`: deliberately no value.

Lists preserve a sequence:

```python
states = ["received", "validated", "parsed"]
```

Dictionaries map keys to values:

```python
run = {
    "trace_id": "demo-001",
    "state": "received",
    "retry_count": 0,
}
```

Conditions choose a branch:

```python
if run["state"] == "received":
    print("validation may begin")
else:
    print("stop and inspect the current state")
```

Indentation is part of Python syntax. The indented line belongs to the branch.

## Functions

A function is a named, reusable piece of behaviour:

```python
def may_execute(approved: bool, output_changed: bool) -> bool:
    if not approved:
        return False
    if output_changed:
        return False
    return True
```

Read it in this order:

1. Name: `may_execute`.
2. Inputs: `approved` and `output_changed`, both expected to be Boolean.
3. Output: a Boolean.
4. Branches: no approval means false; changed output means false.
5. Remaining path: true.

Type hints such as `: bool` help readers and tools but do not prove the caller
provided a correct value. Tests and runtime validation are still required.

## Imports, modules, and packages

```python
from hashlib import sha256
```

A module is a Python file or library component. A package is an installable
collection of modules. An import makes another module's functionality available.
Installing a package and importing it are separate steps.

Use:

```powershell
python -m pip install package-name
```

only when the course requirements or audited setup names the package. Do not
install a package suggested solely because its name resembles a trusted one.

## Virtual environments

A virtual environment is a project-specific Python tool cupboard. It keeps this
course's packages separate from unrelated projects.

```powershell
py -V:3.13 -m venv .venv
```

This creates `.venv` in the current project. Activating it changes which
`python` and `pip` commands the terminal uses. It does not make code safe.

If activation fails, the setup guide shows how to call the environment's Python
directly.

## Tests

A test makes an expected behaviour executable:

```python
def test_changed_output_cannot_execute():
    assert may_execute(approved=True, output_changed=True) is False
```

This test documents one safety rule and fails if the code violates it. A useful
test includes failure and boundary cases, not only a happy path.

`pytest -q` finds and runs tests. Typical output:

```text
3 passed in 0.12s
```

This means three discovered tests passed in that environment. It does **not**
mean every possible behaviour is correct.

## A safe way to read generated code

For each new function, require answers to:

1. What enters this function?
2. What leaves it?
3. What can it change outside itself?
4. Which failures can occur?
5. Which safety rule does it enforce?
6. Which tests prove happy, failure, and boundary paths?
7. What happens with missing, empty, or malicious input?

If you cannot answer those questions, keep the change small and ask for a
line-by-line explanation before running it.

## Practice

Create `hello_course.py` in your practice folder:

```python
def state_message(state: str) -> str:
    if state == "completed":
        return "The run ended safely."
    return "The run still needs attention."


print(state_message("needs_review"))
```

From that folder, run:

```powershell
python hello_course.py
```

Expected output:

```text
The run still needs attention.
```

Change only `"needs_review"` to `"completed"` and rerun. Then deliberately
remove the colon after `if`, observe the syntax error, restore it, and rerun.
The exercise is to see how code, output, error, and correction relate.

## Chapter check

Explain in your own words:

- variable, list, dictionary, condition, function, input, output, and test;
- why “the code ran” is weaker than “the required tests passed”;
- why an AI-generated function must remain small enough for you to explain.

