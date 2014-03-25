#!/bin/sh
#
#   aria2c installation script
#

echo '- installing aria2 ...'
apt-get install aria2

echo '- creation user `aria2c`'
useradd --system --home-dir /var/local/aria2c aria2c

echo '- creation directories and assigning rights' 
mkdir -p /var/local/aria2c/store
touch /var/local/aria2c/session

chown -R aria2c: /var/local/aria2c
chmod -R ug=rwx,o=rx /var/local/aria2c

mkdir -p /var/log/aria2c
chown -R aria2c: /var/log/aria2c

echo '- coping script and conf files'
cp aria2c /etc/init.d/aria2c
cp aria2c.conf /etc/aria2c.conf

