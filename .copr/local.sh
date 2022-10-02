#!/bin/bash
UpstreamTag=$(awk 'NR==2 {print; exit}' < _version)
DownstreamTag=$(awk 'NR==3 {print; exit}' < _version)-$(awk 'NR==4 {print; exit}' < _version)
LocalRepo="$HOME/build/FFXIVQuickLauncher"
xlsource="$(rpmbuild --eval='%_sourcedir')"

# Make sure the script can run properly no matter where it's called from
# The below lines will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"

# Make tarball from local FFXIVQuickLauncher repo
cd "$LocalRepo/.." || exit
tar -czf "$xlsource/FFXIVQuickLauncher-$UpstreamTag.tar.gz" --exclude="FFXIVQuickLauncher/.git" "FFXIVQuickLauncher"

cd "$repodir" || exit
# We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
# Make a directory, copy the needed files of the repo into the directory, then tar the results.
mkdir -p "XIVLauncher4rpm-$DownstreamTag"
cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING "XIVLauncher4rpm-$DownstreamTag/"
tar -czf "$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz" "XIVLauncher4rpm-$DownstreamTag"
# Delete the temp folder we just made.
rm -rf "XIVLauncher4rpm-$DownstreamTag"

cp _version "$xlsource"