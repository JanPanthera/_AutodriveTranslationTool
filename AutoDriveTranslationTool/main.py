# AutoDriveTranslationTool/main.py

# import cProfile
# import pstats

from GuiFramework.utilities.file_ops import FileOps
from GuiFramework.utilities.logging.logger import Logger, LoggerConfig, LOG_LEVEL

from AutoDriveTranslationTool.src.core.constants import APP_NAME, LOGGER_NAME, LOG_NAME
from AutoDriveTranslationTool.src.core.auto_drive_translation_tool import AutoDriveTranslationTool


def main() -> None:
    """Initialize logging and run the AutoDrive Translation Tool."""
    logger_config = LoggerConfig(
        logger_name=LOGGER_NAME,
        log_name=LOG_NAME,
        log_directory=FileOps.resolve_development_path(__file__, "logs", "main.py"),
        log_level=LOG_LEVEL.DEBUG,  # TODO: Change to INFO for production
        module_name=APP_NAME
    )
    logger = Logger(logger_config, rotate_on_init=True)

    ADT_Tool = AutoDriveTranslationTool()
    try:
        ADT_Tool.run()
    except Exception as e:
        logger.log_error(f"An error occurred: {str(e)}", "main")


if __name__ == "__main__":
    #with cProfile.Profile() as pr:
    main()

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.CUMULATIVE)

    # stats.print_stats()
    # stats.dump_stats(filename='profiling_stats.prof')
