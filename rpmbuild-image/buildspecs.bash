set -euo pipefail
[[ "${TRACE-0}" == "1" ]] && set -x

rpmdev-setuptree

cp -nv -t $HOME/rpmbuild/SPECS /rpmspecs/*.spec
cp -nv -t $HOME/rpmbuild/SOURCES /rpmsources/*
cp -nv -t $HOME/rpmbuild/SOURCES /rpmspecs/*

for s in $HOME/rpmbuild/SPECS/*.spec
do
  rpmlint $s
  rpmbuild -ba $s
  rsync -rOi $HOME/rpmbuild/RPMS $HOME/rpmbuild/SRPMS /rpmoutputs/
done
