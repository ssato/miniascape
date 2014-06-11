#
# Copyright (C) 2012 - 2014 Satoru SATOH <ssato@redhat.com>
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
import miniascape.contrib.render
import multiprocessing
import os.path


def _renderto(tpaths, ctx, tmpl, output, ask=False):
    """
    NOTE: Take care of arguments' order.
    """
    miniascape.contrib.render.renderto(tmpl, ctx, tpaths, output, ask=ask)


def renderto(tpaths, ctx, tmpl, output, ask=True, async=False):
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
    d = os.path.dirname(output)
    if not os.path.exists(d):
        os.makedirs(d)

    if not ask and async:
        proc = multiprocessing.Process(target=_renderto,
                                       args=(tpaths, ctx, tmpl, output, ask))
        proc.start()
        return proc
    else:
        _renderto(tpaths, ctx, tmpl, output, ask)

    return True


def finish_renderto_procs(procs):
    for p in procs:
        p.join()


def compile_conf_templates(conf, tmpldirs, workdir, templates_key="templates"):
    """

    :param conf: Config object holding templates info
    :param tmpldirs: Template paths
    :param workdir: Working dir
    :param template_keys: Template keys to search each templates
    """
    for k, v in conf.get(templates_key, {}).iteritems():
        src = v.get("src", None)
        dst = v.get("dst", src)

        if src is None:
            logging.warn("%s lacks 'src' parameter" % k)
            continue

        if os.path.sep in src:
            logging.debug("Adding subdirs of source to template paths: " + src)
            srcdirs = [os.path.join(d, os.path.dirname(src)) for d in tmpldirs]
        else:
            srcdirs = tmpldirs

        # strip dir part as it will be searched from srcdir.
        src = os.path.basename(src)
        dst = os.path.join(workdir, dst)
        tpaths = srcdirs + [workdir]

        logging.info("Generating %s from %s [%s]" % (dst, src, k))
        logging.debug("Template path: " + ", ".join(tpaths))
        renderto(tpaths, conf, src, dst)

# vim:sw=4:ts=4:et:
