import setuptools

setuptools.setup(name="prometry",
    version="0.0.24",
    author="Rachel Alcraft",
    description="Library to calculate geometric parameters of protein structures including criteria searches.",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    install_requires=["leuci_xyz","biopython"],
    python_requires = ">=3.6"
    )