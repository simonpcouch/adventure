# File: AdvRoom.py

"""
This module is responsible for modeling a single room in Adventure.
"""

# Constants

MARKER = "-----"

class AdvRoom:

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""
        self.name = name
        self.shortdesc = shortdesc
        self.longdesc = longdesc
        self.passages = passages
        self.visited = False
        self.objects = {}

    def getName(self):
        """Returns the name of this room.."""
        return self.name

    def getShortDescription(self):
        """Returns a one-line short description of this room.."""
        return self.shortdesc

    def getLongDescription(self):
        """Returns the list of lines describing this room."""
        return self.longdesc

    def getPassages(self):
        """Returns the passages for the room."""
        return self.passages

    def setVisited(self, boolean):
        self.visited = boolean

    def hasBeenVisited(self):
        return(self.visited)

    def addObject(self, object):
        self.objects[object.getName()] = object

    def removeObject(self, name):
        self.objects.pop(name, None)

    def containsObject(self, name):
        return self.objects[name] is not None

    def getContents(self):
        return self.objects

    @staticmethod
    def readRoom(f):
        """Reads a room from the data file."""
        name = f.readline().rstrip()
        if name == "":
            return None
        shortdesc = f.readline().rstrip()
        longdesc = [ ]
        while True:
            line = f.readline().rstrip()
            if line == MARKER: break
            longdesc.append(line)
        passages = []
        while True:
            line = f.readline().rstrip()
            if line == "": break
            slash = line.find("/")
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            if slash == -1:
                response = line[:colon].strip().upper()
                next = line[colon + 1:].strip()
                passage = (response, next, None)
                passages.append(passage)
            else:
                response = line[:colon].strip().upper()
                next = line[colon + 1:slash].strip()
                key = line[slash + 1:].strip()
                passage = (response, next, key)
                passages.append(passage)

        return AdvRoom(name, shortdesc, longdesc, passages)



