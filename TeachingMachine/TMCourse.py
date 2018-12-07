# File: TMCourse.py

"""
This class defines the data structure for a course for use with
the TeachingMachine application.
"""

from TMQuestion import TMQuestion

class TMCourse:

    def __init__(self, questions):
        """Creates a new TMCourse object with the specified questions."""
        self._questions = questions

    def getQuestion(self, name):
        """Returns the question with the specified name."""
        return self._questions[name]

    def run(self):
        """Steps through the questions in this course."""
        current = "START"
        while current != "EXIT":
            question = self.getQuestion(current)
            for line in question.getText():
                print(line)
            answer = input("> ").strip().upper()
            next = question.lookupAnswer(answer)
            if next is None:
                print("I don't understand that response.")
            else:
                current = next

# Implementation notes
# --------------------
# To make sure that the course starts at the first question, this method
# always includes an entry labeled "START" in the question table.

    @staticmethod
    def readCourse(f):
        """Reads the entire course from the data file f."""
        questions = { }
        while True:
            question = TMQuestion.readQuestion(f)
            if question is None: break
            if len(questions) == 0:
                questions["START"] = question
            name = question.getName()
            questions[name] = question
        return TMCourse(questions)
