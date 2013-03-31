#
# Copyright (C) 2012 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato@redhat.com>
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
from miniascape.globals import LOGGER as logging
import miniascape.memoize as M

import glob
import itertools
import os.path
import os
import pwd
import socket

try:
    chain_from_iterable = itertools.chain.from_iterable
except AttributeError:
    # Borrowed from library doc, 9.7.1 Itertools functions:
    def _from_iterable(iterables):
        for it in iterables:
            for element in it:
                yield element

    chain_from_iterable = _from_iterable


def concat(xss):
    """
    >>> concat([[]])
    []
    >>> concat((()))
    []
    >>> concat([[1,2,3],[4,5]])
    [1, 2, 3, 4, 5]
    >>> concat([[1,2,3],[4,5,[6,7]]])
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat((i, i*2) for i in range(3))
    [0, 0, 1, 2, 2, 4]
    """
    return list(chain_from_iterable(xs for xs in xss))


def sglob(files_pattern):
    return sorted(glob.glob(files_pattern))


def list_dirnames(tdir):
    """
    :param tdir: dir in which target dirs exist
    """
    return [
        os.path.basename(x) for x in
            sglob(os.path.join(tdir, "*")) if os.path.isdir(x)
    ]


@M.memoize
def is_superuser():
    return os.getuid() == 0


@M.memoize
def get_username():
    return pwd.getpwuid(os.getuid()).pw_name


@M.memoize
def get_hostname(fqdn=True):
    try:
        h = socket.getfqdn() or socket.gethostname() or os.uname()[1]
    except:
        h = "localhost.localdomain"

    return h if fqdn else (h.split('.')[0] if '.' in h else h)


def find_dups_in_dicts_list_g(ds, keys):
    """
    Generator to find out duplicated items (values) in given list of dicts.

    :param ds: A list of dicts to find out duplicated items.
    :param keys: Key to search duplicated items.

    >>> d0 = {'a': 1, 'b': 2}
    >>> d1 = {'b': 2, 'c': 4}
    >>> ds = [d0, d1, {}]

    >>> dups = [t for t in find_dups_in_dicts_list_g(ds, ('a', 'b'))]
    >>> assert dups == [('b', 2, [d0, d1])]
    """
    seens = dict((k, {}) for k in keys)

    for d in ds:
        for k in keys:
            v = d.get(k, None)
            if v is not None:
                dups = seens[k].get(v, [])
                if dups:
                    seens[k][v].append(d)
                else:
                    seens[k][v] = [d]

    for k in keys:
        for v, dups in seens[k].iteritems():
            if len(dups) > 1:  # duplicated entries
                yield (k, v, dups)


# vim:sw=4:ts=4:et:
