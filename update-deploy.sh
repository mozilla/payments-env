export COMPOSE_FILE=docker-compose-deploy.yml
export COMPOSE_PROJECT_NAME=pay

docker-compose pull
docker-compose stop
docker rm -v $(docker ps -a | grep example | awk '{print $1}')
docker rm -v $(docker ps -a | grep ui | awk '{print $1}')
docker-compose up -d
