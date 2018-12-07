# File: TeachingMachine.py

from TMCourse import TMCourse

def TeachingMachine():
    course = readCourseFile()
    course.run()

def readCourseFile():
    """
    Prompts the user for a course name and then reads in the
    data for that course from the associated data file.  If 
    TMCourse.readCourse raises an IOError exception, the user
    is asked to supply a new course name.
    """
    while True:
        try:
            filename = input("Enter course name: ")
            with open(filename + ".txt") as f:
                return TMCourse.readCourse(f)
        except IOError:
            print("Please enter a valid course name.")

# Startup code

if __name__ == "__main__":
    TeachingMachine()
