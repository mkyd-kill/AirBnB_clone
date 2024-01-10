#!/usr/bin/python3
"""
Implementing a command interpreter in Python
using the cmd module
"""
import sys
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from shlex import split


class HBNBCommand(cmd.Cmd):
    """Defines the structure of the command interpreter
    from which commands to run, and the layout of the command UI"""
    prompt = "(hbnb) "

    # registering the model classes to be used
    __classes = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"
    }

    def default(self, arg):
        """Displaying the default behavior for the command"""
        pass
    
    def emptyline(self):
        """Does nothing when receiving an empty line"""
        pass

    def do_EOF(self, arg):
        """EOF command to exit the program\n"""
        print("")
        return True

    def do_quit(self, arg):
        """Quit command to exit the program\n"""
        return True

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it to a json file
        and prints the id\n"""
        pass

    def do_show(self, arg):
        """Prints the string representation of an instance based on the
        class name and id\n"""
        pass

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        and saves the changes into a json file\n"""
        pass

    def do_all(self, arg):
        """Prints all string representation of all instances based 
        or not on the class name\n"""
        pass

    def do_update(self, arg):
        """Updates an instance based on the class name and id
        by adding or updating attributes and saves the changes
        to a json file\n"""
        pass

if __name__ == "__main__":
    # processing file arguments if any
    if len(sys.argv) > 1:
        HBNBCommand().onecmd(" ".join(sys.argv[1:]))
    else:
        HBNBCommand().cmdloop()
