# objprint
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
  .name = 'Alice',
  .age = 18,
  .items = ['axe', 'armor'],
  .coins = {'gold': 1, 'silver': 33, 'bronze': 57},
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

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/gaogaotiantian/objprint/issues).

## License

Copyright Tian Gao, 2020.

Distributed under the terms of the  [Apache 2.0 license](https://github.com/gaogaotiantian/objprint/blob/master/LICENSE).
