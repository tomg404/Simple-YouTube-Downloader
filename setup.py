"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(

    name='sytd',
    version='1.0.1',
    description='Simple YouTube Downloader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tomg404/Simple-YouTube-Downloader',
    author='Tom Gaimann',
    author_email='tom.gaimann@outlook.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    entry_points={
        'gui_scripts': [
            'sytd = sytd.__main__:main']
    },
    keywords=['youtube', 'download', 'client', 'easy'],
    packages=find_packages(where='sytd'),
    python_requires='>=3.5',
    install_requires=['Eel==0.11.0', 'youtube_dl==2020.3.24'],

)
