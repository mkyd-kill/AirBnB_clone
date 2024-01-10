#!/usr/bin/python3
"""
Place model
"""
from models.base_model import BaseModel


class City(BaseModel):
    """ Attribute:
        state_id: state id
        name: city name
    """
    state_id = ""
    name = ""
