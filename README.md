Deprecated: use https://github.com/pypa/cibuildwheel
====================================================


conda build-wheel
=================

``conda buildwheel`` is a conda subcommand which allows to build a wheel from a recipe much like a
conda recipe.

It makes use of the underlying machinery developed for ``conda build``: 

 * it uses a `meta.yml` from a normal conda build recipe to build an environment with the required 
   dependencies
 * it uses a found `build_wheel.sh` (unix) or a `bld_wheel.bat` to build the wheel package in that 
   environment.
 * if no such build script is found, it simple calls `python setup.py bdist_wheel`. This makes it
   possible to reuse the conda recipes without any changes (at least for simple ones).
 * it copies the build wheel file into a predefined directory (default: ./build)
 * it will optionally upload the wheel to pypi [not yet implemented]
 

Installation
============
Will eventually be installable with:

```
conda install conda-build-wheel -c janschulz
```


Usage
======

```
usage: conda-buildwheel-script.py [-h] [--version]
                                  [--upload-pypi [UPLOAD_PYPI [UPLOAD_PYPI ...]]]
                                  [--wheel-dir WHEEL_DIR_PATH]
                                  [--python PYTHON_VER] [--numpy NUMPY_VER]
                                  [-c CHANNEL] [--override-channels]
                                  recipe

Build a wheel in a conda environment.

positional arguments:
  recipe                The folder containing the wheel recipe to build.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --upload-pypi [UPLOAD_PYPI [UPLOAD_PYPI ...]]
                        The PyPI channel(s) to upload built wheels to.
  --wheel-dir WHEEL_DIR_PATH
                        Path to the directory where the wheels should be
                        created.
  --python PYTHON_VER   Set the Python version used by wheel build. Can be
                        passed multiple times to build against multiple
                        versions. Can be 'all' to build against all known
                        versions (['2.6', '2.7', '3.3', '3.4', '3.5'])
  --numpy NUMPY_VER     Set the NumPy version used by the wheel build. Can be
                        passed multiple times to build against multiple
                        versions. Can be 'all' to build against all known
                        versions (['1.6', '1.7', '1.8', '1.9', '11.0'])
  -c CHANNEL, --channel CHANNEL
                        Additional channel to search for packages. These are
                        URLs searched in the order they are given (including
                        file:// for local directories). Then, the defaults or
                        channels from .condarc are searched (unless
                        --override-channels is given). You can use 'defaults'
                        to get the default packages for conda, and 'system' to
                        get the system packages, which also takes .condarc
                        into account. You can also use any name and the
                        .condarc channel_alias value will be prepended. The
                        default channel_alias is http://conda.anaconda.org/.
  --override-channels   Do not search default or .condarc channels. Requires
                        --channel.

```
