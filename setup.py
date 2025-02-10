from setuptools import setup

setup(
    name="corsmanic",
    version="1.0",
    py_modules=["corsmanic"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "corsmanic=corsmanic:main",
        ],
    },
)
