Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de):	Client f�r das 'trivial file transfer protocol (tftp)'
Summary(fr):	Client pour le � trivial file transfer protocol � (tftp)
Summary(pl):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr):	�lkel dosya aktar�m protokolu (TFTP) i�in sunucu ve istemci
Name:		atftp
Version:	0.6.2
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.mamalinux.com/pub/atftp/%{name}-%{version}.tar.gz
# Source0-md5:	b3b8d4b7e558046adfcaef180ae77c4f
Source1:	atftpd.inetd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libwrap-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	tftp
Obsoletes:	tftp-hpa

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. This package contains tftp client.

%description -l de
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr
Le � trivial file transfer protocol � (tftp) est normalement utilis�
uniquement pour d�marrer les stations de travail sans disque. Il offre
tr�s peu de s�curit� et ne devrait pas �tre activ� sauf si c'est
n�cessaire.

%description -l pl
Tftp (trivial file transfer protocol) jest u�ywany g��wnie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawiera aplikacj�
tftp klienta.

%description -l tr
�lkel dosya aktar�m protokolu genelde disksiz i� istasyonlar�n�n a�
�zerinden a��lmalar�nda kullan�l�r. G�venlik denetimleri �ok az
oldu�undan zorunlu kalmad�k�a �al��t�r�lmamal�d�r.

%package -n atftpd
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(de):	D�mon f�r das 'trivial file transfer protocol (tftp)'
Summary(fr):	D�mon pour le � trivial file transfer protocol � (tftp)
Summary(pl):	Serwer tftp (trivial file transfer protocol)
Summary(tr):	�lkel dosya aktar�m protokolu (TFTP) i�in sunucu ve istemci
Group:		Networking/Daemons
PreReq:		rc-inetd >= 0.8.1
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Provides:	tftpdaemon
Obsoletes:	tftpd-hpa
Obsoletes:	tftp-server
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
Le � trivial file transfer protocol � (tftp) est normalement utilis�
uniquement pour d�marrer les stations de travail sans disque. Il offre
tr�s peu de s�curit� et ne devrait pas �tre activ� sauf si c'est
n�cessaire.

%description -n atftpd -l pl
TFTP (Trivial File Transfer Protocol) jest u�ywany g��wnie do
startowania stacji bezdyskowych z sieci. Serwer tftp powinien by�
instalowany tylko wtedy, kiedy zachodzi taka konieczno�� poniewa�
nale�y on do aplikacji o niskim poziomie bezpiecze�stwa.

%prep
%setup  -q

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},%{_sbindir},/etc/sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,8},/var/lib/tftp}

install atftpd $RPM_BUILD_ROOT%{_sbindir}
install atftp $RPM_BUILD_ROOT%{_bindir}
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install *.1 $RPM_BUILD_ROOT%{_mandir}/man1/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n atftpd
if [ -n "`id -u tftp 2>/dev/null`" ]; then
	if [ "`id -u tftp`" != "15" ]; then
		echo "Error: user tftp doesn't have uid=15. Correct this before installing tftpd." 1>&2
		exit 1
	fi
else
	echo "Adding user tftp UID=15."
	/usr/sbin/useradd -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g ftp tftp 1>&2
fi

%post -n atftpd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server." 1>&2
fi

%postun -n atftpd
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi
if [ "$1" = "0" ]; then
	echo "Removing user tftp."
	/usr/sbin/userdel tftp
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n atftpd
%defattr(644,root,root,755)
%doc README FAQ
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/tftpd
%attr(750,tftp,root) %dir /var/lib/tftp
%{_mandir}/man8/*
