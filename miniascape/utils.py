#
# Utility routines
#
# Copyright (C) 2009, 2010 Satoru SATOH <satoru.satoh at gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import Cheetah.Template
import commands
import crypt
import os
import random
import string
import sys
import yaml  # PyYAML



def kickstart_password(pswd):
    """Generate encoded string for kickstart config from given password.

    >>> kp = kspassword('password')
    >>> assert isinstance(kp, str)
    >>> assert len(kp) == 34
    """
    return crypt.crypt(pswd,
        '$1$' + ''.join((random.choice(string.letters + string.digits + './') \
            for i in range(8)))
    )


def compile_template(file=None, source=None, params={}, **kwargs):
    """Compile template:

    1. file: template is given as a file.
    2. source: template is given as a string.
    3. otherwise:
    """
    if file is not None:
        return Cheetah.Template.Template(file=file, searchList=params).respond()

    elif source is not None:
        return Cheetah.Template.Template(source=tmpl_str, searchList=params).respond()

    else:
        return Cheetah.Template.Template(searchList=params, **kwargs).respond()


def runcmd(cmd_str, dryrun=False):
    """Execute given command sequence.
    """
    return commands.getstatusoutput(cmd_str)


def load_config(config_path):
    """Load given config file in YAML format.
    """
    return yaml.load(open(config_path))


def gen_fence_key(keyfile, force=False):
    """Generate fence_xvm key file.
    """
    if not force:
        assert not os.path.exists(keyfile), "Keyfile %s already exists!" % keyfile

    (rc, _out) = runcmd("dd if=/dev/urandom of=%s bs=4k count=1" % keyfile)
    return rc == 0


# vim:sw=4:ts=4:et:
