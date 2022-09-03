#!/bin/bash
xlsource=$(rpmbuild --eval='%_sourcedir')
UpstreamTag=6246fde
DownstreamTag=copr-test
wget https://github.com/goatcorp/FFXIVQuickLauncher/archive/$UpstreamTag.tar.gz -O $xlsource/FFXIVQuickLauncher-$UpstreamTag.tar.gz
wget https://github.com/rankynbass/XIVLauncher4rpm/archive/$DownstreamTag.tar.gz -O $xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz
