%include	/usr/lib/rpm/macros.java
Summary:	Lightweight and Smart PHP IDE
Name:		phpstorm
Version:	7.1.3
Release:	1
# TODO: figure out what's the licensing and redistribution
License:	?
Group:		Development/Tools
Source0:	http://download.jetbrains.com/webide/PhpStorm-%{version}.tar.gz
# NoSource0-md5:	5c68dce5fa53ce2ff42fa8a590561c40
NoSource:	0
Source1:	%{name}.desktop
Patch0:		pld.patch
URL:		http://www.jetbrains.com/phpstorm/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	jre >= 1.6
Requires:	which
Suggests:	cvs
Suggests:	git-core
Suggests:	subversion
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't strip fsnotifier, it's size is checked for "outdated binary"
# https://bugs.archlinux.org/task/34703
# http://git.jetbrains.org/?p=idea/community.git;a=blob;f=platform/platform-impl/src/com/intellij/openapi/vfs/impl/local/FileWatcher.java;h=004311b96a35df1ffc2c87baba78a8b2a8809f7d;hb=376b939fd6d6ec4c12191a5f90503d9d62c501da#l173
%define		_noautostrip	.*/fsnotifier.*

# use /usr/lib, 64bit files do not conflict with 32bit files (64 suffix)
# this allows to install both arch files and to use 32bit jdk on 64bit os
%define		_appdir		%{_prefix}/lib/%{name}

%description
PhpStorm is a lightweight and smart PHP IDE focused on developer
productivity that deeply understands your code, provides smart code
completion, quick navigation and on-the-fly error checking. It is
always ready to help you shape your code, run unit-tests or provide
visual debugging.

Note: PhpStorm includes all the functionality of WebStorm (HTML/CSS
Editor, JavaScript Editor) and adds full-fledged support for PHP.

%prep
%setup -qn PhpStorm-133.982

# keep only single arch files (don't want to pull 32bit deps by default),
# if you want to mix, install rpm from both arch
%ifarch %{ix86}
rm bin/fsnotifier64
rm bin/libyjpagent-linux64.so
rm bin/phpstorm64.vmoptions
rm -r lib/libpty/linux/x86_64
%endif
%ifarch %{x8664}
rm bin/fsnotifier
rm bin/libyjpagent-linux.so
rm bin/phpstorm.vmoptions
rm -r lib/libpty/linux/x86
%endif
rm -r lib/libpty/{macosx,win}
%patch0 -p1
chmod a+rx bin/*.so bin/fsnotifier*
mv bin/webide.png .

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -l build.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -a$l bin help lib license plugins $RPM_BUILD_ROOT%{_appdir}
ln -s %{_pixmapsdir}/%{name}.png $RPM_BUILD_ROOT%{_appdir}/bin
cp -p webide.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
ln -s %{_appdir}/bin/phpstorm.sh $RPM_BUILD_ROOT%{_bindir}/phpstorm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_appdir}
%{_appdir}/help
%{_appdir}/license
%{_appdir}/plugins
%dir %{_appdir}/bin
%{_appdir}/bin/%{name}*.vmoptions
%{_appdir}/bin/idea.properties
%{_appdir}/bin/log.xml
%{_appdir}/bin/%{name}.png
%attr(755,root,root) %{_appdir}/bin/%{name}.sh
%attr(755,root,root) %{_appdir}/bin/inspect.sh
%attr(755,root,root) %{_appdir}/bin/fsnotifier*
%attr(755,root,root) %{_appdir}/bin/libyjpagent-linux*.so
%dir %{_appdir}/lib
%{_appdir}/lib/*.jar
%dir %{_appdir}/lib/ext
%{_appdir}/lib/ext/*.jar
%dir %{_appdir}/lib/libpty
%dir %{_appdir}/lib/libpty/linux
%dir %{_appdir}/lib/libpty/linux/x86*
%attr(755,root,root) %{_appdir}/lib/libpty/linux/x86*/libpty.so
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
