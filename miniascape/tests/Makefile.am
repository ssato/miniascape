python_test_scripts = \
test_globals.py \
test_config.py \
test_pack.py \
test_tools.py \
test_utils.py \
test_virt.py \
$(NULL)

EXTRA_DIST = $(python_test_scripts) __init__.py virtinst.tmpl.out net-1.yaml net-1.xml config.in

if ENABLE_TESTS
TESTS_ENVIRONMENT = NOSE_VERBOSE=3 NOSE_WITH_DOCTEST=1 \
	HOME=$(abs_top_builddir) PYTHONPATH=$(abs_top_builddir) $(PYTHON)
TESTS = $(python_test_scripts)
endif
