#! /bin/bash
set -e

for f in $(find /var/lib/pulp/content/rpm/ -type f); do
  dir=${f%/*}; checksum=${dir##*/}
  sha1sum=$(sha1sum $f | cut -f 1 -d ' ')
  sha256sum=$(sha256sum $f | cut -f 1 -d ' ')
  if test "x${checksum}" = "x${sha1sum}"; then
    echo "$f: OK [sha1sum]"
  elif test "x${checksum}" = "x${sha256sum}"; then
    echo "$f: OK [sha256sum]"
  else
    echo "$f: NG [checksum=$checksum]"
  fi
done
