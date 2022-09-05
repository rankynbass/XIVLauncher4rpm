# SPEC file for compiling a native version of XIVLauncher for rpm-based distros
# This file has a lot of extra comments, mostly to keep track of what I've learned.
#
# Here's a few docs I've found very helpful:
# http://ftp.rpm.org/max-rpm/s1-rpm-inside-macros.html
# https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html-single/RPM_Guide/index.html
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
# https://docs.fedoraproject.org/en-US/legal/license-field/

# COMPATABILITY
# I've tested on the following distros. It will at least install and launch, although I haven't installed
# or played on all of them.
# Fedora - 35 and 36
# OpenSuse - Leap 15.4 and Tumbleweed

# SOURCES
Source0:        FFXIVQuickLauncher-%{UpstreamTag}.tar.gz
Source1:        XIVLauncher4rpm-%{DownstreamTag}.tar.gz
Source2:        _version

# DEFINITIONS
# Repo tags are now pulled from the _version file, so it only has to be changed in one place.
%define UpstreamTag %(awk 'NR==2 {print; exit}' < %{SOURCE2} )
%define xlversion %(awk 'NR==3 {print; exit}' < %{SOURCE2} )
%define xlrelease %(awk 'NR==4 {print; exit}' < %{SOURCE2} )
%define DownstreamTag %{xlversion}-%{xlrelease}

Name:           XIVLauncher
Version:        %{xlversion}
Release:        %{xlrelease}%{?dist}
Summary:        Custom Launcher for the MMORPG Final Fantasy XIV (Native RPM package)
Group:          Applications/Games
License:        GPL-3.0-only
URL:            https://github.com/rankynbass/XIVLauncher4rpm


# These package names are from the fedora / redhat repos. Other rpm distros might
# have different names for these.
# (x or y) has been used where fedora and opensuse have different package names (fedora-pkg or opensuse-pkg).
BuildRequires:  dotnet-sdk-6.0
Requires:       aria2
Requires:       (SDL2 or libSDL2-2_0-0)
Requires:       (libsecret or libsecret-1-0)
Requires:       (libattr or libattr1)
Requires:       fontconfig
Requires:       lcms2
Requires:       (libXcursor or libXcursor1)
Requires:       (libXrandr or libXrandr2)
Requires:       (libXdamage or libXdamage1)
Requires:       (libXi or libXi6)
Requires:       (gettext or gettext-runtime)
Requires:       freetype
Requires:       (mesa-libGLU or libGLU1)
Requires:       (libSM or libSM6)
Requires:       (libgcc or libgcc_s1)
Requires:       (libpcap or libpcap1)
Requires:       (libFAudio or libFAudio0)
Requires:       desktop-file-utils
Requires:       jxrlib

# There isn't any linux / rpm debug info available with the source git
%global debug_package %{nil}

# Turn off binary stripping, otherwise the binary breaks.
%global __os_install_post %{nil}

# Binaries will be deposited into this directory. Macro'd for convenience.
%define launcher %{_builddir}/XIVLauncher

%description
Third-party launcher for the critically acclaimed MMORPG Final Fantasy XIV. This is a native build for fedora 36 and several other rpm based distos.

### PREP SECTION
# Be aware that rpmbuild DOES NOT download sources from urls. It expects the source files to be in the %%{_sourcedir} directory.
# Run the script .copr/getsources.sh to download tarballs to the appropriate locations. 
%prep
# Set some short names for convenience.
%define repo0 FFXIVQuickLauncher-%{UpstreamTag}
%define repo1 XIVLauncher4rpm-%{DownstreamTag}

# All setup macro calls will first unpack source0. That's not what we want. So we use -T to supress that.
# Next, -a 0 tells it to unpack source 0 after changing directory, -c tells it
# to unpack as if there is no base directory in the tarball, and -n sets the name of the directory to unpack into.     
%setup -T -a 0 -c -n %{repo0}

# The tarball has the full commit hash as part of the path, which we have now unpacked into FFXIVQuickLauncher-<UpstreamTag>.
# So we're going to find this messy directory and then move its contents into the parent directory. We don't care
# about hidden (dot) files, so we wont do anything to grab them.
longtag=$(find -mindepth 1 -maxdepth 1 -type d)
mv $longtag/* .
cd %{_builddir}

# Now unpack the files from the second source into a folder. Again, -T to prevend source0 from unpacking.
# -b 1 tells it to unpack source1, and -n tells it the name of the folder.
%setup -T -b 1 -n %{repo1}


### BUILD SECTION
%build
rm -rf %{launcher}
mkdir -p %{launcher}

# We need to pass two extra -p switches to dotnet publish. The first sets the version of wine to download, and the second sets
# the build hash and prevents the compiler from trying to do a git describe to create or find one. This eliminates git as a
# build requirement (and dirty hack of doing git init) and drastically speeds up the compile.
cd %{_builddir}/%{repo0}
cd %{_builddir}/%{repo0}/src/XIVLauncher.Core
dotnet publish -r linux-x64 --sc -o "%{launcher}" --configuration Release -p:DefineConstants=WINE_XIV_FEDORA_LINUX -p:BuildHash=%{UpstreamTag}
cp ../../misc/linux_distrib/512.png %{launcher}/xivlauncher.png
cp ../../misc/header.png %{launcher}/xivlogo.png
cd %{_builddir}/%{repo1}
cp openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING %{launcher}/

### INSTALL SECTION
%install
install -d "%{buildroot}/usr/bin"
install -d "%{buildroot}/opt/XIVLauncher"
install -d "%{buildroot}/usr/share/doc/xivlauncher"
install -D -m 644 "%{launcher}/XIVLauncher.desktop" "%{buildroot}/usr/share/applications/XIVLauncher.desktop"
install -D -m 644 "%{launcher}/xivlauncher.png" "%{buildroot}/usr/share/pixmaps/xivlauncher.png"
cp -r "%{launcher}"/* "%{buildroot}/opt/XIVLauncher"
cp %{buildroot}/opt/XIVLauncher/COPYING %{buildroot}/usr/share/doc/xivlauncher/COPYING
cd %{buildroot}
ln -sr "opt/XIVLauncher/xivlauncher.sh" "usr/bin/xivlauncher"

### CLEAN SECTION
%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

### FILES SECTION
%files
/usr/bin/xivlauncher
/usr/share/applications/XIVLauncher.desktop
/usr/share/pixmaps/xivlauncher.png
/opt/XIVLauncher/COPYING
/opt/XIVLauncher/libcimgui.so
/opt/XIVLauncher/libskeychain.so
/opt/XIVLauncher/libsteam_api64.so
/opt/XIVLauncher/openssl_fix.cnf
/opt/XIVLauncher/xivlauncher.sh
/opt/XIVLauncher/xivlauncher.png
/opt/XIVLauncher/XIVLauncher.Common.pdb
/opt/XIVLauncher/XIVLauncher.Common.Unix.pdb
/opt/XIVLauncher/XIVLauncher.Common.Unix.xml
/opt/XIVLauncher/XIVLauncher.Common.Windows.pdb
/opt/XIVLauncher/XIVLauncher.Common.Windows.xml
/opt/XIVLauncher/XIVLauncher.Common.xml
/opt/XIVLauncher/XIVLauncher.Core
/opt/XIVLauncher/XIVLauncher.Core.pdb
/opt/XIVLauncher/XIVLauncher.Core.xml
/opt/XIVLauncher/XIVLauncher.desktop
/opt/XIVLauncher/xivlogo.png
%license /usr/share/doc/xivlauncher/COPYING

%changelog
* Sun Sep 04 2022 Rankyn Bass <rankyn@proton.me>
- Bump version-release to 1.0.1.0-4, because 3a is not > 3
- Added _version file. This contains UpstreamTag, Version, and Release.
- Modify getsources.sh
    - Build XIVLauncher4rpm tarball from local git clone.
    - Put in if statements for local builds.
    - Now gets UpstreamTag, DownstreamTag from _version file.
- Modify spec file
    - Now gets UpstreamTag, xlversion, and xlrelease from _version file.

* Sun Sep 04 2022 Rankyn Bass <rankyn@proton.me>
- Bump version-release to 1.0.1.0-3a
- Modify Makefile, getsources.sh
    - Remove wget, replace with curl
- Modify spec file
    - Add -p:BuildHash=UpstreamTag to prevent git describe.
    - Drop unneeded git build dependency
    - Drop git init section
    - Add xivlogo.png to install directory (from misc/header.png)

* Fri Sep 02 2022 Rankyn Bass <rankyn@proton.me>
- Bump version-release to 1.0.1.0-3
- Modify Makefile, add getsources script
    - No longer requires git. Now just needs wget.
    - Makefile now calls getsources.sh, which uses wget to download sources
    - getsources.sh MUST have matching UpstreamTag and DownstreamTag in spec file.
    - No longer call rpmbuild -bp, which should fix problems with building srpm.
- Modify spec file
    - Now works with downloaded sources instead of downloading with git during prep stage.
    - Reorganized importand definitions (%%define) to the top of the script
    - Worked out a method to deal with ugly long hash name in upstream tarball
    - %%setup macro was unpacking source0 tarball multiple times. This has been fixed.
    - More inline documentation of macros and shell commands.
    - Fixed warnings about macros expanding in comments.
- Modify README.md
    - Updated build instructions.
    - Included install instructions for openSUSE.

* Mon Aug 29 2022 Rankyn Bass <rankyn@proton.me>
- First changelog entry - setting up for COPR.
