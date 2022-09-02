
srpm: 
	dnf install -y wget
    sh .copr/getsources.sh
	rpmbuild -bs XIVLauncher4rpm.spec --define "_srcrpmdir $(outdir)"