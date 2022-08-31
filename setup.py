from setuptools import setup, find_packages
import sys

setup(
    name="teachat",
    version="0.0.0+dev",
    author='1107-1108, Yang_qwq',
    author_email='',
    description='',
    license="MIT",
    url='https://github.com/1107-1108/teachat',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9'
    ],
    install_requires=[
        'pip>=22.2.2',
        'setuptools>=65.3.0'
    ],
    zip_safe=True,
)
