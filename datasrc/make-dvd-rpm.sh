#! /bin/bash
set -e
#set -x

workdir=t
destdir=`pwd`/$workdir

filelist2rpm="python $HOME/repos/public/github.com/ssato/rpmkit.git/filelist2rpm.py"
realpath () {
    python -c "import os.path; print os.path.realpath('$1')";
}


test $# -gt 2 && filelist2rpm=$2 || :
if test $# -lt 1; then
    echo "Usage: $0 ISO_PATH [FILELIST2RPM_PATH]"
    exit 1
fi

isoname=${1##*/}
pkgname=`echo ${isoname} | sed -e 's,\.,-,g'`

test -d t/srv/isos || mkdir -p t/srv/isos
cp -f $1 t/srv/isos


echo $destdir/srv/isos/$isoname | $filelist2rpm -n $pkgname -w $workdir --destdir $destdir --build-rpm --no-mock -

