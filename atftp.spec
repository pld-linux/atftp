Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de):	Client für das 'trivial file transfer protocol (tftp)'
Summary(fr):	Client pour le « trivial file transfer protocol » (tftp)
Summary(pl):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr):	Ýlkel dosya aktarým protokolu (TFTP) için sunucu ve istemci
Name:		atftp
Version:	0.7
Release:	10
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.mamalinux.com/pub/atftp/%{name}-%{version}.tar.gz
# Source0-md5:	3b27365772d918050b2251d98a9c7c82
Source1:	%{name}d.inetd
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Patch0:		%{name}-debian.patch
Patch1:		%{name}-tinfo.patch
Patch2:		%{name}-clk.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. This package contains tftp client.

%description -l de
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -l pl
Tftp (trivial file transfer protocol) jest u¿ywany g³ównie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawiera aplikacjê
tftp klienta.

%description -l tr
Ýlkel dosya aktarým protokolu genelde disksiz iþ istasyonlarýnýn að
üzerinden açýlmalarýnda kullanýlýr. Güvenlik denetimleri çok az
olduðundan zorunlu kalmadýkça çalýþtýrýlmamalýdýr.

%package -n atftpd-common
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(de):	Dämon für das 'trivial file transfer protocol (tftp)'
Summary(fr):	Démon pour le « trivial file transfer protocol » (tftp)
Summary(pl):	Serwer tftp (trivial file transfer protocol)
Summary(tr):	Ýlkel dosya aktarým protokolu (TFTP) için sunucu ve istemci
Group:		Networking/Daemons
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Provides:	user(tftp)

%description -n atftpd-common
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. The tftp package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine. It provides very little security, and should not be
enabled unless it is needed.

%description -n atftpd-common -l de
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -n atftpd-common -l fr
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -n atftpd-common -l pl
TFTP (Trivial File Transfer Protocol) jest u¿ywany g³ównie do
startowania stacji bezdyskowych z sieci. Serwer tftp powinien byæ
instalowany tylko wtedy, kiedy zachodzi taka konieczno¶æ poniewa¿
nale¿y on do aplikacji o niskim poziomie bezpieczeñstwa.

%package -n atftpd-inetd
Summary:	inetd configs for atftpd
Summary(pl):	Pliki konfiguracyjne do u¿ycia atftpd poprzez inetd
Group:		Daemons
Requires:	atftpd-common = %{epoch}:%{version}-%{release}
Requires:	rc-inetd >= 0.8.1
Provides:	tftpdaemon
Obsoletes:	atftpd
Obsoletes:	inetutils-tftpd
Obsoletes:	tftp-server
Obsoletes:	tftpd
Obsoletes:	tftpd-hpa
Obsoletes:	utftpd

%description -n atftpd-inetd
atftpd configs for running from inetd.

%description -n atftpd-inetd -l pl
Pliki konfiguracyjna atftpd do startowania demona poprzez inetd.

%package -n atftpd-standalone
Summary:	Standalone daemon configs for atftpd
Summary(pl):	Pliki konfiguracyjne do startowania atftpd w trybie standalone
Group:		Daemons
Requires:	atftpd-common = %{epoch}:%{version}-%{release}
Requires:	rc-scripts
Provides:	tftpdaemon
Obsoletes:	atftpd
Obsoletes:	inetutils-tftpd
Obsoletes:	tftp-server
Obsoletes:	tftpd
Obsoletes:	tftpd-hpa
Obsoletes:	utftpd

%description -n atftpd-standalone
atftpd configs for running as a standalone daemon.

%description -n atftpd-standalone -l pl
Pliki konfiguracyjne atftpd do startowania demona w trybie
standalone.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
sed -i -e 's#argz.h##g' Makefile*
rm -f missing argz.h
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},/var/lib/tftp} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,8},} \
	$RPM_BUILD_ROOT{/etc/sysconfig/rc-inetd,/etc/rc.d/init.d}

install atftpd $RPM_BUILD_ROOT%{_sbindir}
install atftp $RPM_BUILD_ROOT%{_bindir}
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install *.1 $RPM_BUILD_ROOT%{_mandir}/man1/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/atftpd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/atftpd

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n atftpd-common
%useradd -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g ftp tftp

%postun -n atftpd-common
if [ "$1" = "0" ]; then
	%userremove tftp
fi

%post -n atftpd-inetd
%service -q rc-inetd reload

%postun -n atftpd-inetd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%post -n atftpd-standalone
/sbin/chkconfig --add atftpd
%service atftpd restart

%preun
if [ "$1" = "0" ]; then
        %service atftpd stop
        /sbin/chkconfig --del atftpd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n atftpd-common
%defattr(644,root,root,755)
%doc README FAQ
%attr(755,root,root) %{_sbindir}/*
%attr(750,tftp,root) %dir /var/lib/tftp
%{_mandir}/man8/*

%files -n atftpd-inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/tftpd

%files -n atftpd-standalone
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/atftpd
%attr(754,root,root) /etc/rc.d/init.d/atftpd
