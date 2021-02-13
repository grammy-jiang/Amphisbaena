"""
setup.py
"""
from setuptools import find_packages, setup

import versioneer

setup(
    name="Amphisbaena",
    author="Grammy Jiang",
    author_email="grammy.jiang@gmail.com",
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=[
        "orjson",
        "pyyaml",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "amphisbaena=amphisbaena.__main__:entrypoint",
        ],
    },
)
