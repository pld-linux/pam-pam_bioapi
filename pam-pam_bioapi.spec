# TODO:
# - wrong (and unnecessary) pam modules paths in pam.d files
# - wrong (not lib64-aware) libbirdb_sqlite3 path in birdb.conf
#   (maybe this module should be moved to /usr/%{_lib} as it uses libsqlite3 from /usr?)
%define 	modulename pam_bioapi
Summary:	PAM BioAPI module
Summary(pl.UTF-8):	Moduł PAM BioAPI
Name:		pam-%{modulename}
Version:	0.4.0
Release:	0.2
Epoch:		0
License:	GPL v2+
Group:		Applications/System
Source0:	http://pam-bioapi.googlecode.com/files/%{modulename}-%{version}.tar.gz
# Source0-md5:	0896c6549be3720d358b1e8507c36a4d
URL:		http://www.qrivy.net/~michael/blua/
BuildRequires:	bioapi-devel
BuildRequires:	pam-devel
BuildRequires:  sqlite3-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Provides a PAM-compliant interface to use in biometrically
authenticating local users.

%description -l pl.UTF-8
Ten pakiet udostępnia zgody z PAM-em interfejs do biometrycznego
uwierzytelniania użytkowników lokalnych.

%prep
%setup -q -n %{modulename}-%{version}

%build
CPPFLAGS="-I%{_includedir}/bioapi"
# 1. We need to set prefix to empty string to have proper config files generated.
# 2. libdir is set to /lib to allow pam to find modules in /lib/security.
#    However, this package requires sqlite3, which is located under /usr.
%configure \
	--prefix='' \
	--libdir=/%{_lib}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/bioapi/pam

rm $RPM_BUILD_ROOT/%{_lib}/*.la $RPM_BUILD_ROOT/%{_lib}/security/*.la

%find_lang tfmessbsp

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f tfmessbsp.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/birdbtest
%attr(755,root,root) %{_bindir}/test_enroll-pam_bioapi
%attr(755,root,root) %{_bindir}/test_verify-pam_bioapi
# suid?
%attr(755,root,root) %{_sbindir}/bioapi_chbird
# -avoid-version is missing for this module
%attr(755,root,root) /%{_lib}/security/pam_bioapi.so*
%attr(755,root,root) /%{_lib}/libbirdb.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libbirdb.so.0
# -avoid-version is missing for this module
%attr(755,root,root) /%{_lib}/libbirdb_sqlite3.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libbirdb_sqlite3.so.0
%attr(755,root,root) /%{_lib}/libbirdb_sqlite3.so
%dir %{_sysconfdir}/bioapi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bioapi/birdb.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/bioapi_chbird
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/test-pam_bioapi
%{_mandir}/man8/pam_bioapi.8*
