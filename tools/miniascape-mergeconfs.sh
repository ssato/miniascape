#! /bin/bash
set -e

confsdir=$1
if test "x$confsdir" = "x"; then
    cat << EOF
$0 CONFSDIR

Example:
  $0 conf/default/15_guests.yml.d/
EOF
    exit 0
fi

echo -ne "[Info] Merge files in ${confsdir}: "
for f in ${confsdir}/*.yml; do
    out=${f/\.d\/*/}
    outtmp=${out}.t
    sed -n '/^#/d; p' $f >> ${outtmp}
done
test -f ${outtmp} && mv ${outtmp} ${out} || :
echo "Done"

# vim:sw=4:ts=4:et:
