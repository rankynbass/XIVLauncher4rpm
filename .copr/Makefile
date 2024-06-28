srpm:
	dnf update -y && dnf install git -y
	.copr/getsource.sh
	rpmbuild -bs XIVLauncher4rpm.spec --define "_srcrpmdir $(outdir)"