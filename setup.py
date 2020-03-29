import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PiDotLCD",
    version="0.1.1",
    author="Stanley Fuller",
    author_email="stanthesoupking@gmail.com",
    description="Python driver for using a 128x64 dot LCD display on a Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stanthesoupking/PiDotLCD",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)