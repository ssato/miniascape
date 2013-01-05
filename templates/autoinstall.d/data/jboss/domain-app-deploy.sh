#! /bin/bash
#
# Jboss-cli wrapper script to deploy JBoss apps.
#
set -e
set -x

show_usage () {
  cat << EOF
Usage: $0 APP_ARCHIVE_PATH [SERVER_GROUP_0,SERVER_GROUP_1,...]

  where APP_ARCHIVE_PATH = JBoss application archive to deploy
        SERVER_GROUP_<N> = Server groups to deploy \$APP_ARCHIVE_PATH

Examples:

  \$ $0 sample-ee.war server_group_1,server_group_2
  \$ $0 sample-ee.ear  # Deploy to all server groups
EOF
  exit 0
}

jboss_cli_wrappr="/usr/share/jbossas/bin/jboss-cli.sh --connect --controller={{ ip }}:9999 --user={{ jboss.domain.user }} --password={{ jboss.domain.secret.plain }}"

$jboss_cli_wrappr --command="version" > /dev/null || abort=1
if test "x$abort" = "x1"; then
  echo "[Warn] Something goes wrong with jboss-cli. Check your configuration."
  exit 1
fi

if test $# -ge 1; then
  archive=$1; shift
  test $# -ge 1 && opt_groups="--server-groups $@" || opt_groups="--all-server-groups"

  $jboss_cli_wrappr --command="deploy $archive $opt_groups"
else
  show_usage
fi

# vim:sw=2:ts=2:et:
