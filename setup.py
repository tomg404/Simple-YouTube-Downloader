from io import open
from setuptools import setup
from sytd import __version__ as version

setup(
    name='sytd',
    version=version,
    url='https://github.com/tomg404/Simple-YouTube-Downloader',
    license='MIT',
    author='Tom Gaimann',
    author_email='tom.gaimann@outlook.com',
    description='Simple YouTube Downloader',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    keywords=['gui', 'downloader', 'youtube', 'simple'],
    packages=['sytd'],
    include_package_data=True,
    install_requires=['Eel==0.11.0', 'bottle==0.12.18', 'gevent==1.5.0', 'youtube-dl==2020.3.24'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
        'console_scripts': [
            'sytd=sytd.__main__:run',
            'simple-youtube-downloader=sytd.__main__:run',
        ],
    },
)
