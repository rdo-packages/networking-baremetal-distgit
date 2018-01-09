%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global srcname networking_baremetal
%global pkgname networking-baremetal
%global common_summary Neutron plugins for integration with Ironic

Name:           python-%{pkgname}
Version:        XXX
Release:        XXX
Summary:        %{common_summary}

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-pbr
# for documentation
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-sphinx
# for unit tests
BuildRequires:  python-mock
BuildRequires:  python-fixtures
BuildRequires:  python-os-testr
BuildRequires:  python-oslotest
BuildRequires:  python-subunit
BuildRequires:  python-neutron-lib
BuildRequires:  python-neutron-tests
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log

%description
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

%prep
%autosetup -n %{pkgname}-%{upstream_version} -S git
%py_req_cleanup

%build
%py2_build
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%check
ostestr --path %{srcname}/tests/unit

%install
%py2_install


%package -n python2-%{pkgname}
Summary:        %{common_summary}
%{?python_provide:%python_provide python2-%{pkgname}}

Requires:       python-neutron-lib >= 1.11.0
Requires:       python-oslo-config >= 5.1.0
Requires:       python-oslo-i18n >= 3.15.3
Requires:       python-oslo-log >= 3.30.0
Requires:       python-pbr >= 2.0.0

%description -n python2-%{pkgname}
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the plugin itself.

%files -n python2-%{pkgname}
%license LICENSE
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}*.egg-info
%exclude %{python2_sitelib}/%{srcname}/tests


%package -n python2-%{pkgname}-tests
Summary:        %{common_summary} - tests

Requires:       python2-%{pkgname} = %{version}-%{release}
Requires:       python-mock >= 2.0.0
Requires:       python-os-testr >= 1.0.0
Requires:       python-oslotest >= 1.10.0
Requires:       python-subunit >= 1.0.0

%description -n python2-%{pkgname}-tests
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the unit tests.

%files -n python2-%{pkgname}-tests
%license LICENSE
%{python2_sitelib}/%{srcname}/tests


%package doc
Summary:        %{common_summary} - documentation

%description doc
This project's goal is to provide deep integration between the Networking
service and the Bare Metal service and advanced networking features like
notifications of port status changes and routed networks support in clouds with
Bare Metal service.

This package contains the documentation.

%files doc
%license LICENSE
%doc doc/build/html README.rst


%changelog
