# main.py

from src.utilities.logger import CustomLogger
from src.components.AutoDriveTranslationTool import AutoDriveTranslationTool
from src.utilities.utils import trigger_debug_break
from src.utilities import logger


def main():
    logger_instance = CustomLogger(name="AutoDriveTranslationTool", textbox=None, log_level=logger.logging.DEBUG,
                                   log_file="AutoDriveTranslationTool.log", max_log_size=10 << 20,
                                   backup_count=5, rotate_on_start=True, append_datetime_to_rolled_files=True)
    ADT_Tool = AutoDriveTranslationTool(logger_instance)
    try:
        ADT_Tool.run()
    except Exception as e:
        logger_instance.log(logger.logging.ERROR,
                            f"An error occurred: {str(e)}")
        trigger_debug_break()
        raise


if __name__ == "__main__":
    main()