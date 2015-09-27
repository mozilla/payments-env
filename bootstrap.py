#!/usr/bin/env python
# coding=utf-8
import argparse
import os
import subprocess
from string import Template

from blessings import Terminal


DEFAULT_DIRECTORY_NAME = 'mozilla-payments'
GIT_REPOS = [
    {'org': 'Kinto', 'name': 'kinto'},
    {'org': 'mozilla', 'name': 'payments-example'},
    {'org': 'mozilla', 'name': 'payments-service'},
    {'org': 'mozilla', 'name': 'payments-ui'},
    {'org': 'mozilla', 'name': 'solitude'},
    {'org': 'mozilla', 'name': 'solitude-auth'},
]
PAYMENT_ENV_DIR = os.path.abspath(os.path.dirname(__file__))
LOCAL_ENV = Template((os.fdopen(os.open(
    os.path.join(PAYMENT_ENV_DIR, 'env', 'local.env.dist'),
    os.O_RDWR), "r+").read()))
SEPARATOR = "\n" + ("#" * 80) + "\n" + ("💰 " * 39) + "💰" + "\n" + ("#" * 80)


class ShellCommandError(Exception):
    pass


def main():
    args = get_arguments()

    term = Terminal()

    print ("""{s}

Hi there! 😀

Time to set up your 💰 {t.red}{t.bold}Mozilla Payments{t.normal}💰  environment!

First, we are going to create a personlised environment file so you can
process payments in development mode. You'll need to have your
{t.bold}Braintree API keys{t.normal}.

If you don't have a Braintree account yet or don't know your API Keys,
go to {t.blue_underline}braintree.com{t.normal} and create an account/log in, then go to
{t.blue_underline}solitude.readthedocs.org/latest/topics/setup.html#braintree-settings{t.normal}
to see how to get your API keys.
"""  # noqa
).format(
        dir=os.path.abspath(os.path.join(PAYMENT_ENV_DIR, '..', args.dir)),
        s=SEPARATOR, t=term
    )

    env_vars = get_environment_variables()

    create_local_env(env_vars)

    print ("""{s}

Okay, that's all finished. 👍

Next we're going to check out the {t.red}{t.bold}Mozilla Payments{t.normal} git repositories to:

{dir}
"""  # noqa
).format(dir=os.path.abspath(os.path.join(PAYMENT_ENV_DIR, '..', args.dir)),
            s=SEPARATOR, t=term)

    # Create our payments repos.
    create_folder_and_checkout_repos(args.dir)

    print("""{s}

Repositories downloaded! ✅

Next we're going to download Docker images and data.
This will mean hundreds of MBs of downloads and will likely take some time.

Make sure you have a good internet connection. Maybe get a coffee 😉
""".format(s=SEPARATOR))
    bootstrap_docker()

    print("""{s}

Docker all set up! ✅

Payments UI needs some NPM/bower modules to run; we'll install them now.
""".format(s=SEPARATOR))

    bootstrap_ui(args.dir)

    print ("""{s}

Setup complete. 👏

For now there are a few manual, one-time steps.

1. Run this command:

    echo "$(docker-machine ip default) pay.dev" | sudo tee -a /etc/hosts

Now {t.blue_underline}pay.dev{t.normal} resolves to your Docker IP.

2. Add this to your .bashrc, .profile, .zshrc, or similar:

    # Mozilla Payments Egnvironment
    source {dir}/env/local.env

3. Run the payments-ui server:

    cd {ui_directory}
    grunt watch-static

Have fun! 💰
""").format(t=term, dir=os.path.abspath(os.path.join(PAYMENT_ENV_DIR)),
            s=SEPARATOR,
            ui_directory=os.path.abspath(
                os.path.join(PAYMENT_ENV_DIR, '..', args.dir, 'payments-ui')))
    # TODO: Use
    # `echo "$(docker-machine ip default) pay.dev" | sudo tee -a /etc/hosts`
    # to configure the IP address automatically.
    # set_ip_address_in_hosts()


def bootstrap_docker():
    os.chdir(os.path.abspath(os.path.join(PAYMENT_ENV_DIR)))

    shell(
        '''
        eval "$(docker-machine env default)"
        source {dir}/env/local.env
        docker-compose pull
        docker-compose up -d
        '''.format(dir=os.path.abspath(os.path.join(PAYMENT_ENV_DIR))))


def bootstrap_ui(directory):
    os.chdir(os.path.join(PAYMENT_ENV_DIR, '..', directory, 'payments-ui'))
    os.system('npm install')
    os.system('npm install -g bower')
    os.system('bower install')


def create_folder_and_checkout_repos(directory):
    os.chdir(os.path.join(PAYMENT_ENV_DIR, '..'))
    try:
        os.mkdir(directory)
    except OSError:
        pass
    os.chdir(os.path.join(directory))

    for repo in GIT_REPOS:
        shell('git clone git@github.com:{org}/{name}.git'.format(
            org=repo['org'], name=repo['name']))

    os.chdir(os.path.abspath(os.path.join(PAYMENT_ENV_DIR)))

    # Link them all together with the link.py script
    # TODO: Include this as a Python module instead of making the exec call!
    shell('python link.py --root=../{dir}'.format(dir=directory))


def create_local_env(variables):
    env_file = os.fdopen(os.open(os.path.join(PAYMENT_ENV_DIR, 'env',
                                              'local.env'),
                                 os.O_RDWR | os.O_CREAT),
                         "w+")

    env_file.write(LOCAL_ENV.safe_substitute(
        base_env_file=os.path.join(PAYMENT_ENV_DIR, 'env', 'base.env'),
        compose_file=os.path.join(PAYMENT_ENV_DIR, 'docker-compose.yml'),
        merchant_id=variables['merchant_id'],
        public_key=variables['public_key'],
        private_key=variables['private_key'],
    ))

    env_file.close()


def get_arguments():
    parser = argparse.ArgumentParser(description='name of payments directory')
    parser.add_argument(
        '--dir',
        help='name of directory to clone payments repositories into')

    args = parser.parse_args()

    if not args.dir:
        args.dir = DEFAULT_DIRECTORY_NAME

    return args


def get_environment_variables():
    env_vars = {}

    env_vars['merchant_id'] = raw_input('Enter your BRAINTREE_MERCHANT_ID: ')
    env_vars['public_key'] = raw_input('Enter your BRAINTREE_PUBLIC_KEY: ')
    env_vars['private_key'] = raw_input('Enter your BRAINTREE_PRIVATE_KEY: ')

    return env_vars


def shell(command):
    if subprocess.call(command, shell=True) != 0:
        raise ShellCommandError(
            """Failed to execute command:\n{command}""".format(
                command=command))


if __name__ == '__main__':
    main()
