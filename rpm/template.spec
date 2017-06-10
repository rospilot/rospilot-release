Name:           ros-kinetic-rospilot
Version:        1.3.7
Release:        0%{?dist}
Summary:        ROS rospilot package

Group:          Development/Libraries
License:        Apache 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       curl
Requires:       dnsmasq
Requires:       gdal
Requires:       hostapd
Requires:       libcurl-devel
Requires:       libnl3
Requires:       mapnik-python
Requires:       mapnik-utils
Requires:       osm2pgsql
Requires:       postgis
Requires:       pyserial
Requires:       python-cherrypy
Requires:       python-colorama
Requires:       python-psutil
Requires:       python-tilestache
Requires:       ros-kinetic-geometry-msgs
Requires:       ros-kinetic-mavlink
Requires:       ros-kinetic-message-runtime
Requires:       ros-kinetic-rosbash
Requires:       ros-kinetic-rosbridge-suite
Requires:       ros-kinetic-roslaunch
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-sensor-msgs
Requires:       ros-kinetic-std-msgs
Requires:       ros-kinetic-std-srvs
Requires:       ros-kinetic-vision-opencv
Requires:       unzip
BuildRequires:  ffmpeg-devel
BuildRequires:  libgphoto2-devel
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libnl3-devel
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-geometry-msgs
BuildRequires:  ros-kinetic-message-generation
BuildRequires:  ros-kinetic-opencv3
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-roslint
BuildRequires:  ros-kinetic-sensor-msgs
BuildRequires:  ros-kinetic-std-msgs
BuildRequires:  ros-kinetic-std-srvs
BuildRequires:  turbojpeg-devel

%description
rospilot

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/kinetic" \
        -DCMAKE_PREFIX_PATH="/opt/ros/kinetic" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/kinetic

%changelog
* Sat Jun 10 2017 Christopher Berner <christopherberner@gmail.com> - 1.3.7-0
- Autogenerated by Bloom

* Mon May 29 2017 Christopher Berner <christopherberner@gmail.com> - 1.3.6-0
- Autogenerated by Bloom

* Sun Mar 12 2017 Christopher Berner <christopherberner@gmail.com> - 1.3.5-0
- Autogenerated by Bloom

* Wed Mar 08 2017 Christopher Berner <christopherberner@gmail.com> - 1.3.4-0
- Autogenerated by Bloom

* Wed Aug 24 2016 Christopher Berner <christopherberner@gmail.com> - 1.3.3-0
- Autogenerated by Bloom

* Wed Aug 24 2016 Christopher Berner <christopherberner@gmail.com> - 1.3.2-0
- Autogenerated by Bloom

* Sun Aug 21 2016 Christopher Berner <christopherberner@gmail.com> - 1.3.1-0
- Autogenerated by Bloom

* Sat Aug 20 2016 Christopher Berner <christopherberner@gmail.com> - 1.3.0-0
- Autogenerated by Bloom

