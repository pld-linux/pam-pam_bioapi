%define 	modulename pam_bioapi
Summary:	PAM BioAPI module
Summary(pl.UTF-8):	Moduł PAM BioAPI
Name:		pam-%{modulename}
Version:	0.4.0
Release:	0.2
Epoch:		0
License:	GPL v2
Group:		Applications/System
Source0:	http://pam-bioapi.googlecode.com/files/%{modulename}-%{version}.tar.gz
# Source0-md5:	0896c6549be3720d358b1e8507c36a4d
URL:		http://www.qrivy.net/~michael/blua/
BuildRequires:	bioapi-devel
BuildRequires:	pam-devel
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
%configure \
	--libdir=/%{_lib}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/bioapi/pam

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /%{_lib}/security/pam*.so*
%attr(755,root,root) /%{_lib}/libbirdb*.so*
%dir %{_sysconfdir}/bioapi
%{_sysconfdir}/bioapi/*
%{_sysconfdir}/pam.d/*
%{_mandir}/man8/*
