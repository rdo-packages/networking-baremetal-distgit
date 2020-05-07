%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global srcname networking_baremetal
%global pkgname networking-baremetal
%global common_summary Neutron plugins for integration with Ironic
%global docpath doc/build/html


%global with_doc 1

Name:           python-%{pkgname}
Version:        2.0.0
Release:        1%{?dist}
Summary:        %{common_summary}

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz
Source1:        ironic-neutron-agent.service

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-tooz
BuildRequires:  python3-oslo-messaging
# for unit tests
BuildRequires:  /usr/bin/stestr-3
BuildRequires:  python3-mock
BuildRequires:  python3-fixtures
BuildRequires:  python3-oslotest
BuildRequires:  python3-subunit
BuildRequires:  python3-ironicclient
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log

%description
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

%package -n python3-%{pkgname}
Summary:        %{common_summary}
%{?python_provide:%python_provide python3-%{pkgname}}

Requires:       openstack-neutron-common >= 1:14.0.0
Requires:       python3-neutron-lib >= 1.28.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-pbr >= 2.0.0

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
%{?python_provide:%python_provide python3-ironic-neutron-agent}
BuildRequires:  systemd-units

Requires:       python3-%{pkgname}
Requires:       python3-keystoneauth1
Requires:       python3-ironicclient >= 2.3.0
Requires:       python3-neutron
Requires:       python3-neutron-lib >= 1.28.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-service
Requires:       python3-tooz >= 1.58.0
Requires:       python3-oslo-messaging >= 5.29.0
Requires:       python3-oslo-utils >= 3.33.0

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif

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
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-apidoc

%description doc
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the documentation.
%endif

%prep
%autosetup -n %{pkgname}-%{upstream_version} -S git
%py_req_cleanup

%build
%{py3_build}
%if 0%{?with_doc}
sphinx-build-3 -b html doc/source doc/build/html
rm -rf doc/build/html/.{buildinfo,doctrees}
%endif

%check
export PYTHON=python3
stestr-3 --test-path %{srcname}/tests/unit run

%install
%{py3_install}

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
%{python3_sitelib}/%{srcname}*.egg-info
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
* Thu May 07 2020 RDO <dev@lists.rdoproject.org> 2.0.0-1
- Update to 2.0.0


