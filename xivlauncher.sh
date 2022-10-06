#!/bin/bash

### Define env variables. Top one is mandatory. 
export OPENSSL_CONF=/opt/XIVLauncher-git/openssl_fix.cnf
# export DXVK_FRAME_RATE=60
# export MANGOHUD=1
# export MANGOHUD_CONFIGFILE=~/.config/MangoHud/MangoHud.conf
### Use this to use WineD3D (OpenGL) instead of DXVK (Vulkan). Slow and possibly buggy. Doesn't work with Wine-ge or Proton.
# export USE_WINED3D=1

/opt/XIVLauncher-git/XIVLauncher.Core &