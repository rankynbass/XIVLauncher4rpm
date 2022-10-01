#!/bin/bash

LocalRepo="$HOME/build/FFXIVQuickLauncher"

xlsource="$(rpmbuild --eval='%_sourcedir')"

# Make sure the script can run properly no matter where it's called from
# The below lines will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"

# Make tarball from local FFXIVQuickLauncher repo
cd "$LocalRepo/.." || exit
xlcommit=local
xltimestamp="$(date -u +'%y.%m.%d.%H%M')"
tar -czf "$xlsource/FFXIVQuickLauncher-$xlcommit.tar.gz" --exclude="FFXIVQuickLauncher/.git" "FFXIVQuickLauncher"

cd "$repodir" || exit
# We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
# Make a directory, copy the needed files of the repo into the directory, then tar the results.
DownstreamTag="$xltimestamp-utc"
mkdir -p "XIVLauncher4rpm-$DownstreamTag"
cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING "XIVLauncher4rpm-$DownstreamTag/"
tar -czf "$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz" "XIVLauncher4rpm-$DownstreamTag"
# Delete the temp folder we just made.
rm -rf "XIVLauncher4rpm-$DownstreamTag"

# Build the _version file. Make sure all lines are correct.
# This is a "safe" way to do it. This makes sure the version file didn't get any added lines at the end.
{
    echo "# Line 2: UpstreamTag, Line 3: Version, Line 4: Release. DO NOT DELETE THIS COMMENT LINE"
    echo "$xlcommit"
    echo "$xltimestamp"
    echo "utc"
} > "$xlsource/_version"