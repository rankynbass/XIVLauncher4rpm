# Changelog
### Wed Nov 04 2023 Rankyn Bass <rankyn@proton.me>
1.0.6.0:
Purely cosmetic bump to match the official release. The 1.0.6 patches were applied in 1.0.5.1.

### Tue Nov 03 2023 Rankyn Bass <rankyn@proton.me>
1.0.5.0, 1.0.5.1:
Update to support patch 6.50. The .1 release fixed the repair game function.

### Thu Sep 21 2023 Rankyn Bass <rankyn@proton.me>
1.0.4.7-1:
Changed the versioning scheme. Updated scripts and added epoch to .spec file.

### Thu Sep 21 2023 Rankyn Bass <rankyn@proton.me>
1.0.4-7:
Fixed a minor issue with console spamming gamemodeauto: if gamemode was enabled.

### Thu Sep 21 2023 Rankyn Bass <rankyn@proton.me>
1.0.4-6:
Rebased on compatibility-rework-2 branch, which will hopefully be merged in 1.0.5.
- Pruned Wine and Dxvk lists
- Added separate download buttons for Wine and Dxvk
- Reworked scaling. If you were scaling based on Font size, reset font size to 22, and change the scaling factor instead. In the UI, it's shown as a int percentage, but it's stored as a float multiplier (e.g 1.5)
- You can now extract wine folders into `~/.xlcore/compatibilitytool/wine` and they will show up in the list of Wine versions.
- You can do the same with Dxvk folders into `~/.xlcore/compatibilitytool/dxvk`

### Sat Aug 12 2023 Rankyn Bass <rankyn@proton.me>
Added a few new wine versions
- Wine-GE based 8-13
- Wine-staging-tkg 8.13
- proton-wine 8.0.3c (tkg)
- proton-wine-experimental bleeding edge 8.0.52623 (tkg)

Added the ability to use a custom Dxvk folder

### Sat Jul 22 2023 Rankyn Bass <rankyn@proton.me>
Added a Reshade toggle button at the bottom of the Wine Tab. Also added Unofficial-wine-xiv-proton 8-12, with FSR, and a new valve proton-wine with xiv patches and fsr.

### Sat Jul 15 2023 Rankyn Bass <rankyn@proton.me>
Fixed the "Disabled" option for DXVK. Also prevented DXVK Async from showing when Disabled is selected.

### Fri Jul 14 2023 Rankyn Bass <rankyn@proton.me>
Re-added the Auto-launch feature. Up to 3 Windows exes can be launched with the game. Tested as working with winediscordipcbridge.exe.

Confirmed that launching when using Proton, I can launch with ReShade, Dalamud, and MangoHud enabled and not crash, even after several hours of playtime.

### Thu Jul 13 2023 Rankyn Bass <rankyn@proton.me>
Updated to 1.0.4 with Proton compatibility patched in.
- Includes patched wine versions 8.10-12, 8.8, and 7.22
- Includes patched wine-ge versions
- Includes dxvk 2.1 and 2.2 with gplasync patches
- Includes XL_PATH environment variable

### Tue Nov 29 2022 Rankyn Bass <rankyn@proton.me>
Updated the xivlauncher script. It has some management features built in
- It will create .desktop files for your custom scripts in `~/.local/share/applications` (or the $XDG_DATA_HOME directory if that is set).
- You can list scripts with -l, delete with -d <scriptname>, and refresh (to default) with -r <scriptname>.
- There is some basic sanity parsing, but not too much. You can break this if you try. I'm not responsible if you do.

The settings tab has a minor makeover: dropdown menus now show the extended description (previously this was unused in xlcore).

Added support for MangoHud. It needs to be installed to work.

### Sun Nov 27 2022 Rankyn Bass <rankyn@proton.me>
Moved a bunch of code back since the XIVLauncher.Common.Unix pull request got rejected.

Fixed a few minor scripting errors
- getsources.sh will no longer fail if the CoreTag and LauncherTag are the same
- xivlauncher.sh had a minor typo that probably would never have been encountered, but it's fixed anyway.
- xivlauncher.sh now installs a .desktop file to `~/.local/share/applications` when you use a custom arguement.

Bump release to 4.

### Sat Nov 26 2022 Rankyn Bass <rankyn@proton.me>
Added the `XL_FORCE_WINED3D` environment variable. Forces use of WineD3D instead of DXVK

Moved a bunch of code around for ease of management. The XIVLauncher.Common.Unix folder was moved from the FFXIVQuickLauncher repo to the XIVLauncher.Core repo.

The titlebar now has RB-Unofficial at the end to remind you this is not a default build.

Bump release to 3.

### Thu Nov 24 2022 Rankyn Bass <rankyn@proton.me>
XIVLauncher-RB now has a DXVK version switcher!
- It's in the Wine tab.
- Default version is 1.10.1. But you can chose .2, .3, or 2.0.

My fork of the XIVLauncher.Core repo now points to my fork of the FFXIVQuickLauncher repo, at least for this set of branches.

Bump release to 2.

### Sat Nov 12 2022 Rankyn Bass <rankyn@proton.me>
New build! XIVLauncher-RB 1.0.2-1 with custom patches:
- XL_PATH patch - You can now use the environment variable XL_PATH to set a path for the xlcore directory. For example, `XL_PATH=$HOME/.local/share/xlcore` to conform with XDG directory structure.
- DXVK v2 - upgraded to the latest version of DXVK
- The titlebar now says "XIVLauncher-RB" to indicate that you're not running the default launcher.

You must uninstall XIVLauncher, and install XIVLauncher-RB. The two versions cannot coexist.

### Wed Nov 09 2022 Rankyn Bass <rankyn@proton.me>
Release bumped to 6

Changed back to tar.gz files for faster testing. Size saving isn't worth it.
- Changed FFXIVQuickLauncher commit to 261464a. This is only one commit off the offical xlcore 1.0.2 commit, but has the XIVLauncher.Core stuff moved out of the repo. This prevents a bunch of duplicates in the tar.gz / SRPM.
- XIVLauncher.Core is now on commit ad6b701 (it actually has been for a few releases). This commit skips version checking for non-flatpak releases. The version check function can sometimes take up to 5 seconds to execute (at which point it times out and gives up), and the window contents won't load until it's finished.


### Wed Nov 02 2022 Rankyn Bass <rankyn@proton.me>
Release bumped to 5

Redid the xivlauncher script
- Running `/usr/bin/xivlauncher` with no arguements just launches XIVLauncher.
- Running `/usr/bin/xivlauncher custom` will check for `$HOME/.local/bin/xivlauncher-custom.sh`, and launch it if it's found and has valid bash syntax.
    - If the script is found, but is broken, it'll back it up and create a new one.
    - If it doesn't find the custom script, it will created it.
    - If the path `$HOME/.local/bin` doesn't exist, it will be created first. This fixes an error that was reported. This path is *not* part of the XDG basedir specs, but it *is* part of the systemd file heirarchy, and Fedora, openSUSE, Enterprise Linux, and most distros with systemd use it. 

### Sun Oct 30 2022 Rankyn Bass <rankyn@proton.me>
Release bumped to 4

Fixed an error in the xivlauncher.sh script
- The xivlauncher-custom.sh script being created was malformed, resulting in a crash.
- The xivlauncher script now checks it for syntax errors, and backs it up and creates a new one if there are problems. This should fix it for people who got a poorly formed script file.

### Sat Oct 29 2022 Rankyn Bass <rankyn@proton.me>
Release bumped to 3

Minor update to launcher scripts
- The `/usr/bin/xivlauncher` script now checks `~/.local/bin/xivlauncher-custom.sh` for an openssl config line
- If it doesn't find one, it adds it to the top of the file (just under `#!/bin/bash`)
- If it's creating the file for the first time, the line is included.
- The `/usr/bin/xivlauncher` script no longer has the openssl config line. Users can just directly execute the xivlauncher-custom script with no problems now. Calling the main xivlauncher script will still work as well.

### Thu Oct 27 2022 Rankyn Bass <rankyn@proton.me>
Minor packaging update to 1.0.2-2

The last number has been dropped from the versioning. As a result, I had to add an Epoch entry to the .spec file.

The `/usr/bin/xivlauncher` script has been modified. It now calls a custom script from `~/.local/bin/xivlauncher-custom.sh`, and creates it first if it doesn't already exist. This will allow the user to maintain their own edits to the launch script that won't be overwritten with each update. the README.md and install script output have been updated accordingly.

Steam users should now be able to just safely reference the `xivlauncher` script or the .desktop file.

The `cleanupprofile.sh` script now just deletes folders instead of backing them up. There wasn't really a point to that.

### Sun Oct 23 2022 Rankyn Bass <rankyn@proton.me>
New version! 1.0.2.0-1

Now uses a new repo. _version file, scripts, and spec file adjusted to work with it.
- pull tarballs from XIVLauncher.Core repo and FFXIVQuickLauncher repo
- using build hash from XIVLauncher.Core repo for BuildHash

You can now generate a tspack for debugging. It's in the Settings > About tab.

You can now press enter while in the user or password fields and log in.

Update without starting should now actually not start the game.

### Sun Oct 2 2022 Rankyn Bass <rankyn@proton.me>
Bump version-release to 1.0.1.0-6

Modified getsources.sh and version file to allow alternate forks of FFXIVQuickLauncher

Added local.sh to make it easier to test new builds without doing commits or git pushes.

Modified xivlauncher.sh to indicate how to add env variables.

Modified spec file so titlebar will show "1.0.1.0 (rpm-hashnum)"

Modified .desktop file to include (native) in the title, so it's different from flatpak install.

### Sat Sep 10 2022 Rankyn Bass <rankyn@proton.me>
Bump version-release to 1.0.1.0-5

Added cleanupprofile.sh
- Moves compatibilitytool, dalamud, dalamudAssets, devPlugins folders to _old_compat
- Must be run by user. Can't run as part of install, since that is run as root, not as user.

Modified spec file
- Added %post and %postun macros.
- Added reference to cleanupprofile.sh

Modified getsources.sh to include cleanupprofile.sh

Modified README.md to include cleanupprofile.sh

### Sun Sep 04 2022 Rankyn Bass <rankyn@proton.me>
Bump version-release to 1.0.1.0-4, because 3a is not > 3

Added _version file. This contains UpstreamTag, Version, and Release.

Modify getsources.sh
- Build XIVLauncher4rpm tarball from local git clone.
- Put in if statements for local builds.
- Now gets UpstreamTag, DownstreamTag from _version file.

Modify spec file
- Now gets UpstreamTag, xlversion, and xlrelease from _version file.
- Moved source2 up above definitions, because I need it declared before using it in %define tags.

### Sun Sep 04 2022 Rankyn Bass <rankyn@proton.me>
Bump version-release to 1.0.1.0-3a

Modify Makefile, getsources.sh
- Remove wget, replace with curl

Modify spec file
- Add -p:BuildHash=UpstreamTag to prevent git describe.
- Drop unneeded git build dependency
- Drop git init section
- Add xivlogo.png to install directory (from misc/header.png)

### Fri Sep 02 2022 Rankyn Bass <rankyn@proton.me>
Bump version-release to 1.0.1.0-3

Modify Makefile, add getsources script
- No longer requires git. Now just needs wget.
- Makefile now calls getsources.sh, which uses wget to download sources
- getsources.sh MUST have matching UpstreamTag and DownstreamTag in spec file.
- No longer call rpmbuild -bp, which should fix problems with building srpm.

Modify spec file
- Now works with downloaded sources instead of downloading with git during prep stage.
- Reorganized importand definitions (%define) to the top of the script
- Worked out a method to deal with ugly long hash name in upstream tarball
- %setup macro was unpacking source0 tarball multiple times. This has been fixed.
- More inline documentation of macros and shell commands.
- Fixed warnings about macros expanding in comments.

Modify README.md
- Updated build instructions.
- Included install instructions for openSUSE.

### Mon Aug 29 2022 Rankyn Bass <rankyn@proton.me>
First changelog entry for setting up for COPR.