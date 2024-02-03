from setuptools import setup, find_packages

def load_requirements(filename='requirements.txt'):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='TranslationTool',
    version='0.1.0',
    author='JanPanthera',
    author_email='JanPanthera@outlook.de',
    description=('A tool designed to facilitate the creation of dictionaries, '
                 'which can then be used to translate an input file into multiple languages, '
                 'depending on the dictionaries created.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/JanPanthera/_AutodriveTranslationTool',
    packages=find_packages(),
    include_package_data=True,
    install_requires=load_requirements(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
