#!/usr/bin/python3
"""
User State model
"""
from models.base_model import BaseModel


class State(BaseModel):
    """
    State model
    Attributes:
        name: state name
    """
    name = ""
