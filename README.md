# objprint

[![build](https://github.com/gaogaotiantian/objprint/workflows/build/badge.svg)](https://github.com/gaogaotiantian/objprint/actions?query=workflow%3Abuild)  [![coverage](https://img.shields.io/codecov/c/github/gaogaotiantian/objprint)](https://codecov.io/gh/gaogaotiantian/objprint)  [![pypi](https://img.shields.io/pypi/v/objprint.svg)](https://pypi.org/project/objprint/)  [![support-version](https://img.shields.io/pypi/pyversions/objprint)](https://img.shields.io/pypi/pyversions/objprint)  [![license](https://img.shields.io/github/license/gaogaotiantian/objprint)](https://github.com/gaogaotiantian/objprint/blob/master/LICENSE)  [![commit](https://img.shields.io/github/last-commit/gaogaotiantian/objprint)](https://github.com/gaogaotiantian/objprint/commits/master)

A library that can print Python objects in human readable format

## Install
```
pip install objprint
```

## Usage

### op

Use ```op()``` (or ```objprint()```) to print objects.

```python
from objprint import op

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player:
    def __init__(self):
        self.name = "Alice"
        self.age = 18
        self.items = ["axe", "armor"]
        self.coins = {"gold": 1, "silver": 33, "bronze": 57}
        self.position = Position(3, 5)

op(Player())
```

```
<Player 0x7fe44e1e3070
  .age = 18,
  .coins = {'bronze': 57, 'gold': 1, 'silver': 33},
  .items = ['axe', 'armor'],
  .name = 'Alice',
  .position = <Position
    .x = 3,
    .y = 5
  >
>
```

You can print multiple objects just like print, except ``op`` will print them in separate lines

```python
op([1, 2], {'a': 1})
```

```
[1, 2]
{'a': 1}
```

``op`` will return the same object it prints, so you can do something like this

```python
a = MyObject()
# print the args inline with minumum change
function_using_object(op(a))
# the difference is more significant with complex expressions
# original: function_using_object(a.f() + a.g())
function_using_object(op(a.f() + a.g()))
```

It works on multiple objects as well, as it returns a tuple, you need to unpack it for functions

```python
a = MyObject()
function_using_object(*op(a.f(), a.g()))
```

### add_objprint

If you want to use ```print()``` to print your object, you can also use the class decorator
```add_objprint``` to add ```__str__``` method for your class.

```python
from objprint import add_objprint

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

@add_objprint
class Player:
    def __init__(self):
        self.name = "Alice"
        self.age = 18
        self.items = ["axe", "armor"]
        self.coins = {"gold": 1, "silver": 33, "bronze": 57}
        self.position = Position(3, 5)

# This will print the same thing as above
print(Player())
```

### objstr

If you want the ``str`` representation of the object, instead of printing it on the screen,
you can use ``objstr`` function

```python
from objprint import objstr

s = objstr(my_object)
```

### print more

There are some optional information you can print with [config](###config).

#### "Public" Methods

There are no REAL public methods in python, here I simply meant you can print methods that do not start with ``__`` as there will be
a lot of default magic methods and you don't want that.

```python
class Player:
    def attack(self, opponent):
        pass

op(Player(), print_methods=True)
```

```
<Player 0x7fe44e1e3070
  def attack(opponent)
>
```

As you can see, it will also print the method signature(without ``self`` argument).

#### Line numbers

You can print execution info, including the function it's in, the file and the line number of the printing line.
This is helpful for you to locate where this object is printed.

```python
def f():
    op(Player(), line_number=True)
f()
```

```
f (my_script.py:29)
<Player 0x7f30e8cb1ac0
  ...
>
```

### Argument names

You can print the expression of the argument with `arg_name`

```python
op(Player(), arg_name=True)
```

```
Player():
<Player 0x7f495850a8d0
  ...
>
```

### objjson

``objprint`` supports print objects to json to make it easier to serialize an object.

``objjson`` returns a jsonifiable object that can be dumped with ``json.dumps``

```python
from objprint import objjson

json_obj = objjson(Player())

print(json.dumps(json_obj, indent=2))
```

```
{
  ".type": "Player",
  "name": "Alice",
  "age": 18,
  "items": [
    "axe",
    "armor"
  ],
  "coins": {
    "gold": 1,
    "silver": 33,
    "bronze": 57
  },
  "position": {
    ".type": "Position",
    "x": 3,
    "y": 5
  }
}
```

You can use ``op`` to print in json format directly with ``format="json"``. You can pass in argument for ```json.dumps```

```python
op(Player(), format="json", indent=2)
```

``add_objprint`` also works with ``format="json``"

```python
@add_objprint(format="json", indent=2)
class Player:
    pass
```

### Enable/Disable the print

You can disable prints from all the ``op()`` calls globally with ``enable`` config.

```python
from objprint import op

op.disable()
op([1, 2, 3])  # This won't print anything
op.enable()  # This could fix it!
```

Or you can use it for ``op()`` functions individually with some conditions

```python
op(obj, enable=check_do_print())
```

### attribute selection

You can customize which attribute to print with name filters.

``objprint`` will try to match the attribute name with ``attr_pattern`` regex. The default
``attr_pattern`` is ``r"(!_).*"``, which means anything that does NOT start with an `_`.

You can customize ``attr_pattern`` to select the attributes you want to print:

```python
# This will print all the attributes that do not start with __
op(Player(), attr_pattern=r"(!__).*")
```

You can also use ``include`` and ``exclude`` to specify attributes to print with regular expression
so ```objprint``` will only print out the attributes you are interested in.

```python
op(Player(), include=["name"])
```
```
<Player
  .name = 'Alice'
>
```

```python
op(Player(), exclude=[".*s"])
```

```
<Player 0x7fe44e1e3070
  .name = 'Alice',
  .age = 18,
  .position = <Position
    .x = 3,
    .y = 5
  >
>
```

If you specify both ``include`` and ``exclude``, it will do a inclusive check first, then filter out the attributes
that match exclusive check.

```attr_pattern```, ```include``` and ```exclude``` arguments work on ```objprint```, ```objstr``` and ```@add_objprint```.

### Register Custom Type Formatter

You can also customize how certain types of objects are displayed by registering a custom formatter function to transform an object of a specific type into a string. 

For example, you can print all integers in hexadecimal format by registering the ```hex()``` function for the ```int``` data type, or registering a custom ```lambda``` function. 

```python
from objprint import op

op.register_formatter(int, hex)
op.register_formatter(float, lambda x: f"{round(x, 3)}")
op(10)  # prints 0xa
op(3.14159)  # prints 3.142
```

Alternatively, you can also register a custom formatter function using a decorator:

```python
@op.register_formatter(str)
def custom_formatter(obj: str):
    return f"custom_print: {obj}"

op("hi")  # prints custom_print: hi
```

During registration, ```objprint``` will examine the specified object type, and raise a ```TypeError``` if an invalid object type is provided.

When you finish using the custom formatters, you can unregister them with ```unregister_formatter()```.

```python
op.unregister_formatter(int, float, str)
op(10)  # prints 10
op(3.14159)  # prints 3.14159
op("hi")  # prints hi
```

Or you can unregister everything by passing no argument to it.

```python
op.unregister_formatter()
```

The ```register_formatter()``` function also accepts an ```inherit``` argument (default ```True```) to dictate if the registered formatter should also apply to any derived classes of the object type.

```python
class BaseClass:
    name = 'A'

class DerivedClass(BaseClass):
    name = 'B'
```

With ```inherit=True```, derived class will share the same formatter registered under base class. 

```python
def base_formatter(obj: BaseClass) -> str:
    return f'Print {obj.name} with Base Class Formatter'

op.register_formatter(BaseClass, base_formatter, inherit=True)

op(DerivedClass())
```

```
Print B with Base Class Formatter
```

With ```inherit=False```, derived class will use the default formatter provided by ```objprint```. 

```python
@op.register_formatter(BaseClass, inherit=False)
def base_formatter(obj: BaseClass) -> str:
    return f'Print {obj.name} with Base Class Formatter'

op(DerivedClass())
```

```
<DerivedClass 0x7fb42e8216a0
  .name = 'B'
>
```

If a derived class inherits from multiple base classes, each with a registered formatter, the chosen formatter adheres to the Method Resolution Order (MRO) of the derived class.

To check all the registered functions and their inheritance status, you can use the ```get_formatter()``` method. It returns a dictionary-like object that you can print for easy inspection.

```python
fmts = op.get_formatter()
print(fmts)
```

```
{<class '__main__.BaseClass'>: FormatterInfo(formatter=<function base_formatter at 0x7feaf33d1f70>, inherit=False)}
```

Please note that registering a formatter function with ```op``` will affect the output of ```objprint``` and ```objstr``` methods in the same way.

### config

```objprint``` formats the output based on some configs

* ``config_name(default_value)`` - this config's explanation
* ``enable(True)`` - whether to print, it's like a switch
* ``depth(100)`` - how deep ```objprint``` goes into nested data structures
* ``indent(2)`` - the indentation
* ``width(80)`` - the maximum width a data structure will be presented as a single line
* ``elements(-1)`` - the maximum number of elements that will be displayed, ``-1`` means no restriction
* ``color(True)`` - whether to use colored scheme
* ``line_number(False)`` - whether to print the ``function (filename:line_number)`` before printing the object
* ``arg_name(False)`` - whether to print the argument expression before the argument value
* ``skip_recursion(True)`` - whether skip printing recursive data, which would cause infinite recursion without ``depth`` constraint
* ``honor_existing(True)`` - whether to use the existing user defined ``__repr__`` or ``__str__`` method
* ``attr_pattern(r"(!_).*")`` - the regex pattern for attribute selection
* ``include([])`` - the list of attribute regex to do an inclusive filter
* ``exclude([])`` - the list of attribute regex to do an exclusive filter

You can set the configs globally using ``config`` function

```python
from objprint import config
config(indent=4)
```

Or if you don't want to mess up your name space

```python
from objprint import op
op.config(indent=4)
```

Or you can do a one time config by passing the arguments into ``objprint`` function

```python
from objprint import op

op(var, indent=4)
```

### install

Maybe you don't want to import ``op`` in every single file that you want to use. You can
use ``install`` to make it globally accessible

```python
from objprint import op, install

# Now you can use op() in any file
install()

# This is the same
op.install()

# You can specify a name for objprint()
install("my_print")
my_print(my_object)
```

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/gaogaotiantian/objprint/issues).

## License

Copyright 2020-2023 Tian Gao.

Distributed under the terms of the  [Apache 2.0 license](https://github.com/gaogaotiantian/objprint/blob/master/LICENSE).
