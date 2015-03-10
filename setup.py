from distutils.core import setup, Command
from glob import glob

import os
import subprocess
import sys

curdir = os.getcwd()
sys.path.append(curdir)

from miniascape.globals import PACKAGE, VERSION, M_CONF_TOPDIR
from miniascape.utils import concat


# For daily snapshot versioning mode:
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    from miniascape.globals import timestamp
    VERSION = VERSION + timestamp(".%Y%m%d")


def list_files(tdir):
    return [f for f in glob(os.path.join(tdir, '*')) if os.path.isfile(f)]


def list_data_files_g(prefix, srcdir, offset=None):
    for root, dirs, _files in os.walk(srcdir):
        for d in dirs:
            reldir = os.path.join(root, d)
            files = list_files(reldir)

            if not files:
                continue

            if offset is not None:
                if offset in reldir:
                    reldir = reldir.replace(offset, '')

            instdir = os.path.join(prefix, reldir)
            yield (instdir, files)


data_files = list(list_data_files_g(M_CONF_TOPDIR, "conf", "conf/"))
data_files += concat(list_data_files_g(p, d) for p, d in
                     (("share/%s" % PACKAGE, "templates"),  # template files
                      ("share/%s" % PACKAGE, "tests"),      # test cases
                      ))


class SrpmCommand(Command):

    user_options = []

    build_stage = "s"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('sdist')
        self.build_rpm()

    def build_rpm(self):
        curdir = os.path.abspath(os.curdir)
        rpmspec = os.path.join(curdir, "%s.spec" % PACKAGE)

        c = open(rpmspec + ".in").read()
        open(rpmspec, "w").write(c.replace("@VERSION@", VERSION))

        rpmbuild = os.path.join(curdir, "pkg/rpmbuild-wrapper.sh")
        workdir = os.path.join(curdir, "dist")

        subprocess.check_call("%s -w %s -s %s %s" % (rpmbuild, workdir,
                                                     self.build_stage,
                                                     rpmspec),
                              shell=True)


class RpmCommand(SrpmCommand):

    build_stage = "b"


setup(name=PACKAGE,
      version=VERSION,
      description="Personal cloud building and management tool",
      author="Satoru SATOH",
      author_email="ssato@redhat.com",
      license="GPLv3+",
      url="https://github.com/ssato/miniascape",
      packages=["miniascape",
                "miniascape/contrib",
                "miniascape/tests"],
      scripts=glob("tools/*"),
      data_files=data_files,
      cmdclass=dict(srpm=SrpmCommand,
                    rpm=RpmCommand))

# vim:sw=4:ts=4:et:
