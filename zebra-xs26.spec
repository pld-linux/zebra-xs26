#
# _without_snmp - without SNMP support (problematic with IPv6?)
Summary:	Routing daemon - xs26 port
Summary(pl):	Demon routingu - port xs26
Summary(pt_BR):	Servidor de roteamento multi-protocolo - xs26
Summary(ru):	äÅÍÏÎ ÍÁÒÛÒÕÔÉÚÁÃÉÉ Zebra - xs26
Summary(uk):	äÅÍÏÎ ÍÁÒÛÒÕÔÉÚÁÃ¦§ Zebra - xs26
Name:		zebra-xs26
Version:	2.08
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.xs26.net/zebra/%{name}-%{version}.tar.gz
Source10:	%{name}-zebra.init
Source11:	%{name}-bgpd.init
Source12:	%{name}-ospf6d.init
Source20:	%{name}-zebra.sysconfig
Source21:	%{name}-bgpd.sysconfig
Source22:	%{name}-ospf6d.sysconfig
Source30:	%{name}-zebra.logrotate
Source31:	%{name}-bgpd.logrotate
Source32:	%{name}-ospf6d.logrotate
Patch1:		%{name}-proc.patch
#Patch3:		%{name}-autoconf.patch
#Patch4:		%{name}-automake.patch
#Patch5:		%{name}-autoheader.patch
Patch6:		%{name}-smallfixes.patch
URL:		http://www.zebra.org/
BuildRequires:	texinfo
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	readline-devel >= 4.1
BuildRequires:	ncurses-devel >= 5.1
BuildRequires:	pam-devel
%{?!_without_snmp:BuildRequires:	ucd-snmp-devel >= 4.2.6}
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Provides:	routingdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	bird
Obsoletes:	gated
Obsoletes:	mrt
Obsoletes:	zebra

%define		_sysconfdir /etc/zebra

%description
Zebra is a multi-server routing software package which provides TCP/IP
based routing protocols also with IPv6 support such as RIP, OSPF, BGP
and so on. Zebra turns your machine into a full powered router.

Daemons for each routing protocols are available in separate packages.

%description -l pl
Program do dynamicznego ustawiania tablicy tras. Mo¿e tak¿e ustalaæ
trasy dla IPv6.

Demony obs³uguj±ce poszczególne protoko³y dostêpne s± w osobnych
pakietach.

%description -l pt_BR
Zebra é um servidor múltiplo para roteamento, provendo suporte aos
protocolos baseados em TCP/IP (inclusive IPv6) tais como RIP, OSPF,
BGP, entre outros. Zebra transforma sua máquina em um poderoso
roteador.

%description -l ru
GNU Zebra - ÜÔÏ Ó×ÏÂÏÄÎÏÅ ÐÒÏÇÒÁÍÍÎÏÅ ÏÂÅÓÐÅÞÅÎÉÅ, ÒÁÂÏÔÁÀÝÅÅ Ó
ÏÓÎÏ×ÁÎÎÙÍÉ ÎÁ TCP/IP ÐÒÏÔÏËÏÌÁÍÉ ÍÁÒÛÒÕÔÉÚÁÃÉÉ.

GNU Zebra ÐÏÄÄÅÒÖÉ×ÁÅÔ BGP4, BGP4+, OSPFv2, OSPFv3, RIPv1, RIPv2 É
RIPng.

%description -l uk
GNU Zebra - ÃÅ ×¦ÌØÎÅ ÐÒÏÇÒÁÍÎÅ ÚÁÂÅÚÐÅÞÅÎÎÑ, ÝÏ ÐÒÁÃÀ¤ Ú ÂÁÚÏ×ÁÎÉÍÉ
ÎÁ TCP/IP ÐÒÏÔÏËÏÌÁÍÉ ÍÁÒÛÒÕÔÉÚÁÃ¦§.

GNU Zebra Ð¦ÄÔÒÉÍÕ¤ BGP4, BGP4+, OSPFv2, OSPFv3, RIPv1, RIPv2 ÔÁ
RIPng.

%package bgpd
Summary:	BGP routing daemon
Summary(pl):	Demon routingu BGP
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Obsoletes:	zebra-bgpd

%description bgpd
BGP routing daemon. Includes IPv6 support.

%description bgpd -l pl
Demon obs³ugi protoko³u BGP. Obs³uguje tak¿e IPv6.

%package ospf6d
Summary:	IPv6 OSPF routing daemon
Summary(pl):	Demon routingu OSPF w sieciach IPv6
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Obsoletes:	zebra-ospf6d

%description ospf6d
OSPF6 routing daemon for IPv6 networks.

%description ospf6d -l pl
Demon obs³ugi protoko³u OSPF w sieciach IPv6.

%prep
%setup  -q -n %{name}
%patch1 -p1
#%patch3 -p1
#%patch4 -p1
#%patch5 -p1
%patch6 -p1

%build
rm -f ./missing
rm -f doc/zebra.info
%{__aclocal}
%{__autoconf}
%{__automake}
%{__autoheader}
%configure \
	--enable-netlink \
	%{?_without_snmp:--disable-snmp} \
	%{?!_without_snmp:--enable-snmp} \
	--enable-ipv6 \
	--enable-ospf6d \
	--enable-bgpd

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d,pam.d} \
	$RPM_BUILD_ROOT/var/log/{archiv,}/zebra \
	$RPM_BUILD_ROOT/var/run/zebra

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE10} $RPM_BUILD_ROOT/etc/rc.d/init.d/zebra
install %{SOURCE11} $RPM_BUILD_ROOT/etc/rc.d/init.d/bgpd
install %{SOURCE12} $RPM_BUILD_ROOT/etc/rc.d/init.d/ospf6d

install %{SOURCE20} $RPM_BUILD_ROOT/etc/sysconfig/zebra
install %{SOURCE21} $RPM_BUILD_ROOT/etc/sysconfig/bgpd
install %{SOURCE22} $RPM_BUILD_ROOT/etc/sysconfig/ospf6d

install %{SOURCE30} $RPM_BUILD_ROOT/etc/logrotate.d/zebra
install %{SOURCE31} $RPM_BUILD_ROOT/etc/logrotate.d/bgpd
install %{SOURCE32} $RPM_BUILD_ROOT/etc/logrotate.d/ospf6d

touch $RPM_BUILD_ROOT/var/log/zebra/{zebra,bgpd,ospf6d}.log

touch $RPM_BUILD_ROOT%{_sysconfdir}/{vtysh.conf,zebra.conf}

gzip -9nf AUTHORS NEWS README REPORTING-BUGS SERVICES TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add zebra >&2
if [ ! -s %{_sysconfdir}/zebra.conf ]; then
        echo "hostname `hostname`" > %{_sysconfdir}/zebra.conf
fi
if [ -f /var/lock/subsys/zebra ]; then
	/etc/rc.d/init.d/zebra restart >&2
else
	echo "Run '/etc/rc.d/init.d/zebra start' to start main routing deamon." >&2
fi

%post bgpd
/sbin/chkconfig --add bgpd >&2
if [ -f /var/lock/subsys/bgpd ]; then
	/etc/rc.d/init.d/bgpd restart >&2
else
	echo "Run '/etc/rc.d/init.d/bgpd start' to start bgpd routing deamon." >&2
fi

%post ospf6d
/sbin/chkconfig --add ospf6d >&2
if [ -f /var/lock/subsys/ospf6d ]; then
	/etc/rc.d/init.d/ospf6d restart >&2
else
	echo "Run '/etc/rc.d/init.d/ospf6d start' to start ospf6d routing deamon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/zebra ]; then
		/etc/rc.d/init.d/zebra stop >&2
	fi
        /sbin/chkconfig --del zebra >&2
fi

%preun bgpd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/bgpd ]; then
		/etc/rc.d/init.d/bgpd stop >&2
	fi
        /sbin/chkconfig --del bgpd >&2
fi

%preun ospf6d
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ospf6d ]; then
		/etc/rc.d/init.d/ospf6d stop >&2
	fi
        /sbin/chkconfig --del ospf6d >&2
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc *.gz
%{_infodir}/*info*
%{_mandir}/man1/*
%dir %attr(750,root,root) %{_sysconfdir}
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) %{_sysconfdir}/*.conf
%dir %attr(750,root,root) /var/run/zebra
%dir %attr(750,root,root) /var/log/zebra
%dir %attr(750,root,root) /var/log/archiv/zebra

%doc zebra/*sample*
%{_mandir}/man8/zebra*
%attr(755,root,root) %{_sbindir}/zebra
%attr(754,root,root) /etc/rc.d/init.d/zebra
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) /etc/sysconfig/zebra
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) /etc/logrotate.d/zebra
%ghost /var/log/zebra/zebra*

%files bgpd
%defattr(644,root,root,755)
%doc bgpd/*sample*
%{_mandir}/man8/bgpd*
%attr(755,root,root) %{_sbindir}/bgpd
%attr(754,root,root) /etc/rc.d/init.d/bgpd
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) /etc/sysconfig/bgpd
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) /etc/logrotate.d/bgpd
%ghost /var/log/zebra/bgpd*

%files ospf6d
%defattr(644,root,root,755)
%doc ospf6d/*sample*
%{_mandir}/man8/ospf6d*
%attr(755,root,root) %{_sbindir}/ospf6d
%attr(754,root,root) /etc/rc.d/init.d/ospf6d
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) /etc/sysconfig/ospf6d
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) /etc/logrotate.d/ospf6d
%ghost /var/log/zebra/ospf6d*
