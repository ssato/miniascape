#! /bin/bash
set -e

# Defaults:
ADMIN={{ satellite.admin.name|default('admin') }}
PASSWORD="{{ satellite.admin.password|default('') }}"
ORGANIZATION={{ satellite.organization|default('Default_Organization') }}
LOCATION={{ satellite.location|default('Default_Location') }}
MANIFETS_FILE={{ satellite.manifests_file|default('manifests.zip') }}
LIFECYCLE_ENVIRONMENT_PATHS="{{ satellite.lifecycle_environments|join(' ', attribute='name') if satellite.lifecycle_environments else 'Test Prod' }}"
HOST_COLLECTIONS="{{ satellite.host_collections|join(' ', attribute='name') if satellite.host_collections -%}"
LOGDIR=logs


# @see http://gsw-hammer.documentation.rocks/initial_configuration,_adding_red_repos/hammer_credentials.html
function guess_admin_password () {
    sed -nr 's/^ *admin_password: ([^[:blank:]]+) *$/\1/p' \
        /etc/katello-installer/answers.katello-installer.yaml
}

function setup_hammer_userconf () {
    local admin_username=${1:-$ADMIN}
    local admin_password=${2:-$PASSWORD}

    local userconf=$HOME/.hammer/cli_config.yml
    local sysconf=/etc/hammer/cli.modules.d/foreman.yml

    if test -f ${userconf:?}; then
        echo "[Info] ${userconf} already exists! Nothing to do."
    else
        if test -f ${sysconf:?}; then
            if test "x${admin_password}" = "x"; then
                #read -s -p "Password: " -t 20 admin_password
                admin_password=`guess_admin_password`
            fi
            test -d ${userconf%/*} || mkdir -m 0700 ${userconf%/*}
            touch ${userconf} && chmod 0600 ${userconf}
            cat << EOF > ${userconf}
`cat ${sysconf}`

  :username: '${admin_username:?}'
  :password: '${admin_password:?}'
EOF
        else
            echo "[Warn] System configuration ${sysconf} does not exist! Check your installation of satellite 6"
            return 1
        fi
    fi
}

function setup_org_and_location () {
    local org=${1:-$ORGANIZATION}
    local location=${2:-$ORGANIZATION}
    local admin=${3:-$ADMIN}

    local orgid=$(hammer organization list | sed -nr "s/^([[:digit:]]+) .*${org:?}*/\1/p")

    if test "x${org}" != "x${ORGANIZATION}"; then
        test "x${orgid}" = "x" && \
            hammer organization create --name="${org}" --label="${org}"
    fi

    local locid=$(hammer location list | sed -nr "s/^([[:digit:]]+) .*${location:?}*/\1/p")
    if test "x${location:?}" != "x${LOCATION}"; then
        test "x${locid}" = "x" && \
            hammer location create --name="${location}"
    fi

    # TODO: Which of the followings are necessary?
    hammer location add-user --name="${location}" --user="${admin}"
    hammer location add-organization --name="${location}" --organization="${org}"
    hammer organization add-user --name="${org}" --user="${admin:?}"
}

function upload_manifests () {
    local manifests_file=${1:-$MANIFETS_FILE}
    local org=${2:-$ORGANIZATION}
    local product="${3:-Red Hat Enterprise Linux Server}"
    local logdir=${4:-$LOGDIR}

    test -d ${logdir} || mkdir -p ${logdir}

    if test -f ${manifests_file}.base64 -a ! -f ${manifests_file}; then
        base64 -d ${manifests_file}.base64 > ${manifests_file}
    fi

    hammer subscription upload --organization "${org}" --file ${manifests_file:?}
    hammer product list --organization "${org}" --full-results | \
        tee ${logdir}/product.list
    hammer repository-set list --organization "${org}" --product "${product:?}" | \
        tee ${logdir}/rhel-server-repos.list
}

function setup_sync_plan () {
    local org=${1:-$ORGANIZATION}
    local product="${2:-Red Hat Enterprise Linux Server}"
    local logdir=${3:-$LOGDIR}
    local sync_plan_name="Daily sync"

    test -d ${logdir} || mkdir -p ${logdir}

    hammer sync-plan create --organization "${org}" \
        --interval daily --name "${sync_plan_name:?}"
    hammer sync-plan list --organization "${org}"
    hammer product set-sync-plan --organization "${org}" --name "${product}" \
        --sync-plan-id 1  # It seems that --sync-plan is not valid.
}

function sync_product_repos () {
    local org=${1:-$ORGANIZATION}
    local product="${2:-Red Hat Enterprise Linux Server}"
    local logdir=${3:-$LOGDIR}

    local repos_csv=${logdir:?}/repos_$(echo ${product:?} | tr ' ' _).csv

    hammer --csv repository list --organization "${org:?}" | tee ${repos_csv:?}
    for rid in $(sed -nr 's/^([[:digit:]]+),.*/\1/p' ${repos_csv})
    do
        hammer repository synchronize --organization "${org}" \
            --id ${rid:?} --async
    done
}

function setup_content_view () {
    local name="${1:?}"
    local repo_name_pattern="${2:?}"  # ex. 'Red Hat Enterprise Linux 6'
    local org=${3:-$ORGANIZATION}

    (hammer content-view list --organization "${org:?}" | grep "${name:?}") || \
     hammer content-view create --organization "${org}" --name "${name}"
    for rid in \
        $(hammer --csv repository list --organization "${org}" | \
          sed -nr "s/^([[:digit:]]+),${repo_name_pattern}.*/\1/p")
    do
        hammer content-view add-repository --organization "${org}" \
            --name "${name:?}" --repository-id ${rid:?}
    done
}

function create_host_collection() {
    local collection=${1:?}
    local org=${2:-$ORGANIZATION}

    hammer host-collection create --organization "${org}" --name "${collection:?}"
}

function create_activation_key () {
    local name="${1:?}"
    local content_view="${2:?}"
    local lifecycle_env="${3:?}"
    local org=${4:-$ORGANIZATION}

    hammer activation-key create --organization "${org}" \
        --name "${name:?}" \
        --content-view "${content_view:?}" \
        --lifecycle-environment "${lifecycle_env:?}"

# TODO: --max-content-hosts | --unlimited-content-hosts \
}

# pre-defined and common tasks:
function setup_user_repos () {
    local org=${1:-$ORGANIZATION}
    local product="${2:-Red Hat Enterprise Linux Server}"

{% for repo in satellite.repos if repo.name and repo.releasever -%}
    hammer repository-set enable \
        --organization "${org:?}" --product "${product:?}" \
        --name '{{ repo.name }}'
        --basearch {{ repo.arch|default("x86_64") }} \
        --releasever '{{ repo.releasever }}'
{% endfor %}
}

function setup_user_content_views () {
    local org=${1:-$ORGANIZATION}

    {% for cv in satellite.cvs if cv.name and cv.repo_pattern -%}
    setup_content_view "{{ cv.name }}" "{{ cv.repo_pattern }}" "${ORGANIZATION}"
    {% endfor %}
}

function setup_lifecycle_env_paths () {
    local org=${1:-$ORGANIZATION}
    local path_prev="Library"  # All lifecycle env paths start from it.

    shift 1
    local paths="${@:-Test Prod}"

    for path in $paths; do
        hammer lifecycle-environment create --organization "${org}" \
             --prior "${path_prev:?}" --name "${path:?}"
        local path_prev=$path
    done
}

function setup_host_collections () {
    local org=${1:-$ORGANIZATION}
    shift 1
    local hcs="${@:-$ORGANIZATION}"

    local hcs_now=$(hammer host-collection list --organization "${org:?}" | sed -nr '/^([[:digit:]]+)/p')

    for hc in ${hcs}; do
        hammer host-collection create --organization "${org}" --name "${hc}"
    done
}

function publish_content_view () {
    local name="${1}"  # e.g. CV_RHEL_6
    local org=${2:-$ORGANIZATION}

    hammer content-view publish --organization "${org:?}" --name "${name:?}"
}

function publish_content_views_async () {
    local org=${1:-$ORGANIZATION}

    local cvs=$(hammer content-view list --organization "${org:?}" --nondefault Default_Organization_View | sed -nr 's/^([[:digit:]]+) .*/\1/p' | sort)
    for cv in ${cvs}; do
        hammer content-view publish --organization "${org:?}" --name "${cv}" --async
    done
}

function promote_content_views_first_async () {
    local org=${1:-$ORGANIZATION}

    local cvids=$(hammer content-view list --organization "${org:?}" --nondefault Default_Organization_View | sed -nr 's/^([[:digit:]]+) .*/\1/p' | sort)
    local first_lep=$(hammer lifecycle-environment list --organization "${org}" | \
        sed -nr 's/^([[:digit:]]+) .*/\1/p' | sort | sed -n '2p')

    for cvid in ${cvids}; do
        local cvv=$(hammer content-view version list --organization "${org}" \
            --content-view-id "${cvid:?}" | \
            sed -nr "s/^([[:digit:]]+) .*/\1/p" | sort -rn | sed -n '1p')
        hammer content-view version promote --organization "${org}" \
            --content-view-id "${cvid}" --lifecycle-environment-id ${first_lep} \
            --id ${cvv:?} --async
    done
}

function setup_activation_keys_for_lifecycle_environments () {
    local org=${1:-$ORGANIZATION}
    local logdir=${2:-$LOGDIR}
    local akeylist0=${logdir}/akeys.txt.0

    hammer activation-key list --organization "${org:?}" --by ID | tee ${logdir}/akeys.txt.0
    {% for akey in satellite.activation_keys if akey.name and akey.cv and akey.environment -%}
    grep "{{ akey.name }}" ${akeylist0} || \
        create_activation_key "{{ akey.name }}" "{{ akey.cv }}" "{{ akey.environment }}" "${org:?}"
    {% endfor %}
}


usage="Usage: $0 [OPTIONS]"

function show_help () {
  cat <<EOH
$usage
Options:
  -a ADMIN  Admin name [$ADMIN]
  -o ORG    Organization to create and setup [$ORGANIZATION]
  -l LOC    Location to create and setup [$LOCATION]
  -M FILE   Path to manifests file [$MANIFETS_FILE]

  -D        Initialize with script default settings
  -S        Synchronize repos

  -h        Show this help and exit.

Examples:
 $0 -D
EOH
}


# main:
while getopts "a:o:l:M:P:H:h" opt
do
  case $opt in
    a) ADMIN=$OPTARG ;;
    o) ORGANIZATION=$OPTARG ;;
    l) LOCATION=$OPTARG ;;
    M) MANIFETS_FILE=$OPTARG ;;
    P) LIFECYCLE_ENVIRONMENT_PATHS="$OPTARG" ;;
    H) HOST_COLLECTIONS="$OPTARG" ;;
    h) show_help; exit 0 ;;
    \?) show_help; exit 1 ;;
  esac
done
shift $(($OPTIND - 1))
cmd=$1

if test "x$cmd" = "x"; then
    cat << EOH
Usage: $0 [OPTION...] COMMAND
Commands:
  i[nit]     Initialize:
               - Setup hammer user configuration file
               - Setup organization and location for the user
               - Upload manifests
               - Setup repos and products
               - Setup content views
               - Setup lifecycle environment paths
               - Setup host collections
  s[ync]     Synchronize repos
  pu[blish]  Publish content views to library lifecycle environment path asynchronously
  pr[omote]  Promote content views
  a[key]     Setup activation keys

Options:
  -a ADMIN   Administrator's name [$ADMIN]
  -o ORG     Organization name [$ORGANIZATION]
  -l LOC     Location name [$LOCATION]
  -M MFILE   Manifest file [$MANIFETS_FILE]
  -P PATHS   Quoted, space separated lifecycle environment paths [$LIFECYCLE_ENVIRONMENT_PATHS]
  -H HCS     Quoted, space separated host-collection names [$HOST_COLLECTIONS]
EOH
    exit 0
fi

case $cmd in
  i*) setup_hammer_userconf ${ADMIN};
      setup_org_and_location "${ORGANIZATION}" "${LOCATION}" ${ADMIN};
      upload_manifests ${MANIFETS_FILE} "${ORGANIZATION}";
      setup_user_repos "${ORGANIZATION}";
      setup_product "${ORGANIZATION}";
      setup_user_content_views "${ORGANIZATION}";
      setup_lifecycle_env_paths "${ORGANIZATION}" ${LIFECYCLE_ENVIRONMENT_PATHS};
      setup_host_collections "${ORGANIZATION}" ${HOST_COLLECTIONS};
      ;;
  s*) sync_product_repos
      ;;
  pu*) publish_content_views_async  "${ORGANIZATION}";
       ;;
  pr*) promote_content_views_first_async  "${ORGANIZATION}";
       ;;
  a*) setup_activation_keys_for_lifecycle_environments "${ORGANIZATION}";
      ;;
esac

# vim:sw=4:ts=4:et:
