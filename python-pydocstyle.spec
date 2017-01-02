%global srcname pydocstyle
%global sum Python docstring style checker

Name: python-%{srcname}
Version: 1.1.1
Release:0%{?dist}.1
Summary: %{sum}

License: MIT
URL: https://github.com/PyCQA/pydocstyle/
# NOTE: Upstream doesn't provide ordinary tarballs
Source0: https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.zip

BuildArch: noarch

BuildRequires: python2-devel python3-devel

%description
A static analysis tool for checking compliance with Python docstring
conventions.

It supports most of PEP 257 out of the box, but it should not be considered a
reference implementation.


%package -n python2-%{srcname}
Summary: %{sum}
%{?python_provide:%python_provide python2-%{srcname}}

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

# Fix end-of-line enconding (by stripping carriage returns) of README.rst file
sed -i 's/\r$//' README.rst


%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%py2_install
%py3_install


# NOTE: Tests are not included in the source distribution
#%%check


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
# NOTE: pep257 is provided for compatibility reasons since pydocstyle was
# named pep257 before Jan 29 2016
%{_bindir}/pep257


%changelog
* Mon Jan 02 2017 Tadej Janež <tadej.j@nez.si> 1.1.1-0.1
- Initial package.
