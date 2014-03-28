#!/bin/sh

NAME=dev-server.py
SERVER=`pwd`/tests/$NAME
PIDFILE=`pwd`/tests/run/$NAME.pid
LOGFILE=`pwd`/tests/log/dev-server.log

ARGS=' --logfile='$LOGFILE

test -f $SERVER || exit 0

. /lib/lsb/init-functions

case "$1" in

    start)  
        log_daemon_msg "Starting dev server"
        start-stop-daemon --start --quiet -b -m --pidfile $PIDFILE --startas $SERVER -- $ARGS
        log_end_msg $?
        ;;

    stop)  
        log_daemon_msg "Stopping dev server"
        start-stop-daemon --stop --quiet --pidfile $PIDFILE
        log_end_msg $?
        ;;

    restart|reload|force-reload)
        log_daemon_msg "Restarting dev server"
        start-stop-daemon --stop --retry 5 --quiet --pidfile $PIDFILE
        start-stop-daemon --start --quiet -b -m --pidfile $PIDFILE --startas $SERVER -- $ARGS
        log_end_msg $?
        ;;

    status)
        status_of_proc -p $PIDFILE $SERVER dev-server.py && exit 0 
        ;;

    *)
        log_action_msg "Usage: ./tests/dev-server.sh {start|stop|restart|reload|force-reload|status}"
        exit 2
        ;;
esac
exit 0
