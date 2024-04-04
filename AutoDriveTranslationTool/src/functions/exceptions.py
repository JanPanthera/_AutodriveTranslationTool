# AutoDriveTranslationTool/src/functions/exceptions.py


class InvalidFileNameError(Exception):
    """Exception raised for invalid file names."""

    def __init__(self, invalid_chars):
        self.invalid_chars = invalid_chars
        super().__init__(f"Invalid characters in file name: {invalid_chars}")
