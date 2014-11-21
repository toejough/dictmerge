#pymerge

merge arbitrary python objects

#which

version 0.1.0 - basic functionality.  customizable, but not (yet) extensible.

#what

##pymerge.merge

```python
from pymerge import merge

merge(1, 2)  # (1, 2)
merge(1, “hi”)  # (1, “hi”)
merge(“foo”, “bar”)  # (“foo”, “bar”)
merge(list1, list2)  # list1 + list2
merge(set1, set2)  # set1 | set2

# Dictionaries are a special case
d = merge(dict1, dict2)
# d now equals dict1, with any new key/value pairs from dict 2
# if there are overlapping keys, the resulting value is created
# by recursively calling merge:
dict1 = {‘foo’: “FOO”}
dict2 = {‘foo’: “spam”, ‘bar’: “eggs”}
d = merge(dict1, dict2)
# d is now {
#   ‘foo’: (“FOO”, “spam”),
#   ‘bar’: “eggs”
# }
```

The dictionary merge semantics (and all others) are overridable via the pymerge.MERGE_DICTIONARY.
This is ugly, I know, and will be improved upon in future versions.

#what else

I’m planning on adding better semantics for overriding type-specific merge behavior, as well as adding support for merging custom types (which are currently always assumed to be scalar).
For a full list, see the [issues](https://github.com/toejough/pymerge/issues).

#testing

testing is done via py.test, with the tests in [test_main.py](https://github.com/toejough/pymerge/blob/master/test_main.py).

#installation
```sh
pip install --upgrade git+http://github.com/toejough/pymerge
```
