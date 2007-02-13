#
# todo:
# - mono bindings (build crashes on ppc)
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Bluetooth GObject based library
Summary(pl.UTF-8):	Biblioteka do programowania urządzeń Bluetooth
Name:		libbtctl
Version:	0.8.2
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libbtctl/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	00966e109db14f14589739a85fe00941
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bluez-libs-devel >= 2.25
BuildRequires:	glib2-devel >= 1:2.12.4
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	openobex-devel >= 1.2
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-pygtk-devel >= 2.10.3
Requires:	bluez-libs >= 2.25
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a library to control Bluetooth devices.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę do kontrolowania urządzeń Bluetooth.

%package devel
Summary:	Header files for libbtctl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbtctl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bluez-libs-devel >= 2.25
Requires:	glib2-devel >= 1:2.12.4
Requires:	openobex-devel >= 1.2

%description devel
Header files for libbtctl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbtctl.

%package static
Summary:	Static libbtctl library
Summary(pl.UTF-8):	Statyczna biblioteka libbtctl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbtctl library.

%description static -l pl.UTF-8
Statyczna biblioteka libbtctl.

%package -n python-btctl
Summary:	Python bindings for libbtctl library
Summary(pl.UTF-8):	Wiązania dla języka Python biblioteki libbtctl
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-btctl
Static libbtctl library.

%description -n python-btctl -l pl.UTF-8
Wiązania dla języka Python biblioteki libbtctl.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-mono \
	--enable-gtk-doc \
	--with-html-path=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static}
%{__make} \
	pydir=%{py_sitedir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir} \
	pydir=%{py_sitedir}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif

%files -n python-btctl
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
