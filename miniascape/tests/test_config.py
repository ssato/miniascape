import ConfigParser as configparser
import nose

from miniascape.config import *
from tests.globals import TEST_CONFIG_FILE



def compare_co_with_config_parser_obj(config_path, co):
    """
    @config_path  config file path
    @c            config obj.
    """
    cp = configparser.SafeConfigParser()
    cp.read(config_path)

    for s in cp.sections():
        for k,v in cp.items(s):
            assert co[s][k] == v, "co[%s][%s]=%s vs. v=%s" % (s, k, co[s][k], v)
            assert getattr(getattr(co, s), k) == v, "getattr(getattr(co=%s vs. v=%s" % (getattr(getattr(co, s), k), v)


# tests:
def test_Config():
    c = Config()

    assert isinstance(c, ODict)
    assert isinstance(c, Config)


def test_Config_load():
    global TEST_CONFIG_FILE

    c = Config()
    c.load(TEST_CONFIG_FILE)

    compare_co_with_config_parser_obj(TEST_CONFIG_FILE, c)


def test_getInstance_with_path():
    global TEST_CONFIG_FILE

    c = getInstance(TEST_CONFIG_FILE)
    compare_co_with_config_parser_obj(TEST_CONFIG_FILE, c)


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:
