conda build-wheel
=================

``conda build-wheel`` is a conda subcommand which allows to build a wheel from a recipe much like a
conda recipe.

It makes use of the underlying machinery developed for ``conda build``: 

 * it uses a `meta.yml` from a normal conda build recipe to build an environment with the required 
   dependencies
 * it uses a found `build_wheel.sh` (unix) or a `bld_wheel.bat` to build the wheel package in that 
   environment.
 * if no such build script is found, it simple calls `python setup.py bdist_wheel` 
 * it copies the build wheel file into a predefined directory (default: ./build)
 * it will optionally upload the wheel to pypi [not yet implmented]
 

Installation
============
Will eventually be installable with:

```
conda install conda-build-wheel -c janschulz
```


Usage
======

```
usage: conda-buildwheel [-h]
                      [--upload-pypi]
                      recipes

Build a wheel for a packages using a conda environment.

positional arguments:
  recipes               The folder containing conda-wheel recipes to build.

optional arguments:
  -h, --help            show this help message and exit
  --upload-pypi         If given, the package will try to upload the resulting 
                        wheel to PyPI.
  --wheel_dir directory
                        if given the resulting wheels will be created in this 
                        directory (default ./build)
```
