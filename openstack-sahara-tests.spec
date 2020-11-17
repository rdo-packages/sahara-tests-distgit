%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}


%global service sahara-tests
%global pkgname sahara
Name:           openstack-%{service}
Version:        XXX
Release:        XXX
Summary:        Sahara Scenario Test Framework
License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
This project contains Sahara-scenario test framework.

%package -n python3-%{pkgname}-tempest
Summary:        OpenStack Sahara tempest plugin common library
%{?python_provide:%python_provide python3-%{pkgname}-tempest}
Obsoletes:      openstack-%{service} < 0.6.0
Provides:       openstack-%{service} = %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:       python3-mako
BuildRequires:  python3-mako
BuildRequires:  /usr/bin/pathfix.py

# test dependencies requirements
BuildRequires:    python3-mock
BuildRequires:    python3-testtools
BuildRequires:    python3-jsonschema
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-glanceclient
BuildRequires:    python3-saharaclient
BuildRequires:    python3-tempest
BuildRequires:    python3-swiftclient
BuildRequires:    python3-stestr



Requires:       python3-fixtures
Requires:       python3-jsonschema
Requires:       python3-oslo-concurrency >= 3.5.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.5.0
Requires:       python3-oslotest >= 1.10.0
Requires:       python3-stestr >= 1.0.0
Requires:       python3-paramiko
Requires:       python3-pbr
Requires:       python3-keystoneauth1 >= 2.1.0
Requires:       python3-glanceclient >= 1:2.0.0
Requires:       python3-novaclient >= 1:2.29.0
Requires:       python3-saharaclient >= 0.13.0
Requires:       python3-swiftclient >= 2.2.0
Requires:       python3-neutronclient >= 4.2.0
Requires:       python3-rfc3986
Requires:       python3-six
Requires:       python3-tempest >= 16.0.0
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

# additional test dependencies requirements
BuildRequires:  python3-botocore >= 1.5.1

Requires:       python3-%{pkgname}-tempest = %{version}-%{release}
Requires:       python3-os-client-config >= 1.13.1
Requires:       python3-botocore >= 1.5.1

%description -n python3-%{service}-scenario
This project contains OpenStack Sahara tests scenario plugin

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Sahara Tests

BuildRequires:    python3-sphinx
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-reno

%description      doc
This package contains the openstack sahara-tests Documentation files.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup
chmod +x sahara_tests/scenario/runner.py
chmod +x sahara_tests/scenario/defaults/edp-examples/edp-shell/shell-example.sh

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" sahara_tests/scenario/runner.py

%build
%{py3_build}

# docs generation
%if 0%{?with_doc}
%{__python3} setup.py build_sphinx
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
# Remove zero-length files
find doc/build/html -size 0 -delete
%endif

%install
%{py3_install}

install -d -m 755 %{buildroot}%{_sysconfdir}/
mv %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}/

%check
export OS_TEST_PATH='./sahara_tests/unit/scenario'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
export PYTHON=%{__python3}
stestr --test-path $OS_TEST_PATH run

%files -n python3-%{pkgname}-tempest
%doc README.rst
%license LICENSE
%{python3_sitelib}/sahara_tests
%{python3_sitelib}/sahara_tests-*.egg-info
%exclude %{python3_sitelib}/sahara_tests/scenario
%exclude %{python3_sitelib}/sahara_tests/unit/scenario
# moving sahara-scenario and sahara_tempest_plugin
# to python-sahara-tests-tempest and python-sahara-tests-scenario
%exclude %{_bindir}/sahara-scenario
%exclude %{python3_sitelib}/sahara_tempest_plugin
%exclude %{_sysconfdir}/sahara-scenario/*

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
%{_bindir}/sahara-scenario
%config(noreplace) %{_sysconfdir}/sahara-scenario/*

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
