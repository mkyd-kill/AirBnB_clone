#!/usr/bin/python3
"""
BaseModel object that defines all common
attributes/methods of the project
"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Defines the base structure of all methods to other classes"""
    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # assigning value during initialisation
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, date_format)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """updates the public instance attributes"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dict containing all keys of a dict"""
        obj = self.__dict__.copy()
        obj['__class__'] = self.__class__.__name__
        obj['created_at'] = self.created_at.isoformat()
        obj['updated_at'] = self.updated_at.isoformat()
        return obj

    def __str__(self):
        """Returns str representation of the object"""
        clname = self.__class__.__name__
        print("[{}] ({}) {}".format(clname, self.id, self.__dict__))
