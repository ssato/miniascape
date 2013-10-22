%define guests_builddir {{ guests_build_datadir|default('/usr/share/miniascape/build/guests') }}

Name:           {{ name|default('miniascape-guests-build-default') }}
Version:        {{ version|default('0.0.1') }}
Release:        1%{?dist}
Summary:        Packaged data of %{name}
License:        {{ license|default('MIT') }}
URL:            http://example.com
Source0:        %{name}-%{version}.tar.xz
BuildArch:      noarch

%description
Packaged data of %{name}

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%files
# TODO: Add a docuemnt to describe what and how guests are built from scripts
# and kickstart configuration files in this package.
#%doc
%{guests_builddir}/*/*

%changelog
* {{ timestamp }} {{ user|default('miniascape') }} <{{ builder|default('miniascape@localhost') }}> - {{ version|default('0.0.1') }}-1
- Initial (static) packaging
