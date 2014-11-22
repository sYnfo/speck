# Created by pyp2rpm-1.0.1
%global pypi_name click
%global with_python3 1

Name:           test-spec
Version:        1.0.0
Release:        1%{?dist}
Summary:        test spec for the speck program

License:        BSD
URL:            http://github.com/mitsuhiko/click
Source0:        https://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
#https://github.com/mitsuhiko/click/pull/209
Patch0:         foo.patch
Patch1:         bar.patch

BuildArch:      noarch
 
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  pytest
 
%if %{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
%endif # if with_python3


%description
click is a Python package for creating beautiful command line
interfaces in a composable way with as little amount of code as necessary.
It's the "Command Line Interface Creation Kit".  It's highly configurable but
comes with good defaults out of the box.

%prep
%setup -q -n %{pypi_name}-%{version}
%patch0 -p1
%patch1 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}

%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}

%check
PYTHONPATH=$(pwd) py.test-%{python2_version} tests --tb=long --verbose 
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_GB.utf8 LC_ALL=en_GB.utf8 PYTHONPATH=$(pwd) py.test-%{python3_version} tests --tb=long --verbose 
popd
%endif

%files
%doc README 
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3


%changelog
* Sun Aug 24 2014 Robert Kuska <rkuska@redhat.com> - 3.2-2
- Add patch for exception check of TypeError

* Sun Aug 24 2014 Robert Kuska <rkuska@redhat.com> - 3.2-1
- Update to 3.2

* Mon Aug 18 2014 Robert Kuska <rkuska@redhat.com> - 3.1-1
- Update to 3.1

* Wed Jul 16 2014 Robert Kuska <rkuska@redhat.com> - 2.4-1
- Update to 2.4

* Mon Jun 30 2014 Robert Kuska <rkuska@redhat.com> - 2.2-1
- Update to 2.2

* Thu Jun 12 2014 Robert Kuska <rkuska@redhat.com> - 2.0-1
- Update to 2.0

* Fri Jun 06 2014 Robert Kuska <rkuska@redhat.com> - 1.1-3
- Make click own its folder
- Use pythonX_version macros from devel package

* Thu May 29 2014 Robert Kuska <rkuska@redhat.com> - 1.1-2
- Remove __pycache__ folder from tests

* Mon May 12 2014 Robert Kuska <rkuska@redhat.com> - 1.1-1
- Update source

* Wed May 07 2014 Robert Kuska <rkuska@redhat.com> - 0.6-1
- Initial package.
