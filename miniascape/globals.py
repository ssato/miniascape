#
# Copyright (C) 2012 Satoru SATOH <ssato@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import datetime
import locale
import logging
import os.path


_DTOBJ = datetime.datetime.now()


def timestamp(fmt="%a %b %_d %Y", dtobj=_DTOBJ):
    """
    >>> dtobj = datetime.datetime(2013, 10, 20, 12, 11, 59, 345135)
    >>> timestamp(dtobj=dtobj)
    'Sun Oct 20 2013'
    """
    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
    return dtobj.strftime(fmt)


PACKAGE = "miniascape"
VERSION = "0.3.11"

M_SITE_DEFAULT = "default"
M_VMBUILD_SH = "vmbuild.sh"

M_CONF_TOPDIR = "/etc/miniascape.d"
M_TMPL_DIR = "/usr/share/miniascape/templates"
M_GUESTS_BUILDDATA_TOPDIR = "/usr/share/miniascape/build/guests"

M_SITE_DEFAULT = "default"

M_BOOTSTRAP_SUBDIR = "bootstrap"
M_COMMON_CONF_SUBDIR = "common"
M_GUESTS_CONF_SUBDIR = "guests.d"
M_NETS_CONF_SUBDIR = "networks.d"
M_HOST_CONF_SUBDIR = "host.d"
M_CONF_PATTERN = "*.yml"

M_HOST_OUT_SUBDIR = "host"
M_NETS_OUT_SUBDIR = "networks"

M_WORK_TOPDIR = "miniascape-workdir-" + timestamp("%Y%m%d")
M_ENCODING = locale.getdefaultlocale()[1]


def site_confdir(site=M_SITE_DEFAULT, topdir=M_CONF_TOPDIR):
    return os.path.join(topdir, site)


def site_src_ctx(site=M_SITE_DEFAULT, topdir=M_CONF_TOPDIR):
    # return os.path.join(site_confdir(site, topdir), M_CONF_PATTERN)
    return site_confdir(site, topdir)


M_CONFDIR_DEFAULT = os.path.join(M_CONF_TOPDIR, M_SITE_DEFAULT)
M_CTXS_DEFAULT = os.path.join(M_CONFDIR_DEFAULT, M_CONF_PATTERN)

_LOGGING_FORMAT = "%(asctime)s %(name)s: [%(levelname)s] %(message)s"


def getLogger(name="miniascape", format=_LOGGING_FORMAT,
              datefmt="%Y-%m-%d %H:%M:%S",
              level=logging.WARNING, **kwargs):
    """
    Initialize custom logger.
    """
    logging.basicConfig(level=level, format=format, datefmt=datefmt)
    logger = logging.getLogger(name)

    h = logging.StreamHandler()
    h.setLevel(level)
    h.setFormatter(logging.Formatter(format))
    logger.addHandler(h)

    return logger


LOGGER = getLogger()


def set_loglevel(level):
    assert level in (0, 1, 2), "Invalid log level option was passed: " + level
    lvl = [logging.DEBUG, logging.INFO, logging.WARN][level]
    logging.getLogger().setLevel(lvl)
    LOGGER.setLevel(lvl)


logging.getLogger("anytemplate").setLevel(logging.WARN)

# vim:sw=4:ts=4:et:
