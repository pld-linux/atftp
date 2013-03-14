Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de.UTF-8):	Client für das 'trivial file transfer protocol (tftp)'
Summary(fr.UTF-8):	Client pour le « trivial file transfer protocol » (tftp)
Summary(pl.UTF-8):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr.UTF-8):	İlkel dosya aktarım protokolu (TFTP) için sunucu ve istemci
Name:		atftp
Version:	0.7.1
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://downloads.sourceforge.net/project/atftp/%{name}-%{version}.tar.gz
# Source0-md5:	367bf401965fbed04585b1229c2191a8
Source1:	%{name}d.inetd
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Patch0:		%{name}-tinfo.patch
Patch1:		%{name}-clk.patch
URL:		http://sourceforge.net/projects/atftp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. This package contains tftp client.

%description -l de.UTF-8
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr.UTF-8
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -l pl.UTF-8
Tftp (trivial file transfer protocol) jest używany głównie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawiera aplikację
tftp klienta.

%description -l tr.UTF-8
İlkel dosya aktarım protokolu genelde disksiz iş istasyonlarının ağ
üzerinden açılmalarında kullanılır. Güvenlik denetimleri çok az
olduğundan zorunlu kalmadıkça çalıştırılmamalıdır.

%package -n atftpd-common
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(de.UTF-8):	Dämon für das 'trivial file transfer protocol (tftp)'
Summary(fr.UTF-8):	Démon pour le « trivial file transfer protocol » (tftp)
Summary(pl.UTF-8):	Serwer tftp (trivial file transfer protocol)
Summary(tr.UTF-8):	İlkel dosya aktarım protokolu (TFTP) için sunucu ve istemci
Group:		Networking/Daemons/FTP
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

%description -n atftpd-common -l de.UTF-8
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -n atftpd-common -l fr.UTF-8
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -n atftpd-common -l pl.UTF-8
TFTP (Trivial File Transfer Protocol) jest używany głównie do
startowania stacji bezdyskowych z sieci. Serwer tftp powinien być
instalowany tylko wtedy, kiedy zachodzi taka konieczność ponieważ
należy on do aplikacji o niskim poziomie bezpieczeństwa.

%package -n atftpd-inetd
Summary:	inetd configs for atftpd
Summary(pl.UTF-8):	Pliki konfiguracyjne do użycia atftpd poprzez inetd
Group:		Networking/Daemons/FTP
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

%description -n atftpd-inetd -l pl.UTF-8
Pliki konfiguracyjna atftpd do startowania demona poprzez inetd.

%package -n atftpd-standalone
Summary:	Standalone daemon configs for atftpd
Summary(pl.UTF-8):	Pliki konfiguracyjne do startowania atftpd w trybie standalone
Group:		Networking/Daemons/FTP
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

%description -n atftpd-standalone -l pl.UTF-8
Pliki konfiguracyjne atftpd do startowania demona w trybie
standalone.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

sed -i -e 's#AM_CONFIG_HEADER#AC_CONFIG_HEADERS#g' configure.ac
sed -i -e 's#CFLAGS="-g -Wall -D_REENTRANT"##g' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}

%configure \
	--enable-libreadline \
	--enable-libwrap \
	--enable-libpcre \
	--enable-mtftp
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},/var/lib/tftp} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,8},} \
	$RPM_BUILD_ROOT{/etc/sysconfig/rc-inetd,/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
