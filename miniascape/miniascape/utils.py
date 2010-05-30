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
import logging
import os
import random
import shutil
import string
import sys
import yaml  # PyYAML

try:
    import xattr   # pyxattr
except ImportError:
    logging.warn("pyxattr does not look installed. Fallback to Dummy implementation")
    xattr = FakeXattr()



class FakeXattr:
    """Dummy class mimics xattr module.
    """
    def get_all(self, *args):
        return ()

    def set(self, *args):
        return ()


def memoize(fn):
    """memoization decorator.
    """
    cache = {}

    def wrapped(*args, **kwargs):
        key = repr(args) + repr(kwargs)
        if not cache.has_key(key):
            cache[key] = fn(*args, **kwargs)

        return cache[key]

    return wrapped


def kickstart_password(pswd):
    """Generate encoded string for kickstart config from given password.

    >>> kp = kickstart_password('password')
    >>> assert isinstance(kp, str)
    >>> assert len(kp) == 34
    """
    return crypt.crypt(pswd,
        '$1$' + ''.join((random.choice(string.letters + string.digits + './') \
            for i in range(8)))
    )


def compile_template(tmpl, output, params={}):
    """Compile template:

    @tmpl    template file
    @output  output file
    @params  parameters to instantiate the template 
    """
    s = Cheetah.Template.Template(file=file, searchList=params).respond()

    out = open(output, 'w')
    out.write(s)
    out.close()


def runcmd(cmd_str):
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


def mkdir(dir, mode=0700):
    """Create a dir.
    """
    if os.path.exists(dir):
        logging.warn("The dir already exists: '%s'" % dir)
        if not os.path.isdir(dir):
            raise IOError("Not a directory: '%s'" % dir)
    else:
        logging.info("Creating a dir: '%s' (mode: %o)" % (dir, mode))
        os.makedirs(dir, mode)


def copyfile(src, dst, force=False):
    """
    @param  src  source path
    @param  dst  destination to copy to. dst may be a dir.
    """
    assert src != dst, "src == dst!"

    if not os.path.isdir(dst):
        if not force and os.path.exists(dst):
            logging.warn(" Copying destination '%s' already exists! Skipt it." % dst)
            return

    # copy itself and its some metadata (owner, mode, etc.)
    logging.info(" Copying '%s' -> '%s'..." % (src,dst))
    shutil.copy2(src, dst)

    # These are not copyed with the above.
    _xattrs = dict(xattr.get_all(src))
    if _xattrs:
        logging.info(" Copying xattrs...")
        for k,v in _xattrs.iteritems():
            xattr.set(dst, k, v)

    logging.info(" Done.")


# vim:sw=4:ts=4:et:
