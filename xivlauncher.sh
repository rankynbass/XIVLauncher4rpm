#!/bin/bash
xlpath=$HOME/.local/bin/xivlauncher-custom.sh
export OPENSSL_CONF=/opt/XIVLauncher-git/openssl_fix.cnf
# Check to see if $HOME/.local/bin/xivlauncher exists
if [ ! -x "$xlpath" ];
then
    {
        echo '#!/bin/bash'
        echo '# Edit this file for custom launch options.'
        echo '# For example, add "export MANGOHUD=1" to enable mangohud'
        echo '# You can also call other programs, like gamescope'
        echo '# See https://github.com/Plagman/gamescope for more info'
        echo '# Gamescope example, upscale from 720p to 1080p with FSR 1.0 and fullscreen:'
        echo '#'
        echo '# export SDL_VIDEODRIVER=x11 # work around a fedora bug with gamescope'
        echo '# gamescope -w 1280 -h 720 -W 1920 -H 1440 -U -f -- /opt/XIVLauncher-git/XIVLauncher.Core'
        echo ''
        echo '/opt/XIVLauncher-git/XIVLauncher.Core'
    } > $xlpath
    chmod +x $xlpath
fi
$xlpath