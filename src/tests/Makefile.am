python_test_scripts = \
test_hosts_update.py \
test_netxml_del_dhcp.py \
test_netconf_gen.py \
test_package.py \
test_repackage.py

EXTRA_DIST = $(python_test_scripts) rhel-5-4-guest-1.xml

TESTS_ENVIRONMENT = NOSE_VERBOSE=3 @PYTHON@
TESTS = $(python_test_scripts)
