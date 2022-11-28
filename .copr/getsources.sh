#!/bin/bash
# Make sure the script can run properly no matter where it's called from
# The below line will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
CoreRepo=$(awk 'NR==2 {print; exit}' < "$repodir/_version")
CoreTag=$(awk 'NR==3 {print; exit}' < "$repodir/_version")
LauncherRepo=$(awk 'NR==4 {print; exit}' < "$repodir/_version")
LauncherTag=$(awk 'NR==5 {print; exit}' < "$repodir/_version")
DownstreamTag=$(awk 'NR==6 {print; exit}' < "$repodir/_version")-$(awk 'NR==7 {print; exit}' < "$repodir/_version")
xlsource=$(rpmbuild --eval='%_sourcedir')
source0=$xlsource/XIVLauncher.Core-$CoreTag.tar.gz
source1=$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz
workingdir=/tmp/xivlauncher

cd "$repodir" || exit
mkdir -p "$workingdir"
if [ ! -f "$source0" ];
then
    # Source tarballs from github are a mess when you reference by commits. It uses the long hash in the tarball.
    # So we'll do a little bash magic to get the folder names. Then we'll extract everything, rename as appropriate,
    # and rebuild a full source tarball that includes the submodule.
    cd "$workingdir" || exit
    echo "Downloading $CoreTag => xlcore-$CoreTag.tar.gz"
    curl -L "$CoreRepo/archive/$CoreTag.tar.gz" -o "xlcore-$CoreTag.tar.gz"
    echo "Downloading $LauncherTag => launcher-$LauncherTag.tar.gz"
    curl -L "$LauncherRepo/archive/$LauncherTag.tar.gz" -o "launcher-$LauncherTag.tar.gz"
    # These next two lines will get the folder names at the top of the tarball
    CoreDir=$(tar -tf "xlcore-$CoreTag.tar.gz" | head -n 1)
    LauncherDir=$(tar -tf "launcher-$LauncherTag.tar.gz" | head -n 1)
    # Extract XIVLauncher.Core tarball and then rename the folder to XIVLauncher.Core
    echo "Extracting xlcore-$CoreTag.tar.gz"
    tar -xf "xlcore-$CoreTag.tar.gz"
    mv "$CoreDir" XIVLauncher.Core
    # Remove an empty directory that will get in our way
    rmdir XIVLauncher.Core/lib/FFXIVQuickLauncher
    # Extract the FFXIVQuickLauncher tarball to XIVLauncher.Core/lib/, then rename to FFXIVQuickLauncher
    echo "Extracting launcher-$LauncherTag.tar.gz and moving files to lib/FFXIVQuickLauncher"
    tar -C XIVLauncher.Core/lib -xf "launcher-$LauncherTag.tar.gz"
    mv "XIVLauncher.Core/lib/$LauncherDir" "XIVLauncher.Core/lib/FFXIVQuickLauncher"
    # Create a new, complete tarball.
    echo "Writing XIVLauncher.Core-$CoreTag.tar.gz"
    tar -czf "$source0" XIVLauncher.Core
fi
cd "$repodir" || exit
if [ ! -f "$source1" ];
then
    # We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
    # Make a directory, copy the needed files of the repo into the directory, then tar the results.
    mkdir -p "$workingdir/XIVLauncher4rpm-$DownstreamTag"
    cp CHANGELOG.md cleanupprofile.sh openssl_fix.cnf README.md xivlauncher.sh XIVLauncher.desktop XIVLauncher-custom.desktop COPYING "$workingdir/XIVLauncher4rpm-$DownstreamTag/"
    cd "$workingdir" || exit
    echo "Writing XIVLauncher4rpm-$DownstreamTag.tar.gz"
    tar -czf "$source1" "XIVLauncher4rpm-$DownstreamTag"
fi
cp "$repodir/_version" "$xlsource"
rm -rf "$workingdir"