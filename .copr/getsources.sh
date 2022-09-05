#!/bin/bash
UpstreamTag=6246fde
DownstreamTag=1.0.1.0-3a
xlsource=$(rpmbuild --eval='%_sourcedir')
curl -L https://github.com/goatcorp/FFXIVQuickLauncher/archive/$UpstreamTag.tar.gz -o $xlsource/FFXIVQuickLauncher-$UpstreamTag.tar.gz
curl -L https://github.com/rankynbass/XIVLauncher4rpm/archive/$DownstreamTag.tar.gz -o $xlsource/XIVLauncher4rpm-$DownstreamTag.tar.gz
