# XIVLauncher for Fedora

## Setting up the environment

By default, Fedora will want to build in `~/rpmbuild`. When you clone the git repository from github, DO NOT clone it into this folder, do it somewhere else. I'll use `~/build` for these instructions.

Download the required development packages:

```sudo dnf rpmdevtools rpm-build```

Install all the dependencies needed for the build. Theoretically this should be done by the rpmbuild tool, but it doesn't always work.

```sudo dnf install aria2 SDL2 libsecret libattr fontconfig lcms2 libXcursor libXrandr libXdamage libXi gettext freetype mesa-libGLU libSM libgcc libpcap libFAudio desktop-file-utils jxrlib dotnet-sdk-6.0 git```

## Compiling the code

Now pull the source code.

```cd ~/build
git clone https://github.com/rankynbass/FFXIVQuickLauncher.git
cd FFXIVQuickLauncher```








