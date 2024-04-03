# AutoDriveTranslationTool/src/functions/create_dictionary.py

from GuiFramework.utilities import FileOps
from AutoDriveTranslationTool.src.functions.exceptions import InvalidFileNameError


VALID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.")


class DictionaryCreator:
    DIC_TEMPLATE = """###*

    Date: 08.03.2024
    Author: name
    Version: 0.0.1
    Description: dictionary for xyz

    AD Namen Max character 30
    AD Group Max character 20

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

    @staticmethod
    def create_dic_from_file(input_file_path, output_file_path):
        file_name = FileOps.get_file_name(input_file_path)
        file_name = DictionaryCreator._validate_file_name(file_name)
        file_path = FileOps.join_paths(output_file_path, file_name)
        FileOps.copy_file(input_file_path, file_path)

    @staticmethod
    def create_dic_from_text(input_text, output_path, file_name):
        file_name = DictionaryCreator._validate_file_name(file_name)
        file_path = FileOps.join_paths(output_path, file_name)
        FileOps.write_file(file_path, input_text)

    @staticmethod
    def create_default_dic(output_path, file_name):
        file_name = DictionaryCreator._validate_file_name(file_name)
        file_path = FileOps.join_paths(output_path, file_name)
        FileOps.write_file(file_path, DictionaryCreator.DIC_TEMPLATE)

    @staticmethod
    def _validate_file_name(file_name):
        invalid_chars = FileOps.validate_file_name(file_name)
        if invalid_chars and not invalid_chars == file_name:
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
