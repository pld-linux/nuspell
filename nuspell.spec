# TODO: catch2 >= 2.3.0 for tests, https://github.com/catchorg/Catch2.git
#
# Conditional build:
%bcond_without	man	# build without man pages

Summary:	Nuspell spell checking library
Summary(pl.UTF-8):	Biblioteka sprawdzania pisowni Nuspell
Name:		nuspell
Version:	4.2.0
Release:	2
License:	LGPL v3+
Group:		Libraries
#Source0Download: https://github.com/nuspell/nuspell/releases
Source0:	https://github.com/nuspell/nuspell/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	16441229868de708939765e52f75a2b1
URL:		https://nuspell.github.io/
BuildRequires:	cmake >= 3.8
BuildRequires:	libicu-devel
# -std=c++17
BuildRequires:	libstdc++-devel >= 6:7
%{?with_man:BuildRequires:	pandoc}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nuspell is a spell checker library and command-line program designed
for languages with rich morphology and complex word compounding.
Nuspell is a pure C++ re-implementation of Hunspell.

Main features of Nuspell spell checker:
- Full unicode support backed by ICU
- Backward compatibility with Hunspell dictionary file format
- Twofold affix stripping (for agglutinative languages, like Azeri,
  Basque, Estonian, Finnish, Hungarian, Turkish, etc.)
- Support complex compounds (for example, Hungarian and German)
- Support language specific features (for example, special casing of
  Azeri and Turkish dotted i, or German sharp s)
- Handle conditional affixes, circumfixes, fogemorphemes, forbidden
  words, pseudoroots and homonyms.
- Free software. Licensed under GNU LGPL v3.

%description -l pl.UTF-8
Nuspell to biblioteka i narzędzie linii poleceń do sprawdzania
pisowni, zaprojektowane dla języków o bogatej morfologii i złożonym
łączeniu słów. Nuspell jest reimplementacją Hunspella w czystym C++.

Główne cechy Nuspella:
- pełna obsługa Unicode oparta o ICU
- wsteczna zgodność z formatem plików słówników Hunspella
- dwukrotne usuwanie formantów (dla języków aglutynacyjnych, jak
  azerski, baskijski, estoński, fiński, węgierski, turecki...)
- obsługa złożonego łączenia (języki np. węgierski, niemiecki)
- obsługa cech specyficznych dla języków (np. specjalne przypadki
  azerskiego i tureckiego "i" z kropkami czy niemieckiego ß)
- obsługa formantów warunkowych, okołorostków, fogemorfemów, słów
  zakazanych, pseudordzeni i homonimów
- oprogramowanie wolnodostępne, na licencji GNU LGPL v3

%package libs
Summary:	Nuspell spell checking library
Summary(pl.UTF-8):	Biblioteka sprawdzania pisowni Nuspell
Group:		Libraries

%description libs
Nuspell spell checking library.

%description libs -l pl.UTF-8
Biblioteka sprawdzania pisowni Nuspell.

%package devel
Summary:	Header files for Nuspell library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Nuspell
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libicu-devel
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for Nuspell library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Nuspell.

%prep
%setup -q

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/README.md

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md README.md docs/Third-party_licenses
%attr(755,root,root) %{_bindir}/nuspell
%{?with_man:%{_mandir}/man1/nuspell.1*}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnuspell.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnuspell.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnuspell.so
%{_includedir}/nuspell
%{_pkgconfigdir}/nuspell.pc
%{_libdir}/cmake/nuspell
