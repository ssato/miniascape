from distutils.core import setup, Command

import datetime
import glob
import os
import sys

curdir = os.getcwd()
sys.path.append(curdir)

PACKAGE = "miniascape"
VERSION = "0.3.0"

# daily snapshots:
#VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")

data_files = [
    # sysconf files:
    ("/etc/%s/default/common" % PACKAGE, glob.glob("config/default/common/*")),
    ("/etc/%s/default/networks.d" % PACKAGE,
        glob.glob("config/default/networks.d/*")),
    ("/etc/%s/default/guests.d" % PACKAGE,
        glob.glob("config/default/guests.d/*")),
    ("/etc/%s/default/storages.d" % PACKAGE,
        glob.glob("config/default/storages.d/*")),

    # template files:
    ("share/%s/templates/libvirt" % PACKAGE,
        glob.glob("templates/libvirt/*")),
    ("share/%s/templates/autoinstall.d" % PACKAGE,
        glob.glob("templates/autoinstall.d/*-ks.cfg")),
    ("share/%s/templates/autoinstall.d/data" % PACKAGE,
        glob.glob("templates/autoinstall.d/data/*")),
    ("share/%s/templates/autoinstall.d/snippets" % PACKAGE,
        glob.glob("templates/autoinstall.d/snippets/*")),
    ("share/%s/templates/data/rhui/root/setup" % PACKAGE,
        ["templates/data/rhui/root/setup/answers.txt"]),
    ("share/%s/templates/data/rhui/root/setup/certs" % PACKAGE,
        glob.glob("templates/data/rhui/root/setup/certs/*")),
]


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
    ],
    scripts=glob.glob("tools/*"),
    data_files=data_files,
    cmdclass={
        "srpm": SrpmCommand,
        "rpm":  RpmCommand,
    },
)


# vim:sw=4:ts=4:et:
