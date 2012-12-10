# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Summary:        Open Source XML framework for Java
Name:           dom4j
Version:        1.6.1
Release:        8
License:        BSD
URL:            http://www.dom4j.org/
Group:          Development/Java
Source0:        http://downloads.sourceforge.net/dom4j/dom4j-1.6.1.tar.gz
Source1:        dom4j_rundemo.sh
Patch0:         dom4j-1.6.1-build_xml.patch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  junit
BuildRequires:  jtidy
BuildRequires:  junitperf
BuildRequires:  isorelax
BuildRequires:  jaxen-bootstrap >= 0:1.1-0.b7
BuildRequires:  msv-msv
BuildRequires:  relaxngDatatype
BuildRequires:  bea-stax
BuildRequires:  bea-stax-api
BuildRequires:  ws-jaxme
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  jaxp = 1.2
BuildRequires:  xpp2
BuildRequires:  xpp3
BuildRequires:  msv-xsdlib
Requires:  xpp2
Requires:  xpp3
Requires:  xerces-j2
Requires:  msv-msv
Requires:  msv-xsdlib
Requires:  relaxngDatatype
Requires:  isorelax
Requires:  jaxen-bootstrap >= 0:1.1-0.b7
Requires:  jpackage-utils >= 0:1.6
Requires:  bea-stax
Requires:  bea-stax-api
Requires:  ws-jaxme
Requires:  xalan-j2
BuildArch:      noarch

%description
dom4j is an Open Source XML framework for Java. dom4j allows you to read,
write, navigate, create and modify XML documents. dom4j integrates with 
DOM and SAX and is seamlessly integrated with full XPath support. 

%package demo
Summary:        Samples for %{name}
Group:          Development/Java
Requires:       dom4j = 0:%{version}-%{release}

%description demo
Samples for %{name}.

%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Development/Java for %{name}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.


%prep
%setup -q 
# replace run.sh
cp -p %{SOURCE1} run.sh
# remove binary libs
find . -name "*.jar" -exec rm -f {} \;
# fix for deleted jars
mv build.xml build.xml.orig
sed -e '/unjar/d' -e 's|,cookbook/\*\*,|,|' build.xml.orig > build.xml

%patch0 -b .sav

%build
pushd lib
ln -sf $(build-classpath xpp2)
ln -sf $(build-classpath relaxngDatatype)
ln -sf $(build-classpath jaxme/jaxmeapi) 
ln -sf $(build-classpath msv-xsdlib) 
ln -sf $(build-classpath msv-msv) 
ln -sf $(build-classpath jaxen) 
ln -sf $(build-classpath bea-stax-api) 
pushd test
ln -sf $(build-classpath bea-stax-ri) 
ln -sf $(build-classpath junitperf) 
ln -sf $(build-classpath junit) 
popd
ln -sf $(build-classpath xpp3) 
pushd tools
ln -sf $(build-classpath jaxme/jaxmexs) 
ln -sf $(build-classpath xalan-j2) 
ln -sf $(build-classpath jaxme/jaxmejs) 
ln -sf $(build-classpath jtidy) 
ln -sf $(build-classpath isorelax) 
ln -sf $(build-classpath jaxme/jaxme2) 
ln -sf $(build-classpath xerces-j2) 
popd
popd

# FIXME: test needs to be fixed
ant all samples # test

%install
# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
pushd build/doc/javadoc
for f in `find -name \*.html -o -name \*.css`; do
  sed -i 's/\r//g' $f;
done
popd
cp -pr build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# manual
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
rm -rf docs/apidocs docs/clover
pushd docs
for f in `find -name \*.html -o -name \*.css -o -name \*.java`; do
  sed -i 's/\r//g' $f;
done
popd
cp -pr docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
tr -d \\r <LICENSE.txt >tmp.file; mv tmp.file LICENSE.txt
cp -p LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/classes/org/dom4j
cp -pr xml $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/src
cp -pr src/samples $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/src
cp -pr build/classes/org/dom4j/samples $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/classes/org/dom4j
install -m 755 run.sh $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%files
%dir %{_docdir}/%{name}-%{version}
%{_javadir}/%{name}.jar

%files javadoc
%{_javadocdir}/*

%files manual
%doc %{_docdir}/%{name}-%{version}

%files demo
%attr(0755,root,root) %{_datadir}/%{name}-%{version}/run.sh
%dir %{_datadir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}/src
%{_datadir}/%{name}-%{version}/xml
%{_datadir}/%{name}-%{version}/classes



%changelog
* Fri Jul 13 2012 Guilherme Moro <guilherme@mandriva.com> 1.6.1-8
+ Revision: 809256
- rebuild
- imported package dom4j

* Tue Apr 26 2011 Paulo Andrade <pcpa@mandriva.com.br> 0:1.6.1-2.2.7
+ Revision: 659461
- Rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.6.1-2.2.5mdv2009.1
+ Revision: 350834
- rebuild

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 0:1.6.1-2.2.4mdv2008.1
+ Revision: 136373
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.6.1-2.2.3mdv2008.0
+ Revision: 87332
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Fri Jul 06 2007 David Walluck <walluck@mandriva.org> 0:1.6.1-2.2.2mdv2008.0
+ Revision: 48920
- workaround dom4j bug #1618750

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0:1.6.1-2.2.1mdv2008.0
+ Revision: 47796
- Import dom4j

