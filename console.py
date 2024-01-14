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
        """Prints the string representation of an instance of a given id
        Usage: show <class> <id> or <class>.show(<id>)
        """
        argv = parse(arg)
        obj = storage.all()

        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argv[0], argv[1]) not in obj:
            print("** no instance found **")
        else:
            print(obj["{}.{}".format(argv[0], argv[1])])

    def do_destroy(self, arg):
        """Deletes a class instance of a given id
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        """
        argv = parse(arg)
        obj = storage.all()

        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argv[0], argv[1]) not in obj.keys():
            print("** no instance found **")
        else:
            del obj["{}.{}".format(argv[0], argv[1])]
            storage.save()

    def do_all(self, arg):
        """Displays all instances by string representation of a given class
        Usage: all or all <class> or <class>.all()
        """
        argv = parse(arg)

        if len(argv) > 0 and argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj = list()
            for i in storage.all().values():
                if len(argv) > 0 and argv[0] == i.__class__.__name__:
                    obj.append(i.__str__())
                elif len(argv) == 0:
                    obj.append(i.__str__())

    def do_update(self, arg):
        """Updates an instance based on the class name and id
        Usage: update <class> <id> <attr_name> <attr_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
       """
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """Retrieves the number of instances of a class
        Usage: <class>.count()
        """
        argv = parse(arg)
        i = 0

        for obj in storage.all().values():
            if argv[0] == obj.__class__.__name__:
                i += 1
        print(i)

if __name__ == "__main__":
    # processing file arguments if any
    if len(sys.argv) > 1:
        HBNBCommand().onecmd(" ".join(sys.argv[1:]))
    else:
        HBNBCommand().cmdloop()
