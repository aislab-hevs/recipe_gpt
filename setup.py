from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# Requirements for installing the package
REQUIREMENTS = [
'openai',
'pandas ',
'python-dotenv',
'seaborn',
'skickit-learn',
'spacy',
'nltk'
]

# Some details 
CLASSIFIERS = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Web Scraping :: Database :: Database',
        'Intended Audience :: Science/Research',
]

setup(
    name='recipe_gpt',
    version='0.0.1',
    description='',
    author='Victor Hugo Contreras and Davide Calvaresi',
    author_email='victorc365@gmail.com',
    packages=find_packages(),
    install_dependencies=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    python_requires='>=3.9',
)