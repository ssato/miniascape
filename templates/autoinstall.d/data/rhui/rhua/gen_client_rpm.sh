#! /bin/bash
#
# A script to make RHUI client cert and RPM in RHUI v2.
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
#
USAGE="Usage: $0 [Options ...] NAME REPO_0 [REPO_1 [...]]
  where NAME     Name of client config rpm and cert files
        REPO_*   Labels of yum repos to enable in cert.
         
                 You can see the full list by running 'rhui-manager
                 client lables'.
"
NAME=
REPOS=
WORKDIR=/root/setup/clients/
DAYS=3650
RPM_VERSION=1.0
PRIMARY_CDS=
TO_SIGN=no

function show_usage () {
    cat << EOU
${USAGE}

Try '$0 -h/--help' for more info.
EOU
    exit ${1:-0}
}

function show_help () {
    cat <<EOH
${USAGE}

Options:
    -w WORKDIR  Working dir to save cert files [$WORKDIR]
    -d DAYS     Number of days cert will be valid [$DAYS]

    -v VER      Version number of the client config rpm [$RPM_VERSION]
    -c CDS      Name of the cds used as the primary load balancer of
                the cds cluster [auto]
    -S          Sign the client config rpm built
EOH
}

info () { echo "[Info] $@"; }
error () { echo "[Error] $@"; exit 1; }

# main:
while getopts w:d:v:c:Sh OPT
do
    case "$OPT" in
        w) WORKDIR=$OPTARG
           ;;
        d) DAYS=$OPTARG
           ;;
        v) RPM_VERSION=$OPTARG
           ;;
        c) PRIMARY_CDS=$OPTARG
           ;;
        S) TO_SIGN=yes
           ;;
        h) show_help
           exit 0
           ;;
        \?) echo "Invalid option and/or arguments!"
            show_usage
            exit 1
            ;;
    esac
done
shift $((OPTIND - 1))

NAME=$1; shift
REPOS=$(echo $@ | tr ' ' ,)

test "x${NAME}" != "x" -a "x${REPOS}" != "x" || show_usage 1
timeout 3 rhui-manager cert --help &> /dev/null || \
error "Cannot run rhui-manager w/o auth. Try running it manually first."

info "Creating client cert ${NAME} ..."
rhui-manager client cert \
--name ${NAME} --repo_label ${REPOS} --days ${DAYS} --dir ${WORKDIR}/

CLIENT_CERT=${WORKDIR}/${NAME}.crt
CLIENT_KEY=${WORKDIR}/${NAME}.key

test -f ${CLIENT_CERT} -a -f ${CLIENT_KEY} || error "Cert or key were missing! Aborting..."

if test "x${PRIMARY_CDS}" = "x"; then
    info "Primary CDS was not given. Try to find the first one from availables..."
    PRIMARY_CDS=$(rhui-manager cds available | head -n 1)
    test "x${PRIMARY_CDS}" != "x" || error "[Error] Could not get the CDS name. Aborting..."
fi

info "Creating client config rpm ${NAME} ..."
rhui-manager client rpm \
--rpm_name ${NAME} --rpm_version ${RPM_VERSION} --primary_cds ${PRIMARY_CDS} \
--entitlement_cert ${CLIENT_CERT} --private_key ${CLIENT_KEY} \
--ca_cert /etc/pki/rhua/rhua-ssl-ca-cert.crt --dir ${WORKDIR}/rpms

test "x${TO_SIGN}" = "xyes" && \
(rpm --resign ${WORKDIR}/rpms/${NAME}-${RPM_VERSION}/build/RPMS/noarch/*.rpm;
 rpm -Kv ${WORKDIR}/rpms/${NAME}-${RPM_VERSION}/build/RPMS/noarch/*.rpm)

info "Finished. Found the RPM under ${WORKDIR}/rpms/"

# vim:sw=4:ts=4:et:
