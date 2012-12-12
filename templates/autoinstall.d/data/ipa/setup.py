#! /usr/bin/python -tt
#
# Unattended IPA setup script written by Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import sys
import getpass
import logging
import pexpect
import subprocess


def ipa_server_install(password, fqdn, realm=None):
    if realm is None:
        realm = fqdn[fqdn.find('.')+1:]

    c = "ipa-server-install -a %s -p %s -r %s --hostname=%s -U" % \
        (password, password, realm, fqdn)

    logging.info(c)
    return subprocess.Popen(c, shell=True)


def ipa_user_add(firstname="John", lastname="Doe", username, password):
    cmd = "ipa user-add --first='%s' --last='%s' --password %s" % \
        (firstname, lastname, username)

    c = pexpect.spawn(cmd)
    c.expect("Password:")
    c.sendline(password)
    c.expect("Enter Password again to verify:")
    c.sendline(password)
    c.close()

    c = pexpect.spawn("kinit %s" % username)
    c.expect("Password for .*:")
    c.sendline(password)
    #c.expect("Password expired.  You must change it now.")
    c.expect(".*Enter new password:")
    c.sendline(password)
    c.expect("Enter it again:")
    c.sendline(password)
    c.close()

    return subprocess.Popen("ipa user-find --login " + username, shell=True)


def main(password, fqdn):
    c = pexpect.spawn("kinit admin")
    c.expect("Password for .*:")
    c.sendline(password)
    c.close()


# vim:sw=4:ts=4:et:
