#!/bin/bash
# Version info
version=0.6
xlcore=1.0.3
# ~/.local/bin is part of the systemd file hierarchy. Fedora and openSUSE both use it.
bindir=$HOME/.local/bin
# Make sure XDG_DATA_HOME is set
if [[ -z "$XDG_DATA_HOME" ]]; then XDG_DATA_HOME=$HOME/.local/share; fi

# Function to make a new custom script
makeCustomScript ()
{
    # These directories don't always exist! Try to create them, just in case.
    mkdir -p "$bindir"
    echo "Creating new file $bindir/$script."
    {
        echo '#!/bin/bash'
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
    } > "$bindir/$script"
    chmod +x "$bindir/$script"
}

makeDesktop()
{
    echo -e "Creating new xivlauncher-$1.desktop file in\n$XDG_DATA_HOME/applications"
    {
        echo "[Desktop Entry]"
        echo "Name=XIVLauncher-RB RPM $1"
        echo "Comment=XIVLauncher-RB RPM $1 script (~/.local/bin/xivlauncher-$1.sh)"
        echo "Exec=/usr/bin/xivlauncher $1"
        echo "Icon=xivlauncher"
        echo "Terminal=true"
        echo "Type=Application"
        echo "Categories=Game;"
        echo "StartupWMClass=XIVLauncher.Core"
    } > "$XDG_DATA_HOME/applications/XIVLauncher-$1.desktop"
}

# Function to run without script
runDefault()
{
    echo "======================== /usr/bin/xivlauncher ========================"
    echo "No custom script in use. If you with to define custom launch options,"
    echo "run 'xivlauncher custom' at the command line. That will run the custom"
    echo "script at '~/.local/bin/xivlauncher-custom.sh'. If the script does not"
    echo "exist, it will be created first."
    echo "======================== /usr/bin/xivlauncher ========================"
    export OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf
    /opt/XIVLauncher/XIVLauncher.Core
    exit   
}

# Function to check for custom script
checkCustom()
{
    echo "Checking $bindir/$script"
    # Code to check for bad or missing custom script
    if [ -f "$bindir/$script" ]; then
        # Make it executable if it isn't
        if [ ! -x "$bindir/$script" ]; then
            chmod +x "$bindir/$script"
        fi
        # Check the file for bash syntax errors.
        errval=$(bash -n $bindir/$script 2>&1)
        retcode=$?
        if [ ! $retcode == 0 ]; then
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
            sslfix=$(grep -c 'OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf' "$bindir/$script")
            if [ "$sslfix" -eq 0 ]; then
                # If the OPENSSL_CONF line is not found, insert it.
                echo "Updating $script with SSL fix."
                sed -i '2i\export OPENSSL_CONF=/opt/XIVLauncher/openssl_fix.cnf\' "$bindir/$script"
            else
                echo "SSL config found."
            fi   
        fi
    else
        # custom script wasn't found, so create it.
        makeCustomScript
    fi
}

# Function to make .desktop file
checkDesktop()
{
    desktop=$XDG_DATA_HOME/applications/XIVLauncher-$1.desktop
    echo "Checking for XIVLauncher-$1.desktop file"
    if [ ! -f "$desktop" ]; then
        echo "Desktop file not found. Creating in $XDG_DATA_HOME/applications"
        makeDesktop "$1"
    else
        echo "Desktop file found."
    fi
}

# Function to run with script
runCustom()
{
    echo "===================== /usr/bin/xivlauncher $1 ====================="
    echo "Running script ~/.local/bin/$script"
    echo "If it crashes, please delete it, and run /usr/bin/xivlauncher $1"
    echo "again. If the problem persists, please file a ticket on"
    echo "https://github.com/rankynbass/XIVLauncher4rpm describing the error,"
    echo "along with the contents of ~/.local/bin/$script.sh"
    echo "===================== /usr/bin/xivlauncher $1 ====================="
    "$bindir/$script"
}

deleteScript()
{
    if [ -z "$1" ]; then
        echo -e "Missing script name.\n"
        helpText
    fi
    invalidScriptName "$1"
    if [ -f "$bindir/xivlauncher-$1.sh" ]; then
        echo "Deleting $bindir/xivlauncher-$1.sh"
        rm "$bindir/xivlauncher-$1.sh"
        echo "Deleting $XDG_DATA_HOME/applications/XIVLauncher-$1.desktop"
        rm -f "$XDG_DATA_HOME/applications/XIVLauncher-$1.desktop"
    else
        echo "$bindir/xivlauncher-$1.sh does not exist"
        exit 0
    fi
}

helpText()
{
    echo -e "Usage: xivlauncher [OPTION] <script>"
    echo -e "xivlauncher is a helper script that will launch XIVLauncher.Core, or create and"
    echo -e "run a user script at ~/.local/bin/xivlauncher-<script>.sh. This script is user"
    echo -e "modifiable and can be used to export environment variables or launch other"
    echo -e "programs.\n"
    echo -e "No options or script:"
    echo -e "\tRun XIVLauncher.Core without any custom scripts."
    echo -e "No options:"
    echo -e "\tRun ~/.local/bin/xivlauncher-<script>.sh. Create it if it doesn't exist."
    invalidScriptText
    echo -e "Options:"
    echo -e "\t-d script\tdeletes ~/.local/bin/xivlauncher-<script>.sh."
    echo -e "\t-r script\tdeletes ~/.local/bin/xivlauncher-<script>.sh,\n\t\t\t  then creates a fresh one."
    echo -e "\t-l, --list\tList custom xivlauncher scripts."
    echo -e "\t-h, --help\tgive this help list"
    echo -e "\t-v, --version\tprint version information"
    exit 0
}

invalidScriptName()
{
    if [[ "$1" == *@(\\|/|-|\|)* ]]; then
        echo -e "Invalid script name: $1\n"
        echo -e "Usage: xivlauncher [-d,-r] <script>"
        invalidScriptText
        exit 0
    fi
}

invalidScriptText()
{
    echo -e "\t<script> should be a single word. Don't use special characters, spaces,"
    echo -e "\tdashes or slashes. Underscores are okay."
}

# Body of script
if [ -z "$1" ]; then
    runDefault
else
    case "$1" in 
    -d)
        deleteScript "$2"
        echo ""
        exit 0;;
    -r)
        deleteScript "$2"
        shift
        echo -e " Now recreating\nxivlauncher-$1...\n";;
    -h | --help)
        helpText;;
    -l | --list)
        ls "$bindir"/xivlauncher-*.sh
        exit 0;;
    -v | --version)
        echo -e "xivlauncher helper script $version"
        echo -e "Copyright (C) 2022 Rankyn Bass"
        echo -e "License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>."
        echo -e "This is free software: you are free to change and redistribute it."
        echo -e "There is NO WARRANTY, to the extent permitted by law.\n"
        echo -e "This is a bash script. It should be safe, but you should always check before"
        echo -e "running scripts off the internet. This script is not provided by the official"
        echo -e "XIVLauncher development team; it is part of the COPR RPM release.\n"
        echo -e "For use with XIVLauncher.Core $xlcore"
        exit 0;;
    *)
        option=${1:0:1}
        if [ "$option" = "-" ]; then
            echo -e "Invalid option: $1\n"
            helpText
        fi
        invalidScriptName "$1";;
    esac
    script="xivlauncher-$1.sh"
    checkCustom
    checkDesktop "$1"
    runCustom "$1"
fi