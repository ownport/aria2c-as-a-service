# Installation

## Manual install

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

