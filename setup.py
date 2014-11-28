'''Setup.py - things required for python packaging'''


# [ Imports ]
# [ -Python- ]
from setuptools import setup
# [ -Project- ]
import pymerge


# [ Main ]
setup(
    name='pymerge',
    version='0.3.0',
    packages=['pymerge'],
    description=pymerge.__doc__,
    author='toejough',
    url='https://github.com/toejough/pymerge',
    license='MIT'
)


