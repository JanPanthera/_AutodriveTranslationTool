import os

from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs

from GuiFramework.utilities.executable_creator import ExecutableCreator
from GuiFramework.utilities.project_archiver import CopyType, ProjectArchiver


base_path = Path("AutoDriveTranslationTool" if 'VSAPPIDDIR' in os.environ else "")


def create_exe():
    binary_dependencies = collect_dynamic_libs("glfw")

    exe_creator = ExecutableCreator(
        main_script_path=base_path / "main.py",
        exe_name="AutoDriveTranslationTool",
        dist_path=base_path / "dist",
        work_path=base_path / "dist" / "build",
        no_console=True
    )

    hidden_imports = ["GuiFramework", "babel.numbers", "customtkinter", "setuptools", "watchdog", "flake8", "black", "glfw", "PyOpenGL", "Babel"]
    for import_name in hidden_imports:
        exe_creator.add_hidden_import(import_name)

    exe_creator.set_icon(base_path / "resources" / "ad_icon.ico")

    # Include the collected binary dependencies
    for binary_path, binary in binary_dependencies:
        exe_creator.add_data_file(binary_path, binary)  # Adjust the destination if needed

    exe_creator.create_executable()


def create_zip():
    files_folders = {
        base_path / "_dictionaries": CopyType.ROOT_FOLDER,
        base_path / "_input": CopyType.ROOT_FOLDER,
        base_path / "_output": CopyType.ROOT_FOLDER,
        base_path / "config": CopyType.ROOT_FOLDER,
        base_path / "locales": CopyType.ALL,
        base_path / "resources": CopyType.ALL,
        base_path / "dist/AutoDriveTranslationTool.exe": CopyType.FILE
    }
    zip_name = "AutoDriveTranslationTool"
    output_dir = base_path / 'dist'
    temp_folder = output_dir / 'temp'
    archiver = ProjectArchiver(files_folders, zip_name, temp_folder, output_dir)
    archiver.move_files_to_temp_folder()
    archiver.create_zip_archive()


if __name__ == "__main__":
    try:
        print("Creating executable...")
        create_exe()
        print("Executable created successfully!")
        print("Creating zip archive...")
        create_zip()
        print("Zip archive created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press Enter to quit...")
