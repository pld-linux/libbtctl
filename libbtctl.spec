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
Version:	0.6.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libbtctl/0.6/%{name}-%{version}.tar.gz
# Source0-md5:	916cb1b8054b529a8dd944bd72bb7193
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bluez-libs-devel >= 2.8-2
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gtk-doc >= 0.10
BuildRequires:	libtool
BuildRequires:	openobex-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-pygtk-devel >= 2.2.0
Requires:	bluez-libs >= 2.8-2
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
Requires:	bluez-libs-devel >= 2.8-2
Requires:	glib2-devel >= 2.0.0
Requires:	openobex-devel

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
