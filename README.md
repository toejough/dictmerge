#pymerge

merge arbitrary python objects

#which

version 0.2.0 - functional, customizable, extensible.

#what

##pymerge.Merge

[BaseMerge] with some default merge behaviors:

```python
from pymerge import Merge
merge = Merge()

# Non-dictionary iterables of the same type are merged to that type
merge(tuple1, tuple2) # tuple1 + tuple2
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

# Non-iterables merge to a tuple
merge(1, 2)  # (1, 2)
merge(1, “hi”)  # (1, “hi”)
merge(“foo”, “bar”)  # (“foo”, “bar”)

# Iterables of different types merge to a tuple
merge({1, 2}, [3, 4]) # (1, 2, 3, 4)
```

See [BaseMerge] for Merge's interface.

#how

Merge works by:

1. Identifying the types of the arguments
1. Executing a type-pair-specific merge function

Type identification is not done by the standard python ```type(foo)```.  Instead, ```pymerge``` uses duck-typing to identify type via an ordered list of ```("type", predicate)``` tuples, where ```predicate``` returns True if the object is of the labeled type, and False otherwise.

```pymerge``` considers the object to be of the first type whose predicate returns True (which is why ordering is important).  The type API looks like:
```python
merge.define_type('foo', label x: 'foo' in x)  # defines type 'foo' to be anything with 'foo' in it
merge.type([1,2,3])  # returns "list"
merge.type('foobar')  # returns "foo"
merge.type([1, 2, 'foo'])  # returns "foo"
merge.remove_type('foo')  # undefines the 'foo' type.
merge.type('foobar')  # returns "default", because now 'foobar' doesn't fit any of the defined types
merge.list_types()  # lists the defined types (in order of precedence)
merge.reorder_types(<list of types>)  # reorders the list of type checkers
```

```pymerge``` then internally looks up the correct merge function for the two types it identified, and merges the arguments.  The merge rule API looks like:
```python
merge.set_rule('foo', 'bar', lambda a, b: "baz")  # if a "foo" type is merged with a "bar" type, the result is "baz"
merge.delete_rule('foo', 'bar')  # removes that rule
```

The set/delete rule functions also take a ```commutative``` argument, which defaults to ```True```.  This allows you to define different behaviors for different types:
```python
merge.set_rule('default', 'list', lambda a, b: [a] + b, commutative=False)
merge.set_rule('list', 'default', lambda a, b: raise Exception("I don't want to do this for you"), commutative=False)
merge.set_rule('list', 'default', lambda a, b: a + [b])  # ERROR - commutative defalts to true...
# now this will apply to both "[1, 2, 3], 4" (fine) and "1, [2, 3, 4]" (error)
```

#what else

I’m planning on adding a few pre-customized merge classes for non-default behaviors, such as:

- Throw an exception if merged dictionaries contain the same keys (instead of recursing)
- Do a set intersection instead of a union when merging sets
- Support merging generators (not default because it's not clear to me what the correct behavior is)

For a full list, see the [issues](https://github.com/toejough/pymerge/issues/4).

#testing

testing is done via py.test, with the tests in [test_main.py](https://github.com/toejough/pymerge/blob/master/test_main.py).

#installation
```sh
pip install --upgrade git+http://github.com/toejough/pymerge
```
