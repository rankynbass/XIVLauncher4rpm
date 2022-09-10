#!/bin/bash
UpstreamTag=$(awk 'NR==2 {print; exit}' < _version)
DownstreamTag=$(awk 'NR==3 {print; exit}' < _version)-$(awk 'NR==4 {print; exit}' < _version)
xlsource=$(rpmbuild --eval='%_sourcedir')
source0=$xlsource/FFXIVQuickLauncher-$UpstreamTag.tar.gz
source1=$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz
# Make sure the script can run properly no matter where it's called from
# The below line will always point to the repo's root directory.
repodir=$(dirname "${BASH_SOURCE[0]}")/../
cd $repodir
if [ ! -f "$source0" ];
then
    curl -L https://github.com/goatcorp/FFXIVQuickLauncher/archive/$UpstreamTag.tar.gz -o $source0
fi
if [ ! -f "$source1" ];
then
    # We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
    # Make a directory, copy the needed files of the repo into the directory, then tar the results.
    mkdir -p XIVLauncher4rpm-$DownstreamTag
    cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING XIVLauncher4rpm-$DownstreamTag/
    tar -czf $source1 XIVLauncher4rpm-$DownstreamTag
    # Delete the temp folder we just made.
    rm -rf XIVLauncher4rpm-$DownstreamTag
fi
cp _version $xlsource