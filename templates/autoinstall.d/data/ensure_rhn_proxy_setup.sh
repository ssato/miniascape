#! /bin/bash
set -e

proxy_server={{ proxy.server }}
proxy_user={{ proxy.user|default('') }}
proxy_password={{ proxy.password|default('') }}

# pre-check:
if test "x${proxy_server}" = "x"; then
    echo "Proxy server (and port) were not given. Exiting..." 
    exit 0
fi

# main:
cfg=/etc/sysconfig/rhn/up2date
test -f ${cfg:?}

sed_cmds=""

set -x

grep -E '^enableProxy=1' ${cfg} || sed_cmds="s/^enableProxy=.*/enableProxy=1/g"
grep -E "^httpProxy=${proxy_server}" ${cfg} || \
    sed_cmds="${sed_cmds}; s/^httpProxy=.*/=${proxy_server}/g"

if test "x${proxy_user}" = "x"; then
    echo "No need to set proxy user"
else
    grep -E "^proxyUser=${proxy_user}" ${cfg} || \
        sed_cmds="${sed_cmds}; s/^proxyUser=.*/=${proxy_user}/g"
fi

if test "x${proxy_password}" = "x"; then
    echo "No need to set proxy password"
else
    grep -E "^proxyPassword=${proxy_password}" ${cfg} || \
        sed_cmds="${sed_cmds}; s/^proxyPassword=.*/=${proxy_password}/g"
fi

test -f ${cfg}.save || cp -a ${cfg} ${cfg}.save
sed -i -r "${sed_cmds}" ${cfg}

# vim:sw=4:ts=4:et:
