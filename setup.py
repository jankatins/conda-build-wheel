from setuptools import setup
import versioneer

setup(
    name='conda-build-wheel',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Build a wheel from a conda (like) recipe.',
    author='Jan Schulz',
    author_email='jasc@gmx.net',
    url='https://github.com/janschulz/conda-build-wheel',
    packages=['conda_build_wheel'],
    entry_points={
        'console_scripts': [
            'conda-build-wheel = conda_build_wheel.cli:main',
            # This is needed as conda can't deal with dashes in subcommands yet
            # (see https://github.com/conda/conda/pull/1840).
            'conda-buildwheel = conda_build_wheel.cli:main',
        ]
    }, )
