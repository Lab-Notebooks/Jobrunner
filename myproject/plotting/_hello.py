"""Module with implemenation of hello"""

class Hello(object):

    def __init__(self):
        """
        A simple docstring for hello

        - It prints hello
        """
        print("Hello from model\n")

        self._module = 'Plotting'

    @property
    def modulename(self):
        return self._module 
