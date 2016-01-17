# (c) Continuum Analytics, Inc. / http://continuum.io
# (c) Jan Schulz
# All Rights Reserved
#
# conda is distributed under the terms of the BSD 3-clause license.
# Consult LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause.

from locale import getpreferredencoding
import sys
from os import environ as os_environ
from collections import deque

from conda.install import delete_trash
from conda.compat import PY3
from conda_build import exceptions
from conda_build.main_build import all_versions

on_win = (sys.platform == 'win32')

def build_wheel(recipe, versions_combis={"python": None, "numpy": None},
                conda_channel_urls=(),
                conda_override_channels=(),
                upload=[],
                wheel_dir="./build"):
    import sys
    import shutil
    import tarfile
    import tempfile
    from os.path import abspath, isdir, isfile

    from conda.lock import Locked
    from conda_build.config import config
    from conda_build.metadata import MetaData

    import conda_build_wheel.build_wheel as build

    if on_win:
        # needs to happen before any c extensions are imported that might be
        # hard-linked by files in the trash. one of those is markupsafe, used
        # by jinja2. see https://github.com/conda/conda-build/pull/520
        assert 'markupsafe' not in sys.modules
        delete_trash(None)

    conda_version = {
        'python': 'CONDA_PY',
        'numpy': 'CONDA_NPY',
    }
    for lang in ['python', 'numpy']:
        versions = versions_combis[lang]
        if not versions:
            continue
        if versions == ['all']:
            if all_versions[lang]:
                versions = all_versions[lang]
            else:
                print("'all' is not supported for --%s" % lang)
        if len(versions) > 1:
            for ver in versions[:]:
                setattr(versions_combis, lang, [str(ver)])
                build_wheel(recipe, versions_combis, conda_channel_urls=conda_channel_urls,
                            conda_override_channels=conda_override_channels,
                            upload=upload, wheel_dir=wheel_dir)
                # This is necessary to make all combinations build.
                setattr(versions_combis, lang, versions)
            return
        else:
            version = versions[0]
            if lang in ('python', 'numpy'):
                version = int(version.replace('.', ''))
            setattr(config, conda_version[lang], version)
        if not len(str(version)) in (2, 3) and lang in ['python', 'numpy']:
            if all_versions[lang]:
                raise RuntimeError("%s must be major.minor, like %s, not %s" %
                                   (conda_version[lang],
                                    all_versions[lang][-1] / 10, version))
            else:
                raise RuntimeError("%s must be major.minor, not %s" %
                                   (conda_version[lang], version))

    # Using --python, --numpy etc. is equivalent to using CONDA_PY, CONDA_NPY, etc.
    # Auto-set those env variables
    for var in conda_version.values():
        if getattr(config, var):
            # Set the env variable.
            os_environ[var] = str(getattr(config, var))

    with Locked(config.croot):
        # Don't use byte literals for paths in Python 2
        if not PY3:
            arg = recipe.decode(getpreferredencoding() or 'utf-8')
        if isfile(recipe):
            if arg.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
                recipe_dir = tempfile.mkdtemp()
                t = tarfile.open(arg, 'r:*')
                t.extractall(path=recipe_dir)
                t.close()
                need_cleanup = True
            else:
                print("Ignoring non-recipe: %s" % arg)
                return
        else:
            recipe_dir = abspath(recipe)
            need_cleanup = False

        if not isdir(recipe_dir):
            sys.exit("Error: no such directory: %s" % recipe_dir)

        try:
            m = MetaData(recipe_dir)
            if m.get_value('build/noarch_python'):
                config.noarch = True
        except exceptions.YamlParsingError as e:
            sys.stderr.write(e.error_msg())
            sys.exit(1)
        m.check_fields()

        if m.skip():
            print(
                "Skipped: The %s recipe defines build/skip for this "
                "configuration." % m.dist())
            return
        build.build(m, channel_urls=conda_channel_urls,
                    override_channels=conda_override_channels, wheel_dir=wheel_dir)

        if need_cleanup:
            shutil.rmtree(recipe_dir)
