# Copyright (c) 2000-2005, JPackage Project
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

%define gcj_support     1
%define section         free

# -----------------------------------------------------------------------------

Name:           dom2-core-tests
Version:        0.0.1
Release:        %mkrel 0.20040405.1.5
Epoch:          0
Summary:        DOM Conformance Test Suite
Group:          Development/Java
License:        W3C Software License
URL:            http://www.w3.org/DOM/Test/
Source0:        http://www.w3.org/2004/04/dom2-core-tests-20040405.jar
Patch0:         dom2-core-tests-build_xml.patch
Patch1:         dom2-core-tests-no-classpath-in-manifest.patch
#Vendor:         JPackage Project
#Distribution:   JPackage
BuildRequires:  ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel >= 0:1.4.2
%endif
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  junit

%description
The DOM Test Suites (DOM TS) will consist of a number of tests 
for each level of the DOM specification. The tests will be 
represented in an XML grammar which ensures that tests can easily 
be ported from the description format to a number of specific 
language bindings. This grammar will be specified in XML Schema 
and DTD form. The grammar will be automatically generated from the 
DOM specifications themselves, to ensure stability and correctness.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
rm -r junit
find . -name '*.jar' -o -name '*.class' -exec rm {} \;

%patch0 -b .orig
%patch1 -p1

%build
export CLASSPATH=$(build-classpath junit)
export OPT_JAR_LIST=
%{ant} dist

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

vjar=$(echo %{name}.jar | sed s+.jar+-%{version}.jar+g)
install -m 644 %{name}-%{version}/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/$vjar
pushd $RPM_BUILD_ROOT%{_javadir}
   ln -fs $vjar %{name}.jar
popd

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr %{name}-%{version}/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


