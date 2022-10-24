#!/bin/bash
CoreTag=$(awk 'NR==3 {print; exit}' < _version)
LauncherTag=$(awk 'NR==5 {print; exit}' < _version)
DownstreamTag=$(awk 'NR==6 {print; exit}' < _version)-$(awk 'NR==7 {print; exit}' < _version)
xlsource=$(rpmbuild --eval='%_sourcedir')
CoreRepo="$HOME/build/XIVLauncher.Core"
LauncherRepo="$HOME/build/FFXIVQuickLauncher"
xlsource="$(rpmbuild --eval='%_sourcedir')"

# Make sure the script can run properly no matter where it's called from
# The below lines will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"

# Make tarball from local FFXIVQuickLauncher repo
cd "$CoreRepo/.." || exit
tar -czf "$xlsource/XIVLauncher.Core-$CoreTag.tar.gz" --exclude="FFXIVQuickLauncher/.git" "XIVLauncher.Core"
cd "$LauncherRepo/.." || exit
tar -czf "$xlsource/FFXIVQuickLauncher-$LauncherTag.tar.gz" --exclude="FFXIVQuickLauncher/.git" "FFXIVQuickLauncher"

cd "$repodir" || exit
# We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
# Make a directory, copy the needed files of the repo into the directory, then tar the results.
mkdir -p "XIVLauncher4rpm-$DownstreamTag"
cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING "XIVLauncher4rpm-$DownstreamTag/"
tar -czf "$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz" "XIVLauncher4rpm-$DownstreamTag"
# Delete the temp folder we just made.
rm -rf "XIVLauncher4rpm-$DownstreamTag"

cp _version "$xlsource"