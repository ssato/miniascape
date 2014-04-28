"""
 :copyright: (c) 2012, 2013 by Satoru SATOH <ssato@redhat.com>
 :license: BSD-3

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:

   * Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
   * Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
   * Neither the name of the author nor the names of its contributors may
     be used to endorse or promote products derived from this software
     without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
 DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import codecs
import glob
import itertools
import locale
import logging
import os.path
import sys


ENCODING = locale.getdefaultlocale()[1]

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
    from anyconfig.api import container, load
except ImportError:
    container = dict

    try:
        import json
    except ImportError:
        try:
            import simplejson as json
        except ImportError:
            sys.stderr.write("Could not load any json module! Aborting...\n")
            sys.exit(-1)

    def load(filepath, _ftype):
        return json.load(open(filepath))


def uniq(xs):
    """Remove duplicates in given list with its order kept.

    >>> uniq([])
    []
    >>> uniq([1, 4, 5, 1, 2, 3, 5, 10])
    [1, 4, 5, 2, 3, 10]
    """
    acc = xs[:1]
    for x in xs[1:]:
        if x not in acc:
            acc += [x]

    return acc


def chaincalls(callables, x):
    """
    :param callables: callable objects to apply to x in this order
    :param x: Object to apply callables
    """
    for c in callables:
        assert callable(c), "%s is not callable object!" % str(c)
        x = c(x)

    return x


def normpath(path):
    """Normalize given path in various different forms.

    >>> normpath("/tmp/../etc/hosts")
    '/etc/hosts'
    >>> normpath("~root/t")
    '/root/t'
    """
    if "~" in path:
        fs = [os.path.expanduser, os.path.normpath, os.path.abspath]
    else:
        fs = [os.path.normpath, os.path.abspath]

    return chaincalls(fs, path)


def flip(xy):
    (x, y) = xy
    return (y, x)


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


def parse_filespec(fspec, sep=':', gpat='*'):
    """
    Parse given filespec `fspec` and return [(filetype, filepath)].

    Because anyconfig.api.load should find correct file's type to load by the
    file extension, this function will not try guessing file's type if not file
    type is specified explicitly.

    :param fspec: filespec
    :param sep: a char separating filetype and filepath in filespec
    :param gpat: a char for glob pattern

    >>> parse_filespec("base.json")
    [('base.json', None)]
    >>> parse_filespec("json:base.json")
    [('base.json', 'json')]
    >>> parse_filespec("yaml:foo.yaml")
    [('foo.yaml', 'yaml')]
    >>> parse_filespec("yaml:foo.dat")
    [('foo.dat', 'yaml')]

    # FIXME: How to test this?
    # >>> parse_filespec("yaml:bar/*.conf")
    # [('bar/a.conf', 'yaml'), ('bar/b.conf', 'yaml')]

    TODO: Allow '*' (glob pattern) in filepath when escaped with '\\', etc.
    """
    tp = (ft, fp) = tuple(fspec.split(sep)) if sep in fspec else (None, fspec)

    return [(fs, ft) for fs in sorted(glob.glob(fp))] \
        if gpat in fspec else [flip(tp)]


def parse_and_load_contexts(contexts, enc=ENCODING, werr=False):
    """
    :param contexts: list of context file specs
    :param enc: Input encoding of context files (dummy param)
    :param werr: Exit immediately if True and any errors occurrs
        while loading context files
    """
    ctx = container()

    if contexts:
        for fpath, ftype in concat(parse_filespec(f) for f in contexts):
            diff = load(fpath, ftype)
            ctx.update(diff)

    return ctx

# vim:sw=4:ts=4:et:
