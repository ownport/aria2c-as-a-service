aria2c-as-a-service
===================

The collection of scripts and tools for running aria2c as a service for local install.

[aria2](http://sourceforge.net/apps/trac/aria2/wiki) is a light-weight multi-protocol & multi-source download utility operated in command-line. The supported protocols are HTTP(S), FTP, BitTorrent (DHT, PEX, MSE/PE), and Metalink.

## Installation

### configure linux container for aria2c-serv

- create linux container
```shell
$ sudo lxc-create -n aria2c-serv -t ubuntu
```

- add ip address:
```shell
$ sudo vi /var/lib/lxc/aria2c-serv/config 
...
lxc.network.ipv4 = {ip_address} 
...
```

- login to container and install aria2c
```shell
$ sudo apt-get install aria2
```

- create user _aria2c_ and directories
```shell
$ sudo useradd --system --home-dir /var/local/aria2c aria2c

$ sudo mkdir -p /var/local/aria2c/store
$ sudo touch /var/local/aria2c/session

$ sudo chown -R aria2c: /var/local/aria2c
$ sudo chmod -R ug=rwx,o=rx /var/local/aria2c

$ sudo mkdir -p /var/log/aria2c
$ sudo chown -R aria2c: /var/log/aria2c
```

- copy in _aria2c_ script to /etc/init.d/aria2c
```shell
$ sudo cp aria2c /etc/init.d/aria2c
```

- put the following in /etc/aria2.conf
```shell
$ sudo cp etc/aria2c.conf /etc/aria2c.conf
```

## Links

- [YAAW](https://github.com/binux/yaaw) Yet Another Aria2 Web Frontend in pure HTML/CSS/Javascirpt. No HTTP server, backend or server-side program. All you need is just a browser.

- [Aria2JsonRpc](http://xyne.archlinux.ca/projects/python3-aria2jsonrpc/) is a Python 3 module that provides a wrapper class around Aria2's RPC interface. It can be used to build applications that use Aria2 for downloading data.

- This [directory](https://github.com/tatsuhiro-t/aria2/tree/master/doc/xmlrpc) contains sample scripts to interact with aria2 via XML-RPC. For more information, see http://sourceforge.net/apps/trac/aria2/wiki/XmlrpcInterface

- [Aria2 Tools](https://github.com/nmbooker/aria2-tools) Some tools and instructions to help supplement aria2 when used as a download server.

- [aria2remote](https://code.google.com/p/aria2remote/), Simple remote interface to aria2c.

- [Berserker](https://github.com/adityamukho/Berserker) Advanced web-based frontend for Aria2-JSONRPC.



