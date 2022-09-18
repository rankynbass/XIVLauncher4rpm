#!/bin/bash
# Make sure the script can run properly no matter where it's called from
# The below lines will always point to the repo's root directory.
cd $(dirname "${BASH_SOURCE[0]}")/../
repodir=$(pwd)
UpstreamTag=$(awk 'NR==2 {print; exit}' < _version)
DownstreamTag=$(awk 'NR==3 {print; exit}' < _version)-$(awk 'NR==4 {print; exit}' < _version)
xlsource=$(rpmbuild --eval='%_sourcedir')
source0=$xlsource/FFXIVQuickLauncher-$UpstreamTag.tar.gz
source1=$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz
# We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
# Make a directory, copy the needed files of the repo into the directory, then tar the results.
mkdir -p XIVLauncher4rpm-$DownstreamTag
cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING XIVLauncher4rpm-$DownstreamTag/
tar -czf $source1 XIVLauncher4rpm-$DownstreamTag
# Delete the temp folder we just made.
rm -rf XIVLauncher4rpm-$DownstreamTag
cp _version $xlsource
# Now get the latest git from upstream.
rm -rf FFXIVQuickLauncher
git clone https://github.com/goatcorp/FFXIVQuickLauncher.git
cd FFXIVQuickLauncher
# Get timestamp of current commit.
echo "$(date -u -d @$(git show -s --format=%ct) +'%y.%m.%d.%H%M')" > $xlsource/_timestamp
git archive --format=tar.gz -o $source0 --prefix=FFXIVQuickLauncher/ HEAD
cd $repodir
rm -rf FFXIVQuickLauncher