#!/bin/bash

# ~/.local/bin is part of the systemd file hierarchy. Fedora and openSUSE both use it.
bindir=$HOME/.local/bin

# Function to make a new custom script
makeCustomScript ()
{
    # These directories don't always exist! Try to create them, just in case.
    mkdir -p "$bindir"
    echo "Creating new file $bindir/$script."
    {
        echo '#!/bin/bash'
        echo 'export OPENSSL_CONF=/opt/XIVLauncher-git/openssl_fix.cnf'
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
    } > "$bindir/$script"
    chmod +x "$bindir/$script"
}

# Function to run without script
runDefault()
{
    echo "======================== /usr/bin/xivlauncher-git ========================"
    echo "No custom script in use. If you with to define custom launch options,"
    echo "run 'xivlauncher-git custom' at the command line. That will run the custom"
    echo "script at '~/.local/bin/xivlauncher-git-custom.sh'. If the script does not"
    echo "exist, it will be created first."
    echo "======================== /usr/bin/xivlauncher-git ========================"
    export OPENSSL_CONF=/opt/XIVLauncher-git/openssl_fix.cnf
    /opt/XIVLauncher-git/XIVLauncher.Core
    exit   
}

# Function to check for custom script
checkCustom()
{
    echo "Checking $bindir/$script"
    # Code to check for bad or missing custom script
    if [ -f "$bindir/$script" ];
    then
        # Make it executable if it isn't
        if [ ! -x "$bindir/$script" ];
        then
            chmod +x "$bindir/$script"
        fi
        # Check the file for bash syntax errors.
        errval=$(bash -n $bindir/$script 2>&1)
        retcode=$?
        if [ ! $retcode == 0 ];
        then
            # If errors are found, backup the file and create a fresh one.
            rm -f "$bindir/$script.bak"
            mv "$bindir/$script" "$bindir/$script.bak"
            echo "Couldn't run $bindir/$script. It has the following error:"
            echo "$errval"
            echo "It has been renamed to $bindir/$script.bak."
            makeCustomScript
        else
            # Otherwise, check for the SSL fix.
            echo "File exists. Checking for SSL fix."
            sslfix=$(grep -c 'OPENSSL_CONF=/opt/XIVLauncher-git/openssl_fix.cnf' "$bindir/$script")
            if [ "$sslfix" -eq 0 ];
            then
                # If the OPENSSL_CONF line is not found, insert it.
                echo "Updating xivlauncher-git-$1.sh with SSL fix."
                sed -i '2i\export OPENSSL_CONF=/opt/XIVLauncher-git/openssl_fix.cnf\' "$bindir/$script"
            else
                echo "SSL config found."
            fi   
        fi
    else
        # custom script wasn't found, so create it.
        makeCustomScript
    fi
}

# Function to run with script
runCustom()
{
    echo "===================== /usr/bin/xivlauncher-git $1 ====================="
    echo "Running script ~/.local/bin/$script"
    echo "If it crashes, please delete it, and run /usr/bin/xivlauncher-git $1"
    echo "again. If the problem persists, please file a ticket on"
    echo "https://github.com/rankynbass/XIVLauncher4rpm describing the error,"
    echo "along with the contents of ~/.local/bin/$script.sh"
    echo "===================== /usr/bin/xivlauncher-git $1 ====================="
    "$bindir/$script"
}

# Body of script
if [ -z "$1" ];
then
    runDefault
else
    script=xivlauncher-git-$1.sh
    checkCustom "$@"
    runCustom "$@"
fi