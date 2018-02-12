%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%if 0%{?fedora}
%global with_python3 1
%endif

%global service sahara-tests
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

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools

# test dependencies requirements
BuildRequires:    python2-mock

Requires:       python2-pbr
Requires:       python2-mako
Requires:       python2-fixtures
Requires:       python2-jsonschema
Requires:       python2-oslo-concurrency >= 3.5.0
Requires:       python2-oslo-serialization >= 1.10.0
Requires:       python2-oslo-utils >= 3.5.0
Requires:       python2-oslotest >= 1.10.0
Requires:       python2-os-testr >= 0.8.0
Requires:       python2-paramiko
Requires:       python2-keystoneauth1 >= 2.1.0
Requires:       python2-glanceclient >= 1:2.0.0
Requires:       python2-novaclient >= 1:2.29.0
Requires:       python2-saharaclient >= 0.13.0
Requires:       python2-swiftclient >= 2.2.0
Requires:       python2-neutronclient >= 4.2.0
Requires:       python2-rfc3986
Requires:       python2-six
Requires:       python2-tempest >= 16.0.0
Requires:       python2-testrepository
Requires:       python2-testtools

%description
This project contains Sahara-scenario test framework.

%package -n python2-%{service}-tempest
Summary:        OpenStack Sahara tempest plugin
%{?python_provide:%python_provide python2-%{service}-tempest}

Requires:       openstack-%{service} = %{version}-%{release}

%description -n python2-%{service}-tempest
This project contains OpenStack Sahara tests tempest plugin

%package -n python2-%{service}-scenario
Summary:        OpenStack Sahara test scenario plugin
%{?python_provide:%python_provide python2-%{service}-scenario}

Requires:       openstack-%{service} = %{version}-%{release}
Requires:       python2-os-client-config >= 1.13.1

%description -n python2-%{service}-scenario
This project contains OpenStack Sahara tests scenario plugin


%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

# test dependencies requirements
BuildRequires:    python3-mock

Requires:       python3-pbr
Requires:       python3-mako
Requires:       python3-fixtures
Requires:       python3-jsonschema
Requires:       python3-oslo-concurrency >= 3.5.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.5.0
Requires:       python3-oslotest >= 1.10.0
Requires:       python3-os-testr >= 0.8.0
Requires:       python3-paramiko
Requires:       python3-keystoneauth1 >= 2.1.0
Requires:       python3-glanceclient >= 1:2.0.0
Requires:       python3-novaclient >= 1:2.29.0
Requires:       python3-saharaclient >= 0.13.0
Requires:       python3-swiftclient >= 2.2.0
Requires:       python3-neutronclient >= 4.2.0
Requires:       python3-rfc3986
Requires:       python3-six
Requires:       python3-tempest >= 16.0.0
Requires:       python3-testrepository
Requires:       python3-testtools

%package -n python3-%{service}-tempest
Summary:        OpenStack Sahara tempest plugin
%{?python_provide:%python_provide python3-%{service}-tempest}

Requires:       openstack-%{service} = %{version}-%{release}

%description -n python3-%{service}-tempest
This project contains OpenStack Sahara tests tempest plugin

%package -n python3-%{service}-scenario
Summary:        OpenStack Sahara test scenario plugin
%{?python_provide:%python_provide python3-%{service}-scenario}

Requires:       openstack-%{service} = %{version}-%{release}
Requires:       python3-os-client-config >= 1.13.1
%description -n python3-%{service}-scenario
This project contains OpenStack Sahara tests scenario plugin
%endif

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Sahara Tests

BuildRequires:    python2-sphinx
BuildRequires:    python2-openstackdocstheme
BuildRequires:    python2-reno

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
%if 0%{?with_python3}
%py3_build
mv %{buildroot}%{_bindir}/sahara-scenario \
   %{buildroot}%{_bindir}/python3-sahara-scenario
%endif
%py2_build

# docs generation
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
# Remove zero-length files
find doc/build/html -size 0 -delete
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

install -d -m 755 %{buildroot}%{_sysconfdir}/
mv %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}/

%check
%{__python2} setup.py test

%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files
%doc README.rst
%license LICENSE
%exclude %{python2_sitelib}/sahara_tests/scenario
%exclude %{python2_sitelib}/sahara_tests/unit/scenario
%exclude %{python3_sitelib}/sahara_tests/scenario
%exclude %{python3_sitelib}/sahara_tests/unit/scenario
%{python2_sitelib}/sahara_tests
%{python2_sitelib}/sahara_tests-*.egg-info
# moving sahara-scenario and sahara_tempest_plugin
# to python-sahara-tests-tempest and python-sahara-tests-scenario
%exclude %{_bindir}/sahara-scenario
%exclude %{python2_sitelib}/sahara_tempest_plugin
%exclude %{python3_sitelib}/sahara_tempest_plugin
%exclude %{_sysconfdir}/sahara-scenario/*

%files -n python2-%{service}-tempest
%license LICENSE
%{python2_sitelib}/sahara_tempest_plugin

%files -n python2-%{service}-scenario
%license LICENSE
# FIXME /sahara_tests/scenario/defaults contains jar file
# We are need to find a way to build the jar files properly
# https://trello.com/c/jDJnTO22/305-sahara-tests-jar-unbundling-tracker
%{python2_sitelib}/sahara_tests/scenario
%{python2_sitelib}/sahara_tests/unit/scenario
%{_bindir}/sahara-scenario
%config(noreplace) %{_sysconfdir}/sahara-scenario/*

%if 0%{?with_python3}
%files -n python3-%{service}-tempest
%license LICENSE
%{python3_sitelib}/sahara_tempest_plugin

%files -n python3-%{service}-scenario
%license LICENSE
# FIXME /sahara_tests/scenario/defaults contains jar file
# We are need to find a way to build the jar files properly
# https://trello.com/c/jDJnTO22/305-sahara-tests-jar-unbundling-tracker
%{python3_sitelib}/sahara_tests/scenario
%{python3_sitelib}/sahara_tests/unit/scenario
%{_bindir}/python3-sahara-scenario
%config(noreplace) %{_sysconfdir}/sahara-scenario/*
%endif

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
