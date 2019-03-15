#
# todo:
# - mono bindings (build crashes on ppc)
#
# Conditional build:
%bcond_with	apidocs		# enable gtk-doc
%bcond_without	static_libs	# don't build static library

Summary:	Bluetooth GObject based library
Summary(pl.UTF-8):	Biblioteka do programowania urządzeń Bluetooth
Name:		libbtctl
Version:	0.10.0
Release:	11
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libbtctl/0.10/%{name}-%{version}.tar.bz2
# Source0-md5:	83d5f90efb2b26d1bd12a668940d02ba
Patch0:		%{name}-make-jN.patch
Patch1:		%{name}-newapi.patch
Patch2:		glib.patch
Patch3:		format-security.patch
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bluez-libs-devel >= 2.25
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.12.4
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.7}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	openobex-devel >= 1.2
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-pygtk-devel >= 2.10.3
BuildRequires:	rpm-pythonprov
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
Requires:	python-libs

%description -n python-btctl
Static libbtctl library.

%description -n python-btctl -l pl.UTF-8
Wiązania dla języka Python biblioteki libbtctl.

%package apidocs
Summary:	libbtctl API documentation
Summary(pl.UTF-8):	Dokumentacja API libbtctl
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
libbtctl API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libbtctl.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-mono \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
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

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/libbtctl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbtctl.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbtctl.so
%{_libdir}/libbtctl.la
%{_includedir}/%{name}
%{_pkgconfigdir}/libbtctl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbtctl.a
%endif

%files -n python-btctl
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/btctl.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbtctl
%endif
