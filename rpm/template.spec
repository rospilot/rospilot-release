Name:           ros-indigo-rospilot
Version:        0.1.2
Release:        0%{?dist}
Summary:        ROS rospilot package

Group:          Development/Libraries
License:        Apache
Source0:        %{name}-%{version}.tar.gz

Requires:       python-cherrypy
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-rosbridge-suite
Requires:       ros-indigo-roslaunch
Requires:       ros-indigo-rospilot-deps
Requires:       ros-indigo-rospy
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-std-srvs
Requires:       vlc-core
BuildRequires:  libgphoto2-devel
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-roslint
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-std-srvs

%description
rospilot

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo
/etc/init.d/rospilot
/etc/udev/rules.d/rospilot.rules

%changelog
* Mon Jun 27 2016 Christopher Berner <christopherberner@gmail.com> - 0.1.2-0
- Autogenerated by Bloom

* Wed Apr 22 2015 Christopher Berner <christopherberner@gmail.com> - 0.1.1-3
- Autogenerated by Bloom

* Sat Sep 13 2014 Christopher Berner <christopherberner@gmail.com> - 0.1.1-2
- Autogenerated by Bloom

* Fri Sep 12 2014 Christopher Berner <christopherberner@gmail.com> - 0.1.1-1
- Autogenerated by Bloom

* Wed Aug 27 2014 Christopher Berner <christopherberner@gmail.com> - 0.1.1-0
- Autogenerated by Bloom

* Tue Aug 26 2014 Christopher Berner <christopherberner@gmail.com> - 0.1.0-0
- Autogenerated by Bloom

* Tue Aug 26 2014 Christopher Berner <christopherberner@gmail.com> - 0.0.4-1
- Autogenerated by Bloom

