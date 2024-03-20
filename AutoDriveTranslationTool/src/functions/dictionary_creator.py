# AutoDriveTranslationTool/src/functions/create_dictionary.py

from GuiFramework.utilities import FileOps
from AutoDriveTranslationTool.src.functions.exceptions import InvalidFileNameError


VALID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")


class DictionaryCreator:
    DIC_TEMPLATE = """
###*
   
   Author: name
   Date: 08.03.2024
   Version: 0.0.1
   Description: dictionary for xyz

*###

original1,translation1
original2,translation2
original3,translation3
original4,translation4

original5,translation5
original6,translation6
original7,translation7
original8,translation8
"""

    @classmethod
    def create(cls, dictionaries_path, selected_language, file_name):
        file_name = cls._validate_file_name(file_name)
        file_path = FileOps.join_paths(selected_language, file_name)
        cls(dictionaries_path, file_path)

    @staticmethod
    def _validate_file_name(file_name):
        invalid_chars = FileOps.get_invalid_file_name_chars(file_name, VALID_CHARS)
        if invalid_chars:
            raise InvalidFileNameError(invalid_chars)
        if FileOps.get_file_extension(file_name) != ".dic":
            file_name += ".dic"
        return file_name

    def __init__(self, dictionaries_path, new_dictionary):
        """Create a dictionary from the input."""
        template_file = FileOps.join_paths(dictionaries_path, "template_dictionary.dic")
        if not FileOps.file_exists(template_file):
            FileOps.write_file(template_file, self.DIC_TEMPLATE)
        dictionary_file = FileOps.join_paths(dictionaries_path, new_dictionary)
        FileOps.copy_file(template_file, dictionary_file)
