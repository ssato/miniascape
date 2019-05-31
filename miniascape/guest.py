#
# Copyright (C) 2012 Satoru SATOH <ssato redhat.com>
# Copyright (C) 2014 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato redhat.com>
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
from __future__ import print_function
from miniascape.globals import LOGGER as logging

import itertools
import glob
import os.path
import os
import subprocess
import sys

import miniascape.config
import miniascape.globals as G
import miniascape.options
import miniascape.template


_AUTOINST_SUBDIR = "autoinstall.d"


def _workdir(topdir, name, subdir=G.M_GUESTS_CONF_SUBDIR):
    """
    :param topdir: Working top dir
    :param name: Guest's name
    :return: Guest's working (output) directory
    """
    return os.path.join(topdir, subdir, name)


def _guests_workdir(topdir, subdir=G.M_GUESTS_CONF_SUBDIR):
    """
    :param topdir: Working top dir
    :return: Guest's working (output) directory
    """
    return os.path.join(topdir, subdir)


def _find_templates_from_glob_path(tmpl, gtmpldirs):
    """Find templates from global path such as 'data/*/*.sh".

    :return: A generator yields (template_rel_path, template_dir)
    """
    for prefix in gtmpldirs:
        srcs = [f for f in glob.glob(os.path.join(prefix, tmpl))
                if os.path.isfile(f)]
        if not srcs:
            continue

        for src in srcs:
            yield (src.replace(prefix, '')[1:], prefix)
        break


def _template_paths_itr(tmpl, gtmpldirs):
    """compute template search paths from template path.

    This is an iterator version yields it one by one.
    """
    tmpldir = os.path.dirname(tmpl)
    for prefix in gtmpldirs:
        tdir = os.path.join(prefix, tmpldir)
        if os.path.isdir(tdir):
            yield tdir


def _template_paths(tmpl, gtmpldirs):
    """compute template search paths from template path, etc."""
    return gtmpldirs + list(_template_paths_itr(tmpl, gtmpldirs))


def _render_template(tmpl, config, gworkdir, tpaths, dest=None):
    """
    """
    if dest is None:
        dest = tmpl

    out = os.path.join(gworkdir, "setup", dest)
    logging.debug("Generating %s from %s", out, tmpl)
    miniascape.template.render_to(tmpl, config, out, tpaths)


def arrange_setup_data(gtmpldirs, config, gworkdir, glob_marker='*'):
    """
    Arrange setup data to be embedded in kickstart files.

    :param gtmpldirs: Guest's template dirs :: [path]
    :param config: Guest's config :: dict
    :param gworkdir: Guest's workdir
    """
    tmpls = config.get("setup_data", [])
    if not tmpls:
        return  # Nothing to do.

    for t in tmpls:
        src = t.get("src", None)
        content = t.get("content", None)

        if content is None:
            assert src is not None, "'src' must not be empty if content isn't!"

            if glob_marker in src:
                for src_, sdir in _find_templates_from_glob_path(src,
                                                                 gtmpldirs):
                    tpaths = _template_paths(src_, [sdir])
                    _render_template(src_, config, gworkdir, tpaths)
            else:
                dst = t.get("dst", src)
                tpaths = _template_paths(src, gtmpldirs)
                _render_template(src, config, gworkdir, tpaths, dst)
        else:
            dst = t.get("dst", None)
            assert dst is not None, "'dst' must be given if content is set!"

            out = os.path.join(gworkdir, "setup", dst)
            tpaths = gtmpldirs + [os.path.dirname(out)]

            logging.debug("Generating %s from given content and paths: %s",
                          out, ','.join(tpaths))
            miniascape.template.renders_to(content, config, out, tpaths)

    return subprocess.check_output(
        "tar --xz --owner=root --group=root -c setup | base64 > "
        "setup.tar.xz.base64",
        shell=True, cwd=gworkdir
    )


def gen_guest_files(name, conffiles, tmpldirs, workdir,
                    subdir=_AUTOINST_SUBDIR):
    """
    Generate files (vmbuild.sh and ks.cfg) to build VM `name`.

    :param name: Guest's name
    :param conffiles: ConfFiles object
    :param tmpldirs: Template dirs :: [path]
    :param workdir: Working top dir
    """
    logging.info("Generating files for: %s", name)

    conf = conffiles.load_guest_confs(name)
    gtmpldirs = [os.path.join(d, subdir) for d in tmpldirs]

    if not os.path.exists(workdir):
        logging.debug("Creating working dir: %s", workdir)
        os.makedirs(workdir)

    logging.debug("Generating setup data: %s", name)
    arrange_setup_data(gtmpldirs, conf, workdir)
    miniascape.template.compile_conf_templates(conf, tmpldirs, workdir,
                                               "templates")


def show_vm_names(conffiles):
    """
    :param conffiles: config.ConfFiles object
    """
    print("\nAvailable VMs: " + ", ".join(conffiles.list_guest_names()))


_DISTDATA_MAKEFILE_AM_TMPL = """pkgdata%(i)ddir = %(dir)s
dist_pkgdata%(i)d_DATA = \
$(shell for f in %(files)s; do test -f $$f && echo $$f; done)
"""


def mk_distdata_g(guests, tmpl=_DISTDATA_MAKEFILE_AM_TMPL,
                  datadir=G.M_GUESTS_BUILDDATA_TOPDIR):
    """
    Make up distdata snippet in Makefile.am to package files to build guests.
    """
    # pylint: disable=no-member
    ig = itertools.count()
    fs = ["ks.cfg", "net_register.sh", "vmbuild.sh"]  # FIXME: Ugly!

    for name in guests:
        files = ' '.join(os.path.join(name, f) for f in fs)
        for idx in ig:
            yield tmpl % dict(i=idx, dir=os.path.join(datadir, name),
                              files=files)


def gen_all(cf, tmpldirs, workdir):
    """
    Generate files to build VM for all VMs.

    :param conffiles: config.ConfFiles object
    :param tmpldirs: Template dirs :: [path]
    :param workdir: Working top dir
    """
    guests = cf.list_guest_names()

    for name in guests:
        gen_guest_files(name, cf, tmpldirs, _workdir(workdir, name))

    conf = cf.load_host_confs()
    conf["guests_build_datadir"] = G.M_GUESTS_BUILDDATA_TOPDIR
    conf["timestamp"] = G.timestamp()
    conf["distdata"] = list(mk_distdata_g(guests))

    logging.debug("Generating common aux files...")
    miniascape.template.compile_conf_templates(conf, tmpldirs,
                                               _guests_workdir(workdir),
                                               "guests_templates")


def option_parser():
    defaults = dict(genall=False, confdir=G.site_confdir(),
                    **miniascape.options.M_DEFAULTS)

    p = miniascape.options.option_parser(defaults,
                                         "%prog [OPTION ...] [GUEST_NAME]")
    p.add_option("-A", "--genall", action="store_true",
                 help="Generate configs for all guests")
    p.add_option("-c", "--confdir",
                 help="Top dir to hold site configuration files or "
                      "configuration file [%default]")
    return p


def main(argv=sys.argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    G.set_loglevel(options.verbose)
    options = miniascape.options.tweak_options(options)

    cf = miniascape.config.ConfFiles(options.confdir)

    if not args and not options.genall:
        p.print_help()
        show_vm_names(cf)
        sys.exit(0)

    if options.genall:
        gen_all(cf, options.tmpldir, options.workdir)
    else:
        name = args[0]
        gen_guest_files(name, cf, options.tmpldir,
                        _workdir(options.workdir, name))


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
