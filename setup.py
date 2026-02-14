from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrapeba",
    version="0.1.0",
    author="Felix Schier",
    author_email="felix.schier@t-online.de",
    description="Scrape and consolidate data on the German labour market",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fschier/scrapeba",
    project_urls={
        "Bug Reports": "https://github.com/fschier/scrapeba/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
        "requests>=2.26.0",
        "tqdm>=4.62.0",
    ],
    package_data={
        "scrapeba": ["data/*.pkl"],
    },
    include_package_data=True,
)
