#!/bin/bash

# TODO: Change this to Python so Windows users can run it easier?

git checkout master && git pull origin master

cd docker/source-links/

cd kinto && git checkout master && git pull origin master
cd ../payments-example && git checkout master && git pull origin master
cd ../payments-service && git checkout master && git pull origin master
cd ../payments-ui && git checkout master && git pull origin master
cd ../solitude && git checkout master && git pull origin master
cd ../solitude-auth && git checkout master && git pull origin master

cd ../../../

docker-compose stop
docker-compose pull
docker-compose up -d
