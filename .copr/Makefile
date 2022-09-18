srpm:
	dnf install -y git
	.copr/getsources.sh
	rpmbuild -bs XIVLauncher4rpm.spec --define "_srcrpmdir $(outdir)"