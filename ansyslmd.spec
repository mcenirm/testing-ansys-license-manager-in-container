Name:           ansyslmd
Version:        2023.2
Release:        1%{?dist}
Summary:        ANSYS, Inc. License Manager

License:        Proprietary
Source0:        AnsysLicenseManager.tgz
NoSource:       0

BuildRequires:  coreutils >= 8.32
#BuildRequires:  systemd-rpm-macros
#Requires:       

%description
ANSYS, Inc. License Manager and minimal FlexNet Publisher support files

%prep
sha256sum -c - <<EOF
83ced9068633db638d7d420efadebc1258baabfe5615f12210060bf7ebb0ffb9  %{SOURCE0}
EOF

%build
true

%install

cd ${RPM_BUILD_ROOT}

mkdir usr
mkdir usr/ansys_inc
ln -sT usr/ansys_inc ansys_inc
mkdir usr/ansys_inc/shared_files
mkdir usr/ansys_inc/shared_files/licensing
mkdir usr/ansys_inc/shared_files/licensing/linx64

tar xf %{SOURCE0} \
    AnsysLicenseManager/linx64/LICENSE.TXT \
    AnsysLicenseManager/linx64/licserv/LINX64.TGZ
tar xf AnsysLicenseManager/linx64/licserv/LINX64.TGZ \
    -C usr/ansys_inc \
    shared_files/licensing/linx64/update/lmgrd \
    shared_files/licensing/linx64/update/ansyslmd \
    shared_files/licensing/linx64/update/lmutil
rm AnsysLicenseManager/linx64/licserv/LINX64.TGZ

mv -t usr/ansys_inc/shared_files/licensing/linx64 \
    AnsysLicenseManager/linx64/LICENSE.TXT \
    usr/ansys_inc/shared_files/licensing/linx64/update/lmgrd \
    usr/ansys_inc/shared_files/licensing/linx64/update/ansyslmd \
    usr/ansys_inc/shared_files/licensing/linx64/update/lmutil

rmdir usr/ansys_inc/shared_files/licensing/linx64/update

rmdir AnsysLicenseManager/linx64/licserv
rmdir AnsysLicenseManager/linx64
rmdir AnsysLicenseManager

%files
%license %attr(0644,root,root) /usr/ansys_inc/shared_files/licensing/linx64/LICENSE.TXT
/ansys_inc
%attr(0755,root,root) /usr/ansys_inc/shared_files/licensing/linx64/lmgrd
%attr(0755,root,root) /usr/ansys_inc/shared_files/licensing/linx64/ansyslmd
%attr(0755,root,root) /usr/ansys_inc/shared_files/licensing/linx64/lmutil

#%%post
#%%systemd_post ansyslmd-lmgrd.service
#% 
#%%preun
#%%systemd_preun ansyslmd-lmgrd.service
#%
#%%postun
#%%systemd_postun_with_restart ansyslmd-lmgrd.service
