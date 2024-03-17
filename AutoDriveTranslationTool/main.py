# AutoDriveTranslationTool/main.py

from GuiFramework.utilities.file_ops import FileOps
from GuiFramework.utilities.logging.logger import Logger, LoggerConfig, LOG_LEVEL

from src.components.auto_drive_translation_tool import AutoDriveTranslationTool


def main() -> None:
    """
    Initialize logging and run the AutoDrive Translation Tool.
    """
    log_dir = FileOps.resolve_development_path(__file__, "logs", "main.py")
    logger_config = LoggerConfig(
        logger_name="ADT_Tool",
        log_name="adt-tool",
        log_directory=log_dir,
        log_level=LOG_LEVEL.DEBUG,
        module_name="ADT_Tool"
    )
    logger = Logger(logger_config, rotate_on_init=True)

    try:
        ADT_Tool = AutoDriveTranslationTool()
        ADT_Tool.run()
    except Exception as e:
        logger.log_error(f"An error occurred: {str(e)}", "main")


if __name__ == "__main__":
    main()