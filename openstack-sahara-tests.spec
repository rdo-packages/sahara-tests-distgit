%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

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
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

Requires:       python-pbr
Requires:       python-mako
Requires:       python-fixtures
Requires:       python-jsonschema
Requires:       python-oslo-concurrency >= 3.5.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.5.0
Requires:       python-oslotest >= 1.10.0
Requires:       python-os-testr >= 0.8.0
Requires:       python-paramiko
Requires:       python-keystoneauth1 >= 2.1.0
Requires:       python-glanceclient >= 1:2.0.0
Requires:       python-novaclient >= 1:2.29.0
Requires:       python-saharaclient >= 0.13.0
Requires:       python-swiftclient >= 2.2.0
Requires:       python-neutronclient >= 4.2.0
Requires:       python-rfc3986
Requires:       python-six
Requires:       python-tempest >= 12.2.0
Requires:       python-testrepository
Requires:       python-testtools

# test dependencies requirements
BuildRequires:    python-mock
BuildRequires:    python-coverage

%description
This project contains Sahara-scenario test framework.

%package -n python-%{service}-tempest
Summary:        OpenStack Sahara tempest plugin

Requires:       openstack-%{service} = %{version}-%{release}

%description -n python-%{service}-tempest
This project contains OpenStack Sahara tests tempest plugin

%package -n python-%{service}-scenario
Summary:        OpenStack Sahara test scenario plugin

Requires:       openstack-%{service} = %{version}-%{release}
Requires:       python-os-client-config >= 1.13.1

%description -n python-%{service}-scenario
This project contains OpenStack Sahara tests scenario plugin

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Sahara Tests

BuildRequires:    python-sphinx
BuildRequires:    python-openstackdocstheme
BuildRequires:    python-reno
%description      doc
This package contains the openstack sahara-tests Documentation files.
%endif

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

# docs generation
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
# Remove zero-length files
find doc/build/html -size 0 -delete
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

chmod +x %{buildroot}/%{python2_sitelib}/sahara_tests/scenario/runner.py
chmod +x %{buildroot}/%{python2_sitelib}/sahara_tests/scenario/defaults/edp-examples/edp-shell/shell-example.sh

install -d -m 755 %{buildroot}%{_sysconfdir}/
mv %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}/

%check
%{__python2} setup.py test

%files
%doc README.rst
%license LICENSE
%exclude %{python2_sitelib}/sahara_tests/scenario
%exclude %{python2_sitelib}/sahara_tests/unit/scenario
%{python2_sitelib}/sahara_tests
%{python2_sitelib}/sahara_tests-*.egg-info
# moving sahara-scenario and sahara_tempest_plugin
# to python-sahara-tests-tempest and python-sahara-tests-scenario
%exclude %{_bindir}/sahara-scenario
%exclude %{python2_sitelib}/sahara_tempest_plugin
%exclude %{_sysconfdir}/sahara-scenario/*

%files -n python-%{service}-tempest
%license LICENSE
%{python2_sitelib}/sahara_tempest_plugin

%files -n python-%{service}-scenario
%license LICENSE
# FIXME /sahara_tests/scenario/defaults contains jar file
# We are need to find a way to build the jar files properly
# https://trello.com/c/jDJnTO22/305-sahara-tests-jar-unbundling-tracker
%{python2_sitelib}/sahara_tests/scenario
%{python2_sitelib}/sahara_tests/unit/scenario
%{_bindir}/sahara-scenario
%config(noreplace) %{_sysconfdir}/sahara-scenario/*


%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
