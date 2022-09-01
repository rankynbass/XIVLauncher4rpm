# SPEC file for compiling a native version of XIVLauncher for rpm-based distros
# Currently only tested with Fedora 36.

Name:           XIVLauncher
Version:        1.0.1.0
Release:        2
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
# *{VERSION}-*{RELEASE} should be used in most cases.
%define DownstreamTag %{VERSION}-%{RELEASE}
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

# PREP SECTION
# Be aware that rpmbuild DOES NOT download sources from urls. It expects the source files
# to be in the SOURCES folder. That's why we're pulling from git repos and then archiving.
%prep
%define repo0 FFXIVQuickLauncher-%{UpstreamTag}
if [ ! -f "%{_sourcedir}/%{repo0}.tar.gz" ];
then
#   If the tarball is missing, clone the git repo. Then checkout the appropriate tag / commit, and build a tarball
#   for making the src.rpm
    echo "No source file found! Creating..."
    cd %{_builddir}
    rm -rf %{repo0}
    git clone https://github.com/goatcorp/FFXIVQuickLauncher
    mv FFXIVQuickLauncher %{repo0}
    cd %{repo0}
    git checkout %{UpstreamTag}
    git archive --format=tar.gz -o %{_sourcedir}/%{repo0}.tar.gz --prefix=%{repo0}/ HEAD
else
#   If the tarball is present (for example, if building from src.rpm), unzip it, then set up a git repo to
#   work around a build bug in the source. Can't use setup macro because rpmbuild will fail if there's no
#   source files present and the macro is present, even if it wouldn't be used.
    cd %{_builddir}
    rm -rf %{repo0}
    gzip -dc %{_sourcedir}/%{repo0}.tar.gz | tar -xvvf -
    if [ $? -ne 0 ]; then
        exit $?
    fi
    cd %{_builddir}/%{repo0}
    git init
    git add .
    git commit -m "Working around build bug"
fi

%define repo1 XIVLauncher4rpm-%{DownstreamTag}
if [ ! -f "%{_sourcedir}/%{repo1}.tar.gz" ];
then
    echo "No source file found! Creating..."
    cd %{_builddir}
    rm -rf %{repo1}
    git clone https://github.com/rankynbass/XIVLauncher4rpm
    mv XIVLauncher4rpm %{repo1}
    cd %{repo1}
    git checkout %{DownstreamTag}
    git archive --format=tar.gz -o %{_sourcedir}/%{repo1}.tar.gz --prefix=%{repo1}/ HEAD
else
    cd %{_builddir}
    rm -rf %{repo1}
    gzip -dc %{_sourcedir}/%{repo1}.tar.gz | tar -xvvf -
    if [ $? -ne 0 ]; then
        exit $?
    fi
fi

# BUILD SECTION
%build
rm -rf %{launcher}
mkdir -p %{launcher}
cd %{_builddir}/%{repo0}/src/XIVLauncher.Core
dotnet publish -r linux-x64 --sc -o "%{launcher}" --configuration Release -p:DefineConstants=WINE_XIV_FEDORA_LINUX
cp ../../misc/linux_distrib/512.png %{launcher}/xivlauncher.png
cd %{_builddir}/%{repo1}
cp openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop COPYING %{launcher}/

# INSTALL SECTION
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

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{repo0}
rm -rf %{_builddir}/%{repo1}
rm -rf %{_builddir}/%{launcher}

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
%license /usr/share/doc/xivlauncher/COPYING