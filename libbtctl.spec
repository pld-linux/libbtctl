Summary:	Bluetooth controlling GObject
Summary(pl):	GObject do kontrolowania urządzeń Bluetooth
Name:		libbtctl
Version:	0.3
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://usefulinc.com/software/gnome-bluetooth/releases/%{name}-%{version}.tar.gz
# Source0-md5:	40da31270e51c714b899247622a98d32
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	bluez-sdp-devel >= 1.0
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a library to control Bluetooth devices.

%description -l pl
Ten pakiet zawiera bibliotekę do kontrolowania urządzeń Bluetooth.

%package devel
Summary:	Header files for libbtctl library
Summary(pl):	Pliki nagłówkowe biblioteki libbtctl
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	bluez-sdp-devel

%description devel
Header files for libbtctl library.

%description devel -l pl
Pliki nagłówkowe biblioteki libbtctl.

%package static
Summary:	Static libbtctl library
Summary(pl):	Statyczna biblioteka libbtctl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libbtctl library.

%description static -l pl
Statyczna biblioteka libbtctl.

%prep
%setup -q

%build
%configure \
	--enable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
