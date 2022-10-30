#!/bin/bash
# Make sure the script can run properly no matter where it's called from
# The below lines will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
CoreTag=$(awk 'NR==3 {print; exit}' < "$repodir/_version")
DownstreamTag=$(awk 'NR==6 {print; exit}' < "$repodir/_version")-$(awk 'NR==7 {print; exit}' < "$repodir/_version")
xlsource=$(rpmbuild --eval='%_sourcedir')
CoreRepo="$HOME/COPR/XIVLauncher.Core"
# Uncomment next line for different submodule version
# LauncherRepo="$HOME/COPR/FFXIVQuickLauncher"
xlsource="$(rpmbuild --eval='%_sourcedir')"
workingdir=/tmp/xivlauncher-local
mkdir -p "$workingdir"

cd "$repodir" || exit
cp -r $CoreRepo "$workingdir/"
# Uncomment next two lines to use different submodule version
# rm -rf $workingdir/XIVLauncher.Core/lib/FFXIVQuickLauncher
# cp -r $LauncherRepo $workingdir/XIVLauncher.Core/lib/
cd $workingdir || exit
echo "Writing XIVLauncher.Core-$CoreTag.tar.xz"
tar --totals -I 'xz -v -9' -cf "$xlsource/XIVLauncher.Core-$CoreTag.tar.xz" --exclude="XIVLauncher.Core/.git" --exclude="XIVLauncher.Core/lib/FFXIVQuickLauncher/.git" "XIVLauncher.Core"
cd "$repodir" || exit
# We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
# Make a directory, copy the needed files of the repo into the directory, then tar the results.
mkdir -p "$workingdir/XIVLauncher4rpm-$DownstreamTag"
cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING "$workingdir/XIVLauncher4rpm-$DownstreamTag/"
cd "$workingdir" || exit
echo "Writing XIVLauncher4rpm-$DownstreamTag.tar.xz"
tar --totals -I 'xz -v -9' -cf "$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.xz" "XIVLauncher4rpm-$DownstreamTag"
cd "$repodir" || exit
cp _version "$xlsource"
rm -rf "$workingdir"