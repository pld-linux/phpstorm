Summary:	Lightweight and Smart PHP IDE
Name:		phpstorm
Version:	3.0
Release:	1
License:	?
Group:		Development/Tools
Source0:	http://download.jetbrains.com/webide/PhpStorm-%{version}.tar.gz
# NoSource0-md5:	8075fca30a7b56fdf189631db82dfb1f
NoSource:	0
Source1:	%{name}.desktop
Patch0:		pld.patch
URL:		http://www.jetbrains.com/phpstorm/
BuildRequires:	unzip
Requires:	java-commons-codec >= 1.3
Requires:	java-commons-collections
# pld version is 2.1
#Requires:	java-commons-lang >= 2.4
Requires:	java-jgoodies-forms
Requires:	java-log4j
Requires:	jdk >= 1.6
Requires:	which
Suggests:	cvs
Suggests:	git-core
Suggests:	subversion
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# use /usr/lib, 64bit files are renamed,
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
%setup -qn PhpStorm-111.19
# keep only single arch files
%ifarch %{ix86}
rm bin/fsnotifier64
rm bin/libbreakgen64.so
rm bin/libyjpagent64.so
%endif
%ifarch %{x8664}
rm bin/fsnotifier
rm bin/libbreakgen.so
rm bin/libyjpagent.so
%endif
%patch0 -p1
chmod a+rx bin/*.so bin/fsnotifier*
mv bin/webide.png .

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -l build.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -p webide.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -a$l bin help lib license plugins $RPM_BUILD_ROOT%{_appdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
ln -s %{_appdir}/bin/phpstorm.sh $RPM_BUILD_ROOT%{_bindir}/phpstorm

# replace with system jars
ln -snf %{_javadir}/commons-codec-1.3.jar $RPM_BUILD_ROOT%{_appdir}/lib
ln -snf %{_javadir}/jgoodies-forms.jar $RPM_BUILD_ROOT%{_appdir}/lib/jgoodies-forms.jar
ln -snf %{_javadir}/log4j.jar $RPM_BUILD_ROOT%{_appdir}/lib/log4j.jar
# these break:
#ln -snf %{_javadir}/commons-collections.jar $RPM_BUILD_ROOT%{_appdir}/lib/commons-collections.jar
#ln -snf %{_javadir}/jdom.jar $RPM_BUILD_ROOT%{_appdir}/lib/jdom.jar
#ln -snf %{_javadir}/xercesImpl.jar $RPM_BUILD_ROOT%{_appdir}/lib/xerces.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_appdir}
%{_appdir}/help
%{_appdir}/lib
%{_appdir}/license
%{_appdir}/plugins
%dir %{_appdir}/bin
%{_appdir}/bin/phpstorm.vmoptions
%{_appdir}/bin/idea.properties
%{_appdir}/bin/log.xml
%attr(755,root,root) %{_appdir}/bin/phpstorm.sh
%attr(755,root,root) %{_appdir}/bin/fsnotifier*
%attr(755,root,root) %{_appdir}/bin/libbreakgen*.so
%attr(755,root,root) %{_appdir}/bin/libyjpagent*.so
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
