
srpm: 
	
	dnf install rpmdevtools rpm-build
	rpmdev-setuptree
	dnf install aria2 SDL2 libsecret libattr fontconfig lcms2 libXcursor libXrandr libXdamage libXi gettext freetype mesa-libGLU libSM libgcc libpcap libFAudio desktop-file-utils jxrlib  git
	dnf install neofetch
	neofetch
	dnf install dotnet
	mkdir -p ~/build
	cd ~/build
	git clone https://github.com/rankynbass/XIVLauncher4rpm.git
	cd XIVLauncher4rpm
	rpmbuild -ba XIVLauncher4rpm.spec --define "_srcrpmdir $(outdir)" 
