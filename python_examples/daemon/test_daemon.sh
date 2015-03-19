#! /bin/sh
### BEGIN INIT INFO
# Provides:          test_daemon
# Required-Start:    $remote_fs $syslog mysql
# Required-Stop:     $remote_fs $syslog mysql
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts and stops the test_daemon.py
# Description:       starts and stops the test_daemon.py
### END INIT INFO

# Author: Jochen Hertle
# this script is copied to /etc/init.d and needs to be executable
# install this script: update-rc.d test_daemon.sh defaults (with admin rights)

case "$1" in
  start)
    echo "Starting test_daemon"
    # Start the daemon
    /home/pi/www/scripts/test_daemon.py > /dev/null 2> /dev/null &
    ;;
  stop)
    echo "Stopping test_daemon"
    # Stop the daemon using the shell script written by test_daemon.py during __init__
    /tmp/test_daemon_stop
    ;;
  restart)
    echo "Restarting test_daemon"
    /tmp/test_daemon_stop
    sleep 5
    /home/pi/www/scripts/test_daemon.py > /dev/null 2> /dev/null &
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/test_daemon.sh {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
