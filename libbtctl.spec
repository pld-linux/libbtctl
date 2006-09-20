#
# todo:
# - mono bindings (build crashes on ppc)
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Bluetooth GObject based library
Summary(pl):	Biblioteka do programowania urz±dzeñ Bluetooth
Name:		libbtctl
Version:	0.8.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libbtctl/0.8/%{name}-%{version}.tar.gz
# Source0-md5:	a4b35a8d2c963a594fc13da5056f30e2
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bluez-libs-devel >= 2.25
BuildRequires:	glib2-devel >= 1:2.12.3
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	intltool >= 0.18
BuildRequires:	libtool
BuildRequires:	openobex-devel >= 1.2
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-pygtk-devel >= 2.10.1
Requires:	bluez-libs >= 2.25
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a library to control Bluetooth devices.

%description -l pl
Ten pakiet zawiera bibliotekê do kontrolowania urz±dzeñ Bluetooth.

%package devel
Summary:	Header files for libbtctl library
Summary(pl):	Pliki nag³ówkowe biblioteki libbtctl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bluez-libs-devel >= 2.25
Requires:	glib2-devel >= 1:2.12.3
Requires:	openobex-devel >= 1.2

%description devel
Header files for libbtctl library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libbtctl.

%package static
Summary:	Static libbtctl library
Summary(pl):	Statyczna biblioteka libbtctl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbtctl library.

%description static -l pl
Statyczna biblioteka libbtctl.

%package -n python-btctl
Summary:	Python bindings for libbtctl library
Summary(pl):	Wi±zania dla jêzyka Python biblioteki libbtctl
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-btctl
Static libbtctl library.

%description -n python-btctl -l pl
Wi±zania dla jêzyka Python biblioteki libbtctl.

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
