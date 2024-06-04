import os

from GuiFramework.utilities.localization.localizer import Localizer, LocalizerSetup, LocalizationFile
from GuiFramework.utilities.localization.localization_key_generator import LocalizationKeyGenerator

from AutoDriveTranslationTool.loc_keys import LocKeys


def main():
    Localizer.initialize(
        LocalizerSetup(
            active_locale='en',
            localization_files=[
                LocalizationFile('en', 'AutoDriveTranslationTool\\en.json', ["english", "English"]),
                #LocalizationFile('de', 'AutoDriveTranslationTool\\de.json', ["german", "German"]),
                LocalizationFile('de', 'AutoDriveTranslationTool\\de.json'),
            ]
        )
    )

    base_path = os.path.dirname(__file__)
    LocalizationKeyGenerator.generate_keys(os.path.join(base_path, 'en.json'), base_path, 'LocKeys', 'loc_keys.py')

    color_keys = LocKeys.Generic.Colors
    tooltip_keys = LocKeys.TranslationFrame.Tooltips

    test = Localizer.get_available_locales()

    print(color_keys.RED.key)
    print(color_keys.RED.get_localized_string())
    Localizer.set_active_locale('de')
    print(color_keys.RED.get_localized_string())
    print(tooltip_keys.TOOLTIP_2.get_localized_string("arg1"))


if __name__ == "__main__":
    main()
    input("Press Enter to continue...")
