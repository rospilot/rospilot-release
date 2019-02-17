#!/bin/bash
echo "Installing udev and init.d rules"
sudo cp $(catkin_find --share rospilot share/etc/rospilot.rules) /etc/udev/rules.d/
sudo cp $(catkin_find --share rospilot share/etc/rospilot.service) /etc/systemd/system/
message="Enabling rospilot service. \
Disable it with 'systemctl disable rospilot'"

echo "$(tput setaf 1)${message}$(tput sgr 0)"
sudo systemctl enable rospilot
sudo systemctl daemon-reload

echo "Setting up postgis"
# Change to /tmp because postgres user might not be able to see the cwd,
# so suppress any warnings about that
cd /tmp
sudo -u postgres createuser --no-superuser --no-createdb --no-createrole rospilot
sudo -u postgres createdb gis
echo "GRANT ALL ON DATABASE gis TO rospilot;" | sudo -u postgres psql -Upostgres gis
echo "ALTER USER rospilot WITH PASSWORD 'rospilot_password'" | sudo -u postgres psql -Upostgres gis
echo "CREATE EXTENSION postgis;" | sudo -u postgres psql -Upostgres gis
echo "CREATE EXTENSION hstore;" | sudo -u postgres psql -Upostgres gis

echo "Setting up mapnik"
tempdir=$(mktemp -d)
cd $tempdir
if [ $(catkin_find --share rospilot share/mapnik-style/ | wc -l) -ne 1 ]; then
    echo "$(tput setaf 1)Multiple installations of rospilot found. Cannot continue.$(tput sgr 0)"
    exit 1
fi
rosrun rospilot get_mapnik_shapefiles.sh
echo "Copying mapnik files to rospilot data directory"
sudo mv -f $tempdir/data $(catkin_find --share rospilot share/mapnik-style/)
wget -O kathmandu.osm "https://api.openstreetmap.org/api/0.6/map?bbox=27.713,85.308,27.717,85.312"
rosrun rospilot load_osm.sh kathmandu.osm
rm -rf $tempdir

echo "Install more map data by downloading the appropriate osm/osm.pbf file \
(you can find some at \
https://wiki.openstreetmap.org/wiki/Planet.osm#Country_and_area_extracts) \
then run 'rosrun rospilot load_osm.sh --append <file>'"

echo -n "Setup wifi access point? [y/n]"
read wifi_requested

if [ "$wifi_requested" == "y" ]; then
    tempdir=$(mktemp -d)
    cd $tempdir
    hostname=$(hostname)
    wifi_config="$tempdir/wifi.config"
    rosrun rospilot choose_wifi_device $wifi_config
    if [ $? -ne 0 ]; then
        exit 1;
    fi
    wlan=$(cat $wifi_config | awk '{print $1}')
    mode=$(cat $wifi_config | awk '{print $2}')
    channel=$(cat $wifi_config | awk '{print $3}')
    echo -n "Choose ssid (wifi network name): "
    read ssid
    echo
    while true; do
        echo -n "Choose wifi passphrase: "
        read -s wifi_passphrase
        echo
        echo -n "Confirm passphrase: "
        read -s confirm_passphrase
        if [ "$wifi_passphrase" == "$confirm_passphrase" ]; then
            break;
        fi
        echo
        echo "$(tput setaf 1)Passphrase does not match$(tput sgr 0)"
    done

    cp $(catkin_find --share rospilot share/ap_config/netplan.template) $tempdir
    cat $tempdir/netplan.template | sed "s/WLAN_PLACEHOLDER/$wlan/g" > $tempdir/netplan.yaml
    sudo mv $tempdir/netplan.yaml /etc/netplan/99-rospilot.yaml
    
    cp $(catkin_find --share rospilot share/ap_config/dnsmasq.conf.template) $tempdir
    cat $tempdir/dnsmasq.conf.template | sed "s/WLAN_PLACEHOLDER/$wlan/g" > $tempdir/dnsmasq.conf
    sudo mv $tempdir/dnsmasq.conf /etc/dnsmasq.conf
    
    cp $(catkin_find --share rospilot share/ap_config/hosts.dnsmasq.template) $tempdir
    cat $tempdir/hosts.dnsmasq.template | sed "s/HOSTNAME_PLACEHOLDER/$hostname/g" > $tempdir/hosts.dnsmasq
    sudo mv $tempdir/hosts.dnsmasq /etc/hosts.dnsmasq
    
    cp $(catkin_find --share rospilot share/ap_config/hostapd.conf.template) $tempdir
    cat $tempdir/hostapd.conf.template \
        | sed "s/WLAN_PLACEHOLDER/$wlan/g" \
        | sed "s/SSID_PLACEHOLDER/$ssid/g" \
        | sed "s/MODE_PLACEHOLDER/$mode/g" \
        | sed "s/CHANNEL_PLACEHOLDER/$channel/g" \
        | sed "s/PASSPHRASE_PLACEHOLDER/$wifi_passphrase/g" \
        > $tempdir/hostapd.conf
    sudo mv $tempdir/hostapd.conf /etc/hostapd/hostapd.conf
    echo 'DAEMON_CONF=/etc/hostapd/hostapd.conf' > $tempdir/hostapd
    sudo mv $tempdir/hostapd /etc/default/hostapd

    sudo mkdir -p /etc/systemd/system/dnsmasq.service.d/
    echo "[Service]" > $tempdir/override.conf
    echo "# XXX: resolve race with wlan device" >> $tempdir/override.conf
    echo "ExecStartPre=/bin/sleep 10" >> $tempdir/override.conf
    echo "[Unit]" >> $tempdir/override.conf
    echo "After=sys-subsystem-net-devices-$wlan.device" >> $tempdir/override.conf
    sudo mv $tempdir/override.conf /etc/systemd/system/dnsmasq.service.d/override.conf
    sudo systemctl daemon-reload

    echo ""
    echo "Please restart your drone"
fi
