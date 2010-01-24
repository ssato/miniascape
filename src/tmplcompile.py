#! /usr/bin/python
#
# tmplcompile.py - Cheetah based template compiler.
#
# Copyright (C) 2010 Satoru SATOH <satoru.satoh at gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
import optparse
import os.path
import sys
import yaml  # PyYAML

from Cheetah.Template import Template


def compile(template_path, params, output_f):
    tmpl = Template(file=template_path, searchList=params)
    output_f.write(tmpl.respond())


def load_config(config_path):
    return yaml.load(open(config_path, 'r'))


def show_examples(args=sys.argv):
    es = """
Examples:

  %(prog)s -t test.tmpl -o test.out test.yml
  %(prog)s test.yml > test.out  # same as above
  %(prog)s -t templates/test2.tmpl -o out/config.dat config/config.yml
    """ % {'prog': args[0]}
    print >> sys.stderr, es


def main():
    output = sys.stdout

    parser = optparse.OptionParser(usage='%prog [OPTION ...] CONFIG_FILE_PATH')
    parser.add_option("-t", "--template", dest="template",
        help="Template filename. [Default: <basename of config_file> + '.tmpl']")
    parser.add_option("-o", "--output", dest="output",
        help="Output filename [Default: stdout]")

    (options, args) = parser.parse_args()

    if options.output:
        output = sys.stdout

    if len(args) < 1:
        parser.print_help()
        show_examples()
        sys.exit(-1)
    
    config_file = args[0]

    if options.template:
        tmpl = options.template
    else:
        tmpl = os.path.splitext(config_file)[0] + '.tmpl'

    configs = dict()
    configs['template_file'] = tmpl

    # Ex. '/path/to/distros.yml' -> 'distros',
    # '/path/to/configs/distros' -> 'distros'.
    category = os.path.splitext(os.path.basename(config_file))[0]

    configs[category] = load_config(config_file)

    compile(tmpl, configs, output)


if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:et:
