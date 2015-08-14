#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser

from stevedore import extension


def load_providers():
    mgr = extension.ExtensionManager(
        namespace='chrooter.provider',
    )
    return dict((ext.name, ext.plugin()) for ext in mgr)


def get_parser(providers):
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(
        title='distro',
        description='Distribution to create the chroot for',
        dest='distro',
    )
    for provider_name, provider in providers.items():
        subparser = subparsers.add_parser(provider_name)
        provider.populate_parser(subparser)
    return parser


def main():
    providers = load_providers()
    parser = get_parser(providers)
    args = parser.parse_args()
    providers[args.distro].run(args)
