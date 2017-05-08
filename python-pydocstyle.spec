%global srcname pydocstyle
%global sum Python docstring style checker

Name: python-%{srcname}
Version: 2.0.0
Release: 0%{?dist}.1
Summary: %{sum}

License: MIT
URL: https://github.com/PyCQA/pydocstyle/
# NOTE: Temporarily use GitHub archive download service until upstream includes
# tests in the release tarballs.
Source0: https://github.com/PyCQA/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch: noarch


%description
A static analysis tool for checking compliance with Python docstring
conventions.

It supports most of PEP 257 out of the box, but it should not be considered a
reference implementation.


%package -n python2-%{srcname}
Summary: %{sum}
%{?python_provide:%python_provide python2-%{srcname}}

BuildRequires: python2-devel
# Required for running tests
BuildRequires: python2-six
BuildRequires: python2-snowballstemmer
BuildRequires: python2-pytest
BuildRequires: python-pytest-pep8
BuildRequires: python2-mock
# NOTE: pathlib is not in BuildRequires since it is only needed by Integration
# tests which are ignored on Python 2 due to reasons described below.

Requires: python2-six
Requires: python2-snowballstemmer

%description -n python2-%{srcname}
A static analysis tool for checking compliance with Python docstring
conventions.

It supports most of PEP 257 out of the box, but it should not be considered a
reference implementation.

NOTE: Only Python 3 version of 'pydocstyle' executable is packaged. See:
python3-%{srcname}.


%package -n python3-%{srcname}
Summary: %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

BuildRequires: python3-devel
# Required for running tests
BuildRequires: python3-six
BuildRequires: python3-snowballstemmer
BuildRequires: python3-pytest
BuildRequires: python3-pytest-pep8
BuildRequires: python3-mock
# NOTE: pathlib is not in BuildRequires since it is part of the Python standard
# library in Python 3.4+.

Requires: python3-six
Requires: python3-snowballstemmer

%description -n python3-%{srcname}
A static analysis tool for checking compliance with Python docstring
conventions.

It supports most of PEP 257 out of the box, but it should not be considered a
reference implementation.


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build

# Remove (incorrect) Python shebang from package's __main__.py file
sed -i '\|/usr/bin/env|d' build/lib/pydocstyle/__main__.py


%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%py2_install
%py3_install


%check
# Run tests under Python 2

# NOTE: Integration tests are ignored on Python 2 since they require having the
# 'pydocstyle' executable installed on the system. As described below, we only
# package Python 3 version of this executable.
# NOTE: We need to specify the PYTHONPATH environment variable so that Python
# can find the system-installed pydocstyle package in %%{buildroot}.
PYTHONPATH="%{buildroot}%{python2_sitelib}" py.test \
    --pep8 \
    --cache-clear \
    --ignore=src/tests/test_integration.py \
    src/tests

# Run tests under Python 3

# Disable "install_package" fixure for integration tests since we want the
# tests to be run against the system-installed version of the package.
# NOTE: Two following blank lines need to be deleted to prevent the PEP8 E303
# error (too many blank lines).
sed -i '/pytestmark = pytest.mark.usefixtures("install_package")/ { N; N; d; }' \
    src/tests/test_integration.py

# Replace 'python(2|3)*' with '%%{__python3}' in tests that run pydocstyle as
# a named Python module.
sed -E -i 's|"python(2\|3)*( -m pydocstyle)|"%{__python3}\2|' \
    src/tests/test_integration.py

# NOTE: We need to specify the PYTHONPATH environment variable so that Python
# can find the system-installed pydocstyle package in %%{buildroot}.
# NOTE: We need to augment the PATH environment variable so that integration
# tests can find the system-installed pydocstyle executables in %%{buildroot}.
PYTHONPATH="%{buildroot}%{python3_sitelib}" PATH="$PATH:%{buildroot}%{_bindir}" py.test-3 \
    --pep8 \
    --cache-clear \
    src/tests


# NOTE: There is no %%files section for the unversioned python module if we are
# building for several python runtimes
%files -n python2-%{srcname}
%license LICENSE-MIT
%doc README.rst
%{python2_sitelib}/*
# NOTE: Only Python 3 versions of executables are packaged as recommended in:
# https://fedoraproject.org/wiki/Packaging:Python#Executables_in_.2Fusr.2Fbin

%files -n python3-%{srcname}
%license LICENSE-MIT
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/pydocstyle


%changelog
* Mon May 08 2017 Tadej Janež <tadej.j@nez.si> 2.0.0-0.1
- Update to 2.0.0 release.
- Update Requires and BuildRequires for the new version.
- Drop pep257 compatibility console script.

* Fri Apr 07 2017 Tadej Janež <tadej.j@nez.si> 1.1.1-0.2
- Temporarily use GitHub arhive download service until upstream includes tests
  in the release tarballs.
- Run tests in %%check.
- Add appropriate BuildRequires for running the tests.
- Remove end-of-line encoding fixes which are no longer necessary.

* Mon Jan 02 2017 Tadej Janež <tadej.j@nez.si> 1.1.1-0.1
- Initial package.
