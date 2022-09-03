# XIVLauncher4rpm

RPMs and build files for native versions of <a href=https://github.com/goatcorp/FFXIVQuickLauncher>FFXIVQuickLauncher</a>. Currently only tested on
Fedora 35, 36, openSUSE LEAP 15.4, and openSUSE Tumbleweed. It'll probably work for other distros as well, if you can work out the dependencies. Try at
your own risk (minimal as it probably is).

If you don't know what you're doing, I'd suggest following these instructions: <a href=https://goatcorp.github.io/faq/steamdeck>XIVLauncher Steam Deck
Installation Guide</a>. It says Steam Deck, but it should work for most Linux distibutions. Or get it directly from
<a href=https://flathub.org/apps/details/dev.goats.xivlauncher>Flathub</a>.

If you'd like to live on the edge, or the flatpak version is unsuitable for some reason, read on.

## Installation

### Important! If upgrading from 1.0.1.0-1 or earlier!

Starting with patch 1.0.1.0-2, there is a switch to using the Fedora-specific build of wine instead of using the default (which apparently targets
ubuntu). This might cause future issues with compatability, so just in case, you should delete the ~/.xlcore/compatabilitytool folder before installing
the new version. 

### Fedora 35+

You can now install from COPR. Simply open up a terminal and type

```
sudo dnf copr enable rankyn/xivlauncher
sudo dnf install XIVLauncher
```

Otherwise, download the rpm from the release section, and either install it by double-clicking in your graphical environment (or single-clicking if you
have it set that way), or open a terminal and use your package manager to install it. You do know what you're doing, right? In Fedora, the command is:

```
sudo dnf install <filename.rpm>
```

As a last resort, you could install it with

```
sudo rpm -i <filename.rpm>
```

But that might not play nice with your disto's package manager.

### openSUSE

I've only tested this on openSUSE LEAP 15.4 and Tumbleweed. Prior versions of LEAP might have different package names.
If that's the case, the rpm will probably complain about not finding anything to provide certain packages.

You can add the repo with zypper, and then install as you would any other package. I know it says tumbleweed, but it also works with LEAP 15.4.
```
sudo zypper addrepo -r https://copr.fedorainfracloud.org/coprs/rankyn/xivlauncher/repo/opensuse-tumbleweed/rankyn-xivlauncher-opensuse-tumbleweed.repo
sudo zypper install XIVLauncher
```
You'll get a message about accepting the signing key. Hit a to accept.

If you'd prefer to install manually, you can download the rpm from the release section and then do
```
sudo zypper install <filename.rpm>
```
Ignore the warning that the rpm is unsigned. I'm not going to bother with that, and you can avoid it by installing from the repo.

## Building it yourself

### Fedora 35+

**Setting up the environment**

By default, Fedora will want to build in `~/rpmbuild`. If it's somewhere different for your setup, replace ~/rpmbuild with your own build directory.
When you clone the git repository from github, DO NOT clone it into this folder, do it somewhere else. I'll use `~/build` for these instructions.

Download the required development packages:

```
sudo dnf rpmdevtools rpm-build
```

Set up the build directories if they don't already exist (`~/rpmbuild` and subfolders). Do NOT run with sudo:

```
rpmdev-setuptree
```

Install all the dependencies needed for the build. Theoretically this should be done by the rpmbuild tool, but it doesn't always work.

```
sudo dnf install aria2 SDL2 libsecret libattr fontconfig lcms2 libXcursor libXrandr libXdamage libXi gettext freetype mesa-libGLU libSM libgcc libpcap libFAudio desktop-file-utils jxrlib dotnet-sdk-6.0 git
```

**Compiling the code**

Now pull the source code.

```
mkdir -p ~/build
cd ~/build
git clone https://github.com/rankynbass/XIVLauncher4rpm.git
cd XIVLauncher4rpm
```
Now you can build the rpms. First, download the tarballs by using the included script, then build with rpmbuild. The third option is actually what the COPR
build system does. It uses .copr/Makefile to install dependencies for making the binary, then calls the getsources script, then executes rpmbuild -bs. It
then passes the src.rpm off to the various build environments for different distros. However, even if you have src.rpms, you still need to have internet
access. The dotnet publish command needs to grab some remote packages. For manual builds, thats obviously not an issue, since you just cloned the repo.
But for remote builds with copr, or with opensuse's OBS (I haven't tried this one yet), you'll need to make sure the builder has internet access.

```
.copr/getsources.sh
rpmbuild -ba XIVLauncher4rpm.spec   # Build binary and source rpms
#   OR
rpmbuild -bb XIVLauncher4rpm.spec   # Build binary only
#   OR
rpmbuild -bs XIVLauncher4rpm.spec   # Build source rpm
rpmbuild -rb ~/rpmbuild/SRPMS/XIVLauncher-<version>-<release>.src.rpm   # Build binary from source rpm.
```

In the end you should have an rpm file in `~/rpmbuild/RPMS/x86_64/` called `XIVLauncher-<version>-<release>.x86_64.rpm`. If you build sources as well, 
that will be in `~/rpmbuild/SRPMS/`.

Install as mentioned in the "Installing" section. You can also build from the srpm with `rpmbuild --rb <filename.src.rpm>`.

### OpenSUSE

Nothing yet. If anyone wants to try to get it working, feel free, and report back.