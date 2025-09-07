#
# todo:
# - mono bindings (build crashes on ppc)
#
# Conditional build:
%bcond_without	apidocs		# gtk-doc based API documentation
%bcond_without	static_libs	# static library

Summary:	Bluetooth GObject based library
Summary(pl.UTF-8):	Biblioteka do programowania urządzeń Bluetooth
Name:		libbtctl
Version:	0.11.1
Release:	3
# most code is LGPL v2.1+ but obexsdp.c is GPL v2+
License:	GPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libbtctl/0.11/%{name}-%{version}.tar.bz2
# Source0-md5:	5b5ab9e71dd5428c4e5c45cbf581a384
Patch0:		%{name}-openobex.patch
Patch1:		%{name}-pygobject.patch
Patch2:		%{name}-gtkdoc.patch
Patch3:		format-security.patch
Patch4:		%{name}-proto.patch
# dead
#URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	bluez-libs-devel >= 4.0
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.12.4
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.7}
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	openobex-devel >= 1.2
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-pygtk-devel >= 2.10.3
BuildRequires:	rpm-pythonprov
Requires:	bluez-libs >= 4.0
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
Requires:	bluez-libs-devel >= 4.0
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
BuildArch:	noarch

%description apidocs
libbtctl API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libbtctl.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON="%{__python}" \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	--disable-mono \
	%{!?with_static_libs:--disable-static} \
	--with-html-path=%{_gtkdocdir}

%{__make} \
	pydir=%{py_sitedir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir} \
	pydir=%{py_sitedir}

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.a
%endif
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbtctl.la

%if %{without apidocs}
%{__rm} -rf $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libbtctl.so.*.*.*
%ghost %{_libdir}/libbtctl.so.6

%files devel
%defattr(644,root,root,755)
%{_libdir}/libbtctl.so
%{_includedir}/libbtctl
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
