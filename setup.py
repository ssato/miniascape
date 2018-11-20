from glob import glob

import os
import subprocess
import sys
import setuptools.command.bdist_rpm

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


class bdist_rpm(setuptools.command.bdist_rpm.bdist_rpm):
    """Override the default content of the RPM SPEC.
    """
    spec_tmpl = os.path.join(os.path.abspath(os.curdir),
                             "pkg/package.spec.in")

    def _replace(self, line):
        """Replace some strings in the RPM SPEC template"""
        if "@VERSION@" in line:
            return line.replace("@VERSION@", VERSION)

        if "Source0:" in line:  # Dirty hack
            return "Source0: %{name}-%{version}.tar.gz"

        return line

    def _make_spec_file(self):
        return [self._replace(l.rstrip()) for l
                in open(self.spec_tmpl).readlines()]


setuptools.setup(name=PACKAGE,
                 version=VERSION,
                 description="Personal cloud building and management tool",
                 author="Satoru SATOH",
                 author_email="ssato@redhat.com",
                 license="GPLv3+",
                 url="https://github.com/ssato/miniascape",
                 packages=["miniascape", "miniascape/tests"],
                 scripts=glob("tools/*"),
                 data_files=data_files,
                 cmdclass=dict(bdist_rpm=bdist_rpm))

# vim:sw=4:ts=4:et:
