from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyget',
    version='3.2.2',
    description='Python3 Bitget Asyncio HTTP/WebSocket API Connector',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/APF20/pyget',
    license='MIT License',
    author='APF20',
    author_email='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='bitget api connector asyncio',
    packages=['pyget'],
    python_requires='>=3.8',
    install_requires=[
        'aiohttp',
    ],
)
