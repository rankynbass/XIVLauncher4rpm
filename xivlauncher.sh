#!/bin/bash
export OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf
xlpath=$HOME/.local/bin/xivlauncher-custom.sh
# Check to see if $HOME/.local/bin/xivlauncher exists
echo "Checking for $xlpath"
if [ ! -x "$xlpath" ];
then
    echo "File $xlpath doesn't exist or can't be executed. Creating..."
    {
        echo '#!/bin/bash'
        echo "Always keep the next line. It works around an ssl bug on Square's end"
        echo 'export OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf'
        echo '# Edit this file for custom launch options.'
        echo '# For example, add "export MANGOHUD=1" to enable mangohud'
        echo '# You can also call other programs, like gamescope'
        echo '# See https://github.com/Plagman/gamescope for more info'
        echo '# Gamescope example, upscale from 720p to 1080p with FSR 1.0 and fullscreen:'
        echo '#'
        echo '# export SDL_VIDEODRIVER=x11 # work around a fedora bug with gamescope'
        echo '# gamescope -w 1280 -h 720 -W 1920 -H 1440 -U -f -- /opt/XIVLauncher/XIVLauncher.Core'
        echo ''
        echo '/opt/XIVLauncher/XIVLauncher.Core'
    } > "$xlpath"
    chmod +x "$xlpath"
else
    echo "xivlauncher-custom.sh exists. Checking for SSL config"
    sslfix=$(grep -c 'OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf' "$xlpath")
    if [ "$sslfix" -eq 0 ];
    then
        echo "Updating xivlauncher-custom.sh with SSL config"
        sed -i '2i\export OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf\' "$xlpath"
    else
        echo "SSL config found."
    fi
fi
$xlpath 