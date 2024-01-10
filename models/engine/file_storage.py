#!/usr/bin/python3
"""
FileStorage model that serializes instances to a
JSON file and deserializes JSON file to an instance
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Serializes and Deserializes a JSON file"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dict"""
        return FileStorage.__objects

    def new(self, obj):
        """sets the dict with the obj key"""
        obj_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_name, obj.id)] = obj

    def save(self):
        """serializes the object to json file"""
        obj_dict = FileStorage.__objects
        formatted_obj = {obj: obj_dict[obj].to_dict() for obj in obj_dict.keys()}
        
        with open(FileStorage.__file_path, "w") as file:
            json.dump(formatted_obj, file)

    def reload(self):
        """deserializes the json file to object"""
        try:
            with open(FileStorage.__file_path) as file:
                obj_dict = json.load(file)
                for i in obj_dict.values():
                    command_name = i["__class__"]
                    del i["__class__"]
                    self.new(eval(command_name)(**i))
        except FileNotFoundError as error:
            return
