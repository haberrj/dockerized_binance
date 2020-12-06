# This script will install required dependencies
# Script must be run with sudo

if [ "$EUID" -ne 0 ]
  then echo "Please run with elevated permission rights"
  exit
fi

apt-get update
apt-get install -y python-dev python3-pip docker

# Get the git repos here
