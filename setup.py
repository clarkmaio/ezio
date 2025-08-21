

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezioaltair",
    version="0.1.0",
    author="clarkmaio",
    author_email="maioliandrea0@gmail.com",
    description="A simple, opinionated wrapper for Altair visualizations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clarkmaio/ezio", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.10', # Altair often requires newer Python versions
    install_requires=[
        "altair>=5.0", # Specify a minimum version for Altair
        "polars",
    ],
    keywords="altair data-visualization plotting wrapper",
)