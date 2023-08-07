%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}


%global service sahara-tests
%global pkgname sahara
Name:           openstack-%{service}
Version:        XXX
Release:        XXX
Summary:        Sahara Scenario Test Framework
License:        Apache-2.0
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
Provides:       openstack-%{service} = %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros


%description -n python3-%{pkgname}-tempest
This project contains OpenStack Sahara tests tempest plugin common library.

%package -n python3-%{service}-tempest
Summary:        OpenStack Sahara tempest plugin

Requires:       python3-%{pkgname}-tempest = %{version}-%{release}

%description -n python3-%{service}-tempest
This project contains OpenStack Sahara tests tempest plugin

%package -n python3-%{service}-scenario
Summary:        OpenStack Sahara test scenario plugin

Requires:       python3-%{pkgname}-tempest = %{version}-%{release}

%description -n python3-%{service}-scenario
This project contains OpenStack Sahara tests scenario plugin

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Sahara Tests

%description      doc
This package contains the openstack sahara-tests Documentation files.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

chmod +x sahara_tests/scenario/runner.py
chmod +x sahara_tests/scenario/defaults/edp-examples/edp-shell/shell-example.sh

%py3_shebang_fix sahara_tests/scenario/runner.py

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

# docs generation
%if 0%{?with_doc}
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
# Remove zero-length files
find doc/build/html -size 0 -delete
%endif

%install
%pyproject_install

install -d -m 755 %{buildroot}%{_sysconfdir}/
mv %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}/

%check
%tox -e %{default_toxenv}

%files -n python3-%{pkgname}-tempest
%doc README.rst
%license LICENSE
%{python3_sitelib}/sahara_tests
%{python3_sitelib}/sahara_tests-*.dist-info
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
