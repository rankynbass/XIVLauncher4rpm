# SPEC file for compiling a native version of XIVLauncher for rpm-based distros
# This file has a lot of extra comments, mostly to keep track of what I've learned.
#
# Here's a few docs I've found very helpful:
# http://ftp.rpm.org/max-rpm/s1-rpm-inside-macros.html
# https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html-single/RPM_Guide/index.html
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
# https://docs.fedoraproject.org/en-US/legal/license-field/

# COMPATABILITY
# I've tested on the following distros. It will at least install, launch, and log in, although I haven't installed
# or played FFXIV on all of them.
# Fedora - 35 and 36
# OpenSuse - Leap 15.3 and 15.4, and Tumbleweed
# Rocky Linux 9 - Requires out-of-tree packages. Get here: https://copr.fedorainfracloud.org/coprs/rankyn/xl-deps-el9/

# Version File Source
# I've put it here because I need it declared before it's used in some definitions. And it's Source2 because I'm
# not going to renumber them.
Source2:        _version

# DEFINITIONS
# Repo tags are now pulled from the _version file, so it only has to be changed in one place.
# This is why sources were declared above.
%define xlname %(awk 'NR==1 {print; exit}' < %{SOURCE2} )
%define CoreTag %(awk 'NR==3 {print; exit}' < %{SOURCE2} )
%define LauncherTag %(awk 'NR==5 {print; exit}' < %{SOURCE2} )
%define xlversion %(awk 'NR==6 {print; exit}' < %{SOURCE2} )
%define xlrelease %(awk 'NR==7 {print; exit}' < %{SOURCE2} )
%define DownstreamTag %{xlversion}-%{xlrelease}

Name:           %{xlname}
Version:        %{xlversion}
Release:        %{xlrelease}%{?dist}
Summary:        Custom Launcher for the MMORPG Final Fantasy XIV (Native RPM package)
Group:          Applications/Games
License:        GPL-3.0-only
URL:            https://github.com/rankynbass/XIVLauncher4rpm
Source0:        XIVLauncher.Core-%{CoreTag}.tar.gz
Source1:        XIVLauncher4rpm-%{DownstreamTag}.tar.gz

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
Provides:       %{xlname}
Conflicts:      XIVLauncher-testing

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
%define repo0 XIVLauncher.Core
%define repo1 XIVLauncher4rpm-%{DownstreamTag}

# Unpack source0. -n tells the macro the name of the folder.
%setup -n %{repo0}
# Now unpack the files from the second source into a folder. -T to prevent source0 from unpacking.
# -b 1 tells it to unpack source1, and -n tells it the name of the folder.
%setup -T -b 1 -n %{repo1}


### BUILD SECTION
%build
# We need to pass two extra -p switches to dotnet publish. The first sets the version of wine to download, and the second sets
# the build hash and prevents the compiler from trying to do a git describe to create or find one. This eliminates git as a
# build requirement (and dirty hack of doing git init) and drastically speeds up the compile.
cd %{_builddir}/%{repo0}
cd %{_builddir}/%{repo0}/src/XIVLauncher.Core
dotnet publish -r linux-x64 --sc -o "%{_builddir}/%{repo1}" --configuration Release -p:Version=%{xlversion} -p:DefineConstants=WINE_XIV_FEDORA_LINUX -p:BuildHash="r%{xlrelease}-%{CoreTag}"
cp ../../misc/linux_distrib/512.png %{_builddir}/%{repo1}/xivlauncher.png
cp ../../misc/header.png %{_builddir}/%{repo1}/xivlogo.png
cd %{_builddir}/%{repo1}

### INSTALL SECTION
%install
install -d "%{buildroot}/usr/bin"
install -d "%{buildroot}/opt/XIVLauncher"
install -d "%{buildroot}/usr/share/doc/xivlauncher"
install -d "%{buildroot}/usr/share/applications"
install -D -m 644 "%{_builddir}/%{repo1}/xivlauncher.png" "%{buildroot}/usr/share/pixmaps/xivlauncher.png"
cp -r "%{_builddir}/%{repo1}"/* "%{buildroot}/opt/XIVLauncher"
cp %{buildroot}/opt/XIVLauncher/COPYING %{buildroot}/usr/share/doc/xivlauncher/COPYING
cd %{buildroot}
ln -sr "opt/XIVLauncher/xivlauncher.sh" "usr/bin/xivlauncher"
ln -sr "opt/XIVLauncher/XIVLauncher.desktop" "usr/share/applications/XIVLauncher.desktop"

%pre

%post
echo -e "To clean your .xlcore profile when switching from flatpak to native XIVLauncher,"
echo -e "you should run the script /opt/XIVLauncher/cleanupprofile.sh. Do not run with"
echo -e "sudo. This should *not* be done if you are using a custom wine install.\n"
echo -e "The /usr/bin/xivlauncher script will simply launch XIVLauncher.Core with the"
echo -e "proper SSL settings. It can be also be used to create custom scripts by using it"
echo -e "like so:\n"
echo -e "    xivlauncher <script>\n"
echo -e "The custom script will be named ~/.local/bin/xivlauncher-<script>.sh. You can"
echo -e "edit this script to add environment variables and call other programs. For"
echo -e "example, you could use it to call gamescope or launch an IPC bridge for discord."
echo -e "This script file will not be changed when you upgrade, so your changes will be"
echo -e "saved. This will also create a .desktop file in ~/.local/share/applications."

%preun

%postun
if [ "$1" = "0" ]; then
    echo -e "Reminder: Removing this package does not remove your ~/.xlcore folder or"
    echo -e "uninstall the FFXIV game files. There may also be xivlauncher-*.sh scripts in"
    echo -e "~/.local/bin and XIVLauncher-*.desktop files in ~/.local/share/applications"
    echo -e "that you will have to remove manually.\n"
    echo -e "If you are planning to use the flatpak version of XIVLauncher, you should"
    echo -e "delete the '~/.xlcore/compatibilitytool' folder."
fi

### FILES SECTION
%files
/usr/bin/xivlauncher
/usr/share/applications/XIVLauncher.desktop
/usr/share/pixmaps/xivlauncher.png
/opt/XIVLauncher/CHANGELOG.md
/opt/XIVLauncher/cleanupprofile.sh
/opt/XIVLauncher/COPYING
/opt/XIVLauncher/libcimgui.so
/opt/XIVLauncher/libskeychain.so
/opt/XIVLauncher/libsteam_api64.so
/opt/XIVLauncher/openssl_fix.cnf
/opt/XIVLauncher/README.md
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
# See CHANGELOG.md