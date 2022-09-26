#!/usr/bin/bash

# Define env variables. Top one is mandatory. 
export OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf
# export DXVK_FRAME_RATE=60
# export MANGOHUD=1
# export MANGOHUD_CONFIGFILE=~/.config/MangoHud/MangoHud.conf

# Steam overlay (doesn't work yet)
# export LD_PRELOAD="$HOME/.local/share/Steam/ubuntu12_64/gameoverlayrenderer.so"

/opt/XIVLauncher/XIVLauncher.Core &
