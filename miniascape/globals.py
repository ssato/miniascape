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


def date():
    return datetime.datetime.now().strftime("%Y%m%d")


M_CONF_TOPDIR = "/etc/miniascape.d"
M_TMPL_DIR = "/usr/share/miniascape/templates"

M_SITE_DEFAULT = "default"
M_CONFDIR_DEFAULT = os.path.join(M_CONF_TOPDIR, M_SITE_DEFAULT)
M_COMMON_CONF_SUBDIR = "common"
M_GUESTS_CONF_SUBDIR = "guests.d"
M_NETS_CONF_SUBDIR = "networks.d"
M_HOST_CONF_SUBDIR = "host.d"
M_CONF_PATTERN = "*.yml"

M_HOST_OUT_SUBDIR = "host"
M_NETS_OUT_SUBDIR = "usr/share/libvirt/networks"

M_WORK_TOPDIR = "miniascape-workdir-" + date()
M_ENCODING = locale.getdefaultlocale()[1]

PACKAGE = "miniascape"
VERSION = "0.3.6"

_LOGGING_FORMAT = "%(asctime)s %(name)s: [%(levelname)s] %(message)s"


def getLogger(name="miniascape", format=_LOGGING_FORMAT,
              level=logging.WARNING, **kwargs):
    """
    Initialize custom logger.
    """
    logging.basicConfig(level=level, format=format)
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

# vim:sw=4:ts=4:et:
