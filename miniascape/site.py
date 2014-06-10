#
# Copyright (C) 2013, 2014 Satoru SATOH <ssato@redhat.com>
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

import miniascape.globals as G
import miniascape.options as O
import miniascape.template as T
import miniascape.utils as U

import anyconfig
import os.path
import os
import sys


def gen_conf_files(conf, tmpldirs, workdir):
    """
    Generate site specific config files for host, networks and guests from a
    config file or some config files:

        .../src.d/[*.yml] -> .../{common,host,...}/**/*.yml

    :param conf: Object holding config parameters
    :param tmpldirs: Template path list
    :param workdir: Working top dir, e.g. miniascape-workdir-201303121
    """
    tpaths = [os.path.join(d, "config") for d in tmpldirs]
    outdir = os.path.join(workdir, conf.get("site", None))

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    logging.info("Generating site config files into %s" % outdir)

    common_conf = conf.get("common", {})
    common_conf["site"] = conf.get("site", "default")

    baseyml = "00_base.yml"  # Config file loaded first.

    anyconfig.dump(common_conf, os.path.join(outdir, "common", baseyml))
    anyconfig.dump(conf.get("host", {}),
                   os.path.join(outdir, "host.d", baseyml))

    for net in conf.get("networks"):
        netoutdir = os.path.join(outdir, "networks.d", net["name"])
        if not os.path.exists(netoutdir):
            os.makedirs(netoutdir)

        T.renderto(tpaths, net, "network.j2", os.path.join(netoutdir, baseyml))

    guests_key = "guests"
    for ggroup in conf.get("guests"):
        ggoutdir = os.path.join(outdir, "guests.d", ggroup["name"])
        if not os.path.exists(ggoutdir):
            os.makedirs(ggoutdir)

        ggroup_conf = dict()
        for k, v in ggroup.iteritems():
            if k != guests_key:
                ggroup_conf[k] = v

        anyconfig.dump(ggroup_conf, os.path.join(ggoutdir, baseyml))

        for guest in ggroup["guests"]:
            name = guest.get("name", guest.get("hostname", guest.get("fqdn")))
            goutdir = os.path.join(ggoutdir, name)
            if not os.path.exists(goutdir):
                os.makedirs(goutdir)

            anyconfig.dump(guest, os.path.join(goutdir, baseyml))


def option_parser():
    defaults = dict(force=False, **O.M_DEFAULTS)

    p = O.option_parser(defaults, "%prog [OPTION ...]")
    p.add_option("-f", "--force", action="store_true",
                 help="Force outputs even if these exist")
    return p


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    G.set_loglevel(options.verbose)
    options = O.tweak_options(options)

    if os.path.exists(options.workdir) and not options.force:
        yesno = raw_input(
            "Are you sure to re-generate configs in %s ? [y/n]: " %
            options.workdir
        )
        if not yesno.strip().lower().startswith('y'):
            print >> "Cancel re-generation of configs..."
            sys.exit(0)

    for ctxpath in options.ctxs:
        if os.path.isdir(ctxpath):
            confsrc = os.path.join(ctxpath, G.M_CONF_PATTERN)
        else:
            confsrc = ctxpath

        conf = anyconfig.load(confsrc)
        assert conf is not None, "No config loaded from: " + confsrc

    gen_conf_files(conf, options.tmpldir, options.workdir)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
