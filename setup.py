import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pyvieser",
    version="0.0.3",
    author="Radu Boncea",
    author_email="radu.boncea@gmail.com",
    description="A wrapper API of VIES VAT web service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agilegeeks/pyVies",
    packages=setuptools.find_packages(exclude=['tests']),
    entry_points={
        "console_scripts": [
            "pyvies = pyVies.api:console",
        ]
    },
    install_requires=[
          "zeep>=3.1.0"
    ],
    python_requires='>=2.7',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database :: Front-Ends",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
