%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global srcname networking_baremetal
%global pkgname networking-baremetal
%global common_summary Neutron plugins for integration with Ironic
%global docpath doc/build/html

# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%global with_doc 1

Name:           python-%{pkgname}
Version:        XXX
Release:        XXX
Summary:        %{common_summary}

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz
Source1:        ironic-neutron-agent.service

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-tooz
BuildRequires:  python%{pyver}-oslo-messaging
# for unit tests
BuildRequires:  /usr/bin/stestr-%{pyver}
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-ironicclient
BuildRequires:  python%{pyver}-neutron-lib-tests
BuildRequires:  python%{pyver}-neutron-tests
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-oslo-log

%description
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

%package -n python%{pyver}-%{pkgname}
Summary:        %{common_summary}
%{?python_provide:%python_provide python%{pyver}-%{pkgname}}

Requires:       openstack-neutron >= 1:13.0.0
Requires:       python%{pyver}-neutron-lib >= 1.18.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-pbr >= 2.0.0

%description -n python%{pyver}-%{pkgname}
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the plugin itself.


%package -n python%{pyver}-%{pkgname}-tests
Summary:        %{common_summary} - tests

Requires:       python%{pyver}-%{pkgname} = %{version}-%{release}
Requires:       python%{pyver}-mock >= 2.0.0
Requires:       python%{pyver}-neutron-tests
Requires:       python%{pyver}-oslotest >= 1.10.0
Requires:       python%{pyver}-subunit >= 1.0.0

%description -n python%{pyver}-%{pkgname}-tests
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the unit tests.

%package -n python%{pyver}-ironic-neutron-agent
Summary:        %{common_summary} - Ironic Neutron Agent
%{?python_provide:%python_provide python%{pyver}-ironic-neutron-agent}
BuildRequires:  systemd-units

Requires:       python%{pyver}-%{pkgname}
Requires:       python%{pyver}-keystoneauth1
Requires:       python%{pyver}-ironicclient >= 2.3.0
Requires:       python%{pyver}-neutron
Requires:       python%{pyver}-neutron-lib >= 1.18.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-service
Requires:       python%{pyver}-tooz >= 1.58.0
Requires:       python%{pyver}-oslo-messaging >= 5.29.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif

%description -n python%{pyver}-ironic-neutron-agent
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
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx

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
%{pyver_build}
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
rm -rf %{docpath}/.{buildinfo,doctrees}
%endif

%check
export PYTHON=%{pyver_bin}
stestr-%{pyver} --test-path %{srcname}/tests/unit run

%install
%{pyver_install}

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/ironic-neutron-agent.service

%post -n python%{pyver}-ironic-neutron-agent
%systemd_post ironic-neutron-agent.service

%preun -n python%{pyver}-ironic-neutron-agent
%systemd_preun ironic-neutron-agent.service

%postun -n python%{pyver}-ironic-neutron-agent
%systemd_postun_with_restart ironic-neutron-agent.service


%files -n python%{pyver}-%{pkgname}
%license LICENSE
%{pyver_sitelib}/%{srcname}
%{pyver_sitelib}/%{srcname}*.egg-info
%exclude %{pyver_sitelib}/%{srcname}/tests

%files -n python%{pyver}-%{pkgname}-tests
%license LICENSE
%{pyver_sitelib}/%{srcname}/tests

%files -n python%{pyver}-ironic-neutron-agent
%license LICENSE
%{_bindir}/ironic-neutron-agent
%{_unitdir}/ironic-neutron-agent.service

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
