%define debug_package %{nil}

%define	major	1
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname -d %{name}

%ifarch %ix86
%define pkg_arch i386
%else
%define pkg_arch x86_64
%endif

Name:		samsung-unified-driver
Version:	1.00.37
Release:	1
Group:		System/Kernel and hardware
License:	Samsung
Summary:	Unified Linux Driver for Samsung printers and scanners
Url:		https://www.samsung.com
Source0:	http://downloadcenter.samsung.com/content/DR/201512/20151210091120064/uld_v%{version}_00.99.tar.gz
Source1:	xerox_mfp-smfp.conf
Source100:	%{name}.rpmlintrc
ExclusiveArch:  %{ix86} x86_64

%description
Unified Linux Driver for Samsung printers and scanners.

%files
%doc uld/noarch/license/eula*.txt
%{_datadir}/ppd/suld
%{_sysconfdir}/sane.d/*.conf
%{_sysconfdir}/sane.d/dll.d/*
%{_libdir}/cups/filter/*
%{_libdir}/sane/*
%{_libdir}/*.so
%{_sysconfdir}/udev/rules.d/*
%{_libdir}/cups/backend/*
%lang(fr) %{_datadir}/fr/LC_MESSAGES/*.mo


%prep
%setup -qc -n %{name}-%{version}

%build

%install

    mkdir -p %{buildroot}/etc/sane.d
    cp uld/noarch/etc/smfp.conf %{buildroot}/etc/sane.d
    cp %SOURCE1 %{buildroot}/etc/sane.d

    mkdir -p %{buildroot}/etc/sane.d/dll.d
    echo smfp > %{buildroot}/etc/sane.d/dll.d/smfp-scanner
    echo xerox_mfp-smfp > %{buildroot}/etc/sane.d/dll.d/smfp-scanner-fix

    mkdir -p %{buildroot}/%{_libdir}
    cp uld/%pkg_arch/libscmssc.so %{buildroot}/%{_libdir}

    mkdir -p %{buildroot}/%{_libdir}/cups/backend
    cp uld/%pkg_arch/smfpnetdiscovery %{buildroot}/%{_libdir}/cups/backend

    mkdir -p %{buildroot}/%{_libdir}/cups/filter
    cp uld/%pkg_arch/pstosecps %{buildroot}/%{_libdir}/cups/filter
    cp uld/%pkg_arch/rastertospl %{buildroot}/%{_libdir}/cups/filter

    mkdir -p %{buildroot}/%{_libdir}/sane
    cp uld/%pkg_arch/libsane-smfp.so.1.0.1 %{buildroot}/%{_libdir}/sane
    ln -s libsane-smfp.so.1.0.1 %{buildroot}/%{_libdir}/sane/libsane-smfp.so.1
    ln -s libsane-smfp.so.1 %{buildroot}/%{_libdir}/sane/libsane-smfp.so

    mkdir -p %{buildroot}/etc/udev/rules.d
    (
        OEM_FILE=uld/noarch/oem.conf
        INSTALL_LOG_FILE=/dev/null
        source uld/noarch/scripting_utils
        source uld/noarch/package_utils
        source uld/noarch/scanner-script.pkg
        fill_full_template uld/noarch/etc/smfp.rules.in %{buildroot}/etc/udev/rules.d/60_smfp_samsung.rules
    )

    cp -r uld/noarch/share/locale %{buildroot}/usr/share
    rm -f %{buildroot}/usr/share/locale/fr/LC_MESSAGES/install.mo

    mkdir -p %{buildroot}/usr/share/ppd/suld
    for ppd in uld/noarch/share/ppd/*.ppd; do
        gzip < "$ppd" > %{buildroot}/usr/share/ppd/suld/"${ppd##*/}".gz
    done

    mkdir -p %{buildroot}/usr/share/ppd/suld/cms
    for cts in uld/noarch/share/ppd/cms/*.cts; do
        cp "$cts" %{buildroot}/usr/share/ppd/suld/cms
    done
