# Installation

**Warning!** The configation below tested only in Ubuntu environment (13.10)

- download [installation package](https://github.com/ownport/aria2c-as-a-service/archive/master.zip)

## Fast installation

``` 
$ sudo ./install.sh
```

## Manual install

- install aria2c
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

## Manage aria2c service

```
$ sudo service aria2c
 * Usage: /etc/init.d/aria2c {start|stop|restart|reload|force-reload|status}
$
$ sudo service aria2c start
 * Starting aria2c aria2c
$
$ sudo service aria2c status
 * aria2c is running
$
$ sudo service aria2c restart
 * Restarting aria2c aria2c
$ sudo service aria2c stop
 * Stopping aria2c aria2c                                           [ OK ] 
$
$ sudo service aria2c status
 * aria2c is not running
$
```

## to run aria2c at startup:
```
$ sudo update-rc.d aria2c defaults
```

