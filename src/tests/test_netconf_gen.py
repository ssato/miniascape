import glob
import nose
import os
import sys
import shutil
import tempfile

try:
    import xml.etree.ElementTree as ET  # python >= 2.5
except ImportError:
    import elementtree.ElementTree as ET  # python <= 2.4; needs ElementTree.

from nose.tools import with_setup

sys.path.append('../')
import netconf_gen as netconf


WORKDIR = None

NETXML_SRC = 'net-1.xml'
NETXML_0 = None

DNSMASQ_NET_CONF = 'net-1.conf'
DNSMASQ_NET_HOSTSFILE = 'net-1.hostsfile'


def setup():
    global WORKDIR, NETXML_SRC, NETXML_0

    WORKDIR = tempfile.mkdtemp(dir=os.curdir)
    shutil.copy2(NETXML_SRC, WORKDIR)
    shutil.copy2(DNSMASQ_NET_CONF, WORKDIR)
    shutil.copy2(DNSMASQ_NET_HOSTSFILE, WORKDIR)

    NETXML_0 = os.path.join(WORKDIR, os.path.basename(NETXML_SRC))


def teardown():
    global WORKDIR

    [os.remove(f) for f in glob.glob("%s/*" % WORKDIR)]

    if os.path.exists(WORKDIR):
        os.rmdir(WORKDIR)


@with_setup(setup, teardown)
def test_LibvirtNetworkConf_new():
    global NETXML_0
    netxml = NETXML_0

    nconf = netconf.LibvirtNetworkConf(netxml)
    tree = ET.parse(netxml)

    assert nconf['name'] == tree.find('name').text
    assert nconf['listen-address'] == tree.find('ip').attrib.get('address')

    elem = tree.find('domain')
    if elem is not None:
        assert nconf['domain'] == elem.attrib.get('name')

    elem = tree.find('ip/dhcp/range')
    if elem is not None:
        assert nconf['dhcp-range'] == (elem.attrib.get('start'), elem.attrib.get('end'))

    elems = tree.findall('ip/dhcp/host')
    if elems is not None:
        hs = [{'ip': elem.attrib.get('ip'), 'mac': elem.attrib.get('mac'), \
            'name': elem.attrib.get('name')} for elem in elems]

        rhs = nconf['hosts']

        for h in hs:
            assert h in rhs, "NOT found: mac = %(mac)s, ip = %(ip)s, hostname = %(name)s" % h


@with_setup(setup, teardown)
def test_DnsmasqConf():
    global NETXML_0
    global DNSMASQ_NET_CONF, DNSMASQ_NET_HOSTSFILE
    netxml = NETXML_0

    nconf = netconf.LibvirtNetworkConf(netxml)
    dnsmasqconf = netconf.DnsmasqConf(netxml)

    ref_conf_data = open(DNSMASQ_NET_CONF).read()
    ref_hostsfile_data = open(DNSMASQ_NET_HOSTSFILE).read()

    (conf_data, hostsfile_data) = dnsmasqconf.format()

    assert ref_conf_data == conf_data, "\n\nref:\n'%s'\n\ndnsmasqconf:\n'%s'\n" % \
        (ref_conf_data, conf_data)

    assert ref_hostsfile_data == hostsfile_data, "\n\nref:\n'%s'\n\ndnsmasqhostsfile:\n'%s'\n" % \
        (ref_hostsfile_data, hostsfile_data)


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:
