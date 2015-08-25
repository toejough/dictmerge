'''Setup.py - things required for python packaging'''


# [ Imports ]
# [ -Python- ]
from setuptools import setup
# [ -Project- ]
import dictmerge


# [ Main ]
setup(
    name='dictmerge',
    version='0.4.3',
    packages=['dictmerge'],
    description=dictmerge.__doc__,
    author='toejough',
    url='https://github.com/toejough/dictmerge',
    license='MIT'
)


