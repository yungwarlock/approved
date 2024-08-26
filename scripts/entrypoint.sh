#!/usr/bin/env sh

set -e

# Check if it is running in fly.io

if [ -n "$FLY_APP_NAME" ]; then
  echo "Running in fly................"
  echo 'vm.swappiness = 95' >> /etc/sysctl.conf
else
  echo "Not running in fly.io"
fi


exec "$@"
