# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: libarchive
Epoch: 100
Version: 3.6.0
Release: 1%{?dist}
Summary: A library for handling streaming archive formats
License: BSD-3-Clause
URL: https://github.com/libarchive/libarchive/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: bzip2-devel
BuildRequires: e2fsprogs-devel
BuildRequires: gcc
BuildRequires: libacl-devel
BuildRequires: libattr-devel
BuildRequires: libtool
BuildRequires: libxml2-devel
BuildRequires: libzstd-devel
BuildRequires: lz4-devel
BuildRequires: lzo-devel
BuildRequires: make
BuildRequires: nettle-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: sharutils
BuildRequires: xz-devel
BuildRequires: zlib-devel

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
autoreconf -i
%configure
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%check

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n bsdtar
Summary: Utility to read several different streaming archive formats
Group: Productivity/Archiving/Compression
Requires: libarchive13 >= %{epoch}:%{version}-%{release}

%description -n bsdtar
This package contains the bsdtar cmdline utility.

%package -n libarchive13
Summary: Library to work with several different streaming archive formats
Group: System/Libraries

%description -n libarchive13
Libarchive is a programming library that can create and read several
different streaming archive formats, including most popular tar
variants and several cpio formats. It can also write shar archives and
read ISO-9660 CDROM images. The bsdtar program is an implementation of
tar(1) that is built on top of libarchive. It started as a test
harness, but has grown and is now the standard system tar for FreeBSD 5
and 6.

The libarchive library offers a number of features that make it both
very flexible and very powerful.

- Automatic format detection: libarchive can automatically determine
   both the compression and the archive format, regardless of the
   data source. Most tar implementations do not automatically detect
   the compression format, few implementation that can correctly do
   this when reading from stdin or a socket. (The tar program
   included with Gunnar Ritter's heirloom collection also does full
   automatic format detection.)

- Writes POSIX formats: libarchive writes POSIX-standard formats,
   including "ustar," "pax interchange format," and the POSIX "cpio"
   format.

- Supports pax interchange format: Pax interchange format (which,
   despite the name, is really an extended tar format) eliminates
   almost all limitations of historic tar formats and provides a
   standard method for incorporating vendor-specific extensions.
   libarchive exploits this extension mechanism to support ACLs and
   file flags, for example. (Joerg Schilling's star archiver is
   another open-source tar program that supports pax interchange
   format.)

- Reads popular formats: libarchive can read GNU tar, ustar, pax
   interchange format, cpio, and older tar variants. The internal
   architecture is easily extensible. The only requirement for
   support is that it be possible to read the format without seeking
   in the file. (For example, a format that includes a compressed
   size field before the data cannot be correctly written without
   seeking.)

- High-Level API: the libarchive API makes it fairly simple to build
   an archive from a list of filenames or to extract the entries
   from an archive. However, the API also provides extreme
   flexibility with regards to data sources. For example, there are
   generic hooks that allow you to write an archive to a socket or
   read data from an archive entry into a memory buffer.

- Extensible. The internal design uses generic interfaces for
compression, archive format detection and decoding, and archive data
I/O. It should be very easy to add new formats, new compression
methods, or new ways of reading/writing archives.

%package -n libarchive-devel
Summary: Development files for libarchive
Group: Development/Libraries/C and C++
Requires: libarchive13 = %{epoch}:%{version}-%{release}
Requires: glibc-devel

%description -n libarchive-devel
Libarchive is a programming library that can create and read several
different streaming archive formats, including most popular tar
variants and several cpio formats. It can also write shar archives and
read ISO-9660 CDROM images. The bsdtar program is an implementation of
tar(1) that is built on top of libarchive. It started as a test
harness, but has grown and is now the standard system tar for FreeBSD 5
and 6.

This package contains the development files.

%package static-devel
Summary: Static library for libarchive
Group: Development/Libraries/C and C++
Requires: libarchive-devel = %{epoch}:%{version}-%{release}

%description static-devel
Static library for libarchive

%post -n libarchive13 -p /sbin/ldconfig
%postun -n libarchive13 -p /sbin/ldconfig

%files -n bsdtar
%{_bindir}/bsdcat
%{_bindir}/bsdcpio
%{_bindir}/bsdtar
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n libarchive13
%license COPYING
%{_libdir}/libarchive.so.*

%files -n libarchive-devel
%doc examples/
%{_mandir}/man3/*
%{_libdir}/libarchive.so
%{_includedir}/archive*
%{_libdir}/pkgconfig/libarchive.pc

%files static-devel
%{_libdir}/libarchive.a
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package devel
Summary: Development files for libarchive
Requires: libarchive = %{epoch}:%{version}-%{release}

%description devel
The libarchive-devel package contains libraries and header files for
developing applications that use libarchive.

%package -n bsdtar
Summary: Manipulate tape archives
Requires: libarchive = %{epoch}:%{version}-%{release}

%description -n bsdtar
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.

%package -n bsdcpio
Summary: Copy files to and from archives
Requires: libarchive = %{epoch}:%{version}-%{release}

%description -n bsdcpio
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.

%package -n bsdcat
Summary: Expand files to standard output
Requires: libarchive = %{epoch}:%{version}-%{release}

%description -n bsdcat
The bsdcat program typically takes a filename as an argument or reads standard
input when used in a pipe. In both cases decompressed data it written to
standard output.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/libarchive.so.13*
%{_mandir}/*/cpio.*
%{_mandir}/*/mtree.*
%{_mandir}/*/tar.*

%files devel
%{_includedir}/*.h
%{_libdir}/libarchive.a
%{_libdir}/libarchive.so
%{_libdir}/pkgconfig/libarchive.pc
%{_mandir}/*/archive*
%{_mandir}/*/libarchive*

%files -n bsdtar
%license COPYING
%{_bindir}/bsdtar
%{_mandir}/*/bsdtar*

%files -n bsdcpio
%license COPYING
%{_bindir}/bsdcpio
%{_mandir}/*/bsdcpio*

%files -n bsdcat
%license COPYING
%{_bindir}/bsdcat
%{_mandir}/*/bsdcat*
%endif

%changelog
