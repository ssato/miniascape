#! /bin/bash
#
# @see http://stackoverflow.com/questions/2437976/get-color-output-in-bash , etc.
#
ccred=$(echo -e "33[1;31m")
ccyellow=$(echo -e "33[1;33m")
ccend=$(echo -e "33[0m")
make "$@" 2>&1 | sed -e "s/[Ee]rror:/$ccred&$ccend/g" -e "s/[Ww]arning:/$ccyellow&$ccend/g"
exit ${PIPESTATUS[0]}
