# main.py

import os

from GuiFramework.src.utilities.logger import CustomLogger, LOG_LEVEL
from AutoDriveTranslationTool.src.components.auto_drive_translation_tool import AutoDriveTranslationTool


def main():
    log_path = os.path.join("AutoDriveTranslationTool", "logs") if 'VSAPPIDDIR' in os.environ else "logs"
    logger_instance = CustomLogger(
        log_name="ADT-Tool.log",
        log_path=log_path,
        textbox=None,
        log_level=LOG_LEVEL.DEBUG,
        max_log_size=10 << 20,
        backup_count=5,
        rotate_on_start=True,
        append_datetime_to_rolled_files=True
    )

    try:
        ADT_Tool = AutoDriveTranslationTool(logger_instance)
        ADT_Tool.run()
    except Exception as e:
        logger_instance.log(LOG_LEVEL.ERROR, f"An error occurred: {str(e)}")
        raise e


if __name__ == "__main__":
    main()