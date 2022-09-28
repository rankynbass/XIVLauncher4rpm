#!/bin/bash

# Github repo to use. Can use this to point to a fork for testing purposes.
gitrepo="https://github.com/rankynbass/FFXIVQuickLauncher.git"

# Make sure the script can run properly no matter where it's called from
# The below lines will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
cd "$repodir" || exit

xlsource="$(rpmbuild --eval='%_sourcedir')"

# Get the latest git from upstream.
rm -rf FFXIVQuickLauncher
git clone $gitrepo
cd FFXIVQuickLauncher || exit
# Get timestamp of current commit.
xlgitshow=($(git show -s --format='%h %ct'))
xlcommit=${xlgitshow[0]}
xltimestamp="$(date -u -d "@${xlgitshow[1]}" +'%y.%m.%d.%H%M')"
git archive --format=tar.gz -o "$xlsource/FFXIVQuickLauncher-$xlcommit.tar.gz" --prefix=FFXIVQuickLauncher/ HEAD
# Delete the repo.
cd "$repodir" || exit
rm -rf FFXIVQuickLauncher

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