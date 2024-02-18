# AutoDriveTranslationTool

## Introduction
Welcome to AutoDriveTranslationTool, a Python-based utility designed to streamline the translation process for AutoDrive courses. With customtkinter for an enhanced user interface, and a GUI framework (available at [JanPanthera's _GuiFramework](https://github.com/JanPanthera/_GuiFramework)), this tool offers an intuitive and efficient way to translate your AutoDrive Course files into multiple languages.

## Features
- **Intuitive GUI**: Built with customtkinter and a proprietary GUI framework for ease of use and accessibility.
- **Multi-Language Support**: Add or remove languages to translate your project into multiple languages.
- **Efficient Translation Management**: With the integrated Dictionary system, create and edit translations for your Course files.
- **Open Source**: Access the source code, contribute, and customize the tool to fit your unique requirements.

## Requirements
If you want to use the AutoDriveTranslationTool via python, you will need the following:
- **Python**: Ensure you have Python installed on your system. This tool is developed and tested with Python 3.12
- **Dependencies**: Requires Babel, customtkinter, and other dependencies which can be installed via pip. A detailed list will be provided in the Installation section.

## Installation
To get AutoDriveTranslationTool up and running on your system, follow these steps:

1. **Clone the Repository**: First, clone this repository to your local machine using Git:
git clone https://github.com/JanPanthera/_AutodriveTranslationTool.git
cd AutoDriveTranslationTool

2. **Install Dependencies**: Install all required dependencies by running:
pip install -r requirements.txt

This command will install Babel, customtkinter, and any other necessary Python packages.

3. **Set Up GUI Framework**: Ensure you have the custom GUI framework set up by following the instructions provided at [JanPanthera's _GuiFramework](https://github.com/JanPanthera/_GuiFramework). TODO: decide how to handle this.

## Usage
To use the AutoDriveTranslationTool, follow these steps:

1. **Launch the Tool**: Run `main.py` inside the AutoDriveTranslationTool directory to start the application:
python main.py


2. **Configure Settings**: Add or remove your target languages inside the Languages tab. Then, int the Dictionaries tab, create and edit dictionaries for each language to manage your translations.

3. **Translate**: With your dictionaries set up, you can now start translating your AutoDrive Course files. Use the Translation tab to start translating your Courses. Additionally, you can hit the Find Missing Translations button to check for any missing translations in your dictionaries.

4. **Validate**: You can validate the translated files for AutoDrive's maximum character limits.

## Contributing
Contributions to the AutoDriveTranslationTool are welcome! Whether it's bug reports, feature requests, or code contributions, here's how you can help:

1. **Report Issues**: If you encounter any bugs or have suggestions, please file an issue on the GitHub repository.

2. **Submit Pull Requests**: Feel free to fork the repository and submit pull requests with your improvements or new features.

3. **Feedback and Suggestions**: Any feedback or suggestions for improving the tool are greatly appreciated.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- **Babel**: For providing the comprehensive internationalization and localization support that powers the the Gui's multi-language capabilities.
- **customtkinter**: For an awesome modern style gui library.
- **[JanPanthera's _GuiFramework](https://github.com/JanPanthera/_GuiFramework)**: A special thanks to JanPanthera for the bespoke GUI framework that forms the backbone of this tool's interface.
- **Contributors**: A heartfelt thank you to all the contributors who have helped improve this tool through their code contributions, bug reports, and feature suggestions.
