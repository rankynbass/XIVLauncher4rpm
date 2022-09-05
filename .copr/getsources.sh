#!/bin/bash
UpstreamTag=$(awk 'NR==2 {print; exit}' < _version)
DownstreamTag=$(awk 'NR==3 {print; exit}' < _version)-$(awk 'NR==4 {print; exit}' < _version)
xlsource=$(rpmbuild --eval='%_sourcedir')
source0=$xlsource/FFXIVQuickLauncher-$UpstreamTag.tar.gz
source1=$xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz
if [ ! -f "$source0" ];
then
    curl -L https://github.com/goatcorp/FFXIVQuickLauncher/archive/$UpstreamTag.tar.gz -o $source0
fi
if [ ! -f "$source1" ];
then
    curl -L https://github.com/rankynbass/XIVLauncher4rpm/archive/$DownstreamTag.tar.gz -o $source1
fi