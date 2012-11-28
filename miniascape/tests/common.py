#
# Copyright (C) 2012 Satoru SATOH <sssato at redhat.com>
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
import os
import os.path
import tempfile


def setup_workdir():
    return tempfile.mkdtemp(dir="/tmp", prefix="miniascape-tests")


def cleanup_workdir(workdir):
    """
    FIXME: This should be quite danger in some circumstances...
    """
    assert os.system("rm -rf " + workdir) == 0, "Clean up failed: " + workdir


def selfdir():
    return os.path.dirname(__file__)


TOPDIR = os.path.abspath(os.path.join(selfdir(), "..", ".."))

# vim:sw=4 ts=4 et:
