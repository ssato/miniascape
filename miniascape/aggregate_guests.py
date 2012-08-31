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
import miniascape.utils as U
import jinja2_cui.render as R

import codecs
import locale
import logging
import optparse
import os.path
import sys

from itertools import groupby
from logging import DEBUG, INFO
from operator import itemgetter


_ENCODING = locale.getdefaultlocale()[1]
_NETWORK_TEMPLATE = """name: {{ name }}
bridge: {{ bridge }}
gateway: {{ gateway }}
netmask: {{ netmask }}
dhcp:
  start: {{ dhcp.start }}
  end: {{ dhcp.end }}
hosts:
{% for h in hosts %}  - { fqdn: {{ h.fqdn }}, host: {{ h.host }}, ip: {{ h.ip }}, mac: "{{ h.mac }}" }
{% endfor %}
"""
_NETWORK_XML_TEMPLATE = """<network>
  <name>{{ name }}</name>
  {% if mode in ('nat', 'bridge') -%}<forward mode='{{ mode }}'/>{%- endif %}
  <bridge name='{{ bridge }}' stp='on' delay='0' />
  {% if domain is defined -%}<domain name='{{ domain }}'/>{%- endif %}
  <dns>
    <!-- KVM host aliases: -->
    <host ip='{{ gateway }}'><hostname>gw.{{ domain }}</hostname></host>
    <host ip='{{ gateway }}'><hostname>ks.{{ domain }}</hostname></host>
{% for h in hosts %}    <host ip='{{ h.ip }}'><hostname>{{ h.fqdn }}</hostname></host>
{% endfor %}  </dns>
  <ip address='{{ gateway }}' netmask='{{ netmask }}'>
{% if dhcp is defined %}    <dhcp>
      <range start='{{ dhcp.start }}' end='{{ dhcp.end }}'/>
{% for h in hosts %}      <host mac='{{ h.mac }}' {% if h.fqdn is defined %}name='{{ h.fqdn }}'{% endif %} ip='{{ h.ip }}'/>
{% endfor %}    </dhcp>{% endif %}
  </ip>
</network>

"""


def load_network_configs(netconfs):
    """
    Load configuration files for a network
    """
    return R.parse_and_load_contexts(netconfs, _ENCODING, False)


def aggregate(filepaths):
    """
    Aggregate host configurations from each host interface data and return the
    list of host list by each network.
    """
    guests = [R.load_context(f) for f in filepaths]
    hostsets = [
        list(g) for k, g in groupby(
            U.concat(g["interfaces"] for g in guests), itemgetter("network")
        )
    ]
    return hostsets


def load_configs(netconfs, guestconfs):
    netctx = load_network_configs(netconfs)
    hostsets = aggregate(guestconfs)

    hss = [hs for hs in hostsets if hs and hs[0]["network"] == netctx["name"]]
    if hss:
        netctx["hosts"] = hss[0]

    return netctx


def option_parser():
    defaults = dict(
        netconf=[], guestconf=[], output=None, xml=False, debug=False
    )

    p = optparse.OptionParser("%prog [OPTION ...]")
    p.set_defaults(**defaults)

    p.add_option("-N", "--netconf", action="append",
        help="Specify network configuration file[s]"
    )
    p.add_option("-G", "--guestconf", action="append",
        help="Specify guest configuration files one by one"
            "e.g. -C host-a.yml -C host-b.yml ..."
    )
    p.add_option("-o", "--output", help="Output filename [stdout]")
    p.add_option("-X", "--xml", action="store_true",
        help="Output libvirt network XML file instead of conf file"
    )
    p.add_option("-D", "--debug", action="store_true", help="Debug mode")

    return p


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    logging.getLogger().setLevel(DEBUG if options.debug else INFO)

    tmpl = _NETWORK_XML_TEMPLATE if options.xml else _NETWORK_TEMPLATE
    ctx = load_configs(options.netconf, options.guestconf)
    result = R.render_s(tmpl, ctx)

    if options.output and not options.output == '-':
        R.open(options.output, 'w').write(result)
    else:
        codecs.getwriter(_ENCODING)(sys.stdout).write(result)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
