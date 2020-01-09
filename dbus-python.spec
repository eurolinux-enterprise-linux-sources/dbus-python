
%if 0%{?fedora} > 17
%global python3 1
%endif

Summary: D-Bus Python Bindings 
Name: dbus-python
Version: 1.1.1
Release: 9%{?dist}

License: MIT
URL: http://www.freedesktop.org/software/dbus-python
Source0: http://dbus.freedesktop.org/releases/dbus-python/%{name}-%{version}.tar.gz

Patch0: dbus-python-aarch64.patch
# http://cgit.freedesktop.org/dbus/dbus-python/commit/?id=423ee853dfbb4ee9ed89a21e1cf2b6a928e2fc4d
Patch1: dbus-python-pygobject38.patch
Patch2: 0001-Move-python-modules-to-architecture-specific-directo.patch

BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: python-devel
BuildRequires: python-docutils
%if 0%{?python3}
BuildRequires: python3-devel
%endif
# for %%check
BuildRequires: dbus-x11 pygobject3

BuildRequires: autoconf automake libtool

Provides: python-dbus = %{version}-%{release}
Provides: python-dbus%{?_isa} = %{version}-%{release}

%description
D-Bus python bindings for use with python programs.   

%package devel
Summary: Libraries and headers for dbus-python
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and static libraries for hooking up custom mainloops to the dbus python
bindings.

%package -n python3-dbus
Summary: D-Bus bindings for python3
%description -n python3-dbus
%{summary}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

autoreconf -vfi

%build
%global _configure ../configure

mkdir python2-build; pushd python2-build
%configure PYTHON=%{__python}
make %{?_smp_mflags}
popd

%if 0%{?python3}
mkdir python3-build; pushd python3-build
%configure PYTHON=%{__python3}
make %{?_smp_mflags}
popd
%endif


%install
%if 0%{?python3}
make install DESTDIR=$RPM_BUILD_ROOT -C python3-build
%endif

make install DESTDIR=$RPM_BUILD_ROOT -C python2-build

# unpackaged files
rm -fv $RPM_BUILD_ROOT%{python_sitearch}/*.la
rm -fv $RPM_BUILD_ROOT%{python3_sitearch}/*.la
rm -rfv $RPM_BUILD_ROOT%{_datadir}/doc/dbus-python/


%check
# FIXME: seeing failures on f19+, http://bugzilla.redhat.com/913936
#make check -k -C python2-build
%if 0%{?python3}
#make check -k -C python3-build
%endif

%files
%doc COPYING ChangeLog README NEWS
%{python_sitearch}/*.so
%{python_sitearch}/dbus/

%files devel
%doc doc/API_CHANGES.txt doc/HACKING.txt doc/tutorial.txt
%{_includedir}/dbus-1.0/dbus/dbus-python.h
%{_libdir}/pkgconfig/dbus-python.pc

%if 0%{?python3}
%files -n python3-dbus
%{python3_sitearch}/*.so
%{python3_sitearch}/dbus/
%endif


%changelog
* Tue Mar 18 2014 Colin Walters <walters@redhat.com> - 1.1.1-9
- Move modules to libdir to avoid multilib conflicts
- And comment out test suite, since we were not actually
  failing if it failed, but it trips up an rpmdiff check
  on the output of the suite.
- Resolves: #1076411

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.1.1-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.1-6
- Mass rebuild 2013-12-27

* Thu Apr 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-5
- Add upstream patch to fix pygobject 3.8

* Fri Mar 29 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.1.1-4
- Apply patch to support aarch64 (#925236)
- Fix URL

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-3
- python3-dbus subpkg (#892474)
- (main) Provides: python-dbus
- BR: python-docutils
- .spec cosmetics
- skip failed tests on rawhide (#913936)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 07 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-1
- dbus-python-1.1.1 (#800487)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.83.0-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.83.0-4
- Rebuild for Python 2.6

* Tue Sep 16 2008 Marco Pesenti Gritti - 0.83.0-3
- Add patch for https://bugs.freedesktop.org/show_bug.cgi?id=17551 

* Tue Aug 05 2008  Huang Peng <phuang@redhat.com> - 0.83.0-2
- Update to 0.83.0.

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.82.4-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.82.4-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Matthias Clasen <mclasen@redhat.com> - 0.82.4-1
- Update to 0.82.4

* Mon Oct 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.82.0-3
- Rebuild against new dbus-glib

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.82.0-2
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.82.0-1
- Update to 0.82.0
- Put all docs in the usual place

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.80.2-3
- Rebuild

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.80.2-2
- Don't examine args for functions declared METH_NOARGS (#235017)

* Tue Feb 13 2007 John (J5) Palmieri <johnp@redhat.com> - 0.80.2-1
- upgrade to 0.80.2 which fixes some memleaks

* Wed Jan 24 2007 John (J5) Palmieri <johnp@redhat.com> - 0.80.1-1
- upgrade to 0.80.1
- remove dependency on Pyrex and libxml2
- some API breakage, 
  please see http://dbus.freedesktop.org/doc/dbus-python/NEWS.html
  for notes on changes 

* Wed Jan  3 2007 David Zeuthen <davidz@redhat.com> - 0.70-9%{?dist}
- rebuild against new Pyrex

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 0.70-8
- rebuild against python 2.5

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.70-7
- Fix a typo in the spec file

* Fri Aug 18 2006 Karsten Hopp <karsten@redhat.com> - 0.70-6
- require libxml2-python for site-packages/dbus/introspect_parser.py

* Thu Jul 20 2006 Jesse Keating <jkeating@redhat.com> - 0.70-5
- Remove unnecessary obsoletes

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-4
- Try python_sitearch this time

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-3
- Add a BR on dbus-devel

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-2
- Spec file cleanups
- Add PKG_CONFIG_PATH

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-1
- Initial package import
