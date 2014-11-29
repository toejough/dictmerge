#pymerge

merge arbitrary python objects

- [which](#which)
- [why](#why)
- [what](#what)
  - [in general](#in-general)
  - [pymerge.Merge](#pymergemerge)
  - [pymerge.BaseMerge](#pymergebasemerge)
  - [typing](#typing)
    - [default type](#default-type)
  - [merging](#merging)
    - [default merge](#default-merge)
- [what else](#what-else)
  - [pymerge.BasePedanticMerge](#pymergebasepedanticmerge)
  - [pymerge.PedanticMerge](#pymergepedanticmerge)
- [testing](#testing)
- [installation](#installation)
- [design notes](#design-notes)
  - [Merge](#merge)
    - [iterables](#iterables)
    - [non-iterables and iterables](#non-iterables-and-terables)
    - [non-iterables](#non-iterables)
    - [why tuples?](#why-tuples)
  - [PedanticMerge](#merge)
    - [iterables](#iterables)
    - [non-iterables and iterables](#non-iterables-and-terables)
    - [non-iterables](#non-iterables)
    - [why all the errors?](#why-all-the-errors)

#which

latest version - 0.4.1

#why

Because merging dictionaries in python seems like it should be straightforward, but often it's not.

#what

##in general

pymerge is a tool to merge python objects:

- tuple, tuple -> tuple
- list, list -> list
- set, set -> set
- dict, dict -> dict
- other, other -> (other, other)

For specifics, see the [Merge](#pymergemerge) section.

pymerge is also customizable and extensible.  You can use it to create a merge function which merges arbitrary types, and teach it arbitrary definitions for those types. 

##pymerge.Merge

[BaseMerge](#pymergebasemerge) with some default merge behaviors (set up via ```pymerge.define_default_types``` and ```pymerge.set_default_rules```, which define types and rules for the standard python iterators):

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
merge({1, 2}, [3, 4])  # (1, 2, 3, 4)

# Iterables and non-iterables merge to a tuple
merge([1, 2, 3], 4)  # (1, 2, 3, 4)
merge(1, {1: 2})  # (1, {1:2})
```

##pymerge.BaseMerge

```BaseMerge``` works by:

1. Identifying the types of the arguments
1. Executing a type-pair-specific merge function

##typing
Type identification is not done by the standard python ```type(foo)```.  Instead, ```pymerge``` uses duck-typing to identify type via an ordered list of ```("type", predicate)``` tuples, where ```predicate``` returns True if the object is of the labeled type, and False otherwise.

```pymerge``` considers the object to be of the first type whose predicate returns True (which is why ordering is important).  The type API looks like:
```python
merge.define_type('foo', label x: 'foo' in x)  # defines type 'foo' to be anything with 'foo' in it
merge.type([1,2,3])  # returns "list"
merge.type('foobar')  # returns "foo"
merge.type([1, 2, 'foo'])  # returns "foo"
merge.undefine_type('foo')  # undefines the 'foo' type.
merge.type('foobar')  # returns "default", because now 'foobar' doesn't fit any of the defined types
merge.list_types()  # lists the defined types (in order of precedence)
merge.reorder_types(<list of types>)  # reorders the list of type checkers
```

###default type
```BaseMerge``` defines a default type ("default") for anything which doesn't match any of the configured predicates

##merging
```pymerge``` then internally looks up the correct merge function for the two types it identified, and merges the arguments.  The merge rule API looks like:
```python
merge.set_rule('foo', 'bar', lambda a, b: "baz")  # if a "foo" type is merged with a "bar" type, the result is "baz"
merge.unset_rule('foo', 'bar')  # removes that rule
```

The set/unset rule functions also take a ```commutative``` argument, which defaults to ```True```.  This allows you to define different behaviors for different types:
```python
merge.set_rule('default', 'list', lambda a, b: [a] + b, commutative=False)
merge.set_rule('list', 'default', lambda a, b: raise Exception("I don't want to do this for you"), commutative=False)
merge.set_rule('list', 'default', lambda a, b: a + [b])  # ERROR - commutative defalts to true...
# now this will apply to both "[1, 2, 3], 4" (fine) and "1, [2, 3, 4]" (error)
```
###default merge
If there is no merge rule set for a pair of types, ```BaseMerge``` will use whatever is configured for the ('default', 'default') pair.  By default, this is defined as the tuple merge.

#what else

##pymerge.BasePedanticMerge
```BasePedanticMerge``` is the base upon which ```PedanticMerge``` is built.  It has no types defined and no rules defined, but has all the API to allow you to do so.  Rather than defining defaults, throws errors if the user has not explicitly defined a type or a merge rule.

##pymerge.PedanticMerge
```PedanticMerge``` is a modified ```BasePedanticMerge```.  It has all of the type and merge definitions as ```Merge```, with the exception of the dictionary merge.  Instead of merging values if both dictionaries have the same key, ```PedanticMerge``` checks if the values conflict.  If they do, an exception is thrown.  If they don't, one of the (equivalent) values is used:

```python
from pymerge import PedanticMerge
merge = PedanticMerge()

# Non-dictionary iterables of the same type are merged to that type
merge(tuple1, tuple2) # tuple1 + tuple2
merge(list1, list2)  # list1 + list2
merge(set1, set2)  # set1 | set2

# Dictionaries are a special case
d = merge(dict1, dict2)
# d now equals dict1, with any new key/value pairs from dict 2
# unless there are overlapping keys:
merge({'foo':'FOO'}, {'foo':'BAR'})  # raises pymerge.mergers.KeyConflictError
merge({'foo':'FOO'}, {'foo':'FOO'})  # returns {'foo':'FOO'}

# Non-iterables do not have merge types defined, and will raise a MissingTypeError
merge(1, 2)  # pymerge.MissingTypeError: No type predicate matched (1)
merge(“foo”, “bar”)  # pymerge.MissingTypeError: No type predicate matched (foo)

# Iterables of different types do not have merge rules defined, and will raise a MissingRuleError
merge({1, 2}, [3, 4])  # pymerge.MissingRuleError: No rule defined for types (set, list) for objects (set([1, 2]), [3, 4])

# Iterables and non-iterables will raise the MissingTypeError, because non-iterables have no types defined.
merge([1, 2, 3], 4)  # pymerge.MissingTypeError: No type predicate matched (4)
merge(1, {1: 2})  # pymerge.MissingTypeError: No type predicate matched (1)
```


#testing

testing is done via py.test, with the tests in [test_main.py](https://github.com/toejough/pymerge/blob/master/test_main.py).

#installation
```sh
pip install --upgrade git+http://github.com/toejough/pymerge
```

#design notes

##Merge

###iterables

Iterables, if of the same type, are merged to that type.  I think it's reasonable to assume that that's what you want.

Iterables of different types are merged to a tuple.  It's not generically possible to know what you want to merge them to.  Take a ```set``` and a ```list```, for example.  It's reasonable to want to merge to a ```set```, a ```list```, the first type (set, list -> set; list, set -> list), or the second type (set, list -> list; list, set -> set).  The best generic solution might be to provide a desired type argument, but at that point you might as well not introduce complication to the API and just wrap the result:
```python
merge([1, 2, 3], {3, 4, 5}, 'set')  # {1, 2, 3, 4, 5}
set(merge([1, 2, 3], {3, 4, 5}))  # {1, 2, 3, 4, 5}
```
The solution where you wrap the result is:
- the same number of keystrokes (counting shift)
- semantically clearer
- does not introduce new API

This also avoids the "unhashable type" error in the module entirely, so if you end up with an unhashable type in your tuple, you still have the merged tuple and can decide what you'd like to do with it.

###non-iterables and iterables

Non-iterables and iterables are merged to a tuple, because it's not generically possible to know what you want to merge them to.  This is primarily due to sets, which throw an error if you are adding an unhashable type.  For the ```Merge``` object, I want to avoid throwing errors at you where it's reasonable to do so.  For those that prefer errors, there is ```PedanticMerge```.

###non-iterables

Non-iterables are merged to a tuple, because it's the simplest collection, and it's pythonic (think ```return x, y```).

###why tuples?

All of the non-same-type-iterable merges merge to tuples.  This makes sense for the non-iterable merges, and is done for the iterable merges just to be consistent.  If you want something more 'correct' and strict, see [PedanticMerge](pymergepedanticmerge) and add your own types and rules.

##PedanticMerge

###iterables

Iterables, if of the same type, are merged to that type.  I think it's reasonable to assume that that's what you want.

Iterables of different types are not merged.  It's not clear what you want, so I've left it up to you to define that for this case.  If you don't define a merge function for the iterables you are merging, an error will be thrown.

###non-iterables and iterables

Non-iterables and iterables are not merged, becuase there are no non-iterable types defined.  Once you define a non-iterable type, you can also define rules for merging that type.

###non-iterables

Non-iterables are not merged, becuase there are no non-iterable types defined.  Once you define a non-iterable type, you can also define rules for merging that type.

###why all the errors?

Anything where it's not totally clear what "merging" means is left up to you to define, and throws an error if you don't.  This is the pedantic merge, and it's pedantic.  If you want something more generic and permissive, see [Merge](#pymergemerge).

