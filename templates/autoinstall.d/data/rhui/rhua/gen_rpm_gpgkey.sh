#! /bin/bash
set -x

custom_gpg_key=/root/setup/RPM-GPG-KEY-rhui-custom
custom_gpg_conf=/root/setup/rhui-gpg.conf

test -d /root/setup || mkdir -p /root/setup
cat << EOF > ${custom_gpg_conf}
Key-Type: RSA
Key-Length: 1024
# No subkey, RSA (sign only), to keep compatibility w/ RHEL 5 clients:
Key-Usage: sign
Expire-Date: 0
Name-Real: RHUI Admin
Name-Comment: GPG key for custom RPMs from RHUI
Passphrase: {{ gpg.passpharase }}
%no-protection
%transient-key
%commit
EOF

(find / -xdev -type f -exec sha256sum {} >/dev/null \; 2>&1) &
export ENTROPY_GEN_PROCESS=$!
gpg -v --batch --gen-key ${custom_gpg_conf} && kill ${ENTROPY_GEN_PROCESS}

keyid=$(gpg --list-keys | sed -nr 's,^pub[^/]+/(.+) [0-9].*,\1,p')

gpg -a --export ${keyid:?} > ${custom_gpg_key}

cat << EOF > /root/dot.rpmmacros
%_signature gpg
%_gpg_name ${keyid:?}
%__gpg_sign_cmd %{__gpg} \
  gpg --force-v3-sigs --digest-algo=sha1 --batch --no-verbose --no-armor \
      --passphrase-fd 3 --no-secmem-warning -u "%{_gpg_name}" \
      -sbo %{__signature_filename} %{__plaintext_filename}
EOF

(cd /root && test -f .rpmmacros || ln -s dot.rpmmacros .rpmmacros)

#rpm --import ${custom_gpg_key}

# vim:sw=2:ts=2:et:
