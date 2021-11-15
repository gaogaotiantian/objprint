import setuptools

with open("README.md") as f:
    long_description = f.read()

with open("./src/objprint/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

setuptools.setup(
    name="objprint",
    version=version,
    author="Tian Gao",
    author_email="gaogaotiantian@hotmail.com",
    description="A library that can print Python objects in human readable format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaogaotiantian/objprint",
    packages=setuptools.find_packages("src"),
    package_dir={"":"src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
)
