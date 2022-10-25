#!/bin/bash
CoreRepo=$(awk 'NR==2 {print; exit}' < _version)
CoreTag=$(awk 'NR==3 {print; exit}' < _version)
LauncherRepo=$(awk 'NR==4 {print; exit}' < _version)
LauncherTag=$(awk 'NR==5 {print; exit}' < _version)
DownstreamTag=$(awk 'NR==6 {print; exit}' < _version)-$(awk 'NR==7 {print; exit}' < _version)
xlsource=$(rpmbuild --eval='%_sourcedir')
source0=$xlsource/XIVLauncher.Core-$CoreTag.tar.gz
source1=$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz

# Make sure the script can run properly no matter where it's called from
# The below line will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
cd "$repodir" || exit
if [ ! -f "$source0" ];
then
    # Source tarballs from github are a mess when you reference by commits. It uses the long hash in the tarball.
    # So we'll do a little bash magic to get the folder names. Then we'll extract everything, rename as appropriate,
    # and rebuild a full source tarball that includes the submodule.
    mkdir -p tarballs
    cd tarballs || exit
    curl -L "$CoreRepo/archive/$CoreTag.tar.gz" -o "$CoreTag.tar.gz"
    curl -L "$LauncherRepo/archive/$LauncherTag.tar.gz" -o "$LauncherTag.tar.gz"
    # These next two lines will get the folder names at the top of the tarball
    CoreDir=$(tar -tf "$CoreTag.tar.gz" | head -n 1)
    LauncherDir=$(tar -tf "$LauncherTag.tar.gz" | head -n 1)
    # Extract XIVLauncher.Core tarball and then rename the folder to XIVLauncher.Core
    tar -xf "$CoreTag.tar.gz"
    mv "$CoreDir" XIVLauncher.Core
    # Remove an empty directory that will get in our way
    rmdir XIVLauncher.Core/lib/FFXIVQuickLauncher
    # Extract the FFXIVQuickLauncher tarball to XIVLauncher.Core/lib/, then rename to FFXIVQuickLauncher
    tar -C XIVLauncher.Core/lib -xf "$LauncherTag.tar.gz"
    mv "XIVLauncher.Core/lib/$LauncherDir" "XIVLauncher.Core/lib/FFXIVQuickLauncher"
    # Create a new, complete tarball.
    tar -czf "$source0" XIVLauncher.Core
    cd "$repodir" || exit
    rm -rf tarballs
fi
cd "$repodir" || exit
if [ ! -f "$source1" ];
then
    # We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
    # Make a directory, copy the needed files of the repo into the directory, then tar the results.
    mkdir -p "XIVLauncher4rpm-$DownstreamTag"
    cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING "XIVLauncher4rpm-$DownstreamTag/"
    tar -czf "$source1" "XIVLauncher4rpm-$DownstreamTag"
    # Delete the temp folder we just made.
    rm -rf "XIVLauncher4rpm-$DownstreamTag"
fi
cp _version "$xlsource"