#!/usr/bin/python3
"""
Implementing a command interpreter in Python
using the cmd module
"""
import sys
import cmd
from re import search
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from shlex import split


def parse(arg):
        """Parses an input argument"""
        curlys = search(r"\{(.*?)\}", arg)
        brackets = search(r"\[(.*?)\]", arg)

        if curlys is None:
            if brackets is None:
                return [x.strip(",") for x in split(arg)]
            else:
                n = split(arg[:brackets.span()[0]])
                ret = [y.strip(",") for y in n]
                ret.append(brackets.group())
                return ret
        else:
            n = split(arg[:curlys.span()[0]])
            ret = [z.strip(",") for z in n]
            ret.append(curlys.group())
            return ret
        
class HBNBCommand(cmd.Cmd):
    """Defines the structure of the command interpreter
    from which commands to run, and the layout of the command UI"""

    intro = "Welcome to Python Command Interpreter\n"
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
        dictarg = {
                "show": self.do_show,
                "all": self.do_all,
                "destroy": self.do_destroy,
                "update": self.do_update,
                "count": self.do_count
        }
        textmatch = search(r"\.", arg)
        if textmatch is not None:
            arg1 = [arg[:textmatch.span()[0]], arg[textmatch.span()[1]]]
            textmatch = search(r"\((.*?)\)", arg1[1])
            if textmatch is not None:
                command = [arg1[1][:textmatch.span()[0]], textmatch.group()[1:-1]]
                if command[0] in dictarg.keys():
                    call = "{} {}".format(arg1[0], arg1[1])
                    return dictarg[command[0]](call)
        print("*** Unkown syntax: {}".format(arg))
        return False
    
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
        """Creates a new instance of BaseModel and saves it
        Usage: create <class>
        """
        obj = parse(arg)
        
        if len(obj) == 0:
            print("** class name missing **")
        elif obj[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(obj[0])().id)
            storage.save()

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
