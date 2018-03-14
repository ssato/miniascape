#! /bin/bash
set -e
verbose=1

while getopts "sh" opt
do
  case $opt in
    s) verbose=0 ;;
    \?) echo "Usage: $0 [-s[ilent]] [PULP_RPMS_DIR]"
        exit 0
        ;;
  esac
done
shift $(($OPTIND - 1))
pulp_rpmsdir=${1:-/var/lib/pulp/content/rpm/}

vecho () {
  test $verbose = 1 && echo "$@" || :
}

for f in $(find ${pulp_rpmsdir} -type f); do
  dir=${f%/*}; checksum=${dir##*/}
  sha1sum=$(sha1sum $f | cut -f 1 -d ' ')
  sha256sum=$(sha256sum $f | cut -f 1 -d ' ')
  if test "x${checksum}" = "x${sha1sum}"; then
    vecho "$f: OK [sha1sum]"
  elif test "x${checksum}" = "x${sha256sum}"; then
    vecho "$f: OK [sha256sum]"
  else
    echo "$f: NG [checksum=$checksum]"
  fi 
done
