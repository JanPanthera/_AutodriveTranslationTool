# custom_type_handlers.py

import customtkinter as ctk

from GuiFramework.utilities.config.custom_type_handler_base import CustomTypeHandlerBase


class CtkStringVarTypeHandler(CustomTypeHandlerBase):

    def __init__(self, root):
        self.root = root

    def serialize(self, string_var) -> str:
        """Convert StringVar to string."""
        self.validate_type(string_var, ctk.StringVar, "StringVar")
        return string_var.get()

    def deserialize(self, value: str) -> ctk.StringVar:
        """Convert string to StringVar."""
        self.validate_type(value, str, "string")
        return ctk.StringVar(self.root, value=value)

    def get_type(self) -> type:
        """Return the Python type this handler is responsible for."""
        return ctk.StringVar


class CtkBooleanVarTypeHandler(CustomTypeHandlerBase):

    def __init__(self, root):
        self.root = root

    def serialize(self, boolean_var) -> str:
        """Convert BooleanVar to string."""
        self.validate_type(boolean_var, ctk.BooleanVar, "BooleanVar")
        return str(boolean_var.get())

    def deserialize(self, value: str) -> ctk.BooleanVar:
        """Convert string to BooleanVar."""
        self.validate_type(value, str, "string")
        return ctk.BooleanVar(self.root, value=value.lower() in ('true', '1', 't'))

    def get_type(self) -> type:
        """Return the Python type this handler is responsible for."""
        return ctk.BooleanVar


class ListTypeHandler(CustomTypeHandlerBase):
    def serialize(self, list_value: list) -> str:
        """Convert list to comma-separated string."""
        self.validate_type(list_value, list, "list")
        return ','.join([str(item) for item in list_value]) if list_value else ""

    def deserialize(self, list_string: str) -> list:
        """Convert comma-separated string to list."""
        self.validate_type(list_string, str, "string")
        return [item.strip() for item in list_string.split(',') if item.strip()]

    def get_type(self) -> type:
        """Return the Python type this handler is responsible for."""
        return list


class TupleTypeHandler(CustomTypeHandlerBase):
    def serialize(self, tuple_value: tuple) -> str:
        """Convert tuple to comma-separated string."""
        self.validate_type(tuple_value, tuple, "tuple")
        return ",".join(map(str, tuple_value)) if tuple_value else ""

    def deserialize(self, tuple_string: str) -> tuple:
        """Convert comma-separated string to tuple."""
        self.validate_type(tuple_string, str, "string")
        return tuple((int(item) if item.isdigit() else item) for item in map(str.strip, tuple_string.split(","))) if tuple_string else ()

    def get_type(self) -> type:
        """Return the Python type this handler is responsible for."""
        return tuple