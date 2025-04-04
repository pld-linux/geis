#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	An implementation of the GEIS (Gesture Engine Interface and Support) interface
Summary(pl.UTF-8):	Implementacja interfejsu GEIS (Gesture Engine Interface and Support)
Name:		geis
Version:	2.2.17
Release:	12
License:	GPL v3/LGPL v3
Group:		Libraries
Source0:	https://launchpad.net/geis/trunk/%{version}/+download/%{name}-%{version}.tar.xz
# Source0-md5:	2ff9d76a3ea5794516bb02c9d1924faf
Patch0:		build.patch
URL:		https://launchpad.net/geis
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-devel >= 1.2.16
BuildRequires:	frame-devel >= 2.2
BuildRequires:	grail-devel >= 3.0.8
BuildRequires:	libtool >= 2:2.2.6b
BuildRequires:	libxcb-devel >= 1.6
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools > 1:7.0
BuildRequires:	rpm-pythonprov
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel >= 1.3
BuildRequires:	xorg-xserver-server-devel >= 1.10.1
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GEIS is a library for applications and toolkit programmers which
provides a consistent platform independent interface for any
system-wide input gesture recognition mechanism.

%description -l pl.UTF-8
GEIS to biblioteka dla programistów aplikacji i toolkitów,
zapewniająca spójny, niezależny od platformy interfejs do wszystkich
systemowych mechanizmów rozpoznawania gestów.

%package tools
Summary:	Test tools for geis library
Summary(pl.UTF-8):	Testowe narzędzia biblioteki geis
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description tools
Test tools for geis library.

%description tools -l pl.UTF-8
Testowe narzędzia biblioteki geis.

%package devel
Summary:	Header files for geis library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki geis
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for geis library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki geis.

%package static
Summary:	Static geis library
Summary(pl.UTF-8):	Statyczna biblioteka geis
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static geis library.

%description static -l pl.UTF-8
Statyczna biblioteka geis.

%package -n python3-geis
Summary:	Python 3 bindings for geis library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki geis
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-modules

%description -n python3-geis
Python 3 bindings for geis library.

%description -n python3-geis -l pl.UTF-8
Wiązania Pythona 3 do biblioteki geis.

%package -n geisview
Summary:	A tool to view operation of the GEIS API
Summary(pl.UTF-8):	Narzędzie do przeglądania działania GEIS API.
Group:		Applications
Requires:	python3-geis = %{version}-%{release}

%description -n geisview
A tool to view operation of the GEIS API.

%description -n geisview -l pl.UTF-8
Narzędzie do przeglądania działania GEIS API.

%prep
%setup -q
%patch -P 0 -p1

sed -i -e 's#-pedantic##g' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_geis_bindings.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_geis_bindings.a
%endif
# source data for apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/geis

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libgeis.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeis.so.1

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/geistest
%attr(755,root,root) %{_bindir}/pygeis
%{_mandir}/man1/pygeis.1*
%{_mandir}/man1/geistest.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeis.so
%{_includedir}/geis
%{_pkgconfigdir}/libgeis.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgeis.a
%endif

%files -n python3-geis
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_geis_bindings.so
%dir %{py3_sitescriptdir}/geis
%{py3_sitescriptdir}/geis/__pycache__
%{py3_sitescriptdir}/geis/__init__.py*
%{py3_sitescriptdir}/geis/geis_v2.py*

%files -n geisview
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/geisview
%dir %{py3_sitescriptdir}/geisview
%{py3_sitescriptdir}/geisview/__pycache__
%{py3_sitescriptdir}/geisview/*.py*
%{_desktopdir}/geisview.desktop
%dir %{_datadir}/geisview
%{_datadir}/geisview/filter_definition.ui
%{_datadir}/geisview/filter_list.ui
%{_datadir}/geisview/geisview.ui
%{_pixmapsdir}/geisview32x32.xpm
%{_mandir}/man1/geisview.1*
