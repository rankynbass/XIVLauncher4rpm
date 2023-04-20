#!/bin/bash
# This script is for cleaning out some of the old wine and dalamud assets used by
# XIVLauncher. These will be rebuild when you next log in, and are thus safe to delete.
# Cleaning these up when switching between native and flatpak versions is advised.

echo "Checking for existing .xlcore folder..."
# Check to see if the .xlcore directory even exists
if [ ! -d "$HOME/.xlcore" ]; then
    echo "Folder $HOME/.xlcore not found. This is normal for a new install."
else
    echo "Folder $HOME/.xlcore found."

    # List of files and folders to attempt to backup. This is case sensative.
    TOOLLIST="compatibilitytool dalamud dalamudAssets devPlugins runtime wineprefix installedPlugins"
    TOOLLISTBAK=""
  
    # Check for folders. If they exist, delete them
    for TOOL in $TOOLLIST
      do
        if [ -d "$HOME/.xlcore/$TOOL" ]; then
            TOOLLISTBAK="$TOOLLISTBAK $TOOL"
            echo "Checking for $TOOL folder... Found. Deleting..."
            rm -rf $HOME/.xlcore/$TOOL
        else
            echo "Checking for $TOOL folder... Not Found."
        fi
    done

    # List assembled. If $TOOLLISTBAK is empty, there was nothing to backup.
    if [ ! -z "$TOOLLISTBAK" ]; then
        echo "The following folders were removed from $HOME/.xlcore:"
        echo "  $TOOLLISTBAK"
        echo "Your game files and settings are unaffected, but wine and dalamud will be redownloaded on next start to ensure compatability."
        echo "The version of wine used by this native XIVLauncher install may not be compatible with the flatpak version. Don't use them together, or you may end up with odd bugs or crashes."
    else
        echo "Nothing to backup."
    fi
    echo "Your .xlcore folder is clean."
fi