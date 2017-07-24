from __future__ import print_function

import argparse

from . import config, ec2, menu, settings, ssm, ssh


try:

    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument('config', nargs='?', help='Configuration name')
    parser.add_argument('search', nargs='?', help='Instance search string')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    args = parser.parse_args()

    settings.load(verbose=args.verbose)
    config.load(args.config or menu.choose_config())

    instances = ec2.discover_instances()
    instance = menu.choose_instance(instances, args.search)
    if instance:

        bastion = ec2.discover_bastion(instance)

        if config.get('ssm'):
            ssm.send_command(instance, bastion)

        ssh.connect(instance, bastion)

    else:
        print('[ssha] no matching instances found')

except KeyboardInterrupt:
    pass
