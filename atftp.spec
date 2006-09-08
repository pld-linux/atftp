Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de):	Client für das 'trivial file transfer protocol (tftp)'
Summary(fr):	Client pour le « trivial file transfer protocol » (tftp)
Summary(pl):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr):	Ýlkel dosya aktarým protokolu (TFTP) için sunucu ve istemci
Name:		atftp
Version:	0.7
Release:	8
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.mamalinux.com/pub/atftp/%{name}-%{version}.tar.gz
# Source0-md5:	3b27365772d918050b2251d98a9c7c82
Source1:	%{name}d.inetd
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

%package -n atftpd
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(de):	Dämon für das 'trivial file transfer protocol (tftp)'
Summary(fr):	Démon pour le « trivial file transfer protocol » (tftp)
Summary(pl):	Serwer tftp (trivial file transfer protocol)
Summary(tr):	Ýlkel dosya aktarým protokolu (TFTP) için sunucu ve istemci
Group:		Networking/Daemons
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	rc-inetd >= 0.8.1
Provides:	tftpdaemon
Provides:	user(tftp)
Obsoletes:	inetutils-tftpd
Obsoletes:	tftp-server
Obsoletes:	tftpd
Obsoletes:	tftpd-hpa
Obsoletes:	utftpd

%description -n atftpd
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. The tftp package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine. It provides very little security, and should not be
enabled unless it is needed.

%description -n atftpd -l de
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -n atftpd -l fr
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -n atftpd -l pl
TFTP (Trivial File Transfer Protocol) jest u¿ywany g³ównie do
startowania stacji bezdyskowych z sieci. Serwer tftp powinien byæ
instalowany tylko wtedy, kiedy zachodzi taka konieczno¶æ poniewa¿
nale¿y on do aplikacji o niskim poziomie bezpieczeñstwa.

%prep
%setup -q

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},/etc/sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,8},/var/lib/tftp}

install atftpd $RPM_BUILD_ROOT%{_sbindir}
install atftp $RPM_BUILD_ROOT%{_bindir}
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install *.1 $RPM_BUILD_ROOT%{_mandir}/man1/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n atftpd
%useradd -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g ftp tftp

%post -n atftpd
%service -q rc-inetd reload

%postun -n atftpd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
	%userremove tftp
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n atftpd
%defattr(644,root,root,755)
%doc README FAQ
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/tftpd
%attr(750,tftp,root) %dir /var/lib/tftp
%{_mandir}/man8/*
