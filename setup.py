from setuptools import setup, find_packages

setup(
    name="rpgnlp",
    version="0.1.0",
    description="A natural language parser for RPG text commands.",
    author="zship",
    url="https://github.com/zship/rpgnlp",
    packages=find_packages(),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        "nltk>=3.8",
        "spacy>=3.5",
    ],
)
