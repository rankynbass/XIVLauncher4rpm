# Changelog
### Mon Mar 31 2025 Rankyn Bass <rankyn@proton.me>
1.1.2-2
- Use XIVLauncher.Core-fedora.tar.gz from goatcorp repo instead of compiling

### Tue Mar 19 2024 Rankyn Bass <rankyn@proton.me>
1.0.8-2
- Get rid of overly complicated launcher script.
- Make it no longer conflict with -RB package.
- Move to /opt/xivlauncher instead of /opt/XIVLauncher
- Renamed primary launcher script to /usr/bin/xivlauncher-core to match other distros.

### Sun Jun 18 2023 Rankyn Bass <rankyn@proton.me>
Updated to 1.0.4-3. Fixed a bug that would prevent launching if wine had not already been downloaded.

### Sat Jun 17 2023 Rankyn Bass <rankyn@proton.me>
Updated to 1.0.4-2. There's a few minor fixes. Dalamud plugins might work better, now.

### Sat Jun 17 2023 Rankyn Bass <rankyn@proton.me>
Updated to version 1.0.4

### Sat Jan 14 2023 Rankyn Bass <rankyn@proton.me>
Updated to version 1.0.3

### Mon Nov 28 2022 Rankyn Bass <rankyn@proton.me>
Release bumped to 6

Updated the xivlauncher script. It has some management features built in
- It will create .desktop files for your custom scripts in `~/.local/share/applications` (or the $XDG_DATA_HOME directory if that is set).
- You can list scripts with -l, delete with -d <script>, and refresh (to default) with -r <script>.
- There is some basic sanity parsing, but not too much. You can break this if you try. I'm not responsible if you do.

Updated the submodule to the xlcore removed commit. This cuts the source size in half, which means I went back to using tar.gz instead of tar.xz. This doesn't change functionality at all.

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