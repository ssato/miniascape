#! /usr/bin/python
#
# Copyright (C) 2013 Red Hat, Inc.
# Copyright (C) 2013 Satoru SATOH <ssato@redhat.com>
# 
# License: Apache License 2.0
# 
# Reference. qpid-cluster in qpid-tools
#
"""Example session:
::

    [root@rhel-5-mrg-m-1 ~]# ./qpidd_cluster_check.py -h
    usage: Usage: qpidd_cluster_check.py [Options...]

    options:
      -h, --help            show this help message and exit
      -A, --active          Only list active clusters [False]
      -N NAME, --name=NAME  Specify cluster name to show
      --expected-nnodes=EXPECTED_NNODES
                            Do not show stats and only check if the number of
                            nodes of specified cluster (with --name option)
                            matches expected number of nodes.
      -v, --verbose         Verbose mode [False]
      -D, --debug           Debug mode [False]
    [root@rhel-5-mrg-m-1 ~]# ./qpidd_cluster_check.py -v 
    Cluster 'mrgm_cluster' [ACTIVE]:
      amqp:tcp:192.168.155.71:5672
      amqp:tcp:192.168.155.72:5672
    [root@rhel-5-mrg-m-1 ~]# ./qpidd_cluster_check.py -v -N mrgm_cluster 
    Cluster 'mrgm_cluster' [ACTIVE]:
      amqp:tcp:192.168.155.71:5672
      amqp:tcp:192.168.155.72:5672
    [root@rhel-5-mrg-m-1 ~]# ./qpidd_cluster_check.py -v -N mrgm_cluster --expected-nnodes=2; echo $?
    ['amqp:tcp:192.168.155.71:5672', 'amqp:tcp:192.168.155.72:5672']
    0
    [root@rhel-5-mrg-m-1 ~]#

see also: https://cwiki.apache.org/qpid/qpid-management-framework.html
"""
import qmf.console as QC
import logging
import optparse
import sys


_DEFAULTS = dict(active=False,
                 name=None,
                 expected_nnodes=0,
                 verbose=False, 
		 debug=False, )


def get_clusters():
    """
    :return: [Clusters { clusterName, status, members }]
    """
    try:
        session = QC.Session()
    except:
        logging.error("Could not get QMF Console Session object.")
        sys.exit(-1)

    broker = session.addBroker()
    agents = session.getAgents()

    return session.getObjects(_class="cluster", _agent=agents[0])


def option_parser(defaults=_DEFAULTS, usage="Usage: %prog [Options...]"):
    p = optparse.OptionParser(usage)
    p.set_defaults(**defaults)

    p.add_option("-A", "--active", action="store_true",
                 help="Only list active clusters [%default]")
    p.add_option("-N", "--name", help="Specify cluster name to show")
    p.add_option("", "--expected-nnodes", type="int",
                 help="Do not show stats and only check if the number of "
                      "nodes of specified cluster (with --name option) "
                      "matches expected number of nodes.")
    p.add_option("-v", "--verbose", action="store_true", 
                 help="Verbose mode [%default]")
    p.add_option("-D", "--debug", action="store_true", 
                 help="Debug mode [%default]")

    return p


def main():
    p = option_parser()
    (options, args) = p.parse_args()

    if options.expected_nnodes > 0 and not options.name:
        print >> sys.stderr, "--expected-nnodes option requires --name option"
        sys.exit(-1)

    if options.verbose:
        logging.basicConfig(level=logging.INFO)
    elif options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)

    clusters = get_clusters()

    if options.active:
        clusters = [c for c in clusters if c.status == "ACTIVE"]

    if options.expected_nnodes:
        cs = [c for c in clusters if c.clusterName == options.name]
        if not cs:
            print >> sys.stderr, "Cluster '%s' not found." % options.name
            sys.exit(-1)

        cluster = cs[0]

        nodes = cluster.members.split(';')
        logging.debug("Nodes of cluster '%s': %s" % \
                      (cluster.clusterName, ", ".join(nodes)))
        if len(nodes) == options.expected_nnodes:
	    	print nodes
	    	sys.exit(0)
        else:
	    	sys.exit(1)

    else:
        for c in clusters:
            print "Cluster '%s' [%s]:" % (c.clusterName, c.status)
            for m in c.members.split(';'):
                print "  " + m

    
if __name__ == '__main__':
    main()

# vim:sw=4:ts=4:et:

