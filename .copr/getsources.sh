#!/bin/bash
CoreRepo=$(awk 'NR==2 {print; exit}' < _version)
CoreTag=$(awk 'NR==3 {print; exit}' < _version)
LauncherRepo=$(awk 'NR==4 {print; exit}' < _version)
LauncherTag=$(awk 'NR==5 {print; exit}' < _version)
DownstreamTag=$(awk 'NR==6 {print; exit}' < _version)-$(awk 'NR==7 {print; exit}' < _version)
xlsource=$(rpmbuild --eval='%_sourcedir')
source0=$xlsource/XIVLauncher.Core-$CoreTag.tar.gz
source1=$xlsource/FFXIVQuickLauncher-$LauncherTag.tar.gz
source2=$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz

# Make sure the script can run properly no matter where it's called from
# The below line will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
cd "$repodir" || exit
if [ ! -f "$source0" ];
then
    curl -L "$CoreRepo/archive/$CoreTag.tar.gz" -o "$source0"
fi
if [ ! -f "$source1" ];
then
    curl -L "$LauncherRepo/archive/$LauncherTag.tar.gz" -o "$source1"
fi
if [ ! -f "$source2" ];
then
    # We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
    # Make a directory, copy the needed files of the repo into the directory, then tar the results.
    mkdir -p "XIVLauncher4rpm-$DownstreamTag"
    cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING "XIVLauncher4rpm-$DownstreamTag/"
    tar -czf "$source2" "XIVLauncher4rpm-$DownstreamTag"
    # Delete the temp folder we just made.
    rm -rf "XIVLauncher4rpm-$DownstreamTag"
fi
cp _version "$xlsource"