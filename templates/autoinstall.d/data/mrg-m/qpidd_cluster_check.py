#! /usr/bin/python

"""
see: https://cwiki.apache.org/qpid/qpid-management-framework.html


>>> from qmf.console import Session
>>> 
>>> sess = Session()
>>> broker = sess.addBroker()
>>> agents = sess.getAgents()
>>> print len(agents)
2
>>> clusters = sess.getObjects(_class="cluster", _agent=agents[0])
>>> print len(clusters)
1
>>> print clusters[0]
org.apache.qpid.cluster:cluster[0-66-1-0-org.apache.qpid.cluster:cluster:org.apache.qpid.broker:broker:amqp-broker] org.apache.qpid.cluster:cluster:org.apache.qpid.broker:broker:amqp-broker
>>> print clusters[0].clusterName
amqp_local_cluster
>>> print clusters[0].status
ACTIVE
>>> print clusters[0].members
amqp:tcp:192.168.122.13:5671;amqp:tcp:192.168.122.13:5672
>>> 
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

