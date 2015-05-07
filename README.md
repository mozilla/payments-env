This is the main development environment for working on Mozilla payments.

TODO: non-development environments are coming soon.

You will need:
* [Python](https://www.python.org/)
* [Docker](https://docs.docker.com/)
  * On Mac you can run this with
    [VirtualBox](https://www.virtualbox.org/) and
    [Boot2Docker](http://boot2docker.io/)
* [docker-compose](https://docs.docker.com/compose/)

Build your environment:

* Check out the following repositories somewhere on your machine:
  * [solitude](https://github.com/mozilla/solitude/)
  * [payments-example](https://github.com/mozilla/payments-example/)
  * [payments-service](https://github.com/mozilla/payments-service/)
  * [payments-ui](https://github.com/mozilla/payments-ui/)
* Run ``python link.py`` to connect your source.
* Run ``docker-compose build`` to build the containers.

Start up all containers:
* Run ``docker-compose up -d``

Launch the example site:
* Run ``boot2docker ip`` to find your IP.
* You may wish to add an entry in ``/etc/hosts`` for this
  such as ``pay.dev``.
* Open the example site to test out payments at
  [http://pay.dev/](http://pay.dev/)

Now you're good to go!


Update the environment:
* Run ``git pull`` in each linked repository.
* Run ``docker-compose stop`` to make sure all containers are not running.
* Run ``docker-compose pull`` to get the latest images.
* Run ``docker-compose build`` to rebuild containers if necessary.
