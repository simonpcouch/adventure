# File: TMQuestion.py

"""
This module defines a class to represent a single question.
"""

# Constants 

MARKER = "-----"

class TMQuestion:

    def __init__(self, name, text, answers):
        """Creates a new TMQuestion object with these attributes."""
        self._name = name
        self._text = text
        self._answers = answers

    def getName(self):
        """Returns the name of this question."""
        return self._name

    def getText(self):
        """Returns the list containing the text of this question."""
        return self._text

    def lookupAnswer(self, response):
        """Looks up the response to find the next question."""
        next = self._answers.get(response, None)
        if next is None:
            next = self._answers.get("*", None)
        return next

    @staticmethod
    def readQuestion(f):
        """Reads one question from the data file f."""
        name = f.readline().rstrip()
        if name == "":
            return None
        text = [ ]
        while True:
            line = f.readline().rstrip()
            if line == MARKER: break
            text.append(line)
        answers = { }
        while True:
            line = f.readline().rstrip()
            if line == "": break
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            response = line[:colon].strip().upper()
            next = line[colon + 1:].strip()
            answers[response] = next
        return TMQuestion(name, text, answers)
