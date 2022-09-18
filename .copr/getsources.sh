#!/bin/bash
# Make sure the script can run properly no matter where it's called from
# The below lines will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
cd "$repodir" || exit

UpstreamTag=$(awk 'NR==2 {print; exit}' < _version)
xlver=$(awk 'NR==3 {print; exit}' < _version)
xlrel=$(awk 'NR==4 {print; exit}' < _version)
DownstreamTag=$xlver-$xlrel
xlsource=$(rpmbuild --eval='%_sourcedir')
source0=$xlsource/FFXIVQuickLauncher-$UpstreamTag.tar.gz
source1=$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz

# We could download the correct git tag as a tar.gz file, but we already have all the files here! Why do that?
# Make a directory, copy the needed files of the repo into the directory, then tar the results.
mkdir -p "XIVLauncher4rpm-$DownstreamTag"
cp cleanupprofile.sh openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING "XIVLauncher4rpm-$DownstreamTag/"
tar -czf "$source1" "XIVLauncher4rpm-$DownstreamTag"
# Delete the temp folder we just made.
rm -rf "XIVLauncher4rpm-$DownstreamTag"

# Build the _version file. Make sure all lines are correct.
# This is a "safe" way to do it. This makes sure the version file didn't get any added lines at the end.
echo "# Line 2: UpstreamTag, Line 3: Version, Line 4: Release. DO NOT DELETE THIS COMMENT LINE" > $xlsource/_version
echo "$UpstreamTag" >> $xlsource/_version
echo "$xlver" >> $xlsource/_version
echo "$xlrel" >> $xlsource/_version

# Now get the latest git from upstream.
rm -rf FFXIVQuickLauncher
git clone https://github.com/goatcorp/FFXIVQuickLauncher.git
cd FFXIVQuickLauncher || exit
# Get timestamp of current commit.
xltimestamp="$(date -u -d "@$(git show -s --format=%ct)" +'%y.%m.%d.%H%M')"
echo "$xltimestamp" >> "$xlsource/_version"
git archive --format=tar.gz -o "$source0" --prefix=FFXIVQuickLauncher/ HEAD
# Delete the repo.
cd "$repodir" || exit
rm -rf FFXIVQuickLauncher
