This is the main development environment for working on Mozilla payments.

## Requirements

* [Python](https://www.python.org/)
* [Docker](https://docs.docker.com/)
  * On Mac you can run this with
    [VirtualBox](https://www.virtualbox.org/) and
    [Boot2Docker](http://boot2docker.io/) or
    [Kitematic](https://kitematic.com/)
* [docker-compose](https://docs.docker.com/compose/)

## Deployment / QA

The following instructions are for using pre-built
containers for deployment or QA purposes.

* ``git clone https://github.com/mozilla/payments-env.git``
* ``cd payments-env``
* ``docker-compose -f docker-compose-deploy.yml up -d``
* Find the IP address of your docker system.
  * On OS X using boot2docker you can find the address of a container by ``boot2docker ip``
* Edit your ``/etc/hosts`` file so that the host ``pay.dev`` resolves to your IP.
  For example, you might add this line to ``/etc/hosts``:

        192.168.59.103  pay.dev

* Run ``docker-compose up -d``
* Open the example site at
  [http://pay.dev/](http://pay.dev/)

## Development

The following instructions are for developing on the code only.

* Check out the following repositories somewhere on your machine under the same
  root directory:
  * [kinto](https://github.com/mozilla-services/kinto/)
  * [payments-example](https://github.com/mozilla/payments-example/)
  * [payments-service](https://github.com/mozilla/payments-service/)
  * [payments-ui](https://github.com/mozilla/payments-ui/)
  * [solitude](https://github.com/mozilla/solitude/)
  * [solitude-auth](https://github.com/mozilla/solitude-auth/)
* Run ``python link.py`` to connect your sources.
* Export any project-specific environment variables in your shell.
  * Example: for Solitude you'll need to
    [export all braintree variables](https://solitude.readthedocs.org/en/latest/topics/setup.html#braintree-settings)
    such as ``BRAINTREE_MERCHANT_ID=...``.
* Run ``docker-compose pull`` to pull images and build the containers.
* Run ``docker-compose up -d``
* Set up your Solitude database to mirror your Braintree sandbox by running:
  ``python manage.py braintree_config`` in the Solitude container.
  * You will need to add some products to your sandbox; the script will guide you.
  * You can shell into the Solitude container easily with
    [docker-utils](https://pypi.python.org/pypi/docker-utils).
* Find the IP address of your docker system.
  * On OS X using boot2docker you can find the address of a container by
    ``boot2docker ip``
* Edit your ``/etc/hosts`` file so that the host ``pay.dev`` resolves to your IP.
* Open the example site at
  [http://pay.dev/](http://pay.dev/)

Now you're good to go!

## Updating Your Environment

To keep everything up to date, run these commands:

* Run ``git pull`` in each linked repository (or only in ``payments-env`` if
  you're using pre-built containers).
* Run ``docker-compose stop`` to make sure all containers are not running.
* Run ``docker-compose pull`` to get the latest images and rebuild if necessary.
* Run ``docker-compose up -d`` to start the new containers.

## Configurations

There are two docker configurations:
* ``docker-compose.yml`` is for development purposes and requires the source to be checked out.
* ``docker-compose-deploy.yml`` is for deployment purposes and contain the application source.
