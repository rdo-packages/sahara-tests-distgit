%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

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

%global service sahara-tests
%global pkgname sahara
Name:           openstack-%{service}
Version:        XXX
Release:        XXX
Summary:        Sahara Scenario Test Framework
License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
This project contains Sahara-scenario test framework.

%package -n python%{pyver}-%{pkgname}-tempest
Summary:        OpenStack Sahara tempest plugin common library
%{?python_provide:%python_provide python%{pyver}-%{pkgname}-tempest}
Obsoletes:      openstack-%{service} < 0.6.0
Provides:       openstack-%{service} = %{version}-%{release}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools

%if %{pyver} == 2
Requires:       python-mako
BuildRequires:  python-mako
%else
Requires:       python%{pyver}-mako
BuildRequires:  python%{pyver}-mako
%endif

# test dependencies requirements
BuildRequires:    python%{pyver}-mock
BuildRequires:    python%{pyver}-testtools
BuildRequires:    python%{pyver}-jsonschema
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-saharaclient
BuildRequires:    python%{pyver}-tempest
BuildRequires:    python%{pyver}-swiftclient
BuildRequires:    python%{pyver}-stestr

Requires:       python%{pyver}-fixtures
Requires:       python%{pyver}-jsonschema
Requires:       python%{pyver}-oslo-concurrency >= 3.5.0
Requires:       python%{pyver}-oslo-serialization >= 1.10.0
Requires:       python%{pyver}-oslo-utils >= 3.5.0
Requires:       python%{pyver}-oslotest >= 1.10.0
Requires:       python%{pyver}-stestr >= 1.0.0
Requires:       python%{pyver}-paramiko
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-keystoneauth1 >= 2.1.0
Requires:       python%{pyver}-glanceclient >= 1:2.0.0
Requires:       python%{pyver}-novaclient >= 1:2.29.0
Requires:       python%{pyver}-saharaclient >= 0.13.0
Requires:       python%{pyver}-swiftclient >= 2.2.0
Requires:       python%{pyver}-neutronclient >= 4.2.0
Requires:       python%{pyver}-rfc3986
Requires:       python%{pyver}-six
Requires:       python%{pyver}-tempest >= 16.0.0
Requires:       python%{pyver}-testtools

%description -n python%{pyver}-%{pkgname}-tempest
This project contains OpenStack Sahara tests tempest plugin common library.

%package -n python%{pyver}-%{service}-tempest
Summary:        OpenStack Sahara tempest plugin
%{?python_provide:%python_provide python%{pyver}-%{service}-tempest}

Requires:       python%{pyver}-%{pkgname}-tempest = %{version}-%{release}

%description -n python%{pyver}-%{service}-tempest
This project contains OpenStack Sahara tests tempest plugin

%package -n python%{pyver}-%{service}-scenario
Summary:        OpenStack Sahara test scenario plugin
%{?python_provide:%python_provide python%{pyver}-%{service}-scenario}

Requires:       python%{pyver}-%{pkgname}-tempest = %{version}-%{release}
Requires:       python%{pyver}-os-client-config >= 1.13.1
Requires:       python%{pyver}-botocore >= 1.5.1

%description -n python%{pyver}-%{service}-scenario
This project contains OpenStack Sahara tests scenario plugin

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Sahara Tests

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-reno

%description      doc
This package contains the openstack sahara-tests Documentation files.
%endif

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup
chmod +x sahara_tests/scenario/runner.py
chmod +x sahara_tests/scenario/defaults/edp-examples/edp-shell/shell-example.sh

%build
%{pyver_build}

# docs generation
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
# Remove zero-length files
find doc/build/html -size 0 -delete
%endif

%install
%{pyver_install}

install -d -m 755 %{buildroot}%{_sysconfdir}/
mv %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}/

%check
export OS_TEST_PATH='./sahara_tests/unit/scenario'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{pkgname}-tempest
%doc README.rst
%license LICENSE
%{pyver_sitelib}/sahara_tests
%{pyver_sitelib}/sahara_tests-*.egg-info
%exclude %{pyver_sitelib}/sahara_tests/scenario
%exclude %{pyver_sitelib}/sahara_tests/unit/scenario
# moving sahara-scenario and sahara_tempest_plugin
# to python-sahara-tests-tempest and python-sahara-tests-scenario
%exclude %{_bindir}/sahara-scenario
%exclude %{pyver_sitelib}/sahara_tempest_plugin
%exclude %{_sysconfdir}/sahara-scenario/*

%files -n python%{pyver}-%{service}-tempest
%license LICENSE
%{pyver_sitelib}/sahara_tempest_plugin

%files -n python%{pyver}-%{service}-scenario
%license LICENSE
# FIXME /sahara_tests/scenario/defaults contains jar file
# We are need to find a way to build the jar files properly
# https://trello.com/c/jDJnTO22/305-sahara-tests-jar-unbundling-tracker
%{pyver_sitelib}/sahara_tests/scenario
%{pyver_sitelib}/sahara_tests/unit/scenario
%{_bindir}/sahara-scenario
%config(noreplace) %{_sysconfdir}/sahara-scenario/*

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
