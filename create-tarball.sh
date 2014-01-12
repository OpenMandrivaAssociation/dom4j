#!/bin/sh
set -C -e

name=dom4j
version=$(awk '/Version:/{print$2}' ${name}.spec)
url=http://downloads.sourceforge.net/${name}/${name}-${version}.tar.gz

set -x
wget ${url} -O ${name}-${version}.tar.gz
tar xf ${name}-${version}.tar.gz
find ${name}-${version} -name \*.jar -delete
rm -Rf ${name}-${version}/xdocs
# remove file with unclear licensing
rm -Rf ${name}-${version}/src/java/org/dom4j/tree/ConcurrentReaderHashMap.java
tar caf ${name}-${version}-clean.tar.xz ${name}-${version}
