#!/usr/bin/env python
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='link to source code')
    parser.add_argument(
        '--root',
        help='root directory where you cloned the source code')
    args = parser.parse_args()
    if not args.root:
        args.root = raw_input('What directory is your source code in? ')
    args.root = os.path.normpath(os.path.expanduser(args.root))
    payments_env_root = os.path.dirname(__file__)

    errors = False
    for name in [
        'payments-example',
        'payments-service',
        'solitude',
    ]:
        full_name = os.path.join(args.root, name)
        if not os.path.exists(full_name):
            print
            print ('** Repository at {path} does not exist. '
                   'Is it checked out?'.format(path=full_name))
            print
            errors = True
            continue

        dest = os.path.join(payments_env_root, 'docker', 'source-links', name)
        print '{dest} -> {source}'.format(source=full_name, dest=dest)

        if os.path.exists(dest):
            print '(already exists)'
        else:
            os.symlink(full_name, dest)

    if errors:
        parser.error('Not all symlinks were successful')


if __name__ == '__main__':
    main()