#!/bin/bash
# Make sure the script can run properly no matter where it's called from
# The below line will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
CoreRepo=$(awk 'NR==2 {print; exit}' < "$repodir/_version")
CoreTag=$(awk 'NR==3 {print; exit}' < "$repodir/_version")
LauncherRepo=$(awk 'NR==4 {print; exit}' < "$repodir/_version")
LauncherTag=$(awk 'NR==5 {print; exit}' < "$repodir/_version")
DownstreamTag=$(date -u -r "$repodir/_version" +'%y.%m.%d.%H%M')
xlsource=$(rpmbuild --eval='%_sourcedir')
source0=$xlsource/XIVLauncher.Core-$CoreTag.tar.gz
source1=$xlsource/XIVLauncher4rpm-$DownstreamTag-utc.tar.gz
workingdir=/tmp/xivlauncher

cd "$repodir" || exit
mkdir -p "$workingdir"
if [ ! -f "$source0" ];
then
    # Source tarballs from github are a mess when you reference by commits. It uses the long hash in the tarball.
    # So we'll do a little bash magic to get the folder names. Then we'll extract everything, rename as appropriate,
    # and rebuild a full source tarball that includes the submodule.
    cd "$workingdir" || exit
    curl -L "$CoreRepo/archive/$CoreTag.tar.gz" -o "XLCore-$CoreTag.tar.gz"
    curl -L "$LauncherRepo/archive/$LauncherTag.tar.gz" -o "FFXIVQL-$LauncherTag.tar.gz"
    # These next two lines will get the folder names at the top of the tarball
    CoreDir=$(tar -tf "XLCore-$CoreTag.tar.gz" | head -n 1)
    LauncherDir=$(tar -tf "FFXIVQL-$LauncherTag.tar.gz" | head -n 1)
    # Extract XIVLauncher.Core tarball and then rename the folder to XIVLauncher.Core
    tar -xf "XLCore-$CoreTag.tar.gz"
    mv "$CoreDir" XIVLauncher.Core
    # Remove an empty directory that will get in our way
    rmdir XIVLauncher.Core/lib/FFXIVQuickLauncher
    # Extract the FFXIVQuickLauncher tarball to XIVLauncher.Core/lib/, then rename to FFXIVQuickLauncher
    tar -C XIVLauncher.Core/lib -xf "FFXIVQL-$LauncherTag.tar.gz"
    mv "XIVLauncher.Core/lib/$LauncherDir" "XIVLauncher.Core/lib/FFXIVQuickLauncher"
    # Create a new, complete tarball.
    echo "Making tarball for XIVLauncher.Core"
    tar -czf "$source0" XIVLauncher.Core
fi
cd "$repodir" || exit
if [ ! -f "$source1" ];
then
    # We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
    # Make a directory, copy the needed files of the repo into the directory, then tar the results.
    mkdir -p "$workingdir/XIVLauncher4rpm-$DownstreamTag-utc"
    cp CHANGELOG.md README.md cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop XIVLauncher-git-custom.desktop COPYING "$workingdir/XIVLauncher4rpm-$DownstreamTag-utc/"
    cd "$workingdir" || exit
    echo "Making tarball for XIVLauncher4rpm"
    tar -czf "$source1" "XIVLauncher4rpm-$DownstreamTag-utc"
fi
# Build the _version file. Line 6 will get replaced with the current timestamp.
{
    echo "XIVLauncher-git"
    echo "$CoreRepo"
    echo "$CoreTag"
    echo "$LauncherRepo"
    echo "$LauncherTag"
    echo "$DownstreamTag"
    echo "utc"
} > "$xlsource/_version"
rm -rf "$workingdir"