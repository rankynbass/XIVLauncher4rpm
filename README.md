# XIVLauncher4rpm
RPMs and build files for native versions of <a href=https://github.com/goatcorp/FFXIVQuickLauncher>FFXIVQuickLauncher</a>. Currently only tested on
Fedora 36. It'll probably work for Fedora 35 and rawhide as well. I hope to get this set up to build for OpenSUSE eventually. It may even work as is;
I haven't checked. Try at your own risk (minimal as it probably is).

**Warning! This version is not officially supported.**

If you don't know what you're doing, I'd suggest following these instructions: <a href=https://goatcorp.github.io/faq/steamdeck>XIVLauncher Steam Deck
Installation Guide</a>. It says Steam Deck, but it should work for most Linux distibutions. Or get it directly from
<a href=https://flathub.org/apps/details/dev.goats.xivlauncher>Flathub</a>.

If you'd like to live on the edge, or the flatpak version is unsuitable for some reason, read on.

## Installating
Either install it by double-clicking in your graphical environment (or single-clicking if you have it set that way), or open a terminal and use your
package manager to install it. You do know what you're doing, right? In Fedora, the command is:

`sudo dnf install <filename.rpm>`

As a last resort, you could install it with

`sudo rpm -i <filename.rpm>`

But that might not play nice with your disto's package manager.

## Setting up the environment

By default, Fedora will want to build in `~/rpmbuild`. If it's somewhere different for your setup, replace ~/rpmbuild with your own build directory.
When you clone the git repository from github, DO NOT clone it into this folder, do it somewhere else. I'll use `~/build` for these instructions.

Download the required development packages:

`sudo dnf rpmdevtools rpm-build`

Install all the dependencies needed for the build. Theoretically this should be done by the rpmbuild tool, but it doesn't always work.

```sudo dnf install aria2 SDL2 libsecret libattr fontconfig lcms2 libXcursor libXrandr libXdamage libXi gettext freetype mesa-libGLU libSM libgcc libpcap libFAudio desktop-file-utils jxrlib dotnet-sdk-6.0 git```

## Compiling the code

Now pull the source code.

```
mkdir -p ~/build
cd ~/build
git clone https://github.com/rankynbass/XIVLauncher4rpm.git
cd XIVLauncher4rpm
spectool -g -R XIVLauncher4rpm.spec
```
If this works, you should end up with 2 .tar.gz files in `~/rpmbuild/SOURCE`. The version number file is an archive of this repo. The master
file is the lastest version of the master branch of goatcorp's <a href=https://github.com/goatcorp/FFXIVQuickLauncher>FFXIVQuickLauncher</a> repo.
```
$ ls
1.0.0.9-1.tar.gz  master.tar.gz
```
Now you can build the rpms.

`rpmbuild -bb XIVLauncher4rpm.spec` or `rpmbuild -ba XIVLauncher4rpm.spec` if you want to build source rpm as well. Be aware that the srpm will
include the source files from master FFXIVQuickLauncher repository, so it will be fairly large.

In the end you should have an rpm file in `~/rpmbuild/RPMS/x86_64/` called `XIVLauncher-<version>.x86_64.rpm`. If you build sources as well, that 
will be in `~/rpmbuild/SRPMS/`.

Install as mentioned in the "Installing" section. You can also build from the srpm with `rpmbuild --rebuild <filename.src.rpm>`.









