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
import jinja2_cli.render

try:
    import gevent

    _spawn = gevent.spawn
    _joinall = gevent.joinall
except ImportError:
    _spawn = lambda f, *args: f(*args)
    _joinall = lambda _: True


def _renderto(tpaths, ctx, tmpl, output, ask=False):
    """
    NOTE: Take care of arguments' order.
    """
    jinja2_cli.render.renderto(tmpl, ctx, tpaths, output, ask=ask)


def renderto(tpaths, ctx, tmpl, output, ask=False, async=False):
    """
    NOTE: Take care not to forget stop (join) threads run from this function
    if ask = False and async = True.

    :param tpaths: List of template search paths
    :param ctx: Context (dict like obj) to instantiate templates
    :param tmpl: Template filename
    :param output: Output file path
    :param ask: It will ask for paths of missing templates if True
    :param async: Run template rendering function asynchronously if possible
        and it's True.
    """
    if not ask and async:
        return _spawn(_renderto, tpaths, ctx, tmpl, output, ask)
    else:
        _renderto(tpaths, ctx, tmpl, output, ask)

    return True


def finish_renderto_threads(threads):
    _joinall(threads)

# vim:sw=4:ts=4:et:
