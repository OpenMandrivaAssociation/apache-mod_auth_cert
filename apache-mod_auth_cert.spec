#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_auth_cert
%define mod_conf B40_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Maps the Subject DN of a X509 client certificate to a username
Name:		apache-%{mod_name}
Version:	0.3
Release:	%mkrel 8
Group:		System/Servers
License:	GPL
URL:		http://sourceforge.net/projects/mod-auth-cert/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/mod-auth-cert/%{mod_name}-%{version}.tgz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_auth_cert is an authentication module for the Apache 1.3.x/2.x server. It
can be used to map the Subject DN of a X509 client certificate to a username.
The module can be combined with other authentication modules.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix -U {} \;

%build

%{_sbindir}/apxs -c %{mod_name}.c
        
%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

