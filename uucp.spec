Summary:	The uucp utility for copying files between systems
Name:		uucp
Version:	1.07
Release:	14
License:	GPL
Group:		Networking/File transfer
URL:		http://www.airs.com/ian/uucp.html
Source0:	ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.bz2
Source1:	uucp.log
Patch0:		uucp-1.07-misc.patch
Patch7:		uucp-1.07-64bit-fixes.patch
Patch8:		uucp-1.07-config.patch
Patch9:		uucp-1.07-sigfpe.patch
#(peroyvind) depends on lockdev?
Patch10:	uucp-1.07-baudboy.patch
Patch11:	uucp-1.06.1-pipe.patch
Patch12:	uucp-1.07-format_not_a_string_literal_and_no_format_arguments.diff
Patch13:	uucp-1.07-nostrip.diff
BuildRequires:	texinfo
Requires(post):	rpm-helper

%description
The uucp command copies files between systems.  Uucp is primarily used
by remote machines downloading and uploading email and news files to
local machines.

Install the uucp package if you need to use uucp to transfer files
between machines.

%prep
%setup -q
%patch0 -p1 -b .misc
%patch7 -p1 -b .64bit-fixes
%patch8 -p1 -b .config
%patch9 -p1 -b .sigfpe
#%patch10 -p1 -b .baudboy
%patch11 -p1 -b .pipe
%patch12 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch13 -p1 -b .nostrip

%build
STRIP="/bin/echo" \
LDFLAGS="%{ldflags}" \
%configure --with-newconfigdir=%{_sysconfdir}/%{name} --with-oldconfigdir=%{_sysconfdir}/%{name}
%make 

%install
%{makeinstall} STRIP="/bin/echo"

mkdir -p $RPM_BUILD_ROOT/var/spool/uucp
mkdir -p $RPM_BUILD_ROOT/var/spool/uucppublic
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/uucp/oldconfig

rm -rf $RPM_BUILD_ROOT/var/log/uucp
mkdir -p $RPM_BUILD_ROOT/var/log/uucp

mkdir -p $RPM_BUILD_ROOT/var/lock/uucp

mkdir -p $RPM_BUILD_ROOT%{_libdir}/uucp
ln -sf ../../sbin/uucico $RPM_BUILD_ROOT%{_libdir}/uucp

install -m644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/uucp

# Create ghost files
touch $RPM_BUILD_ROOT/var/log/uucp/{Log,Stats,Debug}

# the following is kind of gross, but it is effective
for i in dial passwd port dialcode sys call ; do
cat > $RPM_BUILD_ROOT/etc/uucp/$i <<EOF 
# This is an example of a $i file. This file have the syntax compatible
# with Taylor UUCP (not HDB nor anything else). Please check uucp
# documentation if you are not sure how Taylor config files are supposed to 
# look like. Edit it as appropriate for your system.

# Everything after a '#' character is a comment.
EOF
done

# fix attribs so strip can touch it
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/* $RPM_BUILD_ROOT%{_bindir}/*

%post
# These permissions have to be synced with below %%files
%create_ghostfile /var/log/uucp/Log uucp uucp 644
%create_ghostfile /var/log/uucp/Stats uucp uucp 644
%create_ghostfile /var/log/uucp/Debug uucp uucp 640

%files
%defattr(-,root,root,755)
%doc README ChangeLog NEWS
%doc sample contrib
%attr(-,uucp,uucp) %dir /var/spool/uucp
%attr(-,uucp,uucp) %dir /var/spool/uucppublic
%attr(755,uucp,uucp) %dir %{_sysconfdir}/uucp
%{_infodir}/uucp.info*
%{_sbindir}/uuchk
%{_sbindir}/uuconv
%{_sbindir}/uusched
%attr(6555,uucp,uucp) %{_sbindir}/uucico
%attr(6555,uucp,uucp) %{_sbindir}/uuxqt
%attr(-,uucp,uucp) %{_bindir}/*
%{_mandir}/*/*
%{_libdir}/uucp/uucico
%attr(-,uucp,uucp) %dir /var/lock/uucp
%attr(-,uucp,uucp) %dir /var/log/uucp
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/uucp
%attr(644,uucp,uucp) %ghost /var/log/uucp/Log
%attr(644,uucp,uucp) %ghost /var/log/uucp/Stats
%attr(600,uucp,uucp) %ghost /var/log/uucp/Debug
%config(noreplace) %{_sysconfdir}/uucp/dial
%config(noreplace) %{_sysconfdir}/uucp/dialcode
%config(noreplace) %{_sysconfdir}/uucp/port
%config(noreplace) %{_sysconfdir}/uucp/passwd
%config(noreplace) %{_sysconfdir}/uucp/sys
%config(noreplace) %{_sysconfdir}/uucp/call



%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.07-11mdv2011.0
+ Revision: 670757
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.07-10mdv2011.0
+ Revision: 608119
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.07-9mdv2010.1
+ Revision: 520290
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.07-8mdv2010.0
+ Revision: 427486
- rebuild

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1.07-7mdv2009.1
+ Revision: 317914
- don't strip
- fix build with -Werror=format-security (P12)

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.07-6mdv2009.0
+ Revision: 225914
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.07-5mdv2008.1
+ Revision: 178848
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Thu May 25 2006 Pascal Terjan <pterjan@mandriva.org> 1.07-4mdv2007.0
- create /var/lock/uucp (#22514)
- don't touch the log files before using %%create_ghostfile, the macro would 
  do nothing and rights would be wrong (#22512)
- drop prereq
- mkrel

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.07-3mdk
- Rebuild

* Mon Mar 14 2005 Bruno Cornec <bcornec@mandrake.org> 1.07-2mdk
- conf files used are in /etc/uucp (not /usr/conf/uucp)
- fixes for rpmlint in the spec file

* Thu Jul 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.07-1mdk
- 1.07
- cleanups
- drop old patches P1-P6 (fixed upstream)
- regenerate P0 & P7
- sync with fedora patches

* Thu Sep 04 2003 Florin <florin@mandrakesoft.com> 1.06.1-23mdk
- change the /etc dir permissions to 775

