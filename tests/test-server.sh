#!/bin/sh

NAME=test-server.py
SERVER=`pwd`/tests/$NAME
PIDFILE=`pwd`/tests/run/$NAME.pid
LOGFILE=`pwd`/tests/log/test-server.log

ARGS=' --logfile='$LOGFILE

test -f $SERVER || exit 0

. /lib/lsb/init-functions

case "$1" in

    start)  
        log_daemon_msg "Starting test server"
        start-stop-daemon --start --quiet -b -m --pidfile $PIDFILE --startas $SERVER -- $ARGS
        log_end_msg $?
        ;;

    stop)  
        log_daemon_msg "Stopping test server"
        start-stop-daemon --stop --quiet --pidfile $PIDFILE
        log_end_msg $?
        ;;

    restart|reload|force-reload)
        log_daemon_msg "Restarting test server"
        start-stop-daemon --stop --retry 5 --quiet --pidfile $PIDFILE
        start-stop-daemon --start --quiet -b -m --pidfile $PIDFILE --startas $SERVER -- $ARGS
        log_end_msg $?
        ;;

    status)
        status_of_proc -p $PIDFILE $SERVER test-server.py && exit 0 
        ;;

    *)
        log_action_msg "Usage: ./tests/test-server.sh {start|stop|restart|reload|force-reload|status}"
        exit 2
        ;;
esac
exit 0
