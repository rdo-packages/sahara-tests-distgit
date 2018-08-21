%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%if 0%{?fedora}
%global with_python3 1
%endif

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

%package -n python2-%{pkgname}-tempest
Summary:        OpenStack Sahara tempest plugin common library
%{?python_provide:%python_provide python2-%{pkgname}-tempest}
Obsoletes:      openstack-%{service} < 0.6.0
Provides:       openstack-%{service} = %{version}-%{release}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools

# test dependencies requirements
BuildRequires:    python2-mock
BuildRequires:    python2-testtools
BuildRequires:    python2-jsonschema
BuildRequires:    python2-oslo-utils
BuildRequires:    python2-saharaclient
BuildRequires:    python2-tempest
BuildRequires:    python2-swiftclient
BuildRequires:    python2-stestr

Requires:       python2-pbr
%if 0%{?fedora} > 0
Requires:       python2-mako
BuildRequires:  python2-mako
%else
Requires:       python-mako
BuildRequires:       python-mako
%endif
Requires:       python2-fixtures
Requires:       python2-jsonschema
Requires:       python2-oslo-concurrency >= 3.25.0
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-oslotest >= 1.10.0
Requires:       python2-stestr >= 2.1.0
Requires:       python2-paramiko
Requires:       python2-keystoneauth1 >= 3.4.0
Requires:       python2-glanceclient >= 1:2.10.0
Requires:       python2-novaclient >= 1:10.1.0
Requires:       python2-saharaclient >= 1.5.0
Requires:       python2-swiftclient >= 3.5.0
Requires:       python2-neutronclient >= 6.7.0
Requires:       python2-rfc3986
Requires:       python2-six
Requires:       python2-tempest >= 1:18.0.0
Requires:       python2-testrepository
Requires:       python2-testtools

%description -n python2-%{pkgname}-tempest
This project contains OpenStack Sahara tests tempest plugin common library.

%package -n python2-%{service}-tempest
Summary:        OpenStack Sahara tempest plugin
%{?python_provide:%python_provide python2-%{service}-tempest}

Requires:       python2-%{pkgname}-tempest = %{version}-%{release}

%description -n python2-%{service}-tempest
This project contains OpenStack Sahara tests tempest plugin

%package -n python2-%{service}-scenario
Summary:        OpenStack Sahara test scenario plugin
%{?python_provide:%python_provide python2-%{service}-scenario}

Requires:       python2-%{pkgname}-tempest = %{version}-%{release}
Requires:       python2-os-client-config >= 1.13.1

%description -n python2-%{service}-scenario
This project contains OpenStack Sahara tests scenario plugin

%if 0%{?with_python3}
%package -n python3-%{pkgname}-tempest
Summary:        OpenStack Sahara tempest plugin common library
%{?python_provide:%python_provide python3-%{pkgname}-tempest}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

# test dependencies requirements
BuildRequires:    python3-testtools
BuildRequires:    python3-jsonschema
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-saharaclient
BuildRequires:    python3-tempest
BuildRequires:    python3-swiftclient
BuildRequires:    python3-mako
BuildRequires:    python3-stestr

Requires:       python3-pbr
Requires:       python3-mako
Requires:       python3-fixtures
Requires:       python3-jsonschema
Requires:       python3-oslo-concurrency >= 3.25.0
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-oslotest >= 1.10.0
Requires:       python3-stestr >= 2.1.0
Requires:       python3-paramiko
Requires:       python3-keystoneauth1 >= 3.4.0
Requires:       python3-glanceclient >= 1:2.10.0
Requires:       python3-novaclient >= 1:10.1.0
Requires:       python3-saharaclient >= 1.5.0
Requires:       python3-swiftclient >= 3.5.0
Requires:       python3-neutronclient >= 6.7.0
Requires:       python3-rfc3986
Requires:       python3-six
Requires:       python3-tempest >= 1:18.0.0
Requires:       python3-testrepository
Requires:       python3-testtools

%description -n python3-%{pkgname}-tempest
This project contains OpenStack Sahara tests tempest plugin common library.

%package -n python3-%{service}-tempest
Summary:        OpenStack Sahara tempest plugin
%{?python_provide:%python_provide python3-%{service}-tempest}

Requires:       python3-%{pkgname}-tempest = %{version}-%{release}

%description -n python3-%{service}-tempest
This project contains OpenStack Sahara tests tempest plugin

%package -n python3-%{service}-scenario
Summary:        OpenStack Sahara test scenario plugin
%{?python_provide:%python_provide python3-%{service}-scenario}

Requires:       python3-%{pkgname}-tempest = %{version}-%{release}
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
mv %{buildroot}%{_bindir}/sahara-scenario %{buildroot}%{_bindir}/sahara-scenario-%{python3_version}
ln -s ./sahara-scenario-%{python3_version} %{buildroot}%{_bindir}/sahara-scenario-3
%endif
%py2_install

install -d -m 755 %{buildroot}%{_sysconfdir}/
mv %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}/

%check
export OS_TEST_PATH='./sahara_tests/unit/scenario'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr --test-path $OS_TEST_PATH run

%if 0%{?with_python3}
rm -rf .stestr
stestr-3 --test-path $OS_TEST_PATH run
%endif

%files -n python2-%{pkgname}-tempest
%doc README.rst
%license LICENSE
%{python2_sitelib}/sahara_tests
%{python2_sitelib}/sahara_tests-*.egg-info
%exclude %{python2_sitelib}/sahara_tests/scenario
%exclude %{python2_sitelib}/sahara_tests/unit/scenario
# moving sahara-scenario and sahara_tempest_plugin
# to python-sahara-tests-tempest and python-sahara-tests-scenario
%exclude %{_bindir}/sahara-scenario
%exclude %{python2_sitelib}/sahara_tempest_plugin
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
%files -n python3-%{pkgname}-tempest
%doc README.rst
%license LICENSE
%{python3_sitelib}/sahara_tests
%{python3_sitelib}/sahara_tests-*.egg-info
%exclude %{python3_sitelib}/sahara_tests/scenario
%exclude %{python3_sitelib}/sahara_tests/unit/scenario
%exclude %{python3_sitelib}/sahara_tempest_plugin

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
%{_bindir}/sahara-scenario-3
%{_bindir}/sahara-scenario-%{python3_version}
%config(noreplace) %{_sysconfdir}/sahara-scenario/*
%endif

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
