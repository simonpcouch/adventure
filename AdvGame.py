# File: AdvGame.py

"""
This module defines the AdvGame class, which maintains the information
necessary to play a game.
"""

from AdvRoom import AdvRoom
from AdvObject import AdvObject
from tokenscanner import TokenScanner
import os.path

class AdvGame:

    def __init__(self, prefix):
        """Reads the game data from files with the specified prefix."""
        with open(prefix + "Rooms.txt") as room_file:
            self.rooms = { }
            while True:
                room = AdvRoom.readRoom(room_file)
                if room is None: break
                if len(self.rooms) == 0:
                    self.rooms["START"] = room
                name = room.getName()
                self.rooms[name] = room

        self.objects = None
        # Read in the objects
        if os.path.isfile(prefix + "Objects.txt"):
            with open(prefix + "Objects.txt") as obj_file:
                self.objects = { }
                while True:
                    object = AdvObject.readObject(obj_file)
                    if object is None: break
                    name = object.getName()
                    self.objects[name] = object
            self.player_objects = set()

        self.synonyms = None
        # Read in the synonyms dictionary
        if os.path.isfile(prefix + "Synonyms.txt"):
            with open(prefix + "Synonyms.txt") as f:
                self.synonyms = {}
                while True:
                    line = f.readline().rstrip()
                    if line == "":
                        break
                    eq_index = line.find("=")
                    key = line[:eq_index]
                    value = line[eq_index + 1:]
                    self.synonyms[key] = value

    def getRoom(self, name):
        """Returns the AdvRoom object with the specified name."""
        return self.rooms[name]

    def getNextRoom(self, room, cmd):
        """Returns the next AdvRoom object after the cmd has
        been applied."""
        understood = False
        passages = room.getPassages()
        for i in range(len(passages)):
            response, next, key = passages[i]
            if response == cmd:
                understood = True
                if key is None:
                    return next
                else:
                    for object in self.player_objects:
                        if key == object.getName():
                            return next
        if not understood:
            return None

    def run(self):
        """Plays the adventure game stored in this object."""
        current = "START"

        # Distribute the objects throughout the rooms.
        if self.objects is not None:
            for key, value in self.objects.items():
                if value.getInitialLocation() != "PLAYER":
                    room = self.rooms[value.getInitialLocation()]
                    room.addObject(value)
                elif value.getInitialLocation() == "PLAYER":
                    self.player_objects.add(value)

        # The after_help variable keeps track of which type of command
        # was just given, so that redundant information isn't printed.
        after_help = False

        while True:
            # Check what room the player is in, and print the appropriate description.
            room = self.getRoom(current)

            # If the short description is "-", then we are in a forced room
            # and can skip the rest of the loop, let the player know that 
            # they don't have the key, and move to the forced room
            if room.getShortDescription() == "-":
                for line in room.getLongDescription():
                    print(line)
                forced = self.getNextRoom(room, "FORCED")
                current = forced
            else:
                if room.hasBeenVisited() and not after_help:
                    print(room.getShortDescription())
                elif not after_help:
                    for line in room.getLongDescription():
                        print(line)
                    room.setVisited(True)
                if not after_help:
                    for key, value in room.getContents().items():
                            print("There is " + value.getDescription() + " here." )
                # The rest of the while loop serves to process the given command.
                # Read in the command
                cmd = input("> ").strip().upper()
                # Replace any synonyms with the full command
                if self.synonyms is not None:
                    for key, value in self.synonyms.items():
                        if cmd == key:
                            cmd = value
                # If the command is "LOOK", print the long description and items in the room."
                if cmd.find("LOOK") != -1:
                    for line in room.getLongDescription():
                        print(line)
                    for name, object in room.getContents().items():
                        print("There is " + object.getDescription() + " here.")
                    after_help = True
                # Print the help text is the command is "HELP".
                elif cmd.find("HELP") != -1:
                    for line in HELP_TEXT:
                        print(line)
                    after_help = True
                # Tell the player what they are carrying if they say "INVENTORY".
                elif cmd.find("INVENTORY") != -1:
                    print("You are carrying:")
                    for object in self.player_objects:
                        print("  " + object.getDescription())
                    after_help = True
                # If the player says "TAKE", try to find that object in the room.
                # If it's in the room, remove it from the room and add it to the
                # inventory. Otherwise, notify the player.
                elif cmd.find("TAKE") != -1:
                    objects = room.getContents()
                    scanner = TokenScanner(cmd)
                    found_object = False
                    while scanner.hasMoreTokens():
                        # The token is a word in the command.
                        token = scanner.nextToken()
                        for name, object in objects.items():
                            # If the token is an object in the room
                            if name == token:
                                # Note that we found an object
                                found_object = True
                                # Remove that object from the room
                                room.removeObject(name)
                                # Add the object to the inventory
                                self.player_objects.add(object)
                                # Let the player know it was successful.
                                print("A " + object.getDescription()[2:] + " was added to your inventory.")
                                break
                    # If the object isn't in the room, let the player know
                    if not found_object:
                        print("That object doesn't seem to be in this room.")
                    after_help = True
                # If the command is "DROP" and the object is in the player's
                # inventory, remove it from the player's inventory and add it to
                # the room. Otherwise, notify the player that they don't have that object.
                elif cmd.find("DROP") != -1:
                    scanner = TokenScanner(cmd)
                    found_object = False
                    # For each object in the command, if that object is
                    # in the inventory, take it from the inventory,
                    # leave it in the room, and notify the player.
                    while scanner.hasMoreTokens():
                        token = scanner.nextToken()
                        for object in self.player_objects:
                            if object.getName() == token:
                                self.player_objects.remove(object)
                                room.addObject(object)
                                print("You dropped " + object.getDescription() + ".")
                                found_object = True
                                break
                    if not found_object:
                        print("That object doesn't seem to be in your inventory.")
                # If the command is "EXIT", quit the game.
                elif cmd.find("QUIT") != -1: break
                # Otherwise, the command must refer to the next room
                # that the player wants to go to.
                else:
                    next = self.getNextRoom(room, cmd)
                    after_help = False
                    if next is None:
                        print("I don't understand that response.")
                        after_help = True
                    else:
                        current = next


# Constants

HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are and see which objects,",
    "are in the room, say LOOK. If you want to end your adventure, say QUIT."
]
