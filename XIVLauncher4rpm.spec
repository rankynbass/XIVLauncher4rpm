# SPEC file for compiling a native version of XIVLauncher for rpm-based distros
# This file has a lot of extra comments, mostly to keep track of what I've learned.
#
# Here's a few docs I've found very helpful:
# http://ftp.rpm.org/max-rpm/s1-rpm-inside-macros.html
# https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html-single/RPM_Guide/index.html
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
# https://docs.fedoraproject.org/en-US/legal/license-field/

# COMPATABILITY
# This should work on current fedora releases, the latest opensuse leap, and opensuse tumbleweed.
# Enterprise Linux (Rocky, RedHad, Centos Stream, etc) Requires out-of-tree packages.
# Get here: https://copr.fedorainfracloud.org/coprs/rankyn/xl-deps-el9/

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
# Original Versioning: a.b.c.d-r
# Epoch 1  Versioning: a.b.c-r
Epoch:          1
Summary:        Custom Launcher for the MMORPG Final Fantasy XIV
License:        GPL-3.0-only
URL:            https://github.com/rankynbass/XIVLauncher4rpm
Source0:        XIVLauncher.Core-%{xlversion}.tar.gz
Source1:        XIVLauncher4rpm-%{DownstreamTag}.tar.gz

# These package names are from the fedora / redhat repos. Other rpm distros might
# have different names for these.
# (x or y) has been used where fedora and opensuse have different package names (fedora-pkg or opensuse-pkg).
BuildRequires:  patchelf
Requires:       aria2
Requires:       (SDL3 or llibSDL3-0)
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
Requires:       desktop-file-utils
Provides:       %{xlname}

# There isn't any linux / rpm debug info available with the source git
%global debug_package %{nil}

# Turn off binary stripping, otherwise the binary breaks.
%global __os_install_post %{nil}

# Turn off build_id links to prevent conflict with main XIVLauncher package.
%define _build_id_links none

%description
Third-party launcher for the critically acclaimed MMORPG Final Fantasy XIV.

### PREP SECTION
# Be aware that rpmbuild DOES NOT download sources from urls. It expects the source files to be in the %%{_sourcedir} directory.
# Run the script .copr/getsources.sh to download tarballs to the appropriate locations. 
%prep
# Set some short names for convenience.
%define repo0 XIVLauncher.Core
%define repo1 XIVLauncher4rpm-%{DownstreamTag}

# Unpack source0. -c tells it to create the directory, -n tells the macro the name of the folder.
%setup -c -n %{repo0}
# Now unpack the files from the second source into a folder. -T to prevent source0 from unpacking.
# -b 1 tells it to unpack source1, and -n tells it the name of the folder.
%setup -T -b 1 -n %{repo1}

### BUILD SECTION
# Using this section to fix the libSDL3_image.so file so RPM will build
%build
cd %{_builddir}/%{repo0}
patchelf --remove-rpath libSDL3_image.so

### INSTALL SECTION
%install
install -d "%{buildroot}%{_bindir}"
install -d "%{buildroot}/opt/xivlauncher"
install -d "%{buildroot}%{_datadir}/applications"
install -D -m 644 "%{_builddir}/%{repo1}/xivlauncher.png" "%{buildroot}%{_datadir}/pixmaps/dev.goats.xivlauncher.png"
cp -r "%{_builddir}/%{repo0}"/* "%{buildroot}/opt/xivlauncher"
cp -r "%{_builddir}/%{repo1}"/* "%{buildroot}/opt/xivlauncher"
ln -sr "%{buildroot}/opt/xivlauncher/XIVLauncher.Core" "%{buildroot}/%{_bindir}/xivlauncher-core"
mv "%{buildroot}/opt/xivlauncher/XIVLauncher.desktop" "%{buildroot}/%{_datadir}/applications/XIVLauncher.desktop"

%pre

%post
echo -e "The primary launcher script is now /usr/bin/xivlauncher-core instead of xivlauncher."
echo -e "This brings it in line with the naming scheme used in Debian/Ubuntu and Arch."
echo -e "Modified SSL settings are no longer needed, so you can run"
echo -e "/opt/xivlauncher/XIVLauncher.Core directly if you choose."

%preun

%postun
if [ "$1" = "0" ]; then
    echo -e "Reminder: Removing this package does not remove your ~/.xlcore folder or"
    echo -e "uninstall the FFXIV game files. There may also be xivlauncher-*.sh scripts in"
    echo -e "~/.local/bin and XIVLauncher-*.desktop files in ~/.local/share/applications"
    echo -e "that you will have to remove manually from older versions of this package.\n"
fi

### FILES SECTION
%files
%license /opt/xivlauncher/COPYING
%doc /opt/xivlauncher/CHANGELOG.md
%doc /opt/xivlauncher/README.md
%{_bindir}/xivlauncher-core
%{_datadir}/applications/XIVLauncher.desktop
%{_datadir}/pixmaps/dev.goats.xivlauncher.png
/opt/xivlauncher/

%changelog
* Thu Feb 26 2026 Tarulia <mihawk.90+git@googlemail.com>
- removed unused, discouraged, and deprecated Group tag
- removed unused macro definition
- removed reference to F36 from Description
- use RPM macros instead of absolute paths in install section
- removed wrapper shellscript and symlinked binary directly
- move .desktop file instead of symlinking it
- rename application icon to match official Flatpak
- proper doc and license tags for RPM payload data
- package directory instead of individual file list

* Mon Mar 31 2025 Rankyn Bass <rankyn@proton.me>
- See CHANGELOG.md
