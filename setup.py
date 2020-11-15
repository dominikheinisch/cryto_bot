from setuptools import setup, find_packages

setup(
    name="crypto_bot",
    author="dominik",
    url="https://github.com/dominikheinisch/cryto_bot",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"crypto_bot": ["database/schema.sql"]},
    python_requires=">=3.7",
)
