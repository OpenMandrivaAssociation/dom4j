Name:		dom4j
Version:	2.2.0
Release:	1
Epoch:		0
Summary:	XML framework for Java
Group:		Development/Java
License:	BSD
URL:		https://dom4j.github.io/
Source0:	https://codeload.github.com/dom4j/dom4j/tar.gz/refs/tags/version/2.2.0#/dom4j-%{version}.tar.gz
# Navigator sources. The system jaxen jar omits this adapter.
Source1:	https://github.com/jaxen-xpath/jaxen/archive/refs/tags/v2.0.6.tar.gz#/jaxen-2.0.6.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(jaxen:jaxen)
BuildSystem:	maven
BuildOption(install):	--file-name dom4j --alias dom4j:dom4j --alias org.jvnet.hudson.dom4j:dom4j

Obsoletes:	%{name}-javadoc < %{version}-%{release}
Obsoletes:	%{name}-demo < %{version}-%{release}
Obsoletes:	%{name}-manual < %{version}-%{release}

%description
dom4j is a Java library for reading and writing XML.
2.2.0 requires Java 11. XPath uses the system jaxen jar. The dom4j
navigator classes ship in this jar because the jaxen package was built
without them. Schema datatype, JAXB, and XmlPull integrations are left
out: xsdlib, Jakarta XML Binding, and the pull parsers are not packaged.
Tests are skipped.

%prep
%autosetup -n dom4j-version-%{version}
rm -rf gradle src/test src/example
python - <<'PY'
import shutil
import tarfile
from pathlib import Path

src = Path("src/main/java")
for rel in (
    "org/dom4j/datatype",
    "org/dom4j/jaxb",
    "org/dom4j/xpp",
    "org/dom4j/io/XPPReader.java",
    "org/dom4j/io/XPP3Reader.java",
):
    path = src / rel
    if path.is_dir():
        shutil.rmtree(path)
    elif path.is_file():
        path.unlink()

members = (
    "jaxen-2.0.6/core/src/java/main/org/jaxen/dom4j/DocumentNavigator.java",
    "jaxen-2.0.6/core/src/java/main/org/jaxen/dom4j/Dom4jXPath.java",
)
with tarfile.open("%{SOURCE1}") as archive:
    for name in members:
        extracted = archive.extractfile(name)
        if extracted is None:
            raise SystemExit("missing " + name)
        dest = src / "org/jaxen/dom4j" / Path(name).name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(extracted.read())

java_files = list(src.rglob("*.java"))
if len(java_files) != 164:
    raise SystemExit("java files " + str(len(java_files)))
if list(Path(".").rglob("*.jar")):
    raise SystemExit("prebuilt jar remains")
for rel in (
    "org/dom4j/datatype",
    "org/dom4j/jaxb",
    "org/dom4j/xpp",
    "org/dom4j/io/XPPReader.java",
    "org/dom4j/io/XPP3Reader.java",
):
    if (src / rel).exists():
        raise SystemExit("still present " + rel)
navigator = src / "org/jaxen/dom4j/Dom4jXPath.java"
if "class Dom4jXPath" not in navigator.read_text(encoding="utf-8"):
    raise SystemExit("navigator was not extracted")

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.dom4j</groupId>
  <artifactId>dom4j</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>dom4j</name>
  <description>XML framework. XPath uses the system jaxen jar.</description>
  <url>https://dom4j.github.io/</url>
  <licenses>
    <license>
      <name>BSD</name>
      <url>https://github.com/dom4j/dom4j/blob/master/LICENSE</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>jaxen</groupId>
      <artifactId>jaxen</artifactId>
      <version>2.0.6</version>
    </dependency>
  </dependencies>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
  </properties>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <source>11</source>
          <target>11</target>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <archive>
            <manifestEntries>
              <Automatic-Module-Name>org.dom4j</Automatic-Module-Name>
            </manifestEntries>
          </archive>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<groupId>org.dom4j</groupId>",
    "<artifactId>jaxen</artifactId>",
    "<version>2.0.6</version>",
    "<version>%{version}</version>",
    "<source>11</source>",
    "<target>11</target>",
    "<Automatic-Module-Name>org.dom4j</Automatic-Module-Name>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
for needle in ("junit", "xsdlib", "jakarta.xml.bind", "xpp3", "pull-parser", "SNAPSHOT", "<release>"):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
cat > manifest-addition <<'EOF'
Automatic-Module-Name: org.dom4j
EOF
jar ufm target/dom4j-%{version}.jar manifest-addition
java --module-path target/dom4j-%{version}.jar --describe-module org.dom4j > module-describe.txt
# A versioned jar prints "name@version ... automatic", not "name automatic".
grep -q '^org.dom4j' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q 'contains org.jaxen.dom4j' module-describe.txt || { cat module-describe.txt; exit 1; }

%files -f .mfiles
%doc LICENSE README.md
