# objprint

[![build](https://github.com/gaogaotiantian/objprint/workflows/build/badge.svg)](https://github.com/gaogaotiantian/objprint/actions?query=workflow%3Abuild)  [![coverage](https://img.shields.io/codecov/c/github/gaogaotiantian/objprint)](https://codecov.io/gh/gaogaotiantian/objprint)  [![pypi](https://img.shields.io/pypi/v/objprint.svg)](https://pypi.org/project/objprint/)  [![support-version](https://img.shields.io/pypi/pyversions/objprint)](https://img.shields.io/pypi/pyversions/objprint)  [![license](https://img.shields.io/github/license/gaogaotiantian/objprint)](https://github.com/gaogaotiantian/objprint/blob/master/LICENSE)  [![commit](https://img.shields.io/github/last-commit/gaogaotiantian/objprint)](https://github.com/gaogaotiantian/objprint/commits/master)

A library that can print Python objects in human readable format

## Install
```
pip install objprint
```

## Usage

### objprint

Use ```objprint()``` to print objects.

```python
from objprint import objprint

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

objprint(Player())
```

```
<Player
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

### include/exclude attributes

You can include/exclude attributes using regular expression so ```objprint``` will only print
out the attributes you are interested in.

```python
objprint(Player(), include=["name"])
```
```
<Player
  .name = 'Alice'
>
```

```python
objprint(Player(), exclude=[".*s"])
```

```
<Player
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

```include``` and ```exclude``` arguments work on ```objprint```, ```objstr``` and ```@add_objprint```.

### config

```objprint``` formats the output based on some configs

* ``depth`` determines how deep ```objprint``` goes into nested data structures
* ``indent`` determines the indentation
* ``width`` determines the maximum width a data structure will be presented as a single line
* ``elements`` determines the maximum number of elements that will be displayed 

You can set the configs globally using ``config`` function

```python
from objprint import config

config(indent=4)
```

Or you can do a one time config by passing the arguments into ``objprint`` function

```python
from objprint import objprint

objprint(var, indent=4)
```

### install

Maybe you don't want to import ``objprint`` in every single file that you want to use. You can
use ``install`` to make it globally accessible

```python
from objprint import install

# Now you can use objprint() in any file
install()

# You can specify a name for objprint()
install("op")
op(my_object)
```

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/gaogaotiantian/objprint/issues).

## License

Copyright Tian Gao, 2020.

Distributed under the terms of the  [Apache 2.0 license](https://github.com/gaogaotiantian/objprint/blob/master/LICENSE).
