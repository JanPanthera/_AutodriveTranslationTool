import os
import zipfile
import subprocess


def create_executable(main_script_path, exe_name, dist_path, work_path, no_console=False):
    pyinstaller_command = [
        'pyinstaller',
        '--onefile',
        f'--distpath={dist_path}',
        f'--workpath={work_path}',
        f'--name={exe_name}',
        '--hidden-import=babel.numbers',
        '--hidden-import=customtkinter',
        main_script_path
    ]
    if no_console:
        pyinstaller_command.append('--noconsole')
    subprocess.run(pyinstaller_command, check=True)


def create_zip_archive(zip_name, target_dir, base_path, files_to_include):
    zip_path = os.path.join(target_dir, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            if os.path.isdir(file):
                for root, dirs, files in os.walk(file):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=base_path)
                        zipf.write(file_path, arcname=arcname)
            else:
                arcname = os.path.basename(file)
                zipf.write(file, arcname=arcname)


def main():
    dev_path = "AutoDriveTranslationTool" if 'VSAPPIDDIR' in os.environ else ""
    main_script = os.path.join(dev_path, 'main.py')
    exe_name = 'AutoDriveTranslationTool'
    dist_directory = os.path.join(dev_path, 'dist')
    work_directory = os.path.join(dev_path, 'dist', 'build')

    create_executable(main_script, exe_name, dist_directory, work_directory, no_console=True)

    additional_files = [
        os.path.join(dev_path, '_dictionaries'),
        os.path.join(dev_path, '_input'),
        os.path.join(dev_path, '_output'),
        os.path.join(dev_path, 'config'),
        os.path.join(dev_path, 'locales'),
        os.path.join(dev_path, 'resources'),
        os.path.join(dist_directory, f'{exe_name}.exe')
    ]

    create_zip_archive(f'{exe_name}.zip', dist_directory, dev_path, additional_files)


if __name__ == "__main__":
    main()
