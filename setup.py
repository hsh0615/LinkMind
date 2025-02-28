from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="linkmind",
    version="1.0.0",
    description="Python backend for the LinkMind Obsidian plugin",
    author="hsh0615",
    author_email="hsh0615@example.com",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "linkmind=main:main",
        ],
    },
) 