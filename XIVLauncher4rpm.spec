# SPEC file for compiling a native version of XIVLauncher for rpm-based distros
# This file has a lot of extra comments, mostly to keep track of what I've learned. It will also trigger
# some warnings about macros being expanded in comments. I don't really care about that, I'd rather see
# the name of a variable or macro exactly as I'm going to use it than avoid the warnings.
#
# Here's a few docs I've found very helpful:
# http://ftp.rpm.org/max-rpm/s1-rpm-inside-macros.html
# https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html-single/RPM_Guide/index.html
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/

## COMPATABILITY
# I've tested on the following distros. It will at least install and launch, although I haven't installed
# or played on all of them.
# Fedora - 35 and 36
# OpenSuse - Leap 15.4 and Tumbleweed

Name:           XIVLauncher
Version:        1.0.1.0
Release:        3
Summary:        Custom Launcher for the MMORPG Final Fantasy XIV (Fedora native version)
Group:          Applications/Games
License:        GPLv3
URL:            https://github.com/rankynbass/XIVLauncher4rpm

# Pick a tag, branch, or commit to checkout from the main repo -- master will pull the latest version,
# but this can also be set to any tag or commit in the repo (for example, 6.2.43)
# Using a version tag is useful for archival purposes -- the spec file will pull the same
# sources every time, as long as the tag doesn't change. Rebuilds will be consistant.
%define UpstreamTag 6246fde

# Pick a tag or branch to pull from XIVLauncher4rpm. "main" is used for the primary branch so that it doesn't
# have a name clash with the goatcorp repo. Mostly for my own sanity while testing.
# The canary branch will always have a spec file that just pulls the latest upstream git.
# %{VERSION}-%{RELEASE} should be used in most cases.
%define DownstreamTag copr-test
Source0:        FFXIVQuickLauncher-%{UpstreamTag}.tar.gz
Source1:        XIVLauncher4rpm-%{DownstreamTag}.tar.gz

# These package names are from the fedora / redhat repos. Other rpm distros might
# have different names for these.
# (x or y) has been used where fedora and opensuse have different package names (fedora-pkg or opensuse-pkg).
BuildRequires:  dotnet-sdk-6.0
BuildRequires:  git
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
Third-party launcher for the critically acclaimed MMORPG Final Fantasy XIV. This is a native build for fedora 36 and possibly other rpm based distos.

### PREP SECTION
# Be aware that rpmbuild DOES NOT download sources from urls. It expects the source files to be in the %{_sourcedir} directory.
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
rm -rf $longtag
cd %{_builddir}

# Now unpack the files from the second source into a folder. Again, -T to prevend source0 from unpacking.
# -b 1 tells it to unpack source1, and -n tells it the name of the folder.
%setup -T -b 1 -n %{repo1}


### BUILD SECTION
%build
rm -rf %{launcher}
mkdir -p %{launcher}

# Work around a build bug: it requires an active git repo.
cd %{_builddir}/%{repo0}
git init
git config user.name "COPRBuildUser"
git config user.email "COPRBuildUser@gmail.com"
git add .
git commit -m "Working around build bug"

# Now initialize dotnet publish to make the launcher.
cd %{_builddir}/%{repo0}/src/XIVLauncher.Core
dotnet publish -r linux-x64 --sc -o "%{launcher}" --configuration Release -p:DefineConstants=WINE_XIV_FEDORA_LINUX
cp ../../misc/linux_distrib/512.png %{launcher}/xivlauncher.png
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
/opt/XIVLauncher/xivlauncher.pnghttps://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
/opt/XIVLauncher/XIVLauncher.Common.Windows.pdb
/opt/XIVLauncher/XIVLauncher.Common.Windows.xml
/opt/XIVLauncher/XIVLauncher.Common.xml
/opt/XIVLauncher/XIVLauncher.Core
/opt/XIVLauncher/XIVLauncher.Core.pdb
/opt/XIVLauncher/XIVLauncher.Core.xml
/opt/XIVLauncher/XIVLauncher.desktop
%license /usr/share/doc/xivlauncher/COPYING