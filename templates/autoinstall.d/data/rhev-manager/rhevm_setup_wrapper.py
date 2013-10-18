#! /usr/bin/python -tt
# Simple wrapper script to automate the interactive session of rhevm-dwh-setup
# and rhevm-reports-setup.
#
# @see http://red.ht/1hVK5sx and http://red.ht/16M1nXQ
#
# Copyright (C) 2013 Red Hat, Inc.
# License: MIT
#
import getpass
import optparse
import pexpect
import sys


_DWH_CMD = "rhevm-dwh-setup"
_REPORT_CMD = "rhevm-reports-setup"

_USAGE = """%prog [Options] COMMAND

Commands:
  d[wh]      Run rhevm-dwh-setup to setup RHEV-M History Database
  r[eports]  Run rhevm-reports-setup to setup RHEV-M Reports
  a[ll]      Run both rhevm-dwh-setup and rhevm-reports-setup
"""


def ask_password(postfix=""):
    return getpass.getpass("Enter password%s: " % postfix)


def start_setup_session(setup_cmd=_DWH_CMD, password=None):
    if password is None:
        password = ask_password(" for " + setup_cmd)

    child = pexpect.spawn(setup_cmd)

    if setup_cmd == _REPORT_CMD:
        idx = child.expect(["Exporting current users....*",
                            ".*\? \(yes\|no\): "])
        if idx == 0:
            logging.info("Setup already done.")

        elif idx == 1:
            child.sendline("yes")
            child.expect(".* a password for the admin users .*: ")
            child.sendline(password)
    else:
        child.expect(".*\? \(yes\|no\): ")
        child.sendline("yes")

    if child.isalive():
        child.close()


def option_parser(usage=_USAGE):
    p = optparse.OptionParser(usage)
    p.set_defaults(password=None)
    p.add_option("-p", "--password", help="Specify password [not set]")
    return p


def main(argv=sys.argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    if not args or args[0] != 'a':
        p.print_usage()
        sys.exit()

    if args[0] == 'd':
        start_setup_session(_DWH_CMD, options.password)

    elif args[0] == 'r':
        start_setup_session(_REPORT_CMD, options.password)

    elif args[0] == 'a':
        # Try asking once if password is not given:
        if options.password is None:
            options.password = ask_password()

        start_setup_session(_DWH_CMD, options.password)
        start_setup_session(_REPORT_CMD, options.password)

    else:
        print >> sys.stderr, "Invalid command: " + args
        p.print_usage()
        sys.exit(-1)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
