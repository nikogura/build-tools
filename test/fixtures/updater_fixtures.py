def semver():
    return '1.2.3'

def setup():
    return """from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='blah-blah-blah',
    version='1.0.0',
    url='https://github.com/nikogura/build-tools',
    author='Nik Ogura',
    author_email='nik.ogura@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status ::4 - Beta',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='build',
    packages=['some-package'],
    package_dir={'foo': './'},
    install_requires=['requests'],
    extras_require={},
    package_data={},
    entry_points={}

)
"""

def setup_incremented():
    return """from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='blah-blah-blah',
    version='1.0.1',
    url='https://github.com/nikogura/build-tools',
    author='Nik Ogura',
    author_email='nik.ogura@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status ::4 - Beta',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='build',
    packages=['some-package'],
    package_dir={'foo': './'},
    install_requires=['requests'],
    extras_require={},
    package_data={},
    entry_points={}

)
"""

def metadata():
    return """name              'some-cookbook'
maintainer        'Some Org'
maintainer_email  'cookbooks@org.com'
license           'all_rights'
description       'Installs/Configures orderup'
long_description  'Installs/Configures orderup'
version           '2.0.2'
source_url        'https://github.com/nikogura/build-tools' if respond_to?(:source_url)
issues_url        'https://github.com/nikogura/build-tools/issues' if respond_to?(:issues_url)

# Platforms supported by this cookbook
%w(redhat centos oracle).each do |os|
  supports os
end

# Cookbook dependancies
depends 'chef-vault', '~> 1.3.3'
"""

def metadata_incremented():
    return """name              'some-cookbook'
maintainer        'Some Org'
maintainer_email  'cookbooks@org.com'
license           'all_rights'
description       'Installs/Configures orderup'
long_description  'Installs/Configures orderup'
version           '2.0.3'
source_url        'https://github.com/nikogura/build-tools' if respond_to?(:source_url)
issues_url        'https://github.com/nikogura/build-tools/issues' if respond_to?(:issues_url)

# Platforms supported by this cookbook
%w(redhat centos oracle).each do |os|
  supports os
end

# Cookbook dependancies
depends 'chef-vault', '~> 1.3.3'
"""

def pom():
    return """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
<modelVersion>4.0.0</modelVersion>

<groupId>com.nikogura</groupId>
<artifactId>javabrew</artifactId>
<version>0.1.0</version>

<parent>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-parent</artifactId>
<version>1.4.0</version>
</parent>
</project>
"""

def pom_incremented():
    return """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
<modelVersion>4.0.0</modelVersion>

<groupId>com.nikogura</groupId>
<artifactId>javabrew</artifactId>
<version>0.1.1</version>

<parent>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-parent</artifactId>
<version>1.4.0</version>
</parent>
</project>
"""

