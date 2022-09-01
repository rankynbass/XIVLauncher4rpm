
srpm: 
	
	dnf install -y rpmdevtools rpm-build dotnet-sdk-6.0 git
	rpmdev-setuptree
	rpmbuild -bp XIVLauncher4rpm.spec --define "_srcrpmdir $(outdir)"
	rpmbuild -bs XIVLauncher4rpm.spec --define "_srcrpmdir $(outdir)"