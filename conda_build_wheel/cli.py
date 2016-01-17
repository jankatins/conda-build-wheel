import argparse
import logging

import conda_build_wheel
import conda_build_wheel.builder
from conda.cli.common import add_parser_channels
from conda_build.main_build import PythonVersionCompleter, NumPyVersionCompleter


def main():
    parser = argparse.ArgumentParser(
        description='Build a wheel in a conda environment.')

    parser.add_argument('--version',
                        action='version',
                        version=conda_build_wheel.__version__)

    parser.add_argument('recipe',
                        help='The folder containing the wheel recipe to build.')

    parser.add_argument('--upload-pypi',
                        nargs='*',
                        default=[],
                        help='The PyPI channel(s) to upload built wheels to.')

    parser.add_argument(
        '--wheel-dir',
        nargs='*',
        default="./build",
        action="store",
        metavar='WHEEL_DIR_PATH',
        help="Path to the directory where the wheels should be created.")
    parser.add_argument(
        '--python',
        action="append",
        help="""Set the Python version used by wheel build. Can be passed
    multiple times to build against multiple versions. Can be 'all' to
    build against all known versions (%r)""" %
        [i for i in PythonVersionCompleter() if '.' in i],
        metavar="PYTHON_VER",
        choices=PythonVersionCompleter(), )

    parser.add_argument(
        '--numpy',
        action="append",
        help="""Set the NumPy version used by the wheel build. Can be passed
    multiple times to build against multiple versions. Can be 'all' to
    build against all known versions (%r)""" %
        [i for i in NumPyVersionCompleter() if '.' in i],
        metavar="NUMPY_VER",
        choices=NumPyVersionCompleter(), )

    add_parser_channels(parser)

    args = parser.parse_args()


    b = conda_build_wheel.builder.build_wheel(args.recipe,
                                        versions_combis = {"python": args.python or [],
                                                           "numpy": args.numpy or []},
                                        conda_channel_urls=args.channel or (),
                                        conda_override_channels=args.override_channels or (),
                                        upload=args.upload_pypi or [],
                                        wheel_dir=args.wheel_dir or "./build")


if __name__ == '__main__':
    main()
