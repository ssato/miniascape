#! /bin/bash
set -ex

{% import "snippets/pre_post.find_disk" as F -%}
{{ F.find_disk_device(2) }}

qdiskdev=$1
qdisklabel=$2

test "x$qdiskdev" = "x" && qdiskdev=/dev/${disk1:?}1
test "x$qdisklabel" = "x" && qdisklabel="qdisk-0"

mkqdisk -f ${qdisklabel} || mkqdisk -c ${qdiskdev} -l ${qdisklabel} 
