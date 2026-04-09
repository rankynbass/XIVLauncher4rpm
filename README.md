# XIVLauncher4rpm [![Copr build status](https://copr.fedorainfracloud.org/coprs/rankyn/xivlauncher/package/XIVLauncher/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/rankyn/xivlauncher/package/XIVLauncher/)

XIVLauncher (abbreviated as XL) is a faster launcher for our favorite critically acclaimed MMO, with various available addons and enhancements to the game!

### Repos
[ XIVLauncher.Core git: **[goatcorp/XIVLauncher.Core](https://github.com/goatcorp/XIVLauncher.Core/)** ]
[ FFXIVQuickLauncher git: **[goatcorp/FFXIVQuickLauncher](https://github.com/goatcorp/FFXIVQuickLauncher/)** ]
[ XIVLauncher4rpm git: **[rankynbass/XIVLauncher4rpm](https://github.com/rankynbass/XIVLauncher4rpm)** ]
[ COPR Repo: **[rankyn/xivlauncher](https://copr.fedorainfracloud.org/coprs/rankyn/xivlauncher/)** ]

## Installation and Removal

### Fedora
*Install*
```
sudo dnf copr enable rankyn/xivlauncher
sudo dnf install XIVLauncher
```
*Uninstall*
```
sudo dnf remove XIVLauncher
sudo dnf copr remove rankyn/xivlauncher
```
### openSUSE
The repo is built for tumbleweed, LEAP 15.4 and 15.5. It's possible anything from the 15.x family will work, but 15.2 hit end-of-life on 2021-12-31 and 15.3 will hit EOL on 2022-11-30, so I won't bother testing them. If you ever have problems with the repo not refreshing properly (not seeing a new update, for example), just uninstall and reinstall the repo.

*Install*
```
sudo zypper addrepo -r https://copr.fedorainfracloud.org/coprs/rankyn/xivlauncher/repo/opensuse-tumbleweed/rankyn-xivlauncher-opensuse-tumbleweed.repo
sudo zypper install XIVLauncher
```
Replace opensuse-tumbleweed with opensuse-leap-15.4 or opensuse-leap-15.5 for those distos.

*Uninstall*
```
sudo zypper remove XIVLauncher
sudo zypper removerepo copr:copr.fedorainfracloud.org:rankyn:xivlauncher
```
### Enterprise Linux (EL9 Only)
Red Hat, Rocky Linux, AlmaLinux, etc.

It's not really possible to get this running on el8 due glibc being too old. You'd have to rebuild ALL el8 packages against a new version of glibc. It will run on el9 with an additional copr repo. I had to grab source rpms from the fedora repos and build them for rhel9, since they were removed from the default repos. Tested on Rocky Linux 9. XIVLauncher launches, but I didn't install the game or try to play.

First enable the EPEL repository. Instructions: **[[Red Hat](https://www.tecmint.com/install-epel-repo-rhel-9/)] [[Rocky Linux](https://www.linuxcapable.com/how-to-install-enable-epel-epel-next-on-rocky-linux-9/)] [[AlmaLinux](https://www.linuxcapable.com/how-to-install-enable-epel-epel-next-on-almalinux-9/)]**

*Install*
```
sudo dnf copr enable rankyn/xl-deps-el9
sudo dnf copr enable rankyn/xivlauncher
sudo dnf install XIVLauncher
```
*Uninstall*
```
sudo dnf remove XIVLauncher
sudo dnf copr remove rankyn/xivlauncher
```
If you wish to remove the dependencies as well, you can do this:
```
sudo dnf remove aria2 libFAudio jxrlib
sudo dnf copr remove rankyn/xl-deps-el9
```
## Configuration Info

### First run

You can launch from the terminal with `xivlauncher-core`.

### Non-Steam Configuration

The program installs to `/opt/XIVLauncher`. A .desktop file is included at `/usr/share/applications/XIVLauncher.desktop`.and `XIVLauncher-custom.desktop`.

### Steam Configuration

If you are using steam, you can add a non-Steam game and find "XIVLauncher", or browse to `/usr/bin/xivlauncher-core`.

Start the launcher, and on the main page, make sure "Use Steam Service" is checked if you have a Steam-linked FFXIV account. Also, the launcher sometimes does not properly close, and will show itself as still running after you exit the game. You can just click the STOP button to fix it, or right-click and STOP.

If you want an icon for XIVLauncher in the library list, you can find one at `/opt/XIVLauncher/xivlauncher.png`, and a custom logo at `/opt/XIVLauncher/xivlogo.png`

### More Info

You can find more information about the official (flatpak) version of XIVLauncher at **[XIVLauncher Help](https://goatcorp.github.io/faq/steamdeck)**. Much of the information there applies to this native install as well. You can also join the **[Discord Server](https://goat.place/)**. Linux support can be obtained in the #linux-and-deck channel (don't use the #xivlauncher-help channel).

## Building it yourself

### Fedora setup

By default, Fedora will want to build in `~/rpmbuild`. If it's somewhere different for your setup, replace ~/rpmbuild with your own build directory. When you clone the git repository from github, DO NOT clone it into this folder, do it somewhere else.

Download the required development packages:

```
sudo dnf rpmdevtools rpm-build patchelf
```

Set up the build directories if they don't already exist (`~/rpmbuild` and subfolders). Run the command `rpmdev-setuptree`. Do NOT run with sudo/root access. You want to make these directories in your own home folder.

### OpenSUSE setup

Install rpm build packages with `sudo zypper in rpm-build rpmdevtools patchelf`, and run `rpmdev-setuptree` (NOT as root).

### Compiling the code

Use `git clone` to grab the source code. I use a folder called `~/build` for compiling various git repos, so that's what I'll do here. But you can use any folder you have read/write access to.

```
mkdir -p ~/build
cd ~/build
git clone https://github.com/rankynbass/XIVLauncher4rpm.git
cd XIVLauncher4rpm
```

Now you can build the rpms. First, download the tarballs by using the included script, then build with rpmbuild. The third option is actually what the COPR build system does. It uses .copr/Makefile to install dependencies for making the binary, then calls the getsources script, then executes rpmbuild -bs. It then passes the src.rpm off to the various build environments for different distros. However, even if you have src.rpms, you still need to have internet access. The dotnet publish command needs to grab some remote packages. For manual builds, thats obviously not an issue, since you just cloned the repo. But for remote builds with copr, or with opensuse's OBS (I haven't tried this one yet), you'll need to make sure the builder has internet access. (version and release are listed in the _version file in lines 3 and 4. As of October 28, 2022, these are 1.0.2 and 2.)

Run the script `.copr/getsources.sh` and then do one of the following:
```
rpmbuild -ba --undefine='dist' XIVLauncher4rpm.spec   # Build binary and source rpms
```
OR
```
rpmbuild -bb --undefine='dist' XIVLauncher4rpm.spec   # Build binary only
```
OR
```
rpmbuild -bs --undefine='dist' XIVLauncher4rpm.spec   # Build source rpm
rpmbuild -rb --undefine='dist' ~/rpmbuild/SRPMS/XIVLauncher-version-release.src.rpm   # Build binary from source rpm.
```

By default, Fedora will put a .f42 or similar after the version-release for both the rpm and src.rpm. OpenSUSE may add something like .opensuse.tw, but did not do so during my testing. The COPR build system *does* put the distro in the rpm name. If you want to edit this macro definition yourself, you can pass `--define='dist .mydistro'`. The "." is important, as otherwise you'll get something like `XIVLauncher-1.0.1.0-4mydistro.x86_64.rpm`. Or you can pass `--undefine='dist'` (as above) to make it blank.

In the end you should have an rpm file in `~/rpmbuild/RPMS/x86_64/` called `XIVLauncher-version-release.x86_64.rpm`. If you build sources as well, that will be in `~/rpmbuild/SRPMS/`.

Install with `sudo rpm -i ~/rpmbuild/RPMS/x86_64/XIVLauncher-version-release.rpm`.
