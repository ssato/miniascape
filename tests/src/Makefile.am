python_test_scripts = \
test_hosts_update.py \
test_netxml_del_dhcp.py \
test_netconf_gen.py \
test_package.py

EXTRA_DIST = $(python_test_scripts) \
globals.py.in hosts \
net-1.conf net-1.hostsfile net-1.xml \
test-domain-1.xml

TESTS_ENVIRONMENT = NOSE_VERBOSE=3 \
	PYTHONPATH=@abs_top_builddir@/src @PYTHON@
TESTS = $(python_test_scripts)
