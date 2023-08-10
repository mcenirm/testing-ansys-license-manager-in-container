Name:           ansyslmd
Version:        2023.2
Release:        1%{?dist}
Summary:        ANSYS, Inc. License Manager

License:        Proprietary
Source0:        AnsysLicenseManager.tgz
Source1:        %{name}.sysusers
Source2:        %{name}-tmpfiles.conf
NoSource:       0

ExclusiveArch:  x86_64
BuildRequires:  coreutils >= 8.32
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

Requires:       ld-lsb.so.3()(64bit)

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

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d -m 0755 %{buildroot}/run/%{name}/

%pre
%sysusers_create_compat %{SOURCE1}

%files
%license %attr(0644,root,root) /usr/ansys_inc/shared_files/licensing/linx64/LICENSE.TXT
/ansys_inc
%attr(0755,root,root) /usr/ansys_inc/shared_files/licensing/linx64/lmgrd
%attr(0755,root,root) /usr/ansys_inc/shared_files/licensing/linx64/ansyslmd
%attr(0755,root,root) /usr/ansys_inc/shared_files/licensing/linx64/lmutil
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%dir /run/%{name}/

#%%post
#%%systemd_post %%{name}-lmgrd.service
#% 
#%%preun
#%%systemd_preun %%{name}-lmgrd.service
#%
#%%postun
#%%systemd_postun_with_restart %%{name}-lmgrd.service
