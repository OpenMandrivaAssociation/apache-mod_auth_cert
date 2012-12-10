#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_auth_cert
%define mod_conf B40_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Maps the Subject DN of a X509 client certificate to a username
Name:		apache-%{mod_name}
Version:	0.3
Release:	9
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

%description
mod_auth_cert is an authentication module for the Apache 1.3.x/2.x server. It
can be used to map the Subject DN of a X509 client certificate to a username.
The module can be combined with other authentication modules.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix {} \;

%build

%{_bindir}/apxs -c %{mod_name}.c
        
%install

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

%files
%doc LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.3-9mdv2012.0
+ Revision: 772554
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3-8
+ Revision: 678256
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3-7mdv2011.0
+ Revision: 587914
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3-6mdv2010.1
+ Revision: 516040
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.3-5mdv2010.0
+ Revision: 406523
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.3-4mdv2009.1
+ Revision: 325538
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-3mdv2009.0
+ Revision: 234628
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-2mdv2009.0
+ Revision: 215526
- fix rebuild

* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-1mdv2009.0
+ Revision: 208685
- import apache-mod_auth_cert


* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-1mdv2009.0
- initial Mandriva package
