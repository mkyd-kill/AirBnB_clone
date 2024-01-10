#!/usr/bin/python3
"""
A User class model that inherits
from the BaseModel
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    A User Model
    Attributes:
        email: the email of the user
        password: user's password
        first_name: user's first name
        last_name: user's last name
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
