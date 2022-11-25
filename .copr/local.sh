#!/bin/bash
# Make sure the script can run properly no matter where it's called from
# The below lines will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
CoreTag=$(awk 'NR==3 {print; exit}' < "$repodir/_version")
DownstreamTag=$(date -u -r "$repodir/_version" +'%y.%m.%d.%H%M')
xlsource=$(rpmbuild --eval='%_sourcedir')
CoreRepo="$HOME/COPR/XIVLauncher.Core"
# Uncomment next line for different submodule version
LauncherRepo="$HOME/COPR/FFXIVQuickLauncher"
xlsource="$(rpmbuild --eval='%_sourcedir')"
workingdir=/tmp/xivlauncher-local
mkdir -p "$workingdir"

cd "$repodir" || exit
cp -r $CoreRepo "$workingdir/"
# Uncomment next two lines to use different submodule version
rm -rf $workingdir/XIVLauncher.Core/lib/FFXIVQuickLauncher
cp -r $LauncherRepo $workingdir/XIVLauncher.Core/lib/
cd $workingdir || exit
echo "Writing XIVLauncher.Core-$CoreTag.tar.gz"
tar -czf "$xlsource/XIVLauncher.Core-$CoreTag.tar.gz" --exclude="XIVLauncher.Core/.git" --exclude="XIVLauncher.Core/lib/FFXIVQuickLauncher/.git" "XIVLauncher.Core"
cd "$repodir" || exit
# We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
# Make a directory, copy the needed files of the repo into the directory, then tar the results.
mkdir -p "$workingdir/XIVLauncher4rpm-$DownstreamTag-git"
cp CHANGELOG.md cleanupprofile.sh openssl_fix.cnf README.md xivlauncher.sh XIVLauncher.desktop XIVLauncher-git-custom.desktop COPYING "$workingdir/XIVLauncher4rpm-$DownstreamTag-git/"
cd "$workingdir" || exit
echo "Writing XIVLauncher4rpm-$DownstreamTag-git.tar.gz"
tar -czf "$xlsource/XIVLauncher4rpm-$DownstreamTag-git.tar.gz" "XIVLauncher4rpm-$DownstreamTag-git"
cd "$repodir" || exit
# Build the _version file. Line 6 will get replaced with the current timestamp.
{
    echo "XIVLauncher-git"
    awk 'NR==2 {print; exit}' < "$repodir/_version"
    echo "$CoreTag"
    awk 'NR==4 {print; exit}' < "$repodir/_version"
    awk 'NR==5 {print; exit}' < "$repodir/_version"
    echo "$DownstreamTag"
    echo "git"
} > "$xlsource/_version"
rm -rf "$workingdir"