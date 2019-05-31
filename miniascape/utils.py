#
# Copyright (C) 2012 - 2014 Red Hat, Inc.
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
from miniascape.memoize import memoize

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

try:
    # pylint: disable=no-name-in-module
    from anyconfig import is_mergeabledict_or_dict
    # pylint: enable=no-name-in-module
except ImportError:
    def is_mergeabledict_or_dict(x):
        return isinstance(x, dict)


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
    return [os.path.basename(x) for x in
            sglob(os.path.join(tdir, "*")) if os.path.isdir(x)]


def get_username_():
    return pwd.getpwuid(os.getuid()).pw_name


def get_hostname_(h=None, fqdn=True):
    """
    :param h: A parameter to explicitly pass hostname
    :param fqdn: Try getting FQDN instead of short hostname if True

    :return: A string represents hostname or fqdn

    >>> get_hostname_("foo.example.com")
    'foo.example.com'
    >>> get_hostname_("foo.example.com", False)
    'foo'
    """
    if h is None:
        try:
            h = socket.getfqdn() or socket.gethostname() or os.uname()[1]
        except:
            h = "localhost.localdomain"

    return h if fqdn else (h.split('.')[0] if '.' in h else h)


# Memoized versions:
get_username = memoize(get_username_)
get_hostname = memoize(get_hostname_)


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
        for v, dups in seens[k].items():
            if len(dups) > 1:  # duplicated entries
                yield (k, v, dups)


def noop(*args):
    return args


def walk(x, path=None, sep='.', hook=noop):
    """
    Walk through given object (may-be-a-MergeableDict-instance) ``x`` like
    os.walk. Currently, DFS (depth first search) is used to traverse (walk
    through) ``x``.

    This fucntion will walk through object tree and yield:

        (curpath, value, dic)

    where curpath is the 'path' to the object key, value is dic[key] and dic is
    the dict object reference.

    :param x: Object to walk (traverse), may be an instance of MergeableDict
    :param path: Current 'path'
    :param sep: Path separator
    """
    if is_mergeabledict_or_dict(x):
        for k, v in x.items():
            curpath = k if path is None else "{}{}{}".format(path, sep, k)

            if is_mergeabledict_or_dict(v):
                for path_child, v_child, _d in walk(v, curpath, sep,
                                                    hook):
                    yield hook(path_child, v_child, v)

            # FIXME: process lists.
            elif isinstance(v, (list, tuple)):
                continue
            #    for i, y in enumerate(v):
            #        # Encode index into the path ?
            #        curpath = "{}:{}".format(curpath, i)
            #       yield hook(curpath, y, v)
            else:
                yield hook(curpath, v, x)
    else:
        yield hook(path, x, None)

# vim:sw=4:ts=4:et:
