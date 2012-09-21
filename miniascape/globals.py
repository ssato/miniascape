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


def date():
    return datetime.datetime.now().strftime("%Y%m%d")


M_CONF_DIR = "/etc/miniascape/conf.d/default"
M_TMPL_DIR = "/usr/share/miniascape/templates"
M_WORK_TOPDIR = "workdir-" + date()
M_ENCODING = locale.getdefaultlocale()[1]

M_COMMON_CONFDIR = "common"


PACKAGE = "miniascape"
VERSION = "0.3.2"

# daily snapshots:
# import datetime
VERSION = VERSION + "." + date()


# vim:sw=4:ts=4:et:
