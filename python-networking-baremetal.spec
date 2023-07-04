%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global srcname networking_baremetal
%global pkgname networking-baremetal
%global common_summary Neutron plugins for integration with Ironic
%global docpath doc/build/html


%global with_doc 1

Name:           python-%{pkgname}
Version:        XXX
Release:        XXX
Summary:        %{common_summary}

License:        Apache-2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz
Source1:        ironic-neutron-agent.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-neutron-tests

%description
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

%package -n python3-%{pkgname}
Summary:        %{common_summary}

Requires:       openstack-neutron-common >= 1:14.0.0

%description -n python3-%{pkgname}
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the plugin itself.


%package -n python3-%{pkgname}-tests
Summary:        %{common_summary} - tests
Requires:       python3-%{pkgname} = %{version}-%{release}
Requires:       python3-mock >= 2.0.0
Requires:       python3-neutron-tests
Requires:       python3-oslotest >= 1.10.0
Requires:       python3-subunit >= 1.0.0

%description -n python3-%{pkgname}-tests
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the unit tests.

%package -n python3-ironic-neutron-agent
Summary:        %{common_summary} - Ironic Neutron Agent
BuildRequires:  systemd-units

%{?systemd_ordering}

%description -n python3-ironic-neutron-agent
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains a neutron agent that populates the host to
physical network mapping for baremetal nodes in neutron. Neutron uses this to
calculate the segment to host mapping information.

%if 0%{?with_doc}
%package doc
Summary:        %{common_summary} - documentation

%description doc
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pkgname}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel
%if 0%{?with_doc}
%tox -e docs
rm -rf doc/build/html/.{buildinfo,doctrees}
%endif

%check
%tox -e %{default_toxenv}

%install
%pyproject_install

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/ironic-neutron-agent.service

%post -n python3-ironic-neutron-agent
%systemd_post ironic-neutron-agent.service

%preun -n python3-ironic-neutron-agent
%systemd_preun ironic-neutron-agent.service

%postun -n python3-ironic-neutron-agent
%systemd_postun_with_restart ironic-neutron-agent.service


%files -n python3-%{pkgname}
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}*.dist-info
%exclude %{python3_sitelib}/%{srcname}/tests

%files -n python3-%{pkgname}-tests
%license LICENSE
%{python3_sitelib}/%{srcname}/tests

%files -n python3-ironic-neutron-agent
%license LICENSE
%{_bindir}/ironic-neutron-agent
%{_unitdir}/ironic-neutron-agent.service

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog

