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
# not going to renumber them. Why? Because %%setup macros, that's why.
Source2:        _version

# DEFINITIONS
# Repo tags are now pulled from the _version file, so it only has to be changed in one place.
# This is why sources were declared above.
%define UpstreamTag %(awk 'NR==2 {print; exit}' < %{SOURCE2} )
%define xlversion %(awk 'NR==3 {print; exit}' < %{SOURCE2} )
%define xlrelease %(awk 'NR==4 {print; exit}' < %{SOURCE2} )
%define DownstreamTag %{xlversion}-%{xlrelease}

Name:           XIVLauncher-git
Version:        %{xlversion}
Release:        %{xlrelease}%{?dist}
Summary:        Custom Launcher for the MMORPG Final Fantasy XIV (Native RPM package)
Group:          Applications/Games
License:        GPL-3.0-only
URL:            https://github.com/rankynbass/XIVLauncher4rpm
Source0:        FFXIVQuickLauncher-%{UpstreamTag}.tar.gz
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
Provides:       xivlauncher-git

# There isn't any linux / rpm debug info available with the source git
%global debug_package %{nil}

# Turn off binary stripping, otherwise the binary breaks.
%global __os_install_post %{nil}

# Binaries will be deposited into this directory. Macro'd for convenience.
%define launcher %{_builddir}/XIVLauncher

# Turn off .build-id links so it doesn't conflict with the main package.
%global _build_id_links none

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
# We need to pass two extra -p switches to dotnet publish. The first sets the version of wine to download, and the second sets
# the build hash and prevents the compiler from trying to do a git describe to create or find one. This eliminates git as a
# build requirement (and dirty hack of doing git init) and drastically speeds up the compile.
cd %{_builddir}/%{repo0}
cd %{_builddir}/%{repo0}/src/XIVLauncher.Core
dotnet publish -r linux-x64 --sc -o "%{_builddir}/%{repo1}" --configuration Release -p:DefineConstants=WINE_XIV_FEDORA_LINUX -p:Version=%{xlversion} -p:BuildHash="git-%{UpstreamTag}"
cp ../../misc/linux_distrib/512.png %{_builddir}/%{repo1}/xivlauncher.png
cp ../../misc/header.png %{_builddir}/%{repo1}/xivlogo.png
cd %{_builddir}/%{repo1}

### INSTALL SECTION
%install
install -d "%{buildroot}/usr/bin"
install -d "%{buildroot}/opt/XIVLauncher-git"
install -d "%{buildroot}/usr/share/doc/xivlauncher-git"
install -d "%{buildroot}/usr/share/applications"
install -D -m 644 "%{_builddir}/%{repo1}/xivlauncher.png" "%{buildroot}/usr/share/pixmaps/xivlauncher-git.png"
cp -r "%{_builddir}/%{repo1}"/* "%{buildroot}/opt/XIVLauncher-git"
cp %{buildroot}/opt/XIVLauncher-git/COPYING %{buildroot}/usr/share/doc/xivlauncher-git/COPYING
cd %{buildroot}
ln -sr "opt/XIVLauncher-git/xivlauncher.sh" "usr/bin/xivlauncher-git"
ln -sr "opt/XIVLauncher-git/XIVLauncher.desktop" "usr/share/applications/XIVLauncher-git.desktop"

%pre

%post
echo "To clean your .xlcore profile when switching from flatpak to native XIVLauncher, you should run the script /opt/XIVLauncher-git/cleanupprofile.sh. Do not run with sudo."
echo "This should *not* be done if you are using a custom wine install."

%preun

%postun
echo "If you are planning to use the flatpak version of XIVLauncher, you should delete the '~/.xlcore/compatibilitytool' folder. You can also safely remove '~/.xlcore/_old_compat'."

### CLEAN SECTION
# This is mostly for local builds. chroot build environments usually just destroy all the extra files when done.
%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

### FILES SECTION
%files
/usr/bin/xivlauncher-git
/usr/share/applications/XIVLauncher-git.desktop
/usr/share/pixmaps/xivlauncher-git.png
/opt/XIVLauncher-git/cleanupprofile.sh
/opt/XIVLauncher-git/COPYING
/opt/XIVLauncher-git/libcimgui.so
/opt/XIVLauncher-git/libskeychain.so
/opt/XIVLauncher-git/libsteam_api64.so
/opt/XIVLauncher-git/openssl_fix.cnf
/opt/XIVLauncher-git/xivlauncher.sh
/opt/XIVLauncher-git/xivlauncher.png
/opt/XIVLauncher-git/XIVLauncher.Common.pdb
/opt/XIVLauncher-git/XIVLauncher.Common.Unix.pdb
/opt/XIVLauncher-git/XIVLauncher.Common.Unix.xml
/opt/XIVLauncher-git/XIVLauncher.Common.Windows.pdb
/opt/XIVLauncher-git/XIVLauncher.Common.Windows.xml
/opt/XIVLauncher-git/XIVLauncher.Common.xml
/opt/XIVLauncher-git/XIVLauncher.Core
/opt/XIVLauncher-git/XIVLauncher.Core.pdb
/opt/XIVLauncher-git/XIVLauncher.Core.xml
/opt/XIVLauncher-git/XIVLauncher.desktop
/opt/XIVLauncher-git/xivlogo.png
%license /usr/share/doc/xivlauncher-git/COPYING

%changelog
# See CHANGELOG.md
