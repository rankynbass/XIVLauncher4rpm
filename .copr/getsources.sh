#!/bin/bash
xlsource=$(rpmbuild --eval='%_sourcedir')
uptag=6246fde
downtag=copr-test
wget https://github.com/goatcorp/FFXIVQuickLauncher/archive/$uptag.tar.gz -O $xlsource/FFXIVQuickLauncher-$uptag.tar.gz
wget https://github.com/rankynbass/XIVLauncher4rpm/archive/$downtag.tar.gz -O $xlsource/XIVLauncher4rpm-$downtag.tar.gz