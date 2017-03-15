# Debian setup

## Java 8

``` sh
su -
echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee /etc/apt/sources.list.d/webupd8team-java.list
echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
apt-get update
apt-get install oracle-java8-installer
exit
```

## Docker for neo4j

### Check your debian distribution and kernel number

``` sh
$ uname -r          # at least 3.10
$ lsb_release -cs   # Jessie or Wheezy
``` 

### Setup repository (for Jessie) and get docker community edition

``` sh
$ sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
$ sudo -E apt-get update
$ sudo -E apt-get -y install docker-ce
``` 

### Setup proxy

``` sh
$ sudo mkdir -p /etc/systemd/system/docker.service.d
$ sudo touch http-proxy.conf
``` 
Edit file and write:
``` sh
[Service]
Environment="HTTP_PROXY=http://10.0.4.2:3128/" "HTTPS_PROXY=http://10.0.4.2:3128/" "NO_PROXY=localhost,127.0.0.1"
``` 

Take update into account:
``` sh
$ sudo systemctl daemon-reload
``` 

### Start Docker

``` sh
$ sudo systemctl start docker
``` 

### Test your Docker CE installation


``` sh
$ sudo -E docker run hello-world
``` 

### Neo4j docker