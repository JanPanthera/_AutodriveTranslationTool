# AutoDriveTranslationTool

## Introduction
AutoDriveTranslationTool is a Python utility that facilitates the translation of AutoDrive course files. Utilizing customtkinter for UI elements and leveraging a GUI framework (available at [JanPanthera's _GuiFramework](https://github.com/JanPanthera/_GuiFramework)), the tool provides functionalities to manage translations efficiently.

## Features
- **Customtkinter GUI**: Incorporates customtkinter for a modern UI experience.
- **Language Management**: Allows addition and removal of languages for project translation.
- **Translation Dictionary System**: Integrates a system to create and manage translations.
- **Open Source**: The source code is available for use and contribution on GitHub.

## Requirements
To run AutoDriveTranslationTool, ensure the following are installed:
- **Python**: Python 3.3 or higher is required.
- **Dependencies**: Babel, customtkinter, and other dependencies are needed, which can be installed via pip.

## Installation
Execute the following steps to set up the tool:

1. **Clone the Repository**:
git clone --recurse-submodules https://github.com/JanPanthera/_AutodriveTranslationTool.git
cd AutoDriveTranslationTool

2. **Install Dependencies**:
pip install -r requirements.txt

3. **Set Up GUI Framework**:
If the _GuiFramework submodule has not been initialized, run:
git submodule update --init

## Usage
Follow these steps to operate the tool:

1. **Start the Tool**: Execute `main.py` to launch the application:
python main.py


2. **Configure Languages**: Manage your target languages in the Languages tab.

3. **Manage Dictionaries**: Use the Dictionaries tab to create and edit your Dictionaries.

4. **Translation Process**: Translate your course files using the Translation tab and find any missing translations with the provided functionality.

5. **Validation Button**: Confirms that the translated files adhere to AutoDrive's character limits.

## Contributing
Your contributions are encouraged. To contribute:

1. **Issues**: Report bugs or suggest enhancements via GitHub issues.

2. **Pull Requests**: Submit pull requests with your proposed changes.

3. **Feedback**: Any constructive feedback is welcomed to improve the tool.

## License
The project is under the MIT License. Refer to [LICENSE.md](LICENSE.md) for full details.

## Acknowledgments
- **Babel**: Used for internationalization of the GUI.
- **customtkinter**: For creating the modern styled GUI.
- **[JanPanthera's _GuiFramework](https://github.com/JanPanthera/_GuiFramework)**: The GUI framework is integral to the application's interface.
- **Contributors**: Thanks to those who have contributed to the project.
