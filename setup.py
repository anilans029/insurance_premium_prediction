from setuptools import setup, find_packages
from typing import List


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PROJECT_NAME = "insurance_premium_prediction"
USER_NAME = "anilans029"
REQUIREMENTS_FILE_NAME = 'requirements.txt'


def get_requirements_list()->List[str]:
    """
    The get_requirements_list function returns a list of all the packages in the requirements file.

    :return: A list of strings that contain the contents of the requirements
    :author: anil
    """
  
    with open(REQUIREMENTS_FILE_NAME,"r") as requriemets:
        return requriemets.readlines().remove("-e .")

setup(
    name= PROJECT_NAME,
    version="0.0.1",
    author=USER_NAME,
    author_email="anilsai029@gmail.com",
    description="A small package for insrance_premium_prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires= get_requirements_list()
)
