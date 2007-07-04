%define gcj_support 1

Name:           dom4j
Version:        1.6.1
Release:        %mkrel 2.2.1
Epoch:          0
Summary:        Open Source XML framework for Java
License:        BSD
URL:            http://www.dom4j.org/
Group:          Development/Java
Source0:        http://downloads.sourceforge.net/dom4j/dom4j-1.6.1.tar.gz
Source1:        dom4j_rundemo.sh
Patch0:         dom4j-1.6.1-build_xml.patch
Patch1:         dom4j-gjdoc.patch
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
# package needs this specific version of jaxp
# newer jaxp versions will not work
BuildRequires:  jaxp = 1.2
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
Requires:  jaxp = 1.2
# package needs this specific version of jaxp.
# newer jaxp versions will not work
Requires:  jaxp = 1.2
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

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
Documentation for %{name}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{name}-%{version}
# replace run.sh
cp -p %{SOURCE1} run.sh
# remove binary libs
find . -name "*.jar" -exec rm -f {} \;
#for j in $(find . -name "*.jar"); do 
#       mv $j $j.no
#done
# won't succeed in headless environment
rm src/test/org/dom4j/bean/BeansTest.java
# fix for deleted jars
mv build.xml build.xml.orig
sed -e '/unjar/d' -e 's|,cookbook/\*\*,|,|' build.xml.orig > build.xml

%patch0 -b .sav
%patch1 -b .sav1

%build
pushd lib
ln -sf $(build-classpath xpp2)
ln -sf $(build-classpath relaxngDatatype)
pushd endorsed
ln -sf $(build-classpath xml-commons-jaxp-1.2-apis) 
popd
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
%{ant} all samples # test

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
pushd build/doc/javadoc
for f in `find -name \*.html -o -name \*.css`; do
  sed -i 's/\r//g' $f;
done
popd
cp -pr build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

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

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/*

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_datadir}/%{name}-%{version}/run.sh
%{_datadir}/%{name}-%{version}
