#dictmerge

merge python dictionaries

- [which](#which)
- [why](#why)
- [what](#what)
- [how](#how)
- [testing](#testing)
- [installation](#installation)

#which

latest version - 0.5.0

#why

Because merging dictionaries in python seems like it should be straightforward, but often it's not.

#what

Merge dictionaries according to the following rules:
* return a copy which does not change either of the inputs
* any keys unique to one dictionary are added
* any keys present in both dictionaries cause the optional resolver function to be called

The default resolver function will:
* resolve any keys whose values match in both dictionaries to a single key/value pair to be added
* resolve keys whose values are both dictionaries to a recursively merged dictionary

#how

Example:
```python
from dictmerge import merge

# define dict1, dict2...

d = merge(dict1, dict2)
```

#testing

testing is done via py.test, with the tests in [test_main.py](https://github.com/toejough/dictmerge/blob/master/test_main.py).

#installation
```sh
pip install --upgrade git+http://github.com/toejough/dictmerge
```

