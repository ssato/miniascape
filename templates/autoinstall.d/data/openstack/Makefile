# Makefile to install and setup OpenStack (RDO).
# 
# see also:
# * http://openstack.redhat.com/Neutron-Quickstart
# * http://openstack.redhat.com/Running_an_instance_with_Neutron
# 
WORKDIR ?= /root/setup


install:
	yum install -y http://rdo.fedorapeople.org/openstack-havana/rdo-release-havana.rpm
	yum install -y openstack-packstack
	reboot

setup:
	packstack --allinone

#source /root/keystonerc_demo && \
#	  neutron security-group-rule-create --protocol icmp --direction ingress default && \
#	  neutron security-group-rule-create --protocol tcp --port-range-min 22 --port-range-max 22 --direction ingress default


.PHONY: setup
