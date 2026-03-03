from setuptools import setup, find_packages
import os

# Read README for long description
def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return "Interactive mathematical visualization library"

setup(
    name="mathvizpro",
    version="0.1.0",
    author="MathViz Contributors",
    author_email="mathviz@example.com",
    description="Interactive mathematical visualization library for education and exploration",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/HORRIDBEAST/MathViz---The-Ultimate-Math-Py-Library",
    project_urls={
        "Bug Tracker": "https://github.com/HORRIDBEAST/MathViz---The-Ultimate-Math-Py-Library/issues",
        "Source Code": "https://github.com/HORRIDBEAST/MathViz---The-Ultimate-Math-Py-Library",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "sympy>=1.9.0",
        "mplcursors>=0.5.0",
    ],
    extras_require={
        "jupyter": ["ipywidgets>=7.6.0", "jupyter>=1.0.0"],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "sphinx>=4.0.0",
        ],
        "test": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
        ],
    },

    include_package_data=True,
    package_data={
        "mathviz": ["*.py"],
    },
    keywords="mathematics, visualization, education, calculus, algebra, interactive, plotting",
    zip_safe=False,
)