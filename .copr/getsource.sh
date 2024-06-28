#!/bin/bash
# Make sure the script can run properly no matter where it's called from
# The below line will always point to the repo's root directory.
repodir="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../")"
PkgName=$(awk 'NR==1 {print; exit}' < "$repodir/_version")
CoreRepo=$(awk 'NR==2 {print; exit}' < "$repodir/_version")
CoreTag=$(awk 'NR==3 {print; exit}' < "$repodir/_version")
Release=$(awk 'NR==4 {print; exit}' < "$repodir/_version")
xlsource=$(rpmbuild --eval='%_sourcedir')
source0="$xlsource/XIVLauncher-RB-$CoreTag.tar.gz"
source1=$xlsource/XIVLauncher4rpm-rb-v$CoreTag-$Release.tar.gz
workingdir=/tmp/xivlauncher

mkdir -p "$workingdir"
rm -rf "$workingdir"/XIVLauncher-RB
rm -rf "$workingdir"/XIVLauncher4rpm
rm $source0
rm $source1

cd "$workingdir" || exit
echo "Cloning $CoreTag from git repository $CoreRepo"
git clone "$CoreRepo" -b rb-v$CoreTag --recurse-submodules XIVLauncher-RB
cd XIVLauncher-RB || exit
Hash=$(git rev-parse --short HEAD)
cd "$workingdir" || exit
echo "Creating XIVLauncher-RB-$CoreTag.tar.gz"
tar --exclude=".*" -czf "$source0" XIVLauncher-RB

cd "$repodir" || exit
mkdir -p "$workingdir/XIVLauncher4rpm"
cp CHANGELOG.md README.md xivlauncher.sh XIVLauncher.desktop COPYING "$workingdir/XIVLauncher4rpm/"
cd "$workingdir" || exit
echo "Creating XIVLauncher4rpm-rb-v$CoreTag-$Release.tar.gz"
tar -czf "$source1" "XIVLauncher4rpm"

cat > "$xlsource/_version" << EOF
$PkgName
$CoreRepo
$CoreTag
$Release
$Hash
EOF