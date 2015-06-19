# Builds and pushes the images to docker hub.

images=(nginx)
for i in "${images[@]}"
do
    echo 'Building and pushing' $i
    docker build -t mozillapayments/$i:latest docker/$i
    docker push mozillapayments/$i:latest
    echo '... done.'
done
