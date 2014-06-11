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
import miniascape.options
import miniascape.template
import miniascape.utils

import anyconfig
import os.path
import os
import sys


class EmptyConfigError(RuntimeError):
    pass


class NoNameGuestError(RuntimeError):
    pass


def load_site_ctxs(ctxs):
    """
    Load context (conf) files from ``ctxs``. ``ctxs`` may be a config file,
    glob pattern of config files or dir.

    :param ctxs: List of context file[s], glob pattern or dir :: [str]
    """
    conf = None
    for ctxpath in ctxs:
        if os.path.isdir(ctxpath):
            confsrc = os.path.join(ctxpath, G.M_CONF_PATTERN)
        else:
            if '*' in ctxpath and not miniascape.utils.sglob(ctxpath):
                continue

            elif not os.path.exists(ctxpath):
                logging.info("Not exist and skipped: " + ctxpath)
                continue

            confsrc = ctxpath

        if conf is None:
            conf = diff = anyconfig.load(confsrc)
        else:
            diff = anyconfig.load(confsrc)
            conf.update(diff)

        if not diff:
            logging.warn("No config loaded from: " + confsrc)

    if conf is None:
        raise EmptyConfigError("No config available from: " + ','.join(ctxs))

    return conf


def gen_site_conf_files(conf, tmpldirs, workdir):
    """
    Generate site specific config files for host, networks and guests from a
    config dict.

        conf :: dict -> .../{common,host,networks.d,guests}/**/*.yml

    :param conf: Object holding config parameters
    :param tmpldirs: Template path list
    :param workdir: Working top dir, e.g. miniascape-workdir-201303121

    :return: Configuration topdir where generated config files under
    """
    outdir = os.path.join(workdir, conf.get("site", G.M_SITE_DEFAULT))
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    logging.info("Generating site config files into %s" % outdir)
    baseyml = "00_base.yml"  # Config file loaded first.
    common_conf = conf.get("common", {})
    common_conf["site"] = conf.get("site", G.M_SITE_DEFAULT)

    for (cnf, subdir) in ((common_conf, "common"),
                          (conf.get("host", {}), "host.d")):
        anyconfig.dump(cnf, os.path.join(outdir, subdir, baseyml))

    # ex. /usr/share/miniascape/templates/config/
    tpaths = [os.path.join(d, "config") for d in tmpldirs]
    for net in conf.get("networks", []):
        noutdir = os.path.join(outdir, "networks.d", net["name"])
        miniascape.template.renderto(tpaths, net, "network.j2",
                                      os.path.join(noutdir, baseyml))

    guests_key = "guests"
    for ggroup in conf.get("guests", []):
        ggoutdir = os.path.join(outdir, "guests.d", ggroup["name"])
        if not os.path.exists(ggoutdir):
            os.makedirs(ggoutdir)

        ggroup_conf = dict()
        for k, v in ggroup.iteritems():
            if k != guests_key:
                ggroup_conf[k] = v

        anyconfig.dump(ggroup_conf, os.path.join(ggoutdir, baseyml))

        for guest in ggroup["guests"]:
            for k in ("name", "hostname", "fqdn"):
                name = guest.get(k, None)
                if name is not None:
                    break
            else:
                raise NoNameGuestError("Guest must have a name or hostname or "
                                       "fqdn: guest=" + str(guest))

            goutdir = os.path.join(ggoutdir, name)
            if not os.path.exists(goutdir):
                os.makedirs(goutdir)

            anyconfig.dump(guest, os.path.join(goutdir, baseyml))

    return outdir


def configure(ctxs, tmpldirs, workdir):
    """
    Generate site specific config files for host, networks and guests from a
    config file or some config files:

        .../[*.yml] -> .../{common,host,networks.d,guests}/**/*.yml

    :param ctxs: List of context (config) file[s], glob pattern of context
        (config) file[s] or dir to hold context (config) file[s] :: [str]
    :param tmpldirs: Template path list :: [str]
    :param workdir: Working top dir, e.g. miniascape-workdir-201303121 :: str

    :return: Configuration topdir where generated config files under
    """
    conf = load_site_ctxs(ctxs)
    return gen_site_conf_files(conf, tmpldirs, workdir)


def main(argv):
    p = miniascape.options.option_parser()
    (options, args) = p.parse_args(argv[1:])

    G.set_loglevel(options.verbose)
    options = miniascape.options.tweak_options(options)

    configure(options.ctxs, options.tmpldir, options.workdir)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
