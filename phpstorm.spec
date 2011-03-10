Summary:	Lightweight and Smart PHP IDE
Name:		phpstorm
Version:	2.0
Release:	0.2
License:	?
Group:		Development/Tools
Source0:	http://download.jetbrains.com/webide/PhpStorm-%{version}.tar.gz
# NoSource0-md5:	a772dcf0c01231e814817309faf327a3
NoSource:	0
URL:		http://www.jetbrains.com/phpstorm/
BuildRequires:	unzip
Requires:	jdk >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_libdir}/%{name}

%description
PhpStorm is a lightweight and smart PHP IDE focused on developer
productivity that deeply understands your code, provides smart code
completion, quick navigation and on-the-fly error checking. It is
always ready to help you shape your code, run unit-tests or provide
visual debugging.

Note: PhpStorm includes all the functionality of WebStorm (HTML/CSS
Editor, JavaScript Editor) and adds full-fledged support for PHP.

%prep
%setup -qn PhpStorm-103.99
%ifarch %{ix86}
rm bin/fsnotifier64
rm bin/libbreakgen64.so
rm bin/libyjpagent64.so
%endif
%ifarch %{x8664}
mv -f bin/fsnotifier{64,}
mv -f bin/libbreakgen{64,}.so
mv -f bin/libyjpagent{64,}.so
%endif
chmod a+rx bin/*.so bin/fsnotifier
mv bin/webide.png .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -a bin help lib license plugins $RPM_BUILD_ROOT%{_appdir}
cp -p webide.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
ln -s %{_appdir}/bin/PhpStorm.sh $RPM_BUILD_ROOT%{_bindir}/phpstorm

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
%{_appdir}/bin/PhpStorm.vmoptions
%{_appdir}/bin/idea.properties
%{_appdir}/bin/log.xml
%attr(755,root,root) %{_appdir}/bin/PhpStorm.sh
%attr(755,root,root) %{_appdir}/bin/fsnotifier
%attr(755,root,root) %{_appdir}/bin/libbreakgen.so
%attr(755,root,root) %{_appdir}/bin/libyjpagent.so
%{_pixmapsdir}/%{name}.png
