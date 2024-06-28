#!/bin/bash
# Make sure the script can run properly no matter where it's called from
# The below line will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
PkgName=$(awk 'NR==1 {print; exit}' < "$repodir/_version")
CoreRepo=$(awk 'NR==2 {print; exit}' < "$repodir/_version")
CoreTag=$(awk 'NR==3 {print; exit}' < "$repodir/_version")
Release=$(awk 'NR==4 {print; exit}' < "$repodir/_version")
xlsource=$(rpmbuild --eval='%_sourcedir')
source0="$xlsource/XIVLauncher.Core-$CoreTag.tar.gz"
source1=$xlsource/XIVLauncher4rpm-$CoreTag-$Release.tar.gz
workingdir=/tmp/xivlauncher

mkdir -p "$workingdir"
rm -rf "$workingdir"/XIVLauncher.Core
rm -rf "$workingdir"/XIVLauncher4rpm-$CoreTag-$Release
rm $source0
rm $source1

cd "$workingdir" || exit
echo "Cloning $CoreTag from git repository $CoreRepo"
git clone "$CoreRepo" -b $CoreTag --recurse-submodules
cd XIVLauncher.Core || exit
Hash=$(git rev-parse --short HEAD)
cd "$workingdir" || exit
echo "Creating XIVLauncher.Core-$CoreTag.tar.gz"
tar --exclude=".*" -czf "$source0" XIVLauncher.Core

cd "$repodir" || exit
mkdir -p "$workingdir/XIVLauncher4rpm-$CoreTag-$Release"
cp CHANGELOG.md README.md xivlauncher.sh XIVLauncher.desktop COPYING "$workingdir/XIVLauncher4rpm-$CoreTag-$Release/"
cd "$workingdir" || exit
echo "Creating XIVLauncher4rpm-$CoreTag-$Release.tar.gz"
tar -czf "$source1" "XIVLauncher4rpm-$CoreTag-$Release"

cat > "$xlsource/_version" << EOF
$PkgName
$CoreRepo
$CoreTag
$Release
$Hash
EOF