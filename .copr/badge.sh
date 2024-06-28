#!/bin/bash
DownstreamTag=$(awk 'NR==3 {print; exit}' < _version)-$(awk 'NR==4 {print; exit}' < _version)
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"

# Colors: success (brightgreen), critical (red), informational (blue) 
cd "$repodir" || exit
{
    printf '%s\n' "{"
    printf '\t"%s": %s,\n' "schemaVersion" "1"
    printf '\t"%s": "%s",\n' "label" "copr"
    printf '\t"%s": "%s",\n' "message" "rb-$DownstreamTag"
    printf '\t"%s": "%s"\n' "color" "success"
    printf '%s' "}"
} > badge.json