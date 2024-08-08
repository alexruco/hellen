# setup.py
from setuptools import setup, find_packages

setup(
    name='hellen',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'hellen=hellen.main:main'
        ],
    },
    author='Alex Ruco',
    author_email='alex@ruco.pt',
    description='A package for fetching and processing web links',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alexruco/hellen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
