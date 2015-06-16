#! /usr/bin/python -tt
from __future__ import print_function

import anyconfig
import anytemplate
import jinja2
import jinja2.ext
import sys


_JINJA2_EXTS = [jinja2.ext.do, jinja2.ext.with_, jinja2.ext.loopcontrols,
                jinja2.ext.i18n]


def main(argv=sys.argv):
    if len(argv) < 5:
        print("Usage: %s TEMPLATE_FILE CONTEXT_FILE OUTPUT_FILE TPATHS" % argv[0])
        sys.exit(-1)

    (template, context_f, output, paths) = argv[1:5]
    tpaths = paths.split(':')
    context = anyconfig.load(context_f)

    anytemplate.render_to(template, context, output, at_paths=tpaths,
                          at_engine="jinja2", at_ask_missing=True,
                          extensions=_JINJA2_EXTS)

if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
