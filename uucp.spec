Summary:	The uucp utility for copying files between systems
Name:		uucp
Version:	1.07
Release:	25
License:	GPLv2+
Group:		Networking/File transfer
URL:		http://www.airs.com/ian/uucp.html
Source0:	ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.bz2
Source1:	uucp.log
Source2:	uucp-tmpfiles.conf
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

mkdir -p %{buildroot}/var/spool/uucp
mkdir -p %{buildroot}/var/spool/uucppublic
mkdir -p %{buildroot}%{_sysconfdir}/uucp/oldconfig

rm -rf %{buildroot}/var/log/uucp
mkdir -p %{buildroot}/var/log/uucp

mkdir -p %{buildroot}/var/lock/uucp

mkdir -p %{buildroot}%{_libdir}/uucp
ln -sf ../../sbin/uucico %{buildroot}%{_libdir}/uucp

install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/logrotate.d/uucp
install -m644 %{SOURCE2} -D %{buildroot}%{_tmpfilesdir}/uucp.conf

# Create ghost files
touch %{buildroot}/var/log/uucp/{Log,Stats,Debug}

# the following is kind of gross, but it is effective
for i in dial passwd port dialcode sys call ; do
cat > %{buildroot}/etc/uucp/$i <<EOF 
# This is an example of a $i file. This file have the syntax compatible
# with Taylor UUCP (not HDB nor anything else). Please check uucp
# documentation if you are not sure how Taylor config files are supposed to 
# look like. Edit it as appropriate for your system.

# Everything after a '#' character is a comment.
EOF
done

# fix attribs so strip can touch it
chmod 755 %{buildroot}%{_sbindir}/* %{buildroot}%{_bindir}/*

%post
# These permissions have to be synced with below %%files
%create_ghostfile /var/log/uucp/Log uucp uucp 644
%create_ghostfile /var/log/uucp/Stats uucp uucp 644
%create_ghostfile /var/log/uucp/Debug uucp uucp 640

%files
%defattr(-,root,root,755)
%doc README ChangeLog NEWS
%doc sample contrib
#%%attr(-,uucp,uucp) %dir /var/spool/uucp
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
%attr(775,uucp,uucp) %dir /var/lock/uucp
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
%{_tmpfilesdir}/uucp.conf
