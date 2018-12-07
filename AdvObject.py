# File: AdvObject.js

"""
This module defines a class that models an object in Adventure.
"""

class AdvObject:

    def __init__(self, name, description, location):
        """Creates an AdvObject from the specified properties."""
        self.name = name
        self.description = description
        self.location = location

    def __str__(self):
        """Converts an AdvObject to a string."""
        return str(self.name) + " : " + str(self.location)

    def getName(self):
        """Returns the name of this object."""
        return self.name

    def getDescription(self):
        """Returns the description of this object."""
        return self.description

    def getInitialLocation(self):
        """Returns the initial location of this object."""
        return self.location

    @staticmethod
    def readObject(f):
        """Reads and returns the next object from the file."""
        name = f.readline().rstrip()
        if name == "":
            return None
        description = f.readline().rstrip()
        location = f.readline().rstrip()
        space = f.readline().rstrip()
        return AdvObject(name, description, location)




