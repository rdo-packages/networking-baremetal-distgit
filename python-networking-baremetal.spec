%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global srcname networking_baremetal
%global pkgname networking-baremetal
%global common_summary Neutron plugins for integration with Ironic

%global with_doc 1

Name:           python-%{pkgname}
Version:        1.2.1
Release:        1%{?dist}
Summary:        %{common_summary}

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz
Source1:        ironic-neutron-agent.service

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-tooz
BuildRequires:  python2-oslo-messaging
# for unit tests
BuildRequires:  /usr/bin/ostestr
BuildRequires:  python2-mock
BuildRequires:  python2-fixtures
BuildRequires:  python2-os-testr
BuildRequires:  python2-oslotest
BuildRequires:  python2-subunit
BuildRequires:  python2-ironicclient
BuildRequires:  python-neutron-lib-tests
BuildRequires:  python-neutron-tests
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-oslo-log

%description
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

%package -n python2-%{pkgname}
Summary:        %{common_summary}
%{?python_provide:%python_provide python2-%{pkgname}}

Requires:       python-neutron-lib >= 1.18.0
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-pbr >= 2.0.0

%description -n python2-%{pkgname}
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the plugin itself.


%package -n python2-%{pkgname}-tests
Summary:        %{common_summary} - tests

Requires:       python2-%{pkgname} = %{version}-%{release}
Requires:       python2-mock >= 2.0.0
Requires:       python-neutron-tests
Requires:       python2-oslotest >= 1.10.0
Requires:       python2-subunit >= 1.0.0

%description -n python2-%{pkgname}-tests
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the unit tests.

%package -n python2-ironic-neutron-agent
Summary:        %{common_summary} - Ironic Neutron Agent
%{?python_provide:%python_provide python2-ironic-neutron-agent}
BuildRequires:  systemd-units

Requires:       python-%{pkgname}
Requires:       python2-keystoneauth1
Requires:       python2-ironicclient >= 2.3.0
Requires:       python-neutron
Requires:       python-neutron-lib >= 1.18.0
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-service
Requires:       python2-tooz >= 1.58.0
Requires:       python2-oslo-messaging >= 5.29.0
Requires:       python2-oslo-utils >= 3.33.0
%{?systemd_requires}

%description -n python2-ironic-neutron-agent
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
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-sphinx

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
%py2_build
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%check
ostestr --path %{srcname}/tests/unit

%install
%py2_install

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/ironic-neutron-agent.service

%post -n python2-ironic-neutron-agent
%systemd_post ironic-neutron-agent.service

%preun -n python2-ironic-neutron-agent
%systemd_preun ironic-neutron-agent.service

%postun -n python2-ironic-neutron-agent
%systemd_postun_with_restart ironic-neutron-agent.service


%files -n python2-%{pkgname}
%license LICENSE
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}*.egg-info
%exclude %{python2_sitelib}/%{srcname}/tests

%files -n python2-%{pkgname}-tests
%license LICENSE
%{python2_sitelib}/%{srcname}/tests

%files -n python2-ironic-neutron-agent
%license LICENSE
%{_bindir}/ironic-neutron-agent
%{_unitdir}/ironic-neutron-agent.service

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
* Tue Oct 01 2019 RDO <dev@lists.rdoproject.org> 1.2.1-1
- Update to 1.2.1

* Mon Aug 20 2018 RDO <dev@lists.rdoproject.org> 1.2.0-1
- Update to 1.2.0

