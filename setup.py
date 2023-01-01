from setuptools import setup

setup(
    name="conventionalish",
    version="0.1.0",
    py_modules=["cz_conventionalish"],
    license="MIT",
    description="Extend the Commitizen Conventional-Commits implementation",
    install_requires=["commitizen"],
)
