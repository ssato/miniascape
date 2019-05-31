#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato@redhat.com>
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
import anytemplate
import anytemplate.utils
import jinja2.ext
import os.path

from miniascape.globals import LOGGER as logging


_JINJA2_EXTS = [jinja2.ext.do, jinja2.ext.with_, jinja2.ext.loopcontrols,
                jinja2.ext.i18n]


def renders_to(template, context=None, output=None, at_paths=None):
    """
    :param template: Template content string
    :param context: A dict or dict-like object to instantiate given
        template file
    :param output: File path to write the rendered result string to or None/'-'
        to print it to stdout
    :param at_paths: Template search paths
    """
    res = anytemplate.renders(template, context, at_paths=at_paths,
                              at_engine="jinja2", at_ask_missing=True,
                              extensions=_JINJA2_EXTS)
    anytemplate.utils.write_to_output(res, output)


def render_to(template, context=None, output=None, tpaths=None):
    """
    :param template: Template file path
    :param context: A dict or dict-like object to instantiate given
        template file
    :param output: File path to write the rendered result string to or None/'-'
        to print it to stdout
    :param tpaths: Template search paths
    """
    anytemplate.render_to(template, context, output, at_paths=tpaths,
                          at_engine="jinja2", at_ask_missing=True,
                          extensions=_JINJA2_EXTS)


def compile_conf_templates(conf, tmpldirs, workdir, templates_key="templates"):
    """
    Compile template config files.

    :param conf: Config object holding templates info
    :param tmpldirs: Template paths
    :param workdir: Working dir
    :param template_keys: Template keys to search each templates
    """
    for k, v in conf.get(templates_key, {}).items():
        src = v.get("src", None)
        dst = v.get("dst", src)

        if src is None:
            logging.warn("{} lacks 'src' parameter".format(k))
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

        logging.debug("Generating {} from {} [{}]".format(dst, src, k))
        logging.debug("Template path: " + ", ".join(tpaths))
        anytemplate.render_to(src, conf, dst, at_paths=tpaths,
                              at_engine="jinja2")

# vim:sw=4:ts=4:et:
