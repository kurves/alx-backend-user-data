#!/usr/bin/env python3

"""
storage module
"""

import json
from os import path
from typing import TypeVar, List, Iterable

class Storage:
    """File-based storage model for persisting Base model objects."""

    __file_path = ".db_storage.json"
    __objects = {}

    def __init__(self):
        """Initialize the storage and load data from file if it exists."""
        self.reload()

    def all(self, cls=None) -> Iterable[TypeVar('Base')]:
        """Returns a dictionary of all objects, or objects of a given class."""
        if cls:
            cls_name = cls.__name__
            return {key: obj for key, obj in self.__objects.items() if key.startswith(cls_name)}
        return self.__objects

    def get(self, cls, id: str) -> TypeVar('Base'):
        """Retrieve one object by class name and ID."""
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key, None)

    def new(self, obj: TypeVar('Base')):
        """Add a new object to the storage."""
        key = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes objects to the JSON file."""
        with open(self.__file_path, 'w') as file:
            json.dump({key: obj.to_json(True) for key, obj in self.__objects.items()}, file)

    def reload(self):
        """Deserializes JSON file to objects."""
        if path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, obj_data in data.items():
                    cls_name = key.split('.')[0]
                    cls = globals().get(cls_name)  # Get the class from globals
                    if cls:
                        self.__objects[key] = cls(**obj_data)

    def delete(self, obj=None):
        """Delete an object from the storage."""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def count(self, cls=None) -> int:
        """Count the number of objects in storage or by class."""
        if cls:
            return len(self.all(cls))
        return len(self.__objects)

    def search(self, cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search for objects with matching attributes."""
        return [obj for obj in self.all(cls).values() if all(getattr(obj, k, None) == v for k, v in attributes.items())]

