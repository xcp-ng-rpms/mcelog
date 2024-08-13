%global package_speccommit c34183d888dfa0a8ddde61dc6f155c6c841c7dd1
%global usver 196
%global xsver 3
%global xsrel %{xsver}%{?xscount}%{?xshash}

Summary:	Tool to translate x86-64 CPU Machine Check Exception data
Name:		mcelog
Version:	196
Release:	%{xsrel}%{?dist}
Epoch:		3
Group:		System Environment/Base
License:	GPL-2.0-only
URL:		https://github.com/andikleen/mcelog
Source0: mcelog-196.tar.gz
# note that this source OVERRIDES the one on the tarball above!
Source1: mcelog.conf
Source2: mcelog.service
ExclusiveArch:	i686 x86_64
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: make
BuildRequires: gcc
BuildRequires: systemd

%description
mcelog is a utility that collects and decodes Machine Check Exception data
on x86-32 and x86-64 systems.

%prep
%autosetup

%build
%make_build CFLAGS="$RPM_OPT_FLAGS -fpie -pie"

%install
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man{5,8}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
install -p -m755 mcelog $RPM_BUILD_ROOT/%{_sbindir}/mcelog
install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/mcelog.conf
install -p -m755 triggers/cache-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/cache-error-trigger
install -p -m755 triggers/dimm-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/dimm-error-trigger
install -p -m755 triggers/page-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/page-error-trigger
install -p -m755 triggers/socket-memory-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/socket-memory-error-trigger
install -p -m644 mcelog.service $RPM_BUILD_ROOT%{_unitdir}/mcelog.service
install -p -m644 mcelog*.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -p -m644 mcelog*.5 $RPM_BUILD_ROOT/%{_mandir}/man5/

%post
%systemd_post mcelog.service
systemctl daemon-reload

%preun
%systemd_preun mcelog.service

%postun
%systemd_postun_with_restart mcelog.service

%files
%{_sbindir}/mcelog
%dir %{_sysconfdir}/mcelog
%{_sysconfdir}/mcelog/triggers
%config(noreplace) %{_sysconfdir}/mcelog/mcelog.conf
%{_unitdir}/mcelog.service
%{_mandir}/*/*

%changelog
* Tue Jun 18 2024 Gerald Elder-Vass <gerald.elder-vass@cloud.com> - 3:196-3
- CP-47026: Move mcelog config changes to mcelog.spec

* Wed Jan 03 2024 Gerald Elder-Vass <gerald.elder-vass@cloud.com> - 3:196-2
- Fix up spec file
- CP-46265: Load dmi-sysfs to remove dependency on /dev/mem

* Wed Dec 13 2023 Gerald Elder-Vass <gerald.elder-vass@cloud.com> - 3:196-1
- Complete import for 196 (144 is not actually 144 and will cause issues)

* Wed Dec 13 2023 Gerald Elder-Vass <gerald.elder-vass@citrix.com> - 3:144.8.94d853b2ea81
- First imported release
