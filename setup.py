import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="pinopoly",
    version="1.0.0",
    description="A client to digitalize the boring parts of monopoly",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alexover1/pinopoly",
    author="Alex Overstreet",
    author_email="alex@overstreet.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["monopoly"],
    include_package_data=True,
)
