from distutils.core import setup
from setuptools import find_packages


setup(
    name="dgk",
    version="0.08.1",
    packages=find_packages(),
    package_data={"dgk": ["config/*.ini", "database/*.db"]},
    url="https://github.com/mtaylor33/personaednd",
    license="MIT",
    author="Marcus T Taylor",
    description="A simple graphical application to track your disc golf games.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.0",
    entry_points={"console_scripts": ["dgk=dgk.app:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Database",
        "Topic :: Other/Nonlisted Topic",
    ],
)
