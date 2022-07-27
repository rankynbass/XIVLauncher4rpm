# SPEC file for compiling a native version of XIVLauncher for rpm-based distros
# Currently only tested with Fedora 36.

# Pick a tag to pull from the main repo -- master will pull the latest version,
# but this can also be set to any tag in the repo (for example, 6.2.43)
%define UpstreamTag master

Name:           XIVLauncher
Version:        1.0.0.9
Release:        1
Summary:        Custom Launcher for the MMORPG Final Fantasy XIV (Fedora native version)
License:        GPLv3
URL:            https://github.com/goatcorp/FFXIVQuickLauncher
Source0:        https://github.com/goatcorp/FFXIVQuickLauncher/archive/%{UpstreamTag}.tar.gz
Source1:        https://github.com/rankynbass/XIVLauncher4rpm/archive/XIVLauncher-%{version}-%{release}.tar.gz

# These package names are from the fedora / redhat repos. Other rpm distros might
# have different names for these.
BuildRequires:  dotnet-sdk-6.0
BuildRequires:  git
Requires:       aria2
Requires:       SDL2
Requires:       libsecret
Requires:       libattr
Requires:       fontconfig
Requires:       lcms2
Requires:       libXcursor
Requires:       libXrandr
Requires:       libXdamage
Requires:       libXi
Requires:       gettext
Requires:       freetype
Requires:       mesa-libGLU
Requires:       libSM
Requires:       libgcc
Requires:       libpcap
Requires:       libFAudio
Requires:       desktop-file-utils
Requires:       jxrlib

# There isn't any linux / rpm debug info available with the source git
%global debug_package %{nil}
# Turn off binary stripping, otherwise the binary breaks.
%global __os_install_post %{nil}
# Binaries will be deposited into this directory. Macro'd for convenience.
%define launcher %{_builddir}/output

%description
Third-party launcher for the critically acclaimed MMORPG Final Fantasy XIV. This is a native build for fedora 36 and possibly other rpm based distos.

# PREP SECTION
# Be aware that rpmbuild DOES NOT download sources from urls. It expects the source files
# to be in the SOURCES folder. Use 'spectool -g -R XIVLauncher4rpm.spec' before running
# rpmbuild.
%prep
# The official repo is used for Source0, so unpack that first.
%setup -b 0 -n FFXIVQuickLauncher-%{UpstreamTag}
# Now unpack the extra files from this repo into a folder
%setup -b 1 -n XIVLauncher4rpm

# BUILD SECTION
%build
mkdir -p %{launcher}
cd %{_builddir}/FFXIVQuickLauncher-%{UpstreamTag}
# initialize a git archive. Otherwise build will fail.
git init
git add .
git commit -m "work around bug needing git repo to build"
cd src/XIVLauncher.Core
dotnet publish -r linux-x64 --sc -o "%{launcher}" --configuration Release
cp ../../misc/linux_distrib/512.png %{launcher}/xivlauncher.png
cd %{_builddir}/XIVLauncher4rpm
cp openssl_fix.cnf xivlauncher.sh XIVLauncher.desktop %{launcher}/

# INSTALL SECTION
%install
install -d "%{buildroot}/usr/bin"
install -d "%{buildroot}/opt/XIVLauncher"
install -D -m 644 "%{launcher}/XIVLauncher.desktop" "%{buildroot}/usr/share/applications/XIVLauncher.desktop"
install -D -m 644 "%{launcher}/xivlauncher.png" "%{buildroot}/usr/share/pixmaps/xivlauncher.png"
cp -r "%{launcher}"/* "%{buildroot}/opt/XIVLauncher"
cd %{buildroot}
ln -sr "opt/XIVLauncher/xivlauncher.sh" "usr/bin/xivlauncher"

%clean
rm -rf %{buildroot}

%files
/usr/bin/xivlauncher
/usr/share/applications/XIVLauncher.desktop
/usr/share/pixmaps/xivlauncher.png
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


