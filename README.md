aria2c-as-a-service
===================

The collection of scripts and tools for running aria2c as a service for local install.

[aria2](http://sourceforge.net/apps/trac/aria2/wiki) is a light-weight multi-protocol & multi-source download utility operated in command-line. The supported protocols are HTTP(S), FTP, BitTorrent (DHT, PEX, MSE/PE), and Metalink.

## Installation

### configure linux container for aria2c-serv

- create linux container
```
$ sudo lxc-create -n aria2c-serv -t ubuntu
$ sudo vi /var/lib/lxc/aria2c-serv/config 
```

- add ip address:
``` lxc.network.ipv4 = {ip_address} ```

- to install aria2c
```
$ sudo apt-get install aria2
```

- create user `aria2c`
```
$ sudo useradd --system --home-dir /var/local/aria2c aria2c

$ sudo mkdir -p /var/local/aria2c/store
$ sudo touch /var/local/aria2c/session

$ sudo chown -R aria2c: /var/local/aria2c
$ sudo chmod -R ug=rwx,o=rx /var/local/aria2c

$ sudo mkdir -p /var/log/aria2c
$ sudo chown -R aria2c: /var/log/aria2c
```

- copy in `aria2c` script to /etc/init.d/aria2c
```
$ sudo cp aria2c /etc/init.d/aria2c
```

- put the following in /etc/aria2.conf
```
$ sudo cp etc/aria2c.conf /etc/aria2c.conf
```

## Links

**Web UI**
- https://github.com/binux/yaaw

- http://xyne.archlinux.ca/projects/python3-aria2jsonrpc/

- This [directory](https://github.com/tatsuhiro-t/aria2/tree/master/doc/xmlrpc) contains sample scripts to interact 
with aria2 via XML-RPC. For more information, see
http://sourceforge.net/apps/trac/aria2/wiki/XmlrpcInterface

- https://github.com/nmbooker/aria2-tools

- [aria2remote](https://code.google.com/p/aria2remote/), Simple remote interface to aria2c.

- https://github.com/adityamukho/Berserker
Advanced web-based frontend for Aria2-JSONRPC

