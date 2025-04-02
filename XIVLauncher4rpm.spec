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
%define xlversion %(awk 'NR==3 {print; exit}' < %{SOURCE2} )
%define xlrelease %(awk 'NR==4 {print; exit}' < %{SOURCE2} )
%define DownstreamTag %{xlversion}-%{xlrelease}

Name:           %{xlname}
Version:        %{xlversion}
Release:        %{xlrelease}%{?dist}
Epoch:          1
Summary:        Custom Launcher for the MMORPG Final Fantasy XIV (Native RPM package)
Group:          Applications/Games
License:        GPL-3.0-only
URL:            https://github.com/rankynbass/XIVLauncher4rpm
Source0:        XIVLauncher-RB-%{xlversion}.tar.gz
Source1:        XIVLauncher4rpm-rb-v%{DownstreamTag}.tar.gz

# These package names are from the fedora / redhat repos. Other rpm distros might
# have different names for these.
# (x or y) has been used where fedora and opensuse have different package names (fedora-pkg or opensuse-pkg).
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
Requires:       (freetype or libfreetype6)
Requires:       (mesa-libGLU or libGLU1)
Requires:       (libSM or libSM6)
Requires:       (libgcc or libgcc_s1)
Requires:       (libpcap or libpcap1)
Requires:       (libFAudio or libFAudio0)
Requires:       desktop-file-utils
Requires:       zstd
Provides:       %{xlname}

# There isn't any linux / rpm debug info available with the source git
%global debug_package %{nil}

# Turn off binary stripping, otherwise the binary breaks.
%global __os_install_post %{nil}

# Turn off build_id links to prevent conflict with main XIVLauncher package.
%define _build_id_links none

# Binaries will be deposited into this directory. Macro'd for convenience.
%define launcher %{_builddir}/XIVLauncher

%description
Third-party launcher for the critically acclaimed MMORPG Final Fantasy XIV. This is a native build for fedora 36 and several other rpm based distos.

### PREP SECTION
# Be aware that rpmbuild DOES NOT download sources from urls. It expects the source files to be in the %%{_sourcedir} directory.
# Run the script .copr/getsources.sh to download tarballs to the appropriate locations. 
%prep
# Set some short names for convenience.
%define repo0 XIVLauncher-RB
%define repo1 XIVLauncher4rpm-rb-v%{DownstreamTag}

# Unpack source0. -c tells it to create the directory, -n tells the macro the name of the folder.
%setup -c -n %{repo0}
# Now unpack the files from the second source into a folder. -T to prevent source0 from unpacking.
# -b 1 tells it to unpack source1, and -n tells it the name of the folder.
%setup -T -b 1 -n %{repo1}

### BUILD SECTION
# This is no longer done. The pre-built tarball from https://github.com/rankynbass/XIVLauncher.Core is used instead.

### INSTALL SECTION
%install
install -d "%{buildroot}/usr/bin"
install -d "%{buildroot}/opt/xivlauncher-rb"
install -d "%{buildroot}/usr/share/doc/xivlauncher-rb"
install -d "%{buildroot}/usr/share/applications"
install -D -m 644 "%{_builddir}/%{repo1}/xivlauncher.png" "%{buildroot}/usr/share/pixmaps/xivlauncher-rb.png"
rm -f "%{_builddir}/%{repo0}"/openssl_fix.cnf
cp -r "%{_builddir}/%{repo0}"/* "%{buildroot}/opt/xivlauncher-rb"
cp -r "%{_builddir}/%{repo1}"/* "%{buildroot}/opt/xivlauncher-rb"
cp %{buildroot}/opt/xivlauncher-rb/COPYING %{buildroot}/usr/share/doc/xivlauncher-rb/COPYING
cd %{buildroot}
ln -sr "opt/xivlauncher-rb/xivlauncher.sh" "usr/bin/xivlauncher-rb"
ln -sr "opt/xivlauncher-rb/XIVLauncher.desktop" "usr/share/applications/XIVLauncher-RB.desktop"

%pre

%post
echo -e "\nModified SSL settings are no longer needed, so you can run"
echo -e "/opt/xivlauncher/XIVLauncher.Core directly if you choose."
echo -e "/usr/bin/xivlauncher-rb is still provided."

%preun

%postun
if [ "$1" = "0" ]; then
    echo -e "\nReminder: Removing this package does not remove your ~/.xlcore folder or"
    echo -e "uninstall the FFXIV game files. There may also be xivlauncher-*.sh scripts in"
    echo -e "~/.local/bin and XIVLauncher-*.desktop files in ~/.local/share/applications"
    echo -e "that you will have to remove manually from older versions of this package."
fi

### FILES SECTION
%files
/usr/bin/xivlauncher-rb
/usr/share/applications/XIVLauncher-RB.desktop
/usr/share/pixmaps/xivlauncher-rb.png
/opt/xivlauncher-rb/CHANGELOG.md
/opt/xivlauncher-rb/COPYING
/opt/xivlauncher-rb/libcimgui.so
/opt/xivlauncher-rb/libskeychain.so
/opt/xivlauncher-rb/libsteam_api64.so
/opt/xivlauncher-rb/README.md
/opt/xivlauncher-rb/xivlauncher.sh
/opt/xivlauncher-rb/xivlauncher.png
/opt/xivlauncher-rb/XIVLauncher.Common.pdb
/opt/xivlauncher-rb/XIVLauncher.Common.Unix.pdb
/opt/xivlauncher-rb/XIVLauncher.Common.Unix.xml
/opt/xivlauncher-rb/XIVLauncher.Common.Windows.pdb
/opt/xivlauncher-rb/XIVLauncher.Common.Windows.xml
/opt/xivlauncher-rb/XIVLauncher.Common.xml
/opt/xivlauncher-rb/XIVLauncher.Core
/opt/xivlauncher-rb/XIVLauncher.Core.pdb
/opt/xivlauncher-rb/XIVLauncher.Core.xml
/opt/xivlauncher-rb/XIVLauncher.desktop
/opt/xivlauncher-rb/xivlogo.png
%license /usr/share/doc/xivlauncher-rb/COPYING

%changelog
* Tue Apr 01 2025 Rankyn Bass <rankyn@proton.me>
- See CHANGELOG.md
