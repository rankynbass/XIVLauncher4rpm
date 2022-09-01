
srpm: 
	
	dnf install -y rpmdevtools rpm-build dotnet-sdk-6.0 git
	rpmdev-setuptree
	rpmbuild -bb XIVLauncher4rpm.spec --define "_srcrpmdir $(outdir)"