from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-simple-hooks",
    version="0.1.1",
    author="Andrzej Klajnert",
    author_email="python@aklajnert.pl",
    description="Define your own hooks for mkdocs, without having to create a new package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aklajnert/mkdocs-simple-hooks",
    license="MIT",
    packages=find_packages(),
    install_requires=["mkdocs>=1"],
    extras_require={"test": ["pytest>=4.0", "pytest-cov"]},
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "mkdocs.plugins": [
            "mkdocs-simple-hooks = mkdocs_simple_hooks:SimpleHooksPlugin"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Documentation",
    ],
)
