# custom_type_handlers.py

import customtkinter as ctk


def string_var_creator(root, value):
    return ctk.StringVar(root, value=value)


def string_var_saver(string_var):
    return string_var.get()


def boolean_var_creator(root, value):
    return ctk.BooleanVar(root, value=value)


def boolean_var_saver(boolean_var):
    return boolean_var.get()


def list_saver(list_value):
    # Validate input is a list
    if not isinstance(list_value, list):
        raise ValueError("Input must be a list.")

    # Handle empty list
    if not list_value:
        return ""

    # Convert non-string elements to strings and join with commas
    return ','.join([str(item) for item in list_value])


def list_creator(list_string):
    # Validate input is a string
    if not isinstance(list_string, str):
        raise ValueError("Input must be a string.")

    # Split by commas and trim whitespace from each element
    return [item.strip() for item in list_string.split(',') if item.strip()]
