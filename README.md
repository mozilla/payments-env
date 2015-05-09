This is the main development environment for working on Mozilla payments.

You will need:
* [Python](https://www.python.org/)
* [Docker](https://docs.docker.com/)
  * On Mac you can run this with
    [VirtualBox](https://www.virtualbox.org/) and
    [Boot2Docker](http://boot2docker.io/) or
    [Kitematic](https://kitematic.com/)
* [docker-compose](https://docs.docker.com/compose/)

For deployment or testing:

* ``git clone https://github.com/mozilla/payments-env.git``
* ``cd payments-env``
* ``docker-compose -f docker-compose-deploy.yml up -d``
* Find the IP address of your container then access that in a browser.
  * On OS X using boot2docker you can find the address of a container by ``boot2docker ip``

The following instructions are for developing on the code only.

For development:

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

There are two docker configurations:
* ``docker-compose.yml`` for development purposes and requires the source to be checked out.
* ``docker-compose-deploy.yml`` for deployment purposes and contain the application source.
