from distutils.core import setup, Command
from glob import glob

import os
import sys

curdir = os.getcwd()
sys.path.append(curdir)

from miniascape.globals import PACKAGE, VERSION
from miniascape.utils import concat


def list_files(tdir):
    return [f for f in glob(os.path.join(tdir, '*')) if os.path.isfile(f)]


def list_data_files_g(prefix, srcdir):
    for root, dirs, _files in os.walk(srcdir):
        for d in dirs:
            reldir = os.path.join(root, d)
            instdir = os.path.join(prefix, reldir)
            files = list_files(reldir)
            if files:
                yield (instdir, files)


data_files = concat(
    list_data_files_g(p, d) for p, d in
        (("/etc/%s.d" % PACKAGE, "default"),      # config files
         ("share/%s" % PACKAGE, "templates"),  # template files
        )
)


class SrpmCommand(Command):

    user_options = []

    build_stage = "s"
    cmd_fmt = """rpmbuild -b%(build_stage)s \
        --define \"_topdir %(rpmdir)s\" \
        --define \"_sourcedir %(rpmdir)s\" \
        --define \"_buildroot %(BUILDROOT)s\" \
        %(rpmspec)s
    """

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('sdist')
        self.build_rpm()

    def build_rpm(self):
        params = dict()

        params["build_stage"] = self.build_stage
        rpmdir = params["rpmdir"] = os.path.join(
            os.path.abspath(os.curdir), "dist"
        )
        rpmspec = params["rpmspec"] = os.path.join(
            rpmdir, "../%s.spec" % PACKAGE
        )

        for subdir in ("SRPMS", "RPMS", "BUILD", "BUILDROOT"):
            sdir = params[subdir] = os.path.join(rpmdir, subdir)

            if not os.path.exists(sdir):
                os.makedirs(sdir, 0755)

        c = open(rpmspec + ".in").read()
        open(rpmspec, "w").write(c.replace("@VERSION@", VERSION))

        os.system(self.cmd_fmt % params)


class RpmCommand(SrpmCommand):

    build_stage = "b"


setup(name=PACKAGE,
    version=VERSION,
    description="Personal cloud building and management tool",
    author="Satoru SATOH",
    author_email="ssato@redhat.com",
    license="GPLv3+",
    url="https://github.com/ssato/miniascape",
    packages=[
        "miniascape",
        "miniascape/tests",
    ],
    scripts=glob("tools/*"),
    data_files=data_files,
    cmdclass={
        "srpm": SrpmCommand,
        "rpm":  RpmCommand,
    },
)

# vim:sw=4:ts=4:et:
