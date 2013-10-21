Name:           {{ name|default('miniascape-host-data-default') }}
Version:        {{ version|default('0.0.1') }}
Release:        1%{?dist}
Summary:        Packaged data of %{name}
License:        {{ license|default('MIT') }}
URL:            http://example.com
Source0:        %{name}-%{version}.tar.xz
BuildArch:      noarch

%description
Packaged data of %{name}

%package        overrides
Summary:        Configuration files to override existing ones

%description    overrides
This package provides configuration files to override existing files provided
by other packages. Current provided configuraion overrides are
/etc/fence_virt.conf.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

# Avoid to conflict w/ /etc/fence_virt.conf provided by fence-virtd rpm:
mv $RPM_BUILD_ROOT/%{_sysconfdir}/fence_virt.conf $RPM_BUILD_ROOT/%{_sysconfdir}/fence_virt.conf.ovrrd

# FIXME: Too simple and not safe. How about making use of some rpm scriptlets
# derived from the rpm scriptlet templates in packagermaker.
%post           overrides
if [ $1 = 1 -o $1 = 2 ]; then    # install or update
    test -f %{_sysconfdir}/fence_virt.conf.ovrrdsave || cp %{_sysconfdir}/fence_virt.conf %{_sysconfdir}/fence_virt.conf.ovrrdsave
    cp -f %{_sysconfdir}/fence_virt.conf.ovrrd %{_sysconfdir}/fence_virt.conf
fi

%preun          overrides
if [ $1 = 0 ]; then    # uninstall (! update)
    cp -f %{_sysconfdir}/fence_virt.conf.ovrrdsave %{_sysconfdir}/fence_virt.conf
fi

%files
#%doc
%{_datadir}/miniascape/networks.d/*.xml
%{_libexecdir}/miniascape/*.sh
%{_libexecdir}/miniascape/default/*.sh
%{_sysconfdir}/modprobe.d/kvm.conf
%{_sysconfdir}/httpd/conf.d/miniascape_autoinst.conf
%{_sysconfdir}/auto.master.d/isos.autofs
%{_sysconfdir}/auto.isos

%files          overrides
%{_sysconfdir}/fence_virt.conf.ovrrd

%changelog
* {{ timestamp }} {{ packager|default('miniascape') }} <{{ email|default('miniascape@localhost') }}> - {{ version|default('0.0.1') }}-1
- Initial (static) packaging
