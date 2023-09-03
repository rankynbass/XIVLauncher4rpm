# Changelog
### Sun Sep 03 2023 Rankyn Bass <rankyn@proton.me>
Updated with latest compatibility-rework-2 patches. No proton. This should be very close to the eventual 1.0.5.

### Sat Jun 24 2023 Rankyn Bass <rankyn@proton.me>
Updated to 1.0.4, and added my compatibility rework patch, proton edition. Proton should now be a working option. 

### Sat Jun 03 2023 Rankyn Bass <rankyn@proton.me>
Updated xivlauncher-git to start using my xlcore-testing branch. I'm now using 1.0.3 as a base, with all relevant pull requests to XIVLauncher.Core and FFXIVQuickLauncher repos.

From [XIVLauncher.Core](https://github.com/goatcorp/XIVLauncher.Core)

[PR #17](https://github.com/goatcorp/XIVLauncher.Core/pull/17): add DXVK settings tab
- Allow switching Dxvk versions from 1.10.1 - 1.10.3 and 2.0 - 2.2. You can also disable Dxvk and use OpenGL instead.
- Add MangoHud support
- Allow custom DxvkHud strings
- Limit frame rate

[PR #28](https://github.com/goatcorp/XIVLauncher.Core/pull/28): Launch without 3rd party plugins

[PR #31](https://github.com/goatcorp/XIVLauncher.Core/pull/31): Implement auto-start for pre- and post-game launch
- Allows launching of linux programs / shell scripts from pre- and post- options
- Allows launching of windows programs / scripts from pre-wine and post-wine options

[PR #32](https://github.com/goatcorp/XIVLauncher.Core/pull/32): Add troubleshooting options
- Add a troubleshooting tab with a bunch of options for clearing parts of the .xlcore folder
- Add environment variables for troubleshooting (XL_DECK={0 or 1} is probably most useful)
- Allows environment variables to be passed in the "Additional Arguments" field

[PR #40](https://github.com/goatcorp/XIVLauncher.Core/pull/40): UI/UX Adjustments - featuring a much-improved Debug tab!

[PR #41](https://github.com/goatcorp/XIVLauncher.Core/pull/41): Fix: IsIgnoringSteam problems on Steam Deck

From [FFXIVQuickLauncher](https://github.com/goatcorp/FFXIVQuickLauncher)

[PR #1205](https://github.com/goatcorp/FFXIVQuickLauncher/pull/): Dxvk settings rework

[PR #1257](https://github.com/goatcorp/FFXIVQuickLauncher/pull/1257): Implement Run functions on the runners

[PR #1316](https://github.com/goatcorp/FFXIVQuickLauncher/pull/1316): Allow patched versions of proton-wine to work, and improve compatibility with unpatched wine.

[PR #1332](https://github.com/goatcorp/FFXIVQuickLauncher/pull/1332): Update Mac video patch to 1.1.2, since 1.0.8 has been removed from the CDN.

[PR #1333](https://github.com/goatcorp/FFXIVQuickLauncher/pull/1333): Update the managed wine to the latest from wine-xiv-git (8.5.r4.g4211bac7)

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