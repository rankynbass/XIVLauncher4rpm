#!/bin/bash
DownstreamTag=$(awk 'NR==6 {print; exit}' < _version)-$(awk 'NR==7 {print; exit}' < _version)
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"

cd "$repodir" || exit
{
    printf '%s\n' "{"
    printf '\t"%s": %s,\n' "schemaVersion" "1"
    printf '\t"%s": "%s",\n' "label" "copr"
    printf '\t"%s": "%s",\n' "message" "$DownstreamTag: build ok"
    printf '\t"%s": "%s"\n' "color" "blue"
    printf '%s' "}"
} > badge.json