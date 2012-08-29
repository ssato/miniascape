"""

:copyright: (c) 2012 by Satoru SATOH <ssato@redhat.com>
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

 Requirements: python-jinja2-cui
"""
import jinja2_cui.cui as C

import codecs
import jinja2
import locale
import logging
import optparse
import os.path
import sys
import yaml

from itertools import chain, groupby
from logging import DEBUG, INFO
from operator import itemgetter


try:
    chain_from_iterable = chain.from_iterable
except AttributeError:
    # Borrowed from library doc, 9.7.1 Itertools functions:
    def _from_iterable(iterables):
        for it in iterables:
            for element in it:
                yield element

    chain_from_iterable = _from_iterable


_ENCODING = locale.getdefaultlocale()[1]
_NETWORK_TEMPLATE = """
name: {{ name }}
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
_NETWORK_XML_TEMPLATE = """
<network>
  <name>{{ name }}</name>
  {% if mode in ('nat', 'bridge') -%}<forward mode='{{ mode }}'/>{%- endif %}
  <bridge name='{{ bridge }}' stp='on' delay='0' />
  {% if domain is defined -%}<domain name='{{ domain }}'/>{%- endif %}
  <dns>
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


def render_s(ctx, tmpl_s=_NETWORK_TEMPLATE):
    """
    :param ctx: Context to instantiate `tmpl_s`
    :param tmpl_s: Template string


    >>> render_s('a = {{ a }}, b = "{{ b }}"', {'a': 1, 'b': 'bbb'})
    'a = 1, b = "bbb"'
    """
    return jinja2.Environment().from_string(tmpl_s).render(**ctx)


def load_network_configs(netconfs):
    """
    Load configuration files for a network
    """
    return C.parse_and_load_contexts(netconfs, _ENCODING, False)


def aggregate(filepaths):
    """
    Aggregate host configurations from each host interface data and return the
    list of host list by each network.
    """
    guests = [C.load_context(f) for f in filepaths]
    hostsets = [
        list(g) for k, g in groupby(
            concat(g["interfaces"] for g in guests), itemgetter("network")
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
        netconf=[],
        guestconf=[],
        output=None,
        xml=False,
        debug=False
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
    result = render_s(ctx, tmpl)

    if options.output and not options.output == '-':
        C.open(options.output, 'w').write(result)
    else:
        codecs.getwriter(_ENCODING)(sys.stdout).write(result)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
