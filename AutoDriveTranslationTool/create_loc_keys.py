# AutoDriveTranslationTool/create_loc_keys.py

from GuiFramework.utilities.file_ops import FileOps
from GuiFramework.utilities.localization.localization_key_generator import LocalizationKeyGenerator


def main():
    root_path = FileOps.resolve_development_path(__file__, "", "AutoDriveTranslationTool")
    output_dir = FileOps.join_paths(root_path, "src", "core")
    input_file = FileOps.join_paths(root_path, "locales", "en_US.json")
    LocalizationKeyGenerator.generate_keys(input_file, output_dir, 'LocKeys', 'loc_keys.py')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to continue...")
