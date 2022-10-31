#!/bin/bash

xlpath=$HOME/.local/bin/xivlauncher-custom.sh

makeCustomScript () {
    echo "Creating new file $xlpath."
    {
        echo '#!/bin/bash'
        echo "# Always keep the next line. It works around an ssl bug on Square's end"
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
}

echo "=========================/usr/bin/xivlauncher========================="
echo "Checking $xlpath"
# Code to check for bad or missing $HOME/.local/bin/xivlauncher-custom.sh
if [ -f "$xlpath" ];
then
    # Make it executable if it isn't
    if [ ! -x "$xlpath" ];
    then
        chmod +x "$xlpath"
    fi
    # Check the file for bash syntax errors.
    errval=$(bash -n $xlpath 2>&1)
    retcode=$?
    if [ ! $retcode == 0 ];
    then
        # If errors are found, backup the file and create a fresh one.
        rm -f "$xlpath.bak"
        mv "$xlpath" "$xlpath.bak"
        echo "Couldn't run $xlpath. It has the following error:"
        echo "$errval"
        echo "It has been renamed to $xlpath.bak."
        makeCustomScript
    else
        # Otherwise, check for the SSL fix.
        echo "File exists. Checking for SSL fix."
        sslfix=$(grep -c 'OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf' "$xlpath")
        if [ "$sslfix" -eq 0 ];
        then
            # If the OPENSSL_CONF line is not found, insert it.
            echo "Updating xivlauncher-custom.sh with SSL fix."
            sed -i '2i\export OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf\' "$xlpath"
        else
            echo "SSL config found."
        fi   
    fi
else
    # xivlauncher-custom.sh wasn't found, so create it.
    makeCustomScript
fi
echo "Running script $xlpath."
echo "If it crashes, please delete it, and run /usr/bin/xivlauncher again."
echo "If the problem persists, please file a ticket on"
echo "https://github.com/rankynbass/XIVLauncher4rpm describing the error,"
echo "along with the contents of ~/.local/bin/xivlauncher-custom.sh"
echo "=========================/usr/bin/xivlauncher========================="
$xlpath