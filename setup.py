import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

REQUIRES_PYTHON = ">=3.8"
# This call to setup() does all the work
setup(
    name="icondetection",
    version="0.1.0",
    description="Detect icons on the screen easily and quickly.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/luiszugasti/IconMatch",
    author="Luis Zugasti",
    author_email="hello@luiszugasti.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["test", "*.test", "*.test.*", "test.*"]),
    include_package_data=True,
    install_requires=["Pillow", "opencv-contrib-python", "numpy"],
)
