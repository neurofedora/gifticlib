Name:           gifticlib
Version:        1.0.9
Release:        1%{?dist}
Summary:        IO library for the GIFTI cortical surface data format
License:        Public Domain
URL:            http://www.nitrc.org/projects/gifti/
Source0:        http://www.nitrc.org/frs/download.php/2262/%{name}-%{version}.tgz
# Taken from Debian
Source1:        gifti_test.1

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  zlib-devel
BuildRequires:  expat-devel
BuildRequires:  nifticlib-devel

%description
GIFTI is an XML-based file format for cortical surface data. This reference
IO implementation is developed by the Neuroimaging Informatics Technology
Initiative (NIfTI).

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        tools
Summary:        Tools shipped with GIFTI library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
This package provides the tools that are shipped with the GIFTI library
(gifti_tool and gifti_test).

%prep
%autosetup
# Remove using ITK-bundled EXPAT and ZLIB (we're not shipping them
# and use proper libsuffix
sed -i \
  -e '/FIND_PACKAGE(ITK)/d' \
  -e '/SET(GIFTI_INSTALL_LIB_DIR/s/lib/%{_lib}/' \
  CMakeLists.txt
rm -rf build/
mkdir -p build/

%build
pushd build/
  %cmake ../
popd

%install
pushd build/
  %make_install
popd
# Remove static libs
rm -f %{buildroot}%{_libdir}/*.a
mkdir -p %{buildroot}%{_mandir}/man1/
install -p -m0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.gifti
%{_libdir}/libgifti*.so.*

%files devel
%doc README.gifti
%{_includedir}/gifti/
%{_libdir}/libgifti*.so

%files tools
%{_bindir}/gifti_*
%{_mandir}/man1/gifti_*.1.*

%changelog
* Sun Nov 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.9-1
- Initial package
